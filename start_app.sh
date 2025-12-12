#!/bin/bash

# 百万字小说AI创作器 - 启动脚本

set -e

echo "=========================================="
echo "   📚 百万字小说AI创作器"
echo "   Million-Word-Novel-AI-Creator"
echo "=========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3.8或更高版本"
    exit 1
fi

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到pip3，请先安装pip"
    exit 1
fi

# 检查依赖
echo "🔍 检查依赖包..."
REQUIRED_PACKAGES=("streamlit" "langchain" "openai")
for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import $package" &> /dev/null; then
        echo "⚠️ 缺少依赖包: $package"
        echo "正在安装依赖包..."
        pip3 install -r requirements.txt
        break
    fi
done

# 检查环境变量
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "⚠️ 未找到.env文件，从.example文件创建"
        cp .env.example .env
        echo "✅ 已创建.env文件"
        echo "请编辑.env文件，填入您的DeepSeek API密钥"
    else
        echo "❌ 未找到.env.example文件"
        exit 1
    fi
fi

# 检查必要的目录
echo "📁 检查目录..."
DIRECTORIES=("outputs" "memory" "templates")
for dir in "${DIRECTORIES[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "创建目录: $dir"
        mkdir -p "$dir"
    fi
done

# 启动应用
echo ""
echo "🚀 启动百万字小说AI创作器..."
echo ""
echo "应用将在浏览器中打开，地址为: http://localhost:8501"
echo "按 Ctrl+C 停止应用"
echo ""

# 设置Streamlit配置
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 运行应用
python3 -m streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=false \
    --browser.gatherUsageStats=false