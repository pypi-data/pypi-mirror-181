# Copyright 2021 Alibaba Group Holding Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

r'''Buffer of embeddings.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import custom_gradient
from tensorflow.python.ops import data_flow_ops
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import variable_scope as vs
from tensorflow.python.training import basic_session_run_hooks

from hybridbackend.tensorflow.common import oplib as _ops
from hybridbackend.tensorflow.framework.context import Context
from hybridbackend.tensorflow.framework.ops import GraphKeys

ops.NotDifferentiable('HbEmbeddingBufferIndexHandleOp')
ops.NotDifferentiable('HbEmbeddingBufferIndexIsInitialized')
ops.NotDifferentiable('HbEmbeddingBufferIndexCreate')
ops.NotDifferentiable('HbEmbeddingBufferIndexLookup')
ops.NotDifferentiable('HbEmbeddingBufferIndexDump')
ops.NotDifferentiable('HbEmbeddingBufferIndexIsOverflowed')


def _lookup_buffered(buffer, weight, inputs):
  r'''Lookup embeddings with buffering.
  '''
  @custom_gradient.custom_gradient
  def _lookup(buffer_storage, ids):
    r'''Look up embeddings with buffering.
    '''
    indices, hit_rows, miss_rows = buffer.index_lookup(ids)
    with ops.name_scope(buffer.name):
      hit_indices = array_ops.gather(indices, hit_rows, name='hit_indices')
      miss_indices = array_ops.gather(indices, miss_rows, name='miss_indices')
      hit_embs = array_ops.gather(buffer_storage, hit_indices, name='hit_embs')
      miss_ids = array_ops.gather(ids, miss_rows, name='miss_ids')
      miss_embs = EmbeddingBackend.get().lookup(
        buffer.column, weight, miss_ids,
        sharded=buffer.sharded,
        buffered=True)
      miss_embs = array_ops.stop_gradient(miss_embs)
      with ops.control_dependencies([hit_embs]):
        sync_op = buffer.sync(weight, indices, miss_embs, miss_indices)
      with ops.control_dependencies([sync_op]):
        embs = data_flow_ops.dynamic_stitch(
          [hit_rows, miss_rows], [hit_embs, miss_embs])

    with ops.colocate_with(buffer_storage):
      dense_shape = array_ops.shape(buffer_storage)

    def grad_fn(*grads):
      r'''Gradient function for embedding lookup with buffering.
      '''
      d_storage = ops.IndexedSlices(grads[0], indices, dense_shape)
      return d_storage, None
    return embs, grad_fn

  return _lookup(buffer.storage, inputs)


class EmbeddingBuffer(object):  # pylint: disable=useless-object-inheritance
  r'''A buffer of embedding lookup.

  Buffered embedding lookup is frequency-oblivious, which takes advantage of
  an accumulation buffer of gradients for reducing data transfer to the
  underlying storage. Compared to frequency-aware caching approach, this
  approach has better performance for worst cases.

  Also, due to high skewness of categorical inputs, high-frequent items have
  more chances to be buffered, and thus data transfer from the underlying
  storage might be reduced after some rounds too.
  '''
  class IndexResource(object):  # pylint: disable=useless-object-inheritance
    r'''Resource object of an embedding buffer index.
    '''
    def __init__(self, name, handle_op, create_op, initialized_op):
      self._name = name
      self._handle_op = handle_op
      self._create_op = create_op
      self._is_initialized_op = initialized_op

    @property
    def name(self):
      r'''Name of the embedding buffer index.
      '''
      return self._name

    @property
    def handle(self):
      r'''Resource handle of the embedding buffer.
      '''
      return self._handle_op

    @property
    def create(self):
      r'''Resource creation op of the embedding buffer.
      '''
      return self._create_op

    @property
    def is_initialized(self):
      r'''Resource creation check op of the embedding buffer.
      '''
      return self._is_initialized_op

  class CheckpointSaverListener(
      basic_session_run_hooks.CheckpointSaverListener):
    r'''Checkpoint saver listener for embedding buffer.
    '''
    def __init__(self, flush_op):
      self._op = flush_op

    def before_save(self, session, global_step_value):
      del global_step_value
      session.run(self._op)

    def end(self, session, global_step_value):
      del global_step_value
      session.run(self._op)

  def __init__(self, column):
    r'''Constructs an embedding buffer.

    Args:
      column: Name of the input column.
    '''
    self._impl = EmbeddingBackend.get()

    load_factor = max(0., self._impl.buffer_load_factor)
    self._size = self._impl.buffer_size
    self._column = column
    num_buckets = self._impl.num_buckets(column)
    if num_buckets is not None and self._size > num_buckets:
      self._size = int(num_buckets * load_factor)
    self._sharded = self._impl.sharded(column)
    self._size = max(0, self._size)
    self._dimension = self._impl.dimension(column)
    self._device = self._impl.device(column)
    self._dtype = self._impl.dtype(column)
    self._input_dtype = self._impl.input_dtype(column)
    self._indices_dtype = dtypes.int32
    self._max_to_keep = int(self._size * load_factor)
    self._name = ops.get_default_graph().unique_name(f'{column}_buffer')

    self._total_bytes = self._calculate_total_bytes()

    if self._total_bytes > 0:
      self._initialize_index()
      self._initialize_storage()

  def _calculate_total_bytes(self):
    r'''Calculate total bytes.
    '''
    if 'gpu' in Context.canonicalize([self._device])[0].lower():
      return 0
    emb_vec_size = self._dimension * self._dtype.size
    if emb_vec_size < 4 * self._indices_dtype.size:
      return 0
    return self._size * emb_vec_size

  def _initialize_index(self):
    r'''Initialize buffer index.
    '''
    with ops.name_scope(self.name):
      with ops.control_dependencies(None):
        with ops.device('/cpu:0'):
          self._index = _ops.hb_embedding_buffer_index_handle_op(
            shared_name=f'{self.name}_index',
            dtype=self._input_dtype,
            indices_dtype=self._indices_dtype)
          index_create_op = _ops.hb_embedding_buffer_index_create(
            self._index,
            size=self._size,
            shared_name=f'{self.name}_index',
            dtype=self._input_dtype,
            indices_dtype=self._indices_dtype)
          index_is_initialized_op = (
            _ops.hb_embedding_buffer_index_is_initialized(
              self._index,
              dtype=self._input_dtype,
              indices_dtype=self._indices_dtype))
        ops.add_to_collection(
          ops.GraphKeys.LOCAL_RESOURCES,
          EmbeddingBuffer.IndexResource(
            self._name,
            self._index,
            index_create_op,
            index_is_initialized_op))

  def _initialize_storage(self):
    r'''Initialize buffer storage.
    '''
    with ops.name_scope(self.name):
      self._storage = vs.get_variable(
        f'{self.name}_storage',
        shape=[self._size, self._dimension],
        dtype=self._dtype,
        initializer=init_ops.zeros_initializer(),
        trainable=True,
        use_resource=False,
        collections=[
          ops.GraphKeys.LOCAL_VARIABLES,
          GraphKeys.NOT_REPLICATED])

  @property
  def name(self):
    r'''Name of the embedding buffer.
    '''
    return self._name

  @property
  def total_bytes(self):
    r'''Total bytes of the embedding buffer.
    '''
    return self._total_bytes

  @property
  def size(self):
    r'''Size of the buffer.
    '''
    return self._size

  @property
  def max_to_keep(self):
    r'''Max items to keep after flushing.
    '''
    return self._max_to_keep

  @property
  def storage(self):
    r'''Storage of the embedding buffer.
    '''
    return self._storage

  @property
  def sharded(self):
    r'''If the weight is sharded.
    '''
    return self._sharded

  @property
  def column(self):
    r'''Name of the input column.
    '''
    return self._column

  def __call__(self, weight, ids):
    r'''Look up embeddings with buffering.
    '''
    if self.total_bytes <= 0:
      with ops.device(self._device):
        return self._impl.lookup(
          self._column, weight, ids,
          sharded=self.sharded)

    Context.get().add_saving_listener(
      self._name, self.CheckpointSaverListener(self.flush(weight)))
    return _lookup_buffered(self, weight, ids)

  def index_lookup(self, ids):
    r'''Lookup in the index.
    '''
    with ops.device('/cpu:0'):
      return _ops.hb_embedding_buffer_index_lookup(
        self._index, ids,
        indices_dtype=self._indices_dtype,
        name=f'{self._name}_index_lookup')

  def is_overflowed(self):
    r'''If True, the buffer is overflowed.
    '''
    with ops.device('/cpu:0'):
      return _ops.hb_embedding_buffer_index_is_overflowed(
        self._index,
        dtype=self._input_dtype,
        indices_dtype=self._indices_dtype)

  def flush(self, weight):
    r'''Flush buffer back to the backend.
    '''
    with ops.device('/cpu:0'):
      all_ids, all_indices = _ops.hb_embedding_buffer_index_dump(
        self._index,
        dtype=self._input_dtype,
        indices_dtype=self._indices_dtype,
        max_to_keep=self._max_to_keep)
    all_embs = array_ops.gather(self._storage, all_indices)
    with ops.device(self._device):
      return self._impl.update(
        self._column, weight, ops.IndexedSlices(all_embs, all_ids, None))

  def sync(self, weight, indices, miss_embs, miss_indices):
    r'''Synchronize buffer from backend.
    '''
    def _initialize():
      initialize_op = self._storage.scatter_update(
        ops.IndexedSlices(miss_embs, miss_indices, None))
      return control_flow_ops.group([initialize_op])

    def _initialize_overflowed():
      with ops.control_dependencies([self.flush(weight)]):
        move_hit_mask = math_ops.greater(indices, self._max_to_keep)
        move_hit_indices = array_ops.boolean_mask(indices, move_hit_mask)
        move_hit_size = array_ops.size(move_hit_indices)
        move_hit_embs = array_ops.gather(self._storage, move_hit_indices)
        new_move_hit_indices = math_ops.range(
          self._max_to_keep,
          move_hit_size + self._max_to_keep)
        new_miss_indices = miss_indices - (self._size - self._max_to_keep)
        move_hit_op = self._storage.scatter_update(
          ops.IndexedSlices(move_hit_embs, new_move_hit_indices, None))
        move_miss_op = self._storage.scatter_update(
          ops.IndexedSlices(miss_embs, new_miss_indices, None))
        return control_flow_ops.group([move_hit_op, move_miss_op])
    return control_flow_ops.cond(
      self.is_overflowed(), _initialize_overflowed, _initialize)
