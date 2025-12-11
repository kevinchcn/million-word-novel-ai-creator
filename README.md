# Million-Word-Novel-AI-Creator
基于LangChain和DeepSeek API的智能长篇小说创作系统，专为百万字级小说设计，具备完整的一致性保持、长时记忆和批量生成能力。

🎯 项目特色
📖 超长篇幅支持：专为10万-100万字小说设计
🧠 智能记忆系统：分层记忆架构，解决长文本一致性问题
🔍 多维度验证：实时一致性检查，自动修复矛盾
⚡ 批量生成：一次生成多个章节，提高创作效率
🔄 一体化调整：统一调整叙事风格、节奏和人物关系
📊 进度监控：实时创作进度和质量评估

1. 架构
2. 安装依赖
   pip install -r requirements.txt

3. 配置环境
   # 复制环境变量文件
    cp .env.example .env
    
    # 编辑.env文件，填入你的DeepSeek API密钥
    # DEEPSEEK_API_KEY=your_api_key_here

4.运行应用
    streamlit run main.py
