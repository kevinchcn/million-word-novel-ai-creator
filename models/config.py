"""
配置模型和常量定义
"""

from typing import Dict, List, Any, Optional
from enum import Enum

class NovelType(str, Enum):
    """小说类型枚举"""
    XUANHUAN = "玄幻"
    XIANXIA = "仙侠"
    DUSHI = "都市"
    KEHUAN = "科幻"
    XUANYI = "悬疑"
    YANQING = "言情"
    LISHI = "历史"
    JUNSHI = "军事"
    WUXIA = "武侠"
    QITA = "其他"

class WritingStyle(str, Enum):
    """写作风格枚举"""
    HUMOROUS = "轻松幽默"
    SERIOUS = "严肃正剧"
    LITERARY = "文艺细腻"
    FAST_PACED = "快节奏"
    SLOW_BURN = "慢热细腻"
    ENSEMBLE = "群像描写"

class ConsistencyLevel(str, Enum):
    """一致性检查强度枚举"""
    RELAXED = "宽松"
    STANDARD = "标准"
    STRICT = "严格"

class ChapterStatus(str, Enum):
    """章节状态枚举"""
    PLANNED = "计划中"
    GENERATING = "生成中"
    GENERATED = "已生成"
    REVIEWING = "审核中"
    APPROVED = "已审核"
    REVISED = "已修改"
    PUBLISHED = "已发布"

class GenerationConfig:
    """生成配置类"""
    
    def __init__(self, 
                 novel_type: NovelType = NovelType.XUANHUAN,
                 writing_style: WritingStyle = WritingStyle.SERIOUS,
                 target_words: int = 100000,
                 consistency_level: ConsistencyLevel = ConsistencyLevel.STANDARD,
                 chapter_length: int = 3000,
                 batch_size: int = 3):
        
        self.novel_type = novel_type
        self.writing_style = writing_style
        self.target_words = target_words
        self.consistency_level = consistency_level
        self.chapter_length = chapter_length
        self.batch_size = batch_size
        self.max_retries = 3
        self.temperature = 0.7
        self.max_tokens = 4000
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "novel_type": self.novel_type.value,
            "writing_style": self.writing_style.value,
            "target_words": self.target_words,
            "consistency_level": self.consistency_level.value,
            "chapter_length": self.chapter_length,
            "batch_size": self.batch_size,
            "max_retries": self.max_retries,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GenerationConfig':
        """从字典创建"""
        config = cls()
        
        # 安全地设置值
        config.novel_type = NovelType(data.get('novel_type', '玄幻'))
        config.writing_style = WritingStyle(data.get('writing_style', '严肃正剧'))
        config.target_words = data.get('target_words', 100000)
        config.consistency_level = ConsistencyLevel(data.get('consistency_level', '标准'))
        config.chapter_length = data.get('chapter_length', 3000)
        config.batch_size = data.get('batch_size', 3)
        config.max_retries = data.get('max_retries', 3)
        config.temperature = data.get('temperature', 0.7)
        config.max_tokens = data.get('max_tokens', 4000)
        
        return config

class MemoryConfig:
    """记忆系统配置类"""
    
    def __init__(self):
        self.memory_dir = "./memory"
        self.max_memory_items = 1000
        self.context_window = 5
        self.retrieval_k = 5
        self.auto_backup = True
        self.backup_count = 5
        self.compression_threshold = 1000  # 超过1000个条目时压缩
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "memory_dir": self.memory_dir,
            "max_memory_items": self.max_memory_items,
            "context_window": self.context_window,
            "retrieval_k": self.retrieval_k,
            "auto_backup": self.auto_backup,
            "backup_count": self.backup_count,
            "compression_threshold": self.compression_threshold
        }

class UISettings:
    """界面设置类"""
    
    def __init__(self):
        self.theme = {
            "primary_color": "#667eea",
            "secondary_color": "#764ba2",
            "background_color": "#f8f9fa",
            "text_color": "#333333",
            "accent_color": "#10b981"
        }
        self.default_layout = "wide"
        self.show_progress_bar = True
        self.show_quality_metrics = True
        self.auto_refresh = False
        self.refresh_interval = 30  # 秒
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "theme": self.theme,
            "default_layout": self.default_layout,
            "show_progress_bar": self.show_progress_bar,
            "show_quality_metrics": self.show_quality_metrics,
            "auto_refresh": self.auto_refresh,
            "refresh_interval": self.refresh_interval
        }

class AppConfig:
    """应用配置类"""
    
    def __init__(self):
        # API配置
        self.api_config = {
            "provider": "deepseek",
            "model": "deepseek-chat",
            "api_base": "https://api.deepseek.com/v1",
            "timeout": 30,
            "max_retries": 3
        }
        
        # 生成配置
        self.generation_config = GenerationConfig()
        
        # 记忆配置
        self.memory_config = MemoryConfig()
        
        # 界面配置
        self.ui_settings = UISettings()
        
        # 文件路径
        self.paths = {
            "outputs": "./outputs",
            "templates": "./templates",
            "logs": "./outputs/logs",
            "backups": "./backups"
        }
        
        # 验证配置
        self.validation = {
            "enable_content_check": True,
            "enable_consistency_check": True,
            "consistency_threshold": 75,
            "max_content_length": 10000,
            "min_content_length": 1000
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "api_config": self.api_config,
            "generation_config": self.generation_config.to_dict(),
            "memory_config": self.memory_config.to_dict(),
            "ui_settings": self.ui_settings.to_dict(),
            "paths": self.paths,
            "validation": self.validation
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        """从字典创建"""
        config = cls()
        
        # 更新API配置
        if 'api_config' in data:
            config.api_config.update(data['api_config'])
        
        # 更新生成配置
        if 'generation_config' in data:
            config.generation_config = GenerationConfig.from_dict(data['generation_config'])
        
        # 更新记忆配置
        if 'memory_config' in data:
            mem_config = data['memory_config']
            config.memory_config.memory_dir = mem_config.get('memory_dir', config.memory_config.memory_dir)
            config.memory_config.max_memory_items = mem_config.get('max_memory_items', config.memory_config.max_memory_items)
            config.memory_config.context_window = mem_config.get('context_window', config.memory_config.context_window)
            config.memory_config.retrieval_k = mem_config.get('retrieval_k', config.memory_config.retrieval_k)
            config.memory_config.auto_backup = mem_config.get('auto_backup', config.memory_config.auto_backup)
            config.memory_config.backup_count = mem_config.get('backup_count', config.memory_config.backup_count)
        
        # 更新界面配置
        if 'ui_settings' in data:
            ui_config = data['ui_settings']
            if 'theme' in ui_config:
                config.ui_settings.theme.update(ui_config['theme'])
            config.ui_settings.default_layout = ui_config.get('default_layout', config.ui_settings.default_layout)
            config.ui_settings.show_progress_bar = ui_config.get('show_progress_bar', config.ui_settings.show_progress_bar)
            config.ui_settings.show_quality_metrics = ui_config.get('show_quality_metrics', config.ui_settings.show_quality_metrics)
            config.ui_settings.auto_refresh = ui_config.get('auto_refresh', config.ui_settings.auto_refresh)
            config.ui_settings.refresh_interval = ui_config.get('refresh_interval', config.ui_settings.refresh_interval)
        
        # 更新文件路径
        if 'paths' in data:
            config.paths.update(data['paths'])
        
        # 更新验证配置
        if 'validation' in data:
            config.validation.update(data['validation'])
        
        return config

# 默认配置
DEFAULT_CONFIG = AppConfig()

# 配置验证函数
def validate_config(config: Dict[str, Any]) -> tuple[bool, str]:
    """验证配置是否有效"""
    
    try:
        # 检查必要字段
        required_fields = ['api_config', 'generation_config', 'memory_config']
        for field in required_fields:
            if field not in config:
                return False, f"缺少必要字段: {field}"
        
        # 检查API配置
        api_config = config['api_config']
        if 'model' not in api_config:
            return False, "API配置缺少model字段"
        
        # 检查生成配置
        gen_config = config['generation_config']
        if 'target_words' not in gen_config:
            return False, "生成配置缺少target_words字段"
        
        target_words = gen_config['target_words']
        if not isinstance(target_words, int) or target_words < 10000:
            return False, "目标字数必须为整数且不小于10000"
        
        # 检查文件路径
        if 'paths' in config:
            paths = config['paths']
            for path_key, path_value in paths.items():
                if not isinstance(path_value, str):
                    return False, f"路径配置 {path_key} 必须是字符串"
        
        return True, "配置验证通过"
    
    except Exception as e:
        return False, f"配置验证异常: {str(e)}"

# 配置工具函数
def load_config_file(config_path: str = "config.yaml") -> AppConfig:
    """从YAML文件加载配置"""
    import yaml
    import os
    
    if not os.path.exists(config_path):
        print(f"⚠️ 配置文件 {config_path} 不存在，使用默认配置")
        return DEFAULT_CONFIG
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        # 验证配置
        valid, message = validate_config(config_data)
        if not valid:
            print(f"⚠️ 配置验证失败: {message}，使用默认配置")
            return DEFAULT_CONFIG
        
        return AppConfig.from_dict(config_data)
        
    except Exception as e:
        print(f"❌ 加载配置文件失败: {str(e)}，使用默认配置")
        return DEFAULT_CONFIG

def save_config_file(config: AppConfig, config_path: str = "config.yaml"):
    """保存配置到YAML文件"""
    import yaml
    import os
    
    try:
        config_data = config.to_dict()
        
        # 确保目录存在
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, allow_unicode=True, default_flow_style=False)
        
        print(f"✅ 配置已保存到: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ 保存配置文件失败: {str(e)}")
        return False

# 测试函数
if __name__ == "__main__":
    print("测试配置系统...")
    
    # 创建默认配置
    config = DEFAULT_CONFIG
    
    # 转换为字典
    config_dict = config.to_dict()
    print(f"配置字典键: {list(config_dict.keys())}")
    
    # 验证配置
    valid, message = validate_config(config_dict)
    print(f"配置验证: {valid}, 消息: {message}")
    
    # 测试从字典创建
    new_config = AppConfig.from_dict(config_dict)
    print(f"新配置创建成功: {new_config.generation_config.novel_type.value}")
    
    # 测试保存和加载
    test_config_path = "./test_config.yaml"
    if save_config_file(config, test_config_path):
        loaded_config = load_config_file(test_config_path)
        print(f"配置加载成功: {loaded_config.api_config['model']}")
    
    # 清理
    import os
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
        print("✅ 清理测试文件")