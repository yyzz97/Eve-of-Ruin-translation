# Vecna: Eve of Ruin 翻译工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

专为《Vecna: Eve of Ruin》冒险模块设计的Markdown文档翻译工具，支持术语一致性管理和自动图片路径处理。

## 功能特性

- 基于DeepSeek API的批量翻译
- 术语表动态生成与管理
- 自动图片路径转换（支持本地/CDN）
- Markdown格式完整保留


## 快速开始

1. **环境准备**
```bash
pip install -r requirements.txt
export DEEPSEEK_API_KEY="your_api_key"
```

2. **文件准备**
- 将源Markdown文件放入 `/original`（需用户自行合法获取）
- 编辑 `/glossary/total_glossary.json`

1. **执行流程**
```bash
# 生成章节术语表
python scripts/generate_glossaries.py

# 处理图片路径
python scripts/img_replace.py

# 执行翻译
python scripts/translate_deepseek.py
```

## 项目结构
```
/project-root
├── original/         # 源文件（*.md）
├── translated/       # 翻译结果
├── glossary/         # 术语表文件
├── scripts/              # 处理脚本
└── requirements.txt      # 依赖清单
```

## 版权声明与数据来源
 **请严格遵守以下条款**：

1. **原文文件**  
   - 来源：[5e.tools](https://5e.tools/)
   - 声明：**本项目不包含任何受版权保护的原文内容**，用户需自行通过合法途径获取并存放至 `/original` 目录。

2. **术语词汇表**  
   - 来源：[Neverwinter Wiki 中文站](https://neverwinter.fandom.com/zh/wiki)（遵循其[使用条款](https://www.fandom.com/terms-of-use)）  
   - 用途：仅用于翻译一致性优化，不包含原文完整内容。

3. **用户责任**  
   - 禁止将翻译内容用于商业用途（除非获得原文版权方授权）  
   - 需在显著位置标注来源（示例：`译自《Vecna: Eve of Ruin》，原文来源：5e.tools`）

## 服务声明

### DeepSeek API 使用说明
本工具使用 [DeepSeek 智能模型 API](https://www.deepseek.com/) 实现翻译功能，需遵守以下条款：
1. **服务归属**：翻译结果由 DeepSeek 模型生成，其知识产权归属遵循[DeepSeek 用户协议](https://cdn.deepseek.com/policies/zh-CN/deepseek-terms-of-use.html)
2. **责任限制**：翻译内容可能存在误差，建议人工校对后使用
3. **合规要求**：禁止将 API 用于违法用途或生成有害内容

## 注意事项
1. **API密钥安全**  
   ```bash
   # 通过环境变量设置（推荐）
   export DEEPSEEK_API_KEY="your_api_key_here"
   ```

2. **图片路径处理**  
   - 默认转换至CDN地址（`https://5e.tools/`）
   - 本地路径支持：修改 `img_replace.py` 中的 `IMAGE_PREFIX` 变量
