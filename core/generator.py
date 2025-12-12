"""
核心生成器模块
极简实现，专注于一致性
"""

import json
import os
from typing import Dict, List, Any, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
import yaml

class JSONOutputParser(BaseOutputParser):
    """JSON输出解析器"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        try:
            # 清理JSON格式
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            return json.loads(text)
        except json.JSONDecodeError:
            # 如果解析失败，返回包含原始文本的简单结构
            return {"content": text.strip(), "error": "JSON解析失败"}

class NovelGenerator:
    """极简小说生成器 - 专注于一致性"""
    
    def __init__(self, api_key: str):
        """
        初始化生成器
        
        Args:
            api_key: DeepSeek API密钥
        """
        if not api_key:
            raise ValueError("API密钥不能为空")
        
        try:
            self.llm = ChatOpenAI(
                model="deepseek-chat",
                openai_api_key=api_key,
                openai_api_base="https://api.deepseek.com/v1",
                temperature=0.7,
                max_tokens=4000,
                timeout=30
            )
            
            self.output_parser = JSONOutputParser()
            
            # 加载配置
            try:
                with open('config.yaml', 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
            except:
                # 使用默认配置
                self.config = {
                    'deepseek': {
                        'model': 'deepseek-chat',
                        'max_tokens': 4000,
                        'temperature': 0.7
                    }
                }
            
            # 初始化提示词模板
            self._init_templates()
            
            print(f"✅ 生成器初始化成功 (模型: {self.config['deepseek'].get('model', 'deepseek-chat')})")
            
        except Exception as e:
            print(f"❌ 生成器初始化失败: {str(e)}")
            raise ValueError(f"生成器初始化失败: {str(e)}")
    
    def _init_templates(self):
        """初始化提示词模板"""
        
        # 大纲生成模板
        self.outline_template = PromptTemplate(
            input_variables=["creative", "word_count", "novel_type", "writing_style"],
            template="""
            你是一个专业的小说创作助手。请基于以下创意生成一个详细的小说大纲：
            
            ## 创意灵感：
            {creative}
            
            ## 创作要求：
            小说类型：{novel_type}
            目标字数：{word_count}字
            写作风格：{writing_style}
            
            ## 输出要求（严格JSON格式）：
            {{
                "title": "小说标题",
                "theme": "核心主题",
                "summary": "300-500字的故事梗概",
                "target_words": {word_count},
                "estimated_chapters": 基于字数估算的章节数,
                "structure": {{
                    "act1": {{
                        "description": "第一幕：建立",
                        "details": "详细描述..."
                    }},
                    "act2": {{
                        "description": "第二幕：对抗",
                        "details": "详细描述..."
                    }},
                    "act3": {{
                        "description": "第三幕：解决",
                        "details": "详细描述..."
                    }}
                }},
                "key_plot_points": [
                    "关键情节点1",
                    "关键情节点2",
                    "关键情节点3",
                    "关键情节点4",
                    "关键情节点5"
                ]
            }}
            
            请确保输出是纯JSON格式，不要有任何其他文本。
            """
        )
        
        # 人物生成模板
        self.character_template = PromptTemplate(
            input_variables=["outline"],
            template="""
            基于以下小说大纲，生成主要人物设定：
            
            大纲：{outline}
            
            要求生成3-5个主要人物，每个人物包含：
            1. 姓名、年龄、性别、外貌特征
            2. 身份背景
            3. 性格特点（显性和隐性）
            4. 核心动机和目标
            5. 成长弧线
            6. 与其他人物关系
            
            输出格式（JSON数组）：
            [
                {{
                    "name": "姓名",
                    "age": "年龄",
                    "gender": "性别",
                    "appearance": "外貌特征",
                    "identity": "身份背景",
                    "personality": "性格特点",
                    "motivation": "核心动机",
                    "growth_arc": "成长弧线",
                    "relationships": ["关系1", "关系2"]
                }}
            ]
            """
        )
        
        # 章节生成模板
        self.chapter_template = PromptTemplate(
            input_variables=["chapter_number", "outline", "characters", "context", "target_words"],
            template="""
            基于以下信息，生成小说章节：
            
            章节编号：{chapter_number}
            目标字数：{target_words}字
            
            ## 小说大纲：
            {outline}
            
            ## 主要人物：
            {characters}
            
            ## 相关上下文：
            {context}
            
            要求：
            1. 保持人物性格和行为一致性
            2. 推进情节发展
            3. 符合故事整体风格
            4. 埋下后续情节的伏笔
            5. 控制字数在目标范围内
            
            输出格式：
            {{
                "title": "章节标题",
                "content": "章节内容",
                "summary": "本章摘要（100-200字）",
                "word_count": 实际字数,
                "key_events": ["本章关键事件1", "本章关键事件2"],
                "character_development": {{
                    "人物1": "发展描述",
                    "人物2": "发展描述"
                }}
            }}
            """
        )
        
        # 世界观生成模板
        self.worldview_template = PromptTemplate(
            input_variables=["outline", "characters"],
            template="""
            基于以下小说大纲和人物，构建详细的世界观设定：
            
            大纲：{outline}
            人物：{characters}
            
            包括：
            1. 世界基本设定（时代、地域、文明等）
            2. 力量体系（如果有）
            3. 社会结构
            4. 文化风俗
            5. 特殊规则
            6. 历史背景
            
            输出格式：
            {{
                "basic_setting": "基本设定",
                "power_system": "力量体系",
                "social_structure": "社会结构",
                "culture": "文化风俗",
                "special_rules": "特殊规则",
                "history": "历史背景"
            }}
            """
        )
    
    def generate_outline(self, creative: str, word_count: int, novel_type: str, writing_style: str) -> Dict[str, Any]:
        """
        生成小说大纲
        
        Args:
            creative: 创意描述
            word_count: 目标字数
            novel_type: 小说类型
            writing_style: 写作风格
            
        Returns:
            大纲字典
        """
        chain = LLMChain(
            llm=self.llm,
            prompt=self.outline_template,
            output_parser=self.output_parser
        )
        
        result = chain.run(
            creative=creative,
            word_count=word_count,
            novel_type=novel_type,
            writing_style=writing_style
        )
        
        return result
    
    def generate_characters(self, outline: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        生成人物设定
        
        Args:
            outline: 小说大纲
            
        Returns:
            人物列表
        """
        chain = LLMChain(
            llm=self.llm,
            prompt=self.character_template,
            output_parser=self.output_parser
        )
        
        result = chain.run(outline=json.dumps(outline, ensure_ascii=False))
        
        if isinstance(result, list):
            return result
        elif isinstance(result, dict) and 'characters' in result:
            return result['characters']
        else:
            # 默认返回3个示例人物
            return [
                {
                    "name": "主角",
                    "age": "20-30",
                    "gender": "男",
                    "appearance": "普通但有个性",
                    "identity": "主要角色",
                    "personality": "坚韧、聪明、有正义感",
                    "motivation": "成长和实现目标",
                    "growth_arc": "从平凡到卓越",
                    "relationships": []
                }
            ]
    
    def generate_worldview(self, outline: Dict[str, Any], characters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成世界观设定
        
        Args:
            outline: 小说大纲
            characters: 人物列表
            
        Returns:
            世界观字典
        """
        chain = LLMChain(
            llm=self.llm,
            prompt=self.worldview_template,
            output_parser=self.output_parser
        )
        
        result = chain.run(
            outline=json.dumps(outline, ensure_ascii=False),
            characters=json.dumps(characters, ensure_ascii=False)
        )
        
        return result if isinstance(result, dict) else {}
    
    def generate_chapter(self, chapter_number: int, outline: Dict[str, Any], 
                        characters: List[Dict[str, Any]], context: str, 
                        target_words: int = 3000) -> Dict[str, Any]:
        """
        生成单个章节
        
        Args:
            chapter_number: 章节编号
            outline: 小说大纲
            characters: 人物列表
            context: 上下文信息
            target_words: 目标字数
            
        Returns:
            章节内容字典
        """
        chain = LLMChain(
            llm=self.llm,
            prompt=self.chapter_template,
            output_parser=self.output_parser
        )
        
        # 简化和筛选相关人物
        relevant_chars = self._get_relevant_characters(chapter_number, characters)
        
        result = chain.run(
            chapter_number=chapter_number,
            outline=json.dumps(outline, ensure_ascii=False),
            characters=json.dumps(relevant_chars, ensure_ascii=False),
            context=context,
            target_words=target_words
        )
        
        # 确保返回结构一致
        if not isinstance(result, dict):
            result = {
                "title": f"第{chapter_number}章",
                "content": str(result),
                "summary": "",
                "word_count": len(str(result)),
                "key_events": [],
                "character_development": {}
            }
        
        return result
    
    def generate_chapter_plan(self, outline: Dict[str, Any], target_words: int) -> List[Dict[str, Any]]:
        """
        生成章节计划
        
        Args:
            outline: 小说大纲
            target_words: 目标字数
            
        Returns:
            章节计划列表
        """
        # 简单估算章节数（每章3000字）
        estimated_chapters = max(10, target_words // 3000)
        
        chapter_plan = []
        for i in range(1, estimated_chapters + 1):
            if i <= estimated_chapters * 0.3:
                act = "第一幕"
            elif i <= estimated_chapters * 0.7:
                act = "第二幕"
            else:
                act = "第三幕"
            
            chapter_plan.append({
                "chapter": i,
                "act": act,
                "target_words": 3000,
                "status": "待生成"
            })
        
        return chapter_plan
    
    def _get_relevant_characters(self, chapter_number: int, characters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        获取本章相关的角色
        
        Args:
            chapter_number: 章节编号
            characters: 所有角色
            
        Returns:
            相关角色列表
        """
        # 简单的规则：前几章引入主角，后续章节轮流出现
        if chapter_number <= 3:
            # 前3章只返回主角和重要配角
            return [char for char in characters if char.get('name', '').startswith('主角')][:3]
        else:
            # 随机选择2-4个角色
            import random
            return random.sample(characters, min(len(characters), random.randint(2, 4)))
    
    def batch_generate_chapters(self, start_chapter: int, count: int, 
                               outline: Dict[str, Any], characters: List[Dict[str, Any]], 
                               memory_system: Any) -> List[Dict[str, Any]]:
        """
        批量生成章节
        
        Args:
            start_chapter: 起始章节
            count: 生成数量
            outline: 小说大纲
            characters: 人物列表
            memory_system: 记忆系统
            
        Returns:
            生成的章节列表
        """
        chapters = []
        
        for i in range(count):
            chapter_num = start_chapter + i
            
            # 获取上下文
            context = memory_system.get_context(chapter_num)
            
            # 生成章节
            chapter = self.generate_chapter(
                chapter_number=chapter_num,
                outline=outline,
                characters=characters,
                context=context
            )
            
            chapters.append(chapter)
            
            # 更新记忆系统
            memory_system.update_with_chapter(chapter_num, chapter)
        
        return chapters

# 示例使用
if __name__ == "__main__":
    # 从环境变量获取API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key:
        print("请设置 DEEPSEEK_API_KEY 环境变量")
    else:
        generator = NovelGenerator(api_key)
        
        # 测试生成
        test_creative = "一个程序员穿越到修真世界，用代码重构修仙体系"
        
        outline = generator.generate_outline(
            creative=test_creative,
            word_count=100000,
            novel_type="玄幻",
            writing_style="轻松幽默"
        )
        
        print(f"生成大纲: {outline.get('title', '未命名')}")
        print(f"主题: {outline.get('theme', '')}")