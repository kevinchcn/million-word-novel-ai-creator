#!/usr/bin/env python3
"""
Million-Word-Novel-AI-Creator 主程序入口
支持命令行模式和API模式
"""

import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.generator import NovelGenerator
from core.memory_system import SmartMemory
from utils.file_utils import ensure_directories

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="百万字小说AI创作器 - 命令行界面",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s --creative "一个程序员穿越到修真世界" --words 100000 --type 玄幻
  %(prog)s --config custom_config.yaml
  %(prog)s --interactive
        """
    )
    
    parser.add_argument(
        "--creative", 
        type=str, 
        help="创意描述",
        default=""
    )
    
    parser.add_argument(
        "--words", 
        type=int, 
        help="目标字数",
        default=100000
    )
    
    parser.add_argument(
        "--type", 
        type=str, 
        help="小说类型",
        choices=["玄幻", "仙侠", "都市", "科幻", "悬疑", "言情", "历史", "军事"],
        default="玄幻"
    )
    
    parser.add_argument(
        "--style", 
        type=str, 
        help="写作风格",
        choices=["轻松幽默", "严肃正剧", "文艺细腻", "快节奏", "慢热细腻", "群像描写"],
        default="严肃正剧"
    )
    
    parser.add_argument(
        "--chapters", 
        type=int, 
        help="生成章节数",
        default=3
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        help="输出目录",
        default="./outputs"
    )
    
    parser.add_argument(
        "--config", 
        type=str, 
        help="配置文件路径",
        default="config.yaml"
    )
    
    parser.add_argument(
        "--interactive", 
        action="store_true",
        help="交互模式"
    )
    
    return parser.parse_args()

def init_environment():
    """初始化环境"""
    # 确保必要的目录存在
    directories = [
        "./outputs",
        "./outputs/novels",
        "./outputs/outlines",
        "./outputs/logs",
        "./memory",
        "./memory/characters",
        "./memory/summaries",
        "./templates"
    ]
    
    for directory in directories:
        ensure_directories(directory)
    
    print("✅ 环境初始化完成")

# 在 interactive_mode 函数中修改
def interactive_mode():
    """交互模式"""
    print("\n" + "="*60)
    print("百万字小说AI创作器 - 交互模式")
    print("="*60)
    
    creative = input("\n📝 请输入你的小说创意: ")
    
    print("\n📊 请选择目标字数:")
    print("1. 3000字 (测试)")
    print("2. 5000字 (测试)")
    print("3. 1万字 (测试)")
    print("4. 10万字")
    print("5. 30万字")
    print("6. 50万字")
    print("7. 80万字")
    print("8. 100万字")
    print("9. 自定义")
    
    word_choice = input("请选择 (1-9): ")
    
    word_options = {
        "1": 3000,
        "2": 5000,
        "3": 10000,
        "4": 100000,
        "5": 300000,
        "6": 500000,
        "7": 800000,
        "8": 1000000
    }
    
    if word_choice == "9":
        words = int(input("请输入字数: "))
    else:
        words = word_options.get(word_choice, 3000)
    
    print("\n🎭 请选择小说类型:")
    types = ["玄幻", "仙侠", "都市", "科幻", "悬疑", "言情", "历史", "军事"]
    for i, t in enumerate(types, 1):
        print(f"{i}. {t}")
    
    type_idx = int(input("请选择 (1-8): ")) - 1
    novel_type = types[type_idx] if 0 <= type_idx < len(types) else "玄幻"
    
    return {
        "creative": creative,
        "words": words,
        "type": novel_type
    }

def main():
    """主函数"""
    args = parse_arguments()
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 错误: 请设置 DEEPSEEK_API_KEY 环境变量")
        print("   1. 复制 .env.example 为 .env")
        print("   2. 在 .env 中填入你的API密钥")
        sys.exit(1)
    
    # 初始化环境
    init_environment()
    
    # 交互模式
    if args.interactive or not args.creative:
        params = interactive_mode()
        args.creative = params["creative"]
        args.words = params["words"]
        args.type = params["type"]
    
    if not args.creative:
        print("❌ 错误: 需要提供创意描述")
        sys.exit(1)
    
    print(f"\n🚀 开始生成小说...")
    print(f"   创意: {args.creative[:50]}...")
    print(f"   字数: {args.words:,}字")
    print(f"   类型: {args.type}")
    print(f"   风格: {args.style}")
    
    try:
        # 初始化生成器
        generator = NovelGenerator(api_key)
        memory = SmartMemory()
        
        # 生成大纲
        print("\n📋 正在生成大纲...")
        outline = generator.generate_outline(
            creative=args.creative,
            word_count=args.words,
            novel_type=args.type,
            writing_style=args.style
        )
        
        # 保存大纲
        from utils.file_utils import save_json
        save_json(outline, f"./outputs/outlines/{outline.get('title', 'novel')}_outline.json")
        
        print(f"✅ 大纲生成完成: {outline.get('title', '未命名')}")
        
        # 生成人物
        print("\n👥 正在生成人物设定...")
        characters = generator.generate_characters(outline)
        memory.save_characters(characters)
        
        print(f"✅ 人物生成完成: {len(characters)} 个角色")
        
        # 生成章节
        print(f"\n📖 正在生成前 {args.chapters} 章...")
        for i in range(1, args.chapters + 1):
            print(f"   正在生成第 {i} 章...")
            
            # 获取上下文
            context = memory.get_context(i)
            
            # 生成章节
            chapter = generator.generate_chapter(
                chapter_number=i,
                outline=outline,
                characters=characters,
                context=context,
                target_words=3000
            )
            
            # 保存章节
            chapter_file = f"./outputs/novels/{outline.get('title', 'novel')}_chapter_{i}.txt"
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(chapter.get('content', ''))
            
            # 更新记忆
            memory.update_with_chapter(i, chapter)
            
            print(f"   ✅ 第 {i} 章完成: {chapter.get('title', f'第{i}章')}")
        
        print(f"\n🎉 小说生成完成!")
        print(f"   大纲文件: ./outputs/outlines/{outline.get('title', 'novel')}_outline.json")
        print(f"   章节文件: ./outputs/novels/{outline.get('title', 'novel')}_chapter_*.txt")
        
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()