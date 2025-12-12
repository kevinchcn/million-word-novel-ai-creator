#!/usr/bin/env python3
"""
安装脚本 - 设置百万字小说AI创作器
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     📚 百万字小说AI创作器 - 安装程序                          ║
    ║    Million-Word-Novel-AI-Creator Setup                      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    
    if sys.version_info < (3, 8):
        print(f"❌ Python版本过低: {sys.version}")
        print("   请安装Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本符合要求: {sys.version}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("\n📦 安装依赖包...")
    
    # 检查pip是否可用
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
    except:
        print("❌ pip不可用，请先安装pip")
        return False
    
    # 安装requirements.txt中的依赖
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"❌ 找不到依赖文件: {requirements_file}")
        return False
    
    try:
        print("正在安装依赖，这可能需要几分钟...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 依赖包安装完成")
            return True
        else:
            print(f"❌ 安装依赖失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 安装依赖时出错: {str(e)}")
        return False

def create_directories():
    """创建必要的目录"""
    print("\n📁 创建项目目录...")
    
    directories = [
        "./outputs",
        "./outputs/novels",
        "./outputs/outlines",
        "./outputs/logs",
        "./memory",
        "./memory/characters",
        "./memory/summaries",
        "./memory/relationships",
        "./memory/plots",
        "./memory/locations",
        "./memory/backups",
        "./templates",
        "./backups"
    ]
    
    created_count = 0
    for directory in directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"  ✅ 创建目录: {directory}")
            created_count += 1
        except Exception as e:
            print(f"  ⚠️ 创建目录失败 {directory}: {str(e)}")
    
    print(f"✅ 创建了 {created_count} 个目录")
    return True

def copy_env_file():
    """复制环境变量示例文件"""
    print("\n⚙️ 设置环境变量...")
    
    env_example = ".env.example"
    env_file = ".env"
    
    if not os.path.exists(env_example):
        print(f"❌ 找不到环境变量示例文件: {env_example}")
        return False
    
    if os.path.exists(env_file):
        print(f"⚠️ 环境变量文件已存在: {env_file}")
        print("   如果您需要重新配置，请手动编辑该文件")
    else:
        try:
            import shutil
            shutil.copy2(env_example, env_file)
            print(f"✅ 已创建环境变量文件: {env_file}")
            print("   请编辑该文件，填入您的DeepSeek API密钥")
        except Exception as e:
            print(f"❌ 复制环境变量文件失败: {str(e)}")
            return False
    
    return True

def create_templates():
    """创建模板文件"""
    print("\n📝 创建模板文件...")
    
    try:
        # 运行模板创建脚本
        if os.path.exists("create_templates.py"):
            subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True)
            print("✅ 模板文件创建完成")
        else:
            print("⚠️ 模板创建脚本不存在，跳过此步骤")
    except Exception as e:
        print(f"⚠️ 创建模板时出错: {str(e)}")
    
    return True

def create_shortcuts():
    """创建快捷方式（可选）"""
    print("\n🔗 创建快捷方式...")
    
    system = platform.system()
    
    if system == "Windows":
        # 创建Windows批处理文件
        batch_content = """@echo off
echo Starting Million-Word-Novel-AI-Creator...
python -m streamlit run app.py
pause
"""
        
        with open("start_app.bat", "w", encoding='utf-8') as f:
            f.write(batch_content)
        print("✅ 已创建启动脚本: start_app.bat")
        
    elif system == "Linux" or system == "Darwin":
        # 创建Linux/Mac shell脚本
        shell_content = """#!/bin/bash
echo "Starting Million-Word-Novel-AI-Creator..."
python -m streamlit run app.py
"""
        
        with open("start_app.sh", "w", encoding='utf-8') as f:
            f.write(shell_content)
        
        # 添加执行权限
        os.chmod("start_app.sh", 0o755)
        print("✅ 已创建启动脚本: start_app.sh")
    
    return True

def verify_installation():
    """验证安装结果"""
    print("\n🔍 验证安装...")
    
    # 检查必要文件
    required_files = [
        "requirements.txt",
        "app.py",
        "main.py",
        "config.yaml"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有必要文件都存在")
    
    # 检查Python模块
    # NOTE: the PyYAML package exposes the module name 'yaml' (not 'pyyaml').
    required_modules = [
        "streamlit",
        "langchain",
        "openai",
        "pydantic",
        "yaml"
    ]
    
    print("检查Python模块...")
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} 未安装")
            return False
    
    print("✅ 所有必要模块都已安装")
    return True

def print_instructions():
    """打印使用说明"""
    instructions = """
    🎉 安装完成！
    
    📋 接下来需要做的：
    
    1. 配置API密钥
       编辑 .env 文件，填入您的DeepSeek API密钥：
          DEEPSEEK_API_KEY=您的API密钥
    
    2. 启动应用
       Windows: 双击 start_app.bat
       Linux/Mac: 运行 ./start_app.sh
       或者直接在命令行运行:
          streamlit run app.py
    
    3. 访问应用
       在浏览器中打开: http://localhost:8501
    
    4. 开始创作！
       在应用中输入创意，选择参数，开始生成您的小说
    
    📞 如需帮助：
       - 查看项目文档
       - 提交GitHub Issue
       - 联系开发者
    
    🚀 开始创作您的百万字小说吧！
    """
    
    print(instructions)

def main():
    """主安装函数"""
    print_banner()
    
    print("开始安装百万字小说AI创作器...")
    print("=" * 60)
    
    # 执行安装步骤
    steps = [
        ("检查Python版本", check_python_version),
        ("安装依赖包", install_dependencies),
        ("创建项目目录", create_directories),
        ("设置环境变量", copy_env_file),
        ("创建模板文件", create_templates),
        ("创建快捷方式", create_shortcuts),
        ("验证安装", verify_installation)
    ]
    
    success = True
    for step_name, step_func in steps:
        print(f"\n[{step_name}]")
        if not step_func():
            print(f"❌ {step_name} 失败")
            success = False
            break
    
    if success:
        print_instructions()
        return 0
    else:
        print("\n❌ 安装失败，请检查错误信息并重试")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装过程中出现未知错误: {str(e)}")
        sys.exit(1)