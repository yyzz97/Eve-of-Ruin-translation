import os
import json
import re
from nltk.stem import WordNetLemmatizer
import nltk

# 确保下载 NLTK 必需的资源
#nltk.download('wordnet')
#nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# 定义函数：从文本中提取相关术语
def extract_relevant_terms(source_text, glossary):
    """
    从章节文本中提取术语，忽略大小写和单复数形式。
    """
    relevant_terms = {}
    # 归一化章节文本：去除标点并转换为小写
    normalized_text = re.sub(r"[^\w\s]", " ", source_text.lower())
    for term, translation in glossary.items():
        # 对术语进行词形还原和小写处理
        normalized_term = " ".join([lemmatizer.lemmatize(word.lower()) for word in term.split()])
        # 检查术语是否出现在文本中
        if re.search(r'\b' + re.escape(normalized_term) + r'\b', normalized_text):
            relevant_terms[term] = translation
    return relevant_terms

# 定义函数：批量处理章节文件
def process_chapters(input_folder, glossary_file, output_folder):
    """
    批量处理章节文本文件，为每个章节生成独立的词汇表。
    input_folder: 存放章节文本的文件夹路径
    glossary_file: 完整术语表文件路径
    output_folder: 存储生成词汇表的文件夹路径
    """
    # 加载完整词汇表
    with open(glossary_file, "r", encoding="utf-8") as file:
        glossary = json.load(file)

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历 input_folder 中的每个章节文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt") or filename.endswith(".md"):  # 处理 .txt 和 .md 文件
            chapter_path = os.path.join(input_folder, filename)
            with open(chapter_path, "r", encoding="utf-8") as chapter_file:
                chapter_text = chapter_file.read()

            # 提取章节中相关术语
            relevant_terms = extract_relevant_terms(chapter_text, glossary)

            # 将提取到的词汇表保存到 output_folder
            output_path = os.path.join(output_folder, f"{filename}_glossary.json")
            with open(output_path, "w", encoding="utf-8") as output_file:
                json.dump(relevant_terms, output_file, ensure_ascii=False, indent=4)

            print(f"章节文件 {filename} 的词汇表已生成并保存到 {output_path}")

# 主函数入口
if __name__ == "__main__":
    # 配置路径
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 工作区路径
    input_folder = os.path.join(workspace, "original")       # 原文文件夹路径
    glossary_file = os.path.join(workspace, "glossary", "total_glossary.json")  # 完整术语表路径
    output_folder = os.path.join(workspace, "glossary")      # 生成的词汇表存储路径

    # 执行批量处理
    process_chapters(input_folder, glossary_file, output_folder)