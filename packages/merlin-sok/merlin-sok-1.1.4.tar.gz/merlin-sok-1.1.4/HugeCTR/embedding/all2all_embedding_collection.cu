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
#include <cub/cub.cuh>

#include "HugeCTR/include/utils.hpp"
#include "all2all_embedding_collection.hpp"
namespace embedding {
namespace tf {

namespace {

template <typename offset_t>
__global__ void reorder_row_lengths_kernel(const offset_t *row_lengths, int num_row_lengths,
                                           offset_t *bucket_range, int batch_size_per_gpu,
                                           int num_gpu, int num_embedding) {
  for (int tid = threadIdx.x + blockIdx.x * blockDim.x; tid < num_row_lengths;
       tid += blockDim.x * gridDim.x) {
    int gpu_id = tid / (batch_size_per_gpu * num_embedding);
    int embedding_id = (tid / batch_size_per_gpu) % num_embedding;
    int batch_id = tid % batch_size_per_gpu;

    int reorder_id =
        embedding_id * batch_size_per_gpu * num_gpu + gpu_id * batch_size_per_gpu + batch_id;
    bucket_range[1 + reorder_id] = row_lengths[tid];
  }
  if (threadIdx.x + blockIdx.x * blockDim.x == 0) {
    bucket_range[0] = 0;
  }
}

template <typename key_t, typename offset_t>
__global__ void reorder_key_kernel(const key_t *key, const offset_t *row_offsets,
                                   int num_row_lengths, const offset_t *bucket_range,
                                   key_t *reorder_key, int batch_size_per_gpu, int num_gpu,
                                   int num_embedding) {
  for (int tid = threadIdx.x + blockIdx.x * blockDim.x; tid < num_row_lengths;
       tid += blockDim.x * gridDim.x) {
    int gpu_id = tid / (batch_size_per_gpu * num_embedding);
    int embedding_id = (tid / batch_size_per_gpu) % num_embedding;
    int batch_id = tid % batch_size_per_gpu;

    int reorder_id =
        embedding_id * batch_size_per_gpu * num_gpu + gpu_id * batch_size_per_gpu + batch_id;
    offset_t start = (tid == 0) ? 0 : row_offsets[tid];
    offset_t end = row_offsets[tid + 1];
    for (offset_t r = 0; r < (end - start); ++r) {
      reorder_key[bucket_range[reorder_id] + r] = key[start + r];
    }
  }
}

}  // namespace

namespace swizzle_key {

void sparse_forward_per_gpu(std::shared_ptr<CoreResourceManager> core,
                            const std::vector<Tensor> &keys, const std::vector<Tensor> &row_lengths,
                            Tensor &key_all_gather_send_buffer,
                            Tensor &row_lengths_all_gather_send_buffer) {
  size_t key_bytes_offset = 0;
  size_t row_lengths_bytes_offset = 0;
  key_all_gather_send_buffer.get();
  for (size_t i = 0; i < keys.size(); ++i) {
    HCTR_LIB_THROW(cudaMemcpyAsync(
        reinterpret_cast<char *>(key_all_gather_send_buffer.get()) + key_bytes_offset,
        keys[i].get(), keys[i].nbytes(), cudaMemcpyDeviceToDevice,
        core->get_local_gpu()->get_stream()));
    key_bytes_offset += keys[i].nbytes();

    HCTR_LIB_THROW(
        cudaMemcpyAsync(reinterpret_cast<char *>(row_lengths_all_gather_send_buffer.get()) +
                            row_lengths_bytes_offset,
                        row_lengths[i].get(), row_lengths[i].nbytes(), cudaMemcpyDeviceToDevice,
                        core->get_local_gpu()->get_stream()));
    row_lengths_bytes_offset += row_lengths[i].nbytes();
  }
}
}  // namespace swizzle_key

namespace model_forward {

std::vector<size_t> get_model_comm_buffer_size(const UniformModelParallelEmbeddingMeta &meta,
                                               int num_gpus, int batch_size) {
  size_t num_ev_elements = 0;
  int batch_size_per_gpu = batch_size / num_gpus;
  for (int lookup_id : meta.h_local_lookup_id_list_) {
    int ev_size = meta.h_ev_size_list_[lookup_id];
    num_ev_elements += ev_size * batch_size_per_gpu;
  }
  return std::vector<size_t>(num_gpus, num_ev_elements);
}

void sparse_forward_per_gpu(std::shared_ptr<CoreResourceManager> core,
                            const UniformModelParallelEmbeddingMeta &meta,
                            const Tensor &key_all_gather_recv_buffer,
                            const Tensor &row_lengths_all_gather_recv_buffer, ILookup *emb_storage,
                            std::vector<Tensor> &emb_vec_model_buffer, int64_t *num_model_key,
                            int64_t *num_model_offsets, Tensor *ret_model_key,
                            Tensor *ret_model_offset) {
  HugeCTR::CudaDeviceContext context(core->get_device_id());

  int num_gpus = core->get_global_gpu_count();
  cudaStream_t stream = core->get_local_gpu()->get_stream();
  int batch_size = row_lengths_all_gather_recv_buffer.get_num_elements() / meta.num_lookup_;

  Tensor keys, bucket_range;
  size_t num_keys = static_cast<size_t>(key_all_gather_recv_buffer.get_num_elements());
  // the shape of key_all_gather is (num_gpus, num_embedding,
  // batch_size_per_gpu) the shape of key is (num_embedding, batch_size)
  auto reorder_from_all_gather_input = [&] {
    Tensor all_gather_row_offsets;

    auto buffer_ptr = GetBuffer(core);
    keys = buffer_ptr->reserve({key_all_gather_recv_buffer.get_num_elements()},
                               key_all_gather_recv_buffer.device(),
                               key_all_gather_recv_buffer.dtype());
    bucket_range = buffer_ptr->reserve({row_lengths_all_gather_recv_buffer.get_num_elements() + 1},
                                       row_lengths_all_gather_recv_buffer.device(),
                                       row_lengths_all_gather_recv_buffer.dtype());
    all_gather_row_offsets = buffer_ptr->reserve(
        {row_lengths_all_gather_recv_buffer.get_num_elements() + 1},
        row_lengths_all_gather_recv_buffer.device(), row_lengths_all_gather_recv_buffer.dtype());
    buffer_ptr->allocate();

    auto get_bucket_range = [&] {
      DISPATCH_INTEGRAL_FUNCTION(row_lengths_all_gather_recv_buffer.dtype().type(), offset_t, [&] {
        constexpr int block_size = 256;
        int grid_size =
            (row_lengths_all_gather_recv_buffer.get_num_elements() - 1) / block_size + 1;

        reorder_row_lengths_kernel<<<grid_size, block_size, 0, stream>>>(
            row_lengths_all_gather_recv_buffer.get<offset_t>(),
            row_lengths_all_gather_recv_buffer.get_num_elements(), bucket_range.get<offset_t>(),
            batch_size / num_gpus, num_gpus, meta.num_lookup_);

        size_t temp_bytes = 0;
        Tensor temp_scan_storage;
        cub::DeviceScan::InclusiveSum(nullptr, temp_bytes, (offset_t *)nullptr, (offset_t *)nullptr,
                                      bucket_range.get_num_elements());
        temp_scan_storage =
            buffer_ptr->reserve(temp_bytes, DeviceType::GPU, TensorScalarType::Void);
        buffer_ptr->allocate();

        cub::DeviceScan::InclusiveSum(temp_scan_storage.get(), temp_bytes,
                                      bucket_range.get<offset_t>(), bucket_range.get<offset_t>(),
                                      bucket_range.get_num_elements(), stream);

        // HCTR_LIB_THROW(cudaStreamSynchronize(stream));

        // std::vector<offset_t> gpu_bucket_range;
        // bucket_range.to(&gpu_bucket_range);
        // std::cout << "gpu_bucket_range:\n";
        // for (auto i : gpu_bucket_range) {
        //   std::cout << i << " ";
        // }
        // std::cout << "\n";
      });
    };

    auto scan_row_lengths = [&] {
      DISPATCH_INTEGRAL_FUNCTION(row_lengths_all_gather_recv_buffer.dtype().type(), offset_t, [&] {
        size_t temp_bytes = 0;
        Tensor temp_scan_storage;
        cub::DeviceScan::InclusiveSum(nullptr, temp_bytes, (offset_t *)nullptr, (offset_t *)nullptr,
                                      row_lengths_all_gather_recv_buffer.get_num_elements() + 1);
        temp_scan_storage =
            buffer_ptr->reserve(temp_bytes, DeviceType::GPU, TensorScalarType::Void);
        buffer_ptr->allocate();

        cub::DeviceScan::InclusiveSum(
            temp_scan_storage.get(), temp_bytes, row_lengths_all_gather_recv_buffer.get<offset_t>(),
            all_gather_row_offsets.get<offset_t>() + 1,
            row_lengths_all_gather_recv_buffer.get_num_elements(), stream);
        // HCTR_LIB_THROW(cudaStreamSynchronize(stream));

        // std::vector<offset_t> gpu_row_lengths;
        // row_lengths_all_gather_recv_buffer.to(&gpu_row_lengths);
        // std::cout << "gpu_row_lengths:\n";
        // for (auto i : gpu_row_lengths) {
        //   std::cout << i << " ";
        // }
        // std::cout << "\n";

        // std::vector<offset_t> gpu_row_offsets;
        // all_gather_row_offsets.to(&gpu_row_offsets);
        // std::cout << "gpu_row_offsets:\n";
        // for (auto i : gpu_row_offsets) {
        //   std::cout << i << " ";
        // }
        // std::cout << "\n";
      });
    };

    auto reorder_key = [&] {
      DISPATCH_INTEGRAL_FUNCTION(key_all_gather_recv_buffer.dtype().type(), key_t, [&] {
        DISPATCH_INTEGRAL_FUNCTION(
            row_lengths_all_gather_recv_buffer.dtype().type(), offset_t, [&] {
              constexpr int block_size = 256;
              int grid_size =
                  (row_lengths_all_gather_recv_buffer.get_num_elements() - 1) / block_size + 1;
              reorder_key_kernel<<<grid_size, block_size, 0, stream>>>(
                  key_all_gather_recv_buffer.get<key_t>(), all_gather_row_offsets.get<offset_t>(),
                  row_lengths_all_gather_recv_buffer.get_num_elements(),
                  bucket_range.get<offset_t>(), keys.get<key_t>(), batch_size / num_gpus, num_gpus,
                  meta.num_lookup_);
              // HCTR_LIB_THROW(cudaStreamSynchronize(stream));

              // std::vector<key_t> gpu_all_gather_key;
              // key_all_gather_recv_buffer.to(&gpu_all_gather_key);
              // std::cout << "gpu_all_gather_key:\n";
              // for (auto i : gpu_all_gather_key) {
              //   std::cout << i << " ";
              // }
              // std::cout << "\n";

              // std::vector<offset_t> gpu_reorder_key;
              // keys.to(&gpu_reorder_key);
              // std::cout << "gpu_reorder_key:\n";
              // for (auto i : gpu_reorder_key) {
              //   std::cout << i << " ";
              // }
              // std::cout << "\n";
            });
      });
    };

    get_bucket_range();
    scan_row_lengths();
    reorder_key();
  };
  reorder_from_all_gather_input();

  DataType key_type = key_all_gather_recv_buffer.dtype();
  ModelIndexCalculation model_index_calculation_ =
      ModelIndexCalculation(core, meta.num_local_lookup_, meta.num_local_hotness_,
                            meta.hotness_sum_, batch_size, key_type);

  Tensor model_key, model_offsets;
  size_t num_model_key_;
  model_index_calculation_.compute(keys, bucket_range, num_keys, meta.d_local_lookup_id_list_,
                                   meta.d_local_shard_id_list_, meta.d_local_num_shards_list_,
                                   batch_size, &model_key, &model_offsets, &num_model_key_);

  CompressOffset compress_offset_ = CompressOffset(core, meta.num_local_lookup_ + 1);
  Tensor num_key_per_lookup_offset;
  compress_offset_.compute(model_offsets, batch_size, &num_key_per_lookup_offset);

  HCTR_LIB_THROW(cudaStreamSynchronize(stream));
  TensorList embedding_vec = TensorList(core.get(), key_all_gather_recv_buffer.get_num_elements(),
                                        DeviceType::GPU, TensorScalarType::Float32);
  emb_storage->lookup(model_key, num_model_key_, num_key_per_lookup_offset,
                      meta.num_local_lookup_ + 1, meta.d_local_table_id_list_, embedding_vec);

  ModelForward model_forward_ = ModelForward(core, num_gpus, meta.h_local_lookup_id_list_);

  TensorList model_comm_buffer{core.get(), emb_vec_model_buffer, DeviceType::GPU,
                               emb_vec_model_buffer[0].dtype(), stream};
  model_forward_.compute(embedding_vec, model_offsets, model_comm_buffer,
                         meta.d_local_ev_size_list_, meta.d_local_ev_size_offset_, batch_size,
                         meta.max_ev_size_);

  *ret_model_key = model_key;
  *ret_model_offset = model_offsets;
  *num_model_key = static_cast<int64_t>(num_model_key_);
  *num_model_offsets = model_offsets.get_num_elements();
}

void copy_model_keys_and_offsets(std::shared_ptr<CoreResourceManager> core, const Tensor &model_key,
                                 const Tensor &model_offset, Tensor &tf_model_key,
                                 Tensor &tf_model_offsets) {
  HCTR_LIB_THROW(cudaMemcpyAsync(tf_model_key.get(), model_key.get(), tf_model_key.nbytes(),
                                 cudaMemcpyDeviceToDevice, core->get_local_gpu()->get_stream()));
  HCTR_LIB_THROW(cudaMemcpyAsync(tf_model_offsets.get(), model_offset.get(),
                                 tf_model_offsets.nbytes(), cudaMemcpyDeviceToDevice,
                                 core->get_local_gpu()->get_stream()));
}
}  // namespace model_forward

namespace network_forward {

void sparse_forward_per_gpu(std::shared_ptr<CoreResourceManager> core,
                            const UniformModelParallelEmbeddingMeta &meta,
                            const std::vector<Tensor> &emb_vec_network_buffer,
                            const std::vector<Tensor> &row_lengths,
                            std::vector<Tensor> &forward_emb_vec) {
  HugeCTR::CudaDeviceContext context(core->get_device_id());
  cudaStream_t stream = core->get_local_gpu()->get_stream();
  int num_gpus = core->get_global_gpu_count();
  NetworkForward network_forward = NetworkForward(core, num_gpus);
  int batch_size_per_gpu = row_lengths[0].get_num_elements();
  int batch_size = batch_size_per_gpu * num_gpus;
  int global_gpu_id = core->get_global_gpu_id();

  TensorList row_lengths_buffer{core.get(), row_lengths, DeviceType::GPU, row_lengths[0].dtype(),
                                stream};
  TensorList network_comm_buffer{core.get(), emb_vec_network_buffer, DeviceType::GPU,
                                 emb_vec_network_buffer[0].dtype(), stream};
  TensorList output_buffer{core.get(), forward_emb_vec, DeviceType::GPU, forward_emb_vec[0].dtype(),
                           stream};
  network_forward.compute(row_lengths_buffer, meta.d_combiner_list_, network_comm_buffer,
                          meta.network_ids_, meta.network_gpu_ids_, meta.network_offsets_,
                          meta.network_dst_lookup_ids_, meta.network_ev_sizes_,
                          meta.network_ev_offsets_, output_buffer, meta.d_ev_size_offset_,
                          batch_size, meta.max_ev_size_);
}
}  // namespace network_forward

namespace network_backward {

void backward_per_gpu(std::shared_ptr<CoreResourceManager> core,
                      const UniformModelParallelEmbeddingMeta &meta,
                      const std::vector<Tensor> &top_grad, const std::vector<Tensor> &row_lengths,
                      std::vector<Tensor> &emb_vec_network_buffer) {
  HugeCTR::CudaDeviceContext context(core->get_device_id());
  cudaStream_t stream = core->get_local_gpu()->get_stream();
  int num_gpus = core->get_global_gpu_count();
  int batch_size_per_gpu = row_lengths[0].get_num_elements();
  int batch_size = batch_size_per_gpu * num_gpus;

  NetworkBackward network_backward = NetworkBackward(core, num_gpus);

  TensorList row_lengths_buffer{core.get(), row_lengths, DeviceType::GPU, row_lengths[0].dtype(),
                                stream};
  TensorList network_comm_buffer{core.get(), emb_vec_network_buffer, DeviceType::GPU,
                                 emb_vec_network_buffer[0].dtype(), stream};
  TensorList top_grad_buffer{core.get(), top_grad, DeviceType::GPU, top_grad[0].dtype(), stream};

  network_backward.compute(row_lengths_buffer, meta.d_combiner_list_, top_grad_buffer,
                           meta.network_ids_, meta.network_gpu_ids_, meta.network_offsets_,
                           meta.network_dst_lookup_ids_, meta.network_ev_sizes_,
                           meta.network_ev_offsets_, network_comm_buffer, meta.d_ev_size_offset_,
                           batch_size, meta.max_ev_size_);
}
}  // namespace network_backward

namespace model_backward {

void sparse_backward_per_gpu(std::shared_ptr<CoreResourceManager> core,
                             const UniformModelParallelEmbeddingMeta &meta,
                             const std::vector<Tensor> &emb_vec_model_buffer,
                             const Tensor &model_key, const Tensor &model_offsets,
                             std::vector<int> *num_unique_key_per_table,
                             std::vector<int> *table_id_list, Tensor *ret_continous_unique_key,
                             Tensor *ret_continous_emb_vec) {
  HugeCTR::CudaDeviceContext context(core->get_device_id());
  int num_gpus = core->get_global_gpu_count();
  cudaStream_t stream = core->get_local_gpu()->get_stream();
  int batch_size = (model_offsets.get_num_elements() - 1) / meta.num_local_lookup_;
  size_t num_model_key = static_cast<size_t>(model_key.get_num_elements());

  Tensor num_key_per_lookup_offset;
  CompressOffset compress_offset{core, meta.num_local_lookup_ + 1};
  compress_offset.compute(model_offsets, batch_size, &num_key_per_lookup_offset);

  ModelBackwardIndexCalculation model_backward_index_calculation_ = ModelBackwardIndexCalculation(
      core, num_gpus, meta.num_local_lookup_, meta.h_local_hotness_list_,
      meta.h_local_table_id_list_, meta.h_local_ev_size_list_, batch_size, model_key.dtype());

  Tensor continous_unique_key, wgrad_idx_offset, sorted_bucket_id_list, sorted_bucket_id_offset,
      d_table_id_list, num_unique_key_per_table_offset, continous_grad_emb_ev, coordinate_key,
      coordinate_wgrad_dst_idx;
  size_t num_unique_key;
  model_backward_index_calculation_.compute(
      model_key, num_model_key, model_offsets, num_key_per_lookup_offset,
      meta.d_local_table_id_list_, batch_size, &continous_unique_key, &num_unique_key,
      &wgrad_idx_offset, &sorted_bucket_id_list, &sorted_bucket_id_offset, &d_table_id_list,
      &num_unique_key_per_table_offset, &coordinate_key, &coordinate_wgrad_dst_idx);

  ModelBackward model_backward_ =
      ModelBackward(core, num_gpus, meta.num_local_lookup_, meta.h_local_hotness_list_,
                    meta.h_local_ev_size_list_, batch_size, meta.max_ev_size_, meta.num_sms_);

  TensorList model_comm_buffer{core.get(), emb_vec_model_buffer, DeviceType::GPU,
                               emb_vec_model_buffer[0].dtype(), stream};
  model_backward_.compute(model_comm_buffer, wgrad_idx_offset, sorted_bucket_id_list,
                          sorted_bucket_id_offset, num_unique_key, coordinate_key,
                          coordinate_wgrad_dst_idx, meta.d_local_ev_size_offset_, batch_size,
                          meta.max_ev_size_, num_model_key, &continous_grad_emb_ev);
  d_table_id_list.to(table_id_list, stream);
  *ret_continous_unique_key = continous_unique_key;
  *ret_continous_emb_vec = continous_grad_emb_ev;
  HCTR_LIB_THROW(cudaStreamSynchronize(stream));
  std::vector<uint32_t> gpu_num_key_per_table_offset;
  num_unique_key_per_table_offset.to(&gpu_num_key_per_table_offset);

  num_unique_key_per_table->resize(d_table_id_list.get_num_elements());
  for (int i = 0; i < d_table_id_list.get_num_elements(); ++i) {
    (*num_unique_key_per_table)[i] =
        gpu_num_key_per_table_offset[i + 1] - gpu_num_key_per_table_offset[i];
  }
}

void copy_backward_key_and_emb_vec(std::shared_ptr<CoreResourceManager> core,
                                   const Tensor &continous_unique_key,
                                   const Tensor &continous_emb_vec, std::vector<Tensor> &unique_key,
                                   std::vector<Tensor> &emb_vec) {
  size_t nbytes_key_offsets = 0ul;
  size_t nbytes_emb_vec_offsets = 0ul;
  for (size_t i = 0; i < unique_key.size(); ++i) {
    HCTR_LIB_THROW(cudaMemcpyAsync(
        unique_key[i].get(),
        reinterpret_cast<char *>(continous_unique_key.get()) + nbytes_key_offsets,
        unique_key[i].nbytes(), cudaMemcpyDeviceToDevice, core->get_local_gpu()->get_stream()));
    HCTR_LIB_THROW(cudaMemcpyAsync(
        emb_vec[i].get(),
        reinterpret_cast<char *>(continous_emb_vec.get()) + nbytes_emb_vec_offsets,
        emb_vec[i].nbytes(), cudaMemcpyDeviceToDevice, core->get_local_gpu()->get_stream()));
    nbytes_key_offsets += unique_key[i].nbytes();
    nbytes_emb_vec_offsets += emb_vec[i].nbytes();
  }
}
}  // namespace model_backward
}  // namespace tf
}  // namespace embedding
