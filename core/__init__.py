"""
核心模块 - 百万字小说AI创作器
"""

from .generator import NovelGenerator
from .memory_system import SmartMemory
from .consistency import ConsistencyChecker
from .summarizer import SmartSummarizer

__all__ = [
    'NovelGenerator',
    'SmartMemory',
    'ConsistencyChecker',
    'SmartSummarizer'
]