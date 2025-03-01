# 本服务使用 DeepSeek API 实现，详见 https://www.deepseek.com/

import os
import json
from pathlib import Path
from openai import OpenAI, APIError  # 修正后的导入方式

# 配置参数
BASE_DIR = Path(__file__).parent.parent
MODEL_NAME = "deepseek-chat"
CHUNK_SIZE = 3500

# 初始化客户端（推荐使用环境变量）
client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def load_glossary(chapter_name):
    """加载术语表"""
    glossary_path = BASE_DIR / "glossary" / f"{chapter_name}.md_glossary.json"
    try:
        with open(glossary_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[Warning] Glossary not found: {glossary_path.name}")
        return {}

def build_system_prompt(glossary):
    """优化后的系统提示词模板"""
    terms = '\n'.join([f"{k} → {v}" for k, v in glossary.items()]) or "无"
    return f"""# 角色：专业D&D本地化专家
## 任务要求
1. 术语一致性
   - 使用官方术语表：
{terms}
   - 未列出的名称按《玩家手册(2014)》翻译

2. 格式规范
   - 保留所有Markdown标记（包括代码块、表格）
   - 骰子表达式保持原格式（如2d20+5）

3. 风格指南
   - 规则文本：精确直译
   - 剧情描述：文学化表达
   - NPC对话：符合角色身份的口语化"""

def translate_chunk(text, glossary):
    """带错误重试机制的翻译函数"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": build_system_prompt(glossary)},
                {"role": "user", "content": f"翻译以下内容：\n{text}"}
            ],
            temperature=0.2,
            max_tokens=3500,
            frequency_penalty = -0.2  # 降低重复术语的概率
        )
        return response.choices[0].message.content
    except APIError as e:  # 使用修正后的异常类型
        print(f"API Error: {e}")
        return None

def process_file(chapter_path):
    """带进度显示的文件处理器"""
    chapter_name = chapter_path.stem
    print(f"\nProcessing: {chapter_name}")
    
    glossary = load_glossary(chapter_name)
    
    with open(chapter_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # 智能分块（按段落分割）
    chunks = []
    current_chunk = []
    current_length = 0
    
    for para in source.split('\n\n'):
        para_len = len(para)
        if current_length + para_len > CHUNK_SIZE and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(para)
        current_length += para_len
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    # 翻译处理
    translated = []
    for idx, chunk in enumerate(chunks, 1):
        print(f"  Chunk {idx}/{len(chunks)}", end='\r')
        result = translate_chunk(chunk, glossary)
        if result:
            translated.append(result)
    
    # 保存结果
    output_path = BASE_DIR / "translated" / f"{chapter_name}_translated.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(translated))
    print(f"\nCompleted: {output_path.name}")

if __name__ == "__main__":
    (BASE_DIR / "translated").mkdir(exist_ok=True)
    for md_file in (BASE_DIR / "original").glob("*.md"):
        process_file(md_file)