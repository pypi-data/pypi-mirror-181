/*
 * Copyright (c) 2022, NVIDIA CORPORATION.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#pragma once

#include "common.hpp"
#include "embedding.hpp"
#include "operators/communication.hpp"
#include "operators/compress_offset.hpp"
#include "operators/dp_index_calculation.hpp"
#include "operators/model_backward.hpp"
#include "operators/model_forward.hpp"

namespace embedding {

class UniformDPEmbedding : public IGroupedEmbeddingOp {
  std::shared_ptr<CoreResourceManager> core_;
  UniformDataParallelEmbeddingMeta meta_;

  DPIndexCalculation index_calculation_;
  DPLocalReduceIndexCalculation dp_local_reduce_index_calculation_;
  CompressOffset compress_offset_;
  DPModelForward dp_model_forward_;
  AverageCombiner average_combiner_;

  DPLocalReduce dp_local_reduce_;
  NcclAllReduceInplaceComm allreduce_comm_;

  TensorList embedding_vec_;
  int batch_size_;
  Tensor keys_;
  size_t num_keys_;
  Tensor bucket_range_;

 public:
  UniformDPEmbedding(std::shared_ptr<CoreResourceManager> core,
                     const EmbeddingCollectionParam &params, size_t grouped_id);

  void forward_per_gpu(const Tensor &keys, const Tensor &bucket_range, size_t num_keys,
                       ILookup *embedding_table, Tensor &output_buffer, int batch_size) override;

  void backward_per_gpu(const Tensor &top_grad, bool do_allreduce, Tensor *unique_key,
                        size_t *num_unique_key, Tensor *num_unique_key_per_table_offset,
                        size_t *num_table_offset, Tensor *table_id_list, Tensor *wgrad,
                        Tensor *wgrad_idx_offset) override;
};
}  // namespace embedding
