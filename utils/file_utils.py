"""
文件工具函数
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

def ensure_directories(directory_path: str) -> bool:
    """
    确保目录存在
    
    Args:
        directory_path: 目录路径
        
    Returns:
        是否成功
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {directory_path}, 错误: {str(e)}")
        return False

def save_json(data: Dict[str, Any], file_path: str, indent: int = 2) -> bool:
    """
    保存数据为JSON文件
    
    Args:
        data: 要保存的数据
        file_path: 文件路径
        indent: 缩进空格数
        
    Returns:
        是否成功
    """
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory:
            ensure_directories(directory)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        
        return True
    except Exception as e:
        print(f"保存JSON文件失败: {file_path}, 错误: {str(e)}")
        return False

def load_json(file_path: str) -> Optional[Dict[str, Any]]:
    """
    从JSON文件加载数据
    
    Args:
        file_path: 文件路径
        
    Returns:
        加载的数据，失败返回None
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载JSON文件失败: {file_path}, 错误: {str(e)}")
        return None

def save_yaml(data: Dict[str, Any], file_path: str) -> bool:
    """
    保存数据为YAML文件
    
    Args:
        data: 要保存的数据
        file_path: 文件路径
        
    Returns:
        是否成功
    """
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory:
            ensure_directories(directory)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        
        return True
    except Exception as e:
        print(f"保存YAML文件失败: {file_path}, 错误: {str(e)}")
        return False

def load_yaml(file_path: str) -> Optional[Dict[str, Any]]:
    """
    从YAML文件加载数据
    
    Args:
        file_path: 文件路径
        
    Returns:
        加载的数据，失败返回None
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"加载YAML文件失败: {file_path}, 错误: {str(e)}")
        return None

def list_files(directory: str, extension: str = None) -> List[str]:
    """
    列出目录中的文件
    
    Args:
        directory: 目录路径
        extension: 文件扩展名（可选）
        
    Returns:
        文件路径列表
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        if os.path.isfile(item_path):
            if extension is None or item.endswith(extension):
                files.append(item_path)
    
    return files

def read_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    读取文件内容
    
    Args:
        file_path: 文件路径
        encoding: 文件编码
        
    Returns:
        文件内容，失败返回None
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {file_path}, 错误: {str(e)}")
        return None

def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
    """
    写入文件内容
    
    Args:
        file_path: 文件路径
        content: 要写入的内容
        encoding: 文件编码
        
    Returns:
        是否成功
    """
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory:
            ensure_directories(directory)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"写入文件失败: {file_path}, 错误: {str(e)}")
        return False

def backup_file(file_path: str, backup_dir: str = "./backups") -> Optional[str]:
    """
    备份文件
    
    Args:
        file_path: 原文件路径
        backup_dir: 备份目录
        
    Returns:
        备份文件路径，失败返回None
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        # 确保备份目录存在
        ensure_directories(backup_dir)
        
        # 生成备份文件名（包含时间戳）
        filename = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{filename}.{timestamp}.bak"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # 复制文件
        import shutil
        shutil.copy2(file_path, backup_path)
        
        return backup_path
    except Exception as e:
        print(f"备份文件失败: {file_path}, 错误: {str(e)}")
        return None

def count_words(text: str) -> int:
    """
    统计中文字数
    
    Args:
        text: 文本内容
        
    Returns:
        字数
    """
    # 简单实现：统计中文字符和标点
    import re
    
    # 统计中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', text)
    
    # 统计标点（中文标点）
    punctuation = re.findall(r'[，。！？；："「」『』【】（）《》]', text)
    
    return len(chinese_chars) + len(punctuation)

def get_file_size(file_path: str) -> Optional[int]:
    """
    获取文件大小（字节）
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件大小，失败返回None
    """
    try:
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        return None
    except:
        return None

def clean_old_files(directory: str, max_files: int = 100) -> int:
    """
    清理旧文件，保留最新的N个
    
    Args:
        directory: 目录路径
        max_files: 保留的最大文件数
        
    Returns:
        删除的文件数
    """
    if not os.path.exists(directory):
        return 0
    
    files = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        if os.path.isfile(item_path):
            mtime = os.path.getmtime(item_path)
            files.append((item_path, mtime))
    
    # 按修改时间排序
    files.sort(key=lambda x: x[1], reverse=True)
    
    deleted_count = 0
    for file_path, _ in files[max_files:]:
        try:
            os.remove(file_path)
            deleted_count += 1
        except:
            pass
    
    return deleted_count

# 测试函数
if __name__ == "__main__":
    # 测试目录创建
    test_dir = "./test_dir/sub_dir"
    if ensure_directories(test_dir):
        print(f"✅ 创建目录成功: {test_dir}")
    
    # 测试JSON保存和加载
    test_data = {
        "name": "测试数据",
        "value": 123,
        "list": [1, 2, 3]
    }
    
    test_json_file = "./test_dir/test.json"
    if save_json(test_data, test_json_file):
        print(f"✅ 保存JSON成功: {test_json_file}")
    
    loaded_data = load_json(test_json_file)
    if loaded_data:
        print(f"✅ 加载JSON成功: {loaded_data['name']}")
    
    # 测试字数统计
    test_text = "这是一个测试文本，包含中文和标点。"
    word_count = count_words(test_text)
    print(f"✅ 字数统计: {word_count} 字")
    
    # 清理测试目录
    import shutil
    if os.path.exists("./test_dir"):
        shutil.rmtree("./test_dir")
        print("✅ 清理测试目录")