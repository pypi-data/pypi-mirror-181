#pragma once
#include <core/hctr_impl/hctr_backend.hpp>
#include <embedding_storage/weight_io/data_info.hpp>
#include <embedding_storage/weight_io/fs_interface.hpp>
#include <embeddings/embedding_collection.hpp>
#include <memory>
#include <unordered_map>
#include <vector>

namespace embedding {

class EmbeddingParameterIO {
 public:
  EmbeddingParameterIO() = default;

  EmbeddingParameterIO(const EmbeddingParameterIO&) = delete;

  EmbeddingParameterIO& operator=(const EmbeddingParameterIO&) = delete;

  EmbeddingParameterIO(std::shared_ptr<HugeCTR::ResourceManager> resource_manager);

  void add_embedding_collection(EmbeddingCollection* embedding_collection);

  void load_metadata(const std::string& parameters_folder_path, int ebc_id,
                     struct EmbeddingParameterInfo& epi);
  void load_embedding_weight(const struct EmbeddingParameterInfo& epi, int fs_table_id,
                             Tensor& keys, Tensor& embedding_weights, embeddingFilter key_select,
                             std::shared_ptr<core::CoreResourceManager> core_resource,
                             const core::DataType& target_key_type = core::DataType(),
                             const core::DataType& target_value_type = core::DataType());

  void load_opt_state(const struct EmbeddingParameterInfo& epi, int fs_table_id, Tensor& keys,
                      Tensor& optimizer_buffer, embeddingFilter key_select,
                      std::shared_ptr<core::CoreResourceManager> core_resource,
                      const core::DataType& target_key_type = core::DataType(),
                      const core::DataType& target_value_type = core::DataType());

  void get_parameter_info_from_model(const std::string& path,
                                     std::vector<struct EmbeddingParameterInfo>& epis);

  void dump_metadata(const std::string& parameters_folder_path,
                     const struct EmbeddingParameterInfo& epi,
                     const std::vector<int>& table_ids = std::vector<int>());

  void dump_embedding_weight(const std::string& parameters_folder_path,
                             struct EmbeddingParameterInfo& epi,
                             const std::vector<int>& table_ids = std::vector<int>());

  void dump_opt_state(const std::string& parameters_folder_path, struct EmbeddingParameterInfo& epi,
                      const std::vector<int>& table_ids = std::vector<int>());

  static std::shared_ptr<EmbeddingWeightIO> get_fs_object(
      const std::string& file_name, SparseFSType fs_type = SparseFSType::AUTO);

 private:
  void write_file_head(const std::string& path, EmbeddingFileType file_type, int table_id,
                       std::shared_ptr<EmbeddingWeightIO>& fs);

 private:
  std::vector<EmbeddingCollection*> embedding_collections_;
  HugeCTR::ResourceManager* resource_manager_ = nullptr;
  std::vector<std::shared_ptr<core::CoreResourceManager>> core_list_;
};

}  // namespace embedding
