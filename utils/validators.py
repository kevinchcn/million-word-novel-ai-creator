"""
验证器函数
用于验证各种输入和数据的有效性
"""

import re
from typing import Dict, Any, Optional, Tuple

def validate_api_key(api_key: str) -> Tuple[bool, str]:
    """
    验证API密钥格式
    
    Args:
        api_key: API密钥字符串
        
    Returns:
        (是否有效, 错误信息)
    """
    if not api_key:
        return False, "API密钥不能为空"
    
    # DeepSeek API密钥通常以'sk-'开头
    if not api_key.startswith('sk-'):
        return False, "API密钥格式不正确，应以'sk-'开头"
    
    if len(api_key) < 20:
        return False, "API密钥长度太短"
    
    return True, "API密钥格式正确"

def validate_novel_type(novel_type: str) -> Tuple[bool, str]:
    """
    验证小说类型
    
    Args:
        novel_type: 小说类型字符串
        
    Returns:
        (是否有效, 错误信息)
    """
    valid_types = [
        "玄幻", "仙侠", "都市", "科幻", "悬疑", 
        "言情", "历史", "军事", "武侠", "其他"
    ]
    
    if novel_type not in valid_types:
        return False, f"小说类型必须为: {', '.join(valid_types)}"
    
    return True, "小说类型有效"

def validate_word_count(word_count: int) -> Tuple[bool, str]:
    """
    验证字数
    
    Args:
        word_count: 字数
        
    Returns:
        (是否有效, 错误信息)
    """
    if word_count < 10000:
        return False, "字数至少为10000字"
    
    if word_count > 5000000:
        return False, "字数不能超过500万字"
    
    return True, "字数有效"

def validate_chapter_content(content: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    验证章节内容
    
    Args:
        content: 章节内容
        
    Returns:
        (是否有效, 错误信息, 统计信息)
    """
    if not content:
        return False, "章节内容不能为空", {}
    
    # 基本统计
    stats = {
        "length": len(content),
        "chinese_chars": 0,
        "paragraphs": 0,
        "sentences": 0
    }
    
    # 统计中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', content)
    stats["chinese_chars"] = len(chinese_chars)
    
    # 统计段落数
    paragraphs = [p for p in content.split('\n') if p.strip()]
    stats["paragraphs"] = len(paragraphs)
    
    # 统计句子数
    sentences = re.split(r'[。！？]', content)
    sentences = [s for s in sentences if s.strip()]
    stats["sentences"] = len(sentences)
    
    # 检查内容质量
    issues = []
    
    if stats["chinese_chars"] < 500:
        issues.append("内容过短（少于500字）")
    
    if stats["paragraphs"] < 3:
        issues.append("段落数过少（建议至少3段）")
    
    if stats["sentences"] < 5:
        issues.append("句子数过少（建议至少5句）")
    
    # 检查重复内容
    if len(content) > 100:
        # 检查是否有大量重复
        words = content.split()
        if len(words) > 20:
            word_freq = {}
            for word in words:
                if len(word) > 1:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # 检查是否有词出现太频繁
            for word, freq in word_freq.items():
                if freq > len(words) * 0.1:  # 超过10%
                    issues.append(f"词语'{word}'出现过于频繁")
                    break
    
    if issues:
        return False, "; ".join(issues), stats
    else:
        return True, "内容验证通过", stats

def validate_creative_input(creative: str) -> Tuple[bool, str]:
    """
    验证创意输入
    
    Args:
        creative: 创意描述
        
    Returns:
        (是否有效, 错误信息)
    """
    if not creative:
        return False, "创意描述不能为空"
    
    if len(creative) < 20:
        return False, "创意描述太短，请至少输入20字"
    
    if len(creative) > 5000:
        return False, "创意描述太长，请控制在5000字以内"
    
    # 检查是否包含有效内容（中文字符）
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', creative)
    if len(chinese_chars) < 10:
        return False, "创意描述中有效内容过少"
    
    return True, "创意输入有效"

def validate_chapter_number(chapter_num: int, max_chapter: int = 1000) -> Tuple[bool, str]:
    """
    验证章节编号
    
    Args:
        chapter_num: 章节编号
        max_chapter: 最大章节数限制
        
    Returns:
        (是否有效, 错误信息)
    """
    if chapter_num < 1:
        return False, "章节编号必须大于0"
    
    if chapter_num > max_chapter:
        return False, f"章节编号不能超过{max_chapter}"
    
    return True, "章节编号有效"

def validate_output_path(path: str) -> Tuple[bool, str]:
    """
    验证输出路径
    
    Args:
        path: 文件路径
        
    Returns:
        (是否有效, 错误信息)
    """
    if not path:
        return False, "输出路径不能为空"
    
    # 检查路径格式
    try:
        import os
        # 尝试规范化路径
        normalized = os.path.normpath(path)
        
        # 检查是否包含非法字符
        illegal_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in illegal_chars:
            if char in path:
                return False, f"路径包含非法字符: {char}"
        
        return True, "输出路径有效"
    except Exception as e:
        return False, f"路径格式错误: {str(e)}"

def validate_consistency_threshold(threshold: int) -> Tuple[bool, str]:
    """
    验证一致性阈值
    
    Args:
        threshold: 阈值（0-100）
        
    Returns:
        (是否有效, 错误信息)
    """
    if threshold < 0 or threshold > 100:
        return False, "一致性阈值必须在0-100之间"
    
    if threshold < 60:
        return False, "一致性阈值建议不低于60"
    
    return True, "一致性阈值有效"

# 综合验证函数
def validate_novel_creation_params(params: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
    """
    验证小说创作参数
    
    Args:
        params: 参数字典
        
    Returns:
        (是否有效, 错误信息, 验证详情)
    """
    validation_results = {}
    
    # 检查必要参数
    required_params = ['creative', 'word_count', 'novel_type']
    for param in required_params:
        if param not in params:
            return False, f"缺少必要参数: {param}", validation_results
    
    # 验证创意
    creative_valid, creative_msg = validate_creative_input(params['creative'])
    validation_results['creative'] = {
        'valid': creative_valid,
        'message': creative_msg
    }
    
    if not creative_valid:
        return False, creative_msg, validation_results
    
    # 验证字数
    word_count_valid, word_count_msg = validate_word_count(params['word_count'])
    validation_results['word_count'] = {
        'valid': word_count_valid,
        'message': word_count_msg
    }
    
    if not word_count_valid:
        return False, word_count_msg, validation_results
    
    # 验证小说类型
    novel_type_valid, novel_type_msg = validate_novel_type(params['novel_type'])
    validation_results['novel_type'] = {
        'valid': novel_type_valid,
        'message': novel_type_msg
    }
    
    if not novel_type_valid:
        return False, novel_type_msg, validation_results
    
    # 验证可选参数
    if 'writing_style' in params:
        # 简单的风格验证
        valid_styles = ["轻松幽默", "严肃正剧", "文艺细腻", "快节奏", "慢热细腻", "群像描写"]
        style_valid = params['writing_style'] in valid_styles
        validation_results['writing_style'] = {
            'valid': style_valid,
            'message': f"风格有效" if style_valid else f"风格必须是: {', '.join(valid_styles)}"
        }
    
    return True, "所有参数验证通过", validation_results

# 测试函数
if __name__ == "__main__":
    # 测试API密钥验证
    test_api_key = "sk-test12345678901234567890"
    valid, msg = validate_api_key(test_api_key)
    print(f"API密钥验证: {valid}, 消息: {msg}")
    
    # 测试创意验证
    test_creative = "一个程序员穿越到修真世界"
    valid, msg = validate_creative_input(test_creative)
    print(f"创意验证: {valid}, 消息: {msg}")
    
    # 测试章节内容验证
    test_content = "这是第一章的内容。\n\n主角来到了新的世界。\n\n他开始探索周围的环境。"
    valid, msg, stats = validate_chapter_content(test_content)
    print(f"章节内容验证: {valid}, 消息: {msg}")
    print(f"统计信息: {stats}")
    
    # 测试综合参数验证
    test_params = {
        'creative': test_creative,
        'word_count': 100000,
        'novel_type': '玄幻',
        'writing_style': '轻松幽默'
    }
    
    valid, msg, results = validate_novel_creation_params(test_params)
    print(f"\n综合参数验证: {valid}, 消息: {msg}")
    print(f"验证详情: {results}")