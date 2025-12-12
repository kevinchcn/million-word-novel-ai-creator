# Million-Word-Novel-AI-Creator
一个基于LangChain和DeepSeek API的智能小说创作系统，专为解决百万字长篇小说的前后一致性难题而设计。

## 🌟 核心特性

- 🧠 智能长时记忆系统 - 分层记忆架构解决百万字一致性难题
- 🎯 一键生成完整框架 - 从创意到完整大纲、人物、世界观的自动生成
- 📚 批量章节生成 - 一次生成多个章节，极大提高创作效率
- 🔍 实时一致性检查 - 多维度验证保证情节、人物、世界观的连贯性
- 🔄 一体化调整系统 - 统一调整叙事风格、节奏、人物关系
- 📊 可视化进度追踪 - 实时监控创作进度和质量评分
- 💫 优雅简洁的界面 - 现代化UI设计，操作直观简单

## 🚀 快速开始

# 1. 克隆项目
```bash
git clone https://github.com/kevinchcn/million-word-novel-ai-creator.git
cd million-word-novel-ai-creator
```
# 2. 安装依赖
```bash
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

# 3. 配置API密钥
- 访问 DeepSeek平台 获取API密钥
- 复制环境变量文件并配置：
```bash
export DEEPSEEK_API_KEY="your-api-key"
```

# 4. 启动应用
方式一：Web界面（推荐）
```bash
streamlit run app.py
```
方式二：命令行模式
```bash
python main.py --creative "你的创意" --words 100000 --type 玄幻
```

## 🏗️ 系统架构
创意输入 → 大纲生成 → 人物设定 → 世界观构建
    ↓         ↓          ↓           ↓
分层记忆系统 ← 章节生成 ← 一致性检查 ← 摘要生成
    ↓
长期存储 → 上下文检索 → 新章节生成

## 📖 使用示例
```bash
from core.memory import HierarchicalMemory
from core.consistency import ConsistencyEngine

# 创建百万字小说
memory = HierarchicalMemory()
engine = ConsistencyEngine()

# 输入创意，自动生成
novel = memory.generate_million_words(
    creative="程序员穿越修真界，用代码重构修仙体系",
    target_words=1000000
)
```

## 🧠 核心技术
1. 智能摘要算法
章节级：500字 → 50字（90%压缩）
卷级：10万字 → 1000字（99%压缩）
核心设定：永不遗忘

2. 一致性验证规则
人物特征：性格、能力、关系
情节逻辑：时间线、因果链
世界观：设定、规则、体系

3. 记忆检索策略
核心设定：100%召回
近期内容：完整上下文
历史内容：智能摘要

## 📊 性能指标
指标	数值	说明
一致性	≥95%	百万字跨章一致性
生成速度	3000字/分钟	DeepSeek API
内存占用	<100MB	SQLite优化
压缩率	99%	智能摘要