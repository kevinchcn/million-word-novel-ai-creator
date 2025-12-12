"""
小说数据模型
使用Pydantic进行数据验证
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator

class NovelOutline(BaseModel):
    """小说大纲模型"""
    title: str = Field(..., description="小说标题")
    theme: str = Field(..., description="核心主题")
    summary: str = Field(..., description="故事梗概")
    target_words: int = Field(default=100000, description="目标字数")
    estimated_chapters: int = Field(default=0, description="预计章节数")
    
    # 三幕结构
    structure: Dict[str, Dict[str, str]] = Field(
        default_factory=dict,
        description="三幕结构"
    )
    
    # 关键情节点
    key_plot_points: List[str] = Field(
        default_factory=list,
        description="关键情节点"
    )
    
    # 主要人物（简要）
    main_characters: List[str] = Field(
        default_factory=list,
        description="主要人物列表"
    )
    
    # 元数据
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @validator('target_words')
    def validate_target_words(cls, v):
        if v < 10000:
            raise ValueError('目标字数至少为10000字')
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Character(BaseModel):
    """人物模型"""
    name: str = Field(..., description="人物姓名")
    age: str = Field("", description="年龄")
    gender: str = Field("", description="性别")
    appearance: str = Field("", description="外貌特征")
    identity: str = Field("", description="身份背景")
    personality: str = Field("", description="性格特点")
    motivation: str = Field("", description="核心动机")
    background: str = Field("", description="背景故事")
    growth_arc: str = Field("", description="成长弧线")
    
    # 能力设定
    abilities: List[str] = Field(default_factory=list, description="能力列表")
    weaknesses: List[str] = Field(default_factory=list, description="弱点列表")
    
    # 人物关系
    relationships: Dict[str, str] = Field(
        default_factory=dict,
        description="人物关系 {人物名: 关系描述}"
    )
    
    # 发展历史
    development_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="发展历史记录"
    )
    
    # 元数据
    importance: int = Field(default=5, ge=1, le=10, description="重要性评分")
    created_at: datetime = Field(default_factory=datetime.now)
    last_appearance: Optional[int] = Field(None, description="最后出现的章节")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class WorldView(BaseModel):
    """世界观模型"""
    # 基本设定
    basic_setting: str = Field("", description="基本设定")
    time_period: str = Field("", description="时代背景")
    geographical_setting: str = Field("", description="地理设定")
    
    # 力量体系
    power_system: str = Field("", description="力量体系")
    cultivation_stages: List[str] = Field(default_factory=list, description="修炼等级")
    special_abilities: List[str] = Field(default_factory=list, description="特殊能力")
    
    # 社会结构
    social_structure: str = Field("", description="社会结构")
    factions: List[str] = Field(default_factory=list, description="势力组织")
    social_rules: List[str] = Field(default_factory=list, description="社会规则")
    
    # 文化风俗
    culture: str = Field("", description="文化风俗")
    customs: List[str] = Field(default_factory=list, description="风俗习惯")
    taboos: List[str] = Field(default_factory=list, description="禁忌")
    
    # 特殊规则
    special_rules: List[str] = Field(default_factory=list, description="特殊规则")
    limitations: List[str] = Field(default_factory=list, description="限制条件")
    
    # 历史背景
    history: str = Field("", description="历史背景")
    major_events: List[str] = Field(default_factory=list, description="重大历史事件")
    
    # 元数据
    consistency_score: int = Field(default=100, ge=0, le=100, description="一致性评分")
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Chapter(BaseModel):
    """章节模型"""
    chapter_number: int = Field(..., ge=1, description="章节编号")
    title: str = Field("", description="章节标题")
    content: str = Field("", description="章节内容")
    summary: str = Field("", description="章节摘要")
    
    # 统计信息
    word_count: int = Field(0, description="字数")
    paragraph_count: int = Field(0, description="段落数")
    
    # 内容分析
    key_events: List[str] = Field(default_factory=list, description="关键事件")
    character_development: Dict[str, str] = Field(
        default_factory=dict,
        description="人物发展"
    )
    new_elements: List[str] = Field(default_factory=list, description="新出现的元素")
    
    # 质量评估
    quality_score: int = Field(default=0, ge=0, le=100, description="质量评分")
    consistency_score: int = Field(default=0, ge=0, le=100, description="一致性评分")
    
    # 元数据
    generated_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    version: int = Field(default=1, description="版本号")
    
    @validator('word_count')
    def validate_word_count(cls, v, values):
        if 'content' in values:
            actual_count = len(values['content'])
            if v != actual_count:
                return actual_count
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ChapterPlan(BaseModel):
    """章节计划模型"""
    chapter: int = Field(..., ge=1, description="章节编号")
    act: str = Field("", description="所属幕")
    target_words: int = Field(3000, ge=1000, le=10000, description="目标字数")
    status: str = Field("待生成", description="状态")
    outline: str = Field("", description="章节概要")
    
    # 计划详情
    key_scenes: List[str] = Field(default_factory=list, description="关键场景")
    involved_characters: List[str] = Field(default_factory=list, description="涉及人物")
    plot_advancement: str = Field("", description="情节推进")
    
    # 时间安排
    planned_date: Optional[datetime] = Field(None, description="计划完成日期")
    actual_date: Optional[datetime] = Field(None, description="实际完成日期")
    
    # 质量目标
    quality_target: int = Field(default=80, ge=0, le=100, description="质量目标")
    consistency_target: int = Field(default=85, ge=0, le=100, description="一致性目标")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ConsistencyCheckResult(BaseModel):
    """一致性检查结果模型"""
    check_id: str = Field(..., description="检查ID")
    check_type: str = Field(..., description="检查类型")
    check_time: datetime = Field(default_factory=datetime.now)
    
    # 检查结果
    passed: bool = Field(False, description="是否通过")
    score: int = Field(0, ge=0, le=100, description="评分")
    
    # 问题详情
    issues: List[str] = Field(default_factory=list, description="问题列表")
    critical_issues: List[str] = Field(default_factory=list, description="严重问题")
    
    # 建议
    suggestions: List[str] = Field(default_factory=list, description="建议列表")
    fixes: List[Dict[str, Any]] = Field(default_factory=list, description="修复方案")
    
    # 上下文信息
    context: Dict[str, Any] = Field(default_factory=dict, description="检查上下文")
    affected_elements: List[str] = Field(default_factory=list, description="受影响的元素")
    
    # 元数据
    duration_seconds: float = Field(0.0, description="检查耗时")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="置信度")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class NovelProject(BaseModel):
    """小说项目模型"""
    project_id: str = Field(..., description="项目ID")
    project_name: str = Field(..., description="项目名称")
    
    # 项目内容
    outline: Optional[NovelOutline] = Field(None, description="小说大纲")
    characters: List[Character] = Field(default_factory=list, description="人物列表")
    worldview: Optional[WorldView] = Field(None, description="世界观")
    chapters: Dict[int, Chapter] = Field(default_factory=dict, description="章节字典")
    
    # 项目状态
    status: str = Field("draft", description="项目状态")
    current_chapter: int = Field(1, ge=1, description="当前章节")
    total_words: int = Field(0, description="总字数")
    completion_percentage: float = Field(0.0, ge=0.0, le=100.0, description="完成百分比")
    
    # 质量指标
    overall_quality: int = Field(0, ge=0, le=100, description="整体质量")
    consistency_score: int = Field(0, ge=0, le=100, description="一致性评分")
    
    # 元数据
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    author: str = Field("", description="作者")
    tags: List[str] = Field(default_factory=list, description="标签")
    
    # 配置
    config: Dict[str, Any] = Field(default_factory=dict, description="项目配置")
    
    @validator('completion_percentage')
    def validate_completion(cls, v, values):
        if 'outline' in values and values['outline']:
            target_words = values['outline'].target_words
            total_words = values.get('total_words', 0)
            
            if target_words > 0:
                calculated = (total_words / target_words) * 100
                return min(100.0, calculated)
        
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# 示例数据创建函数
def create_example_novel() -> NovelProject:
    """创建示例小说项目"""
    
    outline = NovelOutline(
        title="代码修仙",
        theme="科技与修真的融合",
        summary="一个现代程序员穿越到修真世界，用编程思维重构修仙体系的故事。",
        target_words=100000,
        estimated_chapters=33,
        structure={
            "act1": {"description": "穿越与适应", "details": "主角穿越到修真世界，开始适应新环境。"},
            "act2": {"description": "成长与挑战", "details": "主角用编程知识解决修真问题，面临各种挑战。"},
            "act3": {"description": "革命与结局", "details": "主角的革命性想法改变修真界，最终达成目标。"}
        },
        key_plot_points=[
            "穿越事件",
            "发现修真与代码的关联",
            "创建第一个程序法术",
            "宗门大比展示实力",
            "最终决战"
        ],
        main_characters=["李凡", "青云掌门", "小师妹"]
    )
    
    character = Character(
        name="李凡",
        age="25",
        gender="男",
        appearance="普通程序员模样，戴着眼镜",
        identity="穿越者，前程序员",
        personality="聪明、理性、有创造力",
        motivation="用科技改变修真界",
        background="来自21世纪的程序员，意外穿越到修真世界",
        growth_arc="从普通程序员成长为修真革命者",
        abilities=["编程", "逻辑思维", "创新"],
        weaknesses=["身体素质一般", "不熟悉修真界规则"],
        importance=10
    )
    
    worldview = WorldView(
        basic_setting="一个存在修真文明的世界，但修真体系存在诸多问题",
        time_period="修真历三千五百年",
        geographical_setting="分为九州大陆，各有不同宗门势力",
        power_system="传统修真体系：炼气、筑基、金丹、元婴、化神等",
        social_structure="以宗门为单位的等级社会",
        culture="重视传统，尊重强者",
        special_rules=["灵气是修真的基础", "功法决定修炼上限"],
        history="修真文明已存在数千年，但近百年进步缓慢"
    )
    
    project = NovelProject(
        project_id="novel_001",
        project_name="代码修仙",
        outline=outline,
        characters=[character],
        worldview=worldview,
        status="active",
        author="AI创作器",
        tags=["修真", "穿越", "科技", "创新"]
    )
    
    return project

if __name__ == "__main__":
    # 测试模型
    example = create_example_novel()
    
    print("示例小说项目:")
    print(f"项目名称: {example.project_name}")
    print(f"小说标题: {example.outline.title if example.outline else '无'}")
    print(f"主要人物: {len(example.characters)} 个")
    print(f"当前状态: {example.status}")
    
    # 转换为JSON
    import json
    project_json = example.json(ensure_ascii=False, indent=2)
    print("\nJSON格式:")
    print(project_json[:500])