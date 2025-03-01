import json

# 输入文件路径
input_file = "./glossary/EN·CN.txt"
output_file = "./glossary/total_glossary.json"

# 初始化字典
vocabulary_dict = {}

# 读取原始文件
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        # 跳过标题行
        if line.startswith("EN\tCN"):
            continue
        # 分割英文和中文
        parts = line.strip().split("\t")
        if len(parts) == 2:
            en, cn = parts
            vocabulary_dict[en] = cn

# 保存为 JSON 文件
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(vocabulary_dict, json_file, ensure_ascii=False, indent=4)

print(f"词汇表已成功转换为 JSON 格式并保存到 {output_file}")