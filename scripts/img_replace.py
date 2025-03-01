import os
import re

def add_prefix_to_images_in_md(folder_path, prefix):
    """
    遍历指定文件夹中的所有 Markdown 文件，并为其中的图片路径添加前缀，同时保留图片备注。
    
    :param folder_path: str, 包含 Markdown 文件的文件夹路径
    :param prefix: str, 要添加到图片路径前的前缀
    """
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹 {folder_path} 不存在！")
        return

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):  # 只处理 Markdown 文件
            file_path = os.path.join(folder_path, filename)
            print(f"正在处理文件: {filename}")

            # 打开并读取文件内容
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # 使用正则表达式匹配 Markdown 图片路径
            # 匹配格式：![alt text](img/path/to/image.webp)
            updated_content = re.sub(
                r'!\[(.*?)\]\((img/.*?)\)',  # 匹配图片路径和备注
                lambda match: f"![{match.group(1)}]({prefix}{match.group(2)})",  # 替换路径并保留备注
                content
            )

            # 将更新后的内容写回文件
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(updated_content)

            print(f"文件 {filename} 处理完成！")

if __name__ == "__main__":
    # 文件夹路径配置
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 工作区根目录
    original_folder = os.path.join(workspace, "original")  # 原文文件夹路径

    # 图片路径前缀
    image_prefix = "https://5e.tools/"

    # 执行图片路径前缀添加
    add_prefix_to_images_in_md(original_folder, image_prefix)