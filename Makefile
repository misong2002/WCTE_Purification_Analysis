# 定义源文件和目标文件
SRC_FILES := data/Water_data_aa data/Water_data_ab data/Water_data_ac data/Water_data_ad data/Water_data_ae data/Water_data_af data/Water_data_ag data/Water_data_ah
OUTPUT_FILE := data/merged.csv

# 默认目标
all: $(OUTPUT_FILE)

# 生成合并文件的规则
$(OUTPUT_FILE): $(SRC_FILES)
	@echo "Merging CSV files into $(OUTPUT_FILE)"
	
	cat $(SRC_FILES) >> $(OUTPUT_FILE)
# 清理中间文件（如果有的话）
clean:
	rm -f $(OUTPUT_FILE)

.PHONY: all clean
