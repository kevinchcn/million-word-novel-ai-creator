"""
智能摘要系统
生成章节摘要，保留关键信息
"""

import json
from typing import Dict, List, Any
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class SmartSummarizer:
    """智能摘要系统"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self._init_templates()
    
    def _init_templates(self):
        """初始化摘要模板"""
        
        # 章节摘要模板
        self.chapter_summary_template = PromptTemplate(
            input_variables=["content", "chapter_number"],
            template="""
            请为以下小说章节生成智能摘要：
            
            章节编号：{chapter_number}
            章节内容：
            {content}
            
            要求：
            1. 提取重要情节进展（50-100字）
            2. 记录人物关系变化
            3. 标记新出现的设定或伏笔
            4. 总结关键对话和决策
            5. 控制在200字以内
            
            输出格式：
            {{
                "summary": "摘要内容",
                "key_events": ["事件1", "事件2", "事件3"],
                "character_development": {{
                    "人物1": "发展描述",
                    "人物2": "发展描述"
                }},
                "new_elements": ["新设定1", "新伏笔1"],
                "word_count": 摘要字数
            }}
            """
        )
        
        # 卷摘要模板
        self.volume_summary_template = PromptTemplate(
            input_variables=["chapter_summaries", "volume_number"],
            template="""
            基于以下章节摘要，生成本卷的总体摘要：
            
            卷号：{volume_number}
            章节摘要：
            {chapter_summaries}
            
            要求：
            1. 总结本卷的主要情节发展
            2. 梳理人物成长和关系变化
            3. 归纳本卷的核心冲突
            4. 分析情节推进的关键节点
            5. 控制在300字以内
            
            输出格式：
            {{
                "summary": "卷摘要",
                "main_plot": "主要情节",
                "character_arcs": "人物弧光",
                "key_turning_points": ["转折点1", "转折点2"],
                "setup_for_next": "为下一卷的铺垫"
            }}
            """
        )
    
    def create_chapter_summary(self, content: str, chapter_number: int) -> Dict[str, Any]:
        """
        生成章节摘要
        
        Args:
            content: 章节内容
            chapter_number: 章节编号
            
        Returns:
            摘要字典
        """
        if self.llm:
            # 使用LLM生成智能摘要
            chain = LLMChain(
                llm=self.llm,
                prompt=self.chapter_summary_template
            )
            
            result = chain.run(
                content=content[:5000],  # 限制长度
                chapter_number=chapter_number
            )
            
            try:
                return json.loads(result)
            except:
                return {
                    "summary": result[:200] + "..." if len(result) > 200 else result,
                    "key_events": [],
                    "character_development": {},
                    "new_elements": [],
                    "word_count": len(result)
                }
        else:
            # 简单实现：提取前200字作为摘要
            return {
                "summary": content[:200] + "..." if len(content) > 200 else content,
                "key_events": [],
                "character_development": {},
                "new_elements": [],
                "word_count": min(200, len(content))
            }
    
    def create_volume_summary(self, chapter_summaries: List[Dict[str, Any]], 
                             volume_number: int) -> Dict[str, Any]:
        """
        生成卷摘要
        
        Args:
            chapter_summaries: 章节摘要列表
            volume_number: 卷号
            
        Returns:
            卷摘要字典
        """
        if self.llm and chapter_summaries:
            # 准备章节摘要文本
            summaries_text = ""
            for i, summary in enumerate(chapter_summaries, 1):
                summaries_text += f"第{i}章: {summary.get('summary', '')}\n"
            
            chain = LLMChain(
                llm=self.llm,
                prompt=self.volume_summary_template
            )
            
            result = chain.run(
                chapter_summaries=summaries_text,
                volume_number=volume_number
            )
            
            try:
                return json.loads(result)
            except:
                return {
                    "summary": result,
                    "main_plot": "",
                    "character_arcs": "",
                    "key_turning_points": [],
                    "setup_for_next": ""
                }
        else:
            # 简单实现：合并章节摘要
            combined_summary = ""
            for summary in chapter_summaries:
                combined_summary += summary.get('summary', '') + " "
            
            return {
                "summary": combined_summary[:300] + "..." if len(combined_summary) > 300 else combined_summary,
                "main_plot": "",
                "character_arcs": "",
                "key_turning_points": [],
                "setup_for_next": ""
            }
    
    def extract_key_information(self, content: str) -> Dict[str, Any]:
        """
        从内容中提取关键信息
        
        Args:
            content: 文本内容
            
        Returns:
            关键信息字典
        """
        # 简单实现：提取重要元素
        import re
        
        info = {
            "mentioned_characters": [],
            "important_events": [],
            "new_settings": [],
            "potential_foreshadowing": []
        }
        
        # 提取可能的人物名称（中文名称，2-4字）
        chinese_names = re.findall(r'[\u4e00-\u9fa5]{2,4}[\u4e00-\u9fa5]', content)
        info["mentioned_characters"] = list(set(chinese_names))[:10]  # 去重，最多10个
        
        # 提取重要事件（包含动词的短句）
        sentences = re.split(r'[。！？]', content)
        important_sentences = []
        
        important_indicators = ['发现', '遇到', '战斗', '死亡', '获得', '失去', '决定', '承诺']
        for sentence in sentences:
            if any(indicator in sentence for indicator in important_indicators):
                important_sentences.append(sentence.strip())
        
        info["important_events"] = important_sentences[:5]
        
        # 提取可能的新设定
        setting_indicators = ['世界', '法则', '力量', '系统', '组织', '门派']
        for sentence in sentences:
            if any(indicator in sentence for indicator in setting_indicators):
                info["new_settings"].append(sentence.strip())
        
        info["new_settings"] = info["new_settings"][:3]
        
        # 提取可能的伏笔
        foreshadowing_indicators = ['未来', '将会', '可能', '似乎', '暗示', '预兆']
        for sentence in sentences:
            if any(indicator in sentence for indicator in foreshadowing_indicators):
                info["potential_foreshadowing"].append(sentence.strip())
        
        info["potential_foreshadowing"] = info["potential_foreshadowing"][:3]
        
        return info
    
    def create_reading_notes(self, chapter_summaries: List[Dict[str, Any]]) -> str:
        """
        生成阅读笔记
        
        Args:
            chapter_summaries: 章节摘要列表
            
        Returns:
            阅读笔记
        """
        if not chapter_summaries:
            return "暂无阅读笔记"
        
        notes = "📚 阅读笔记\n\n"
        
        # 按章节组织笔记
        for i, summary in enumerate(chapter_summaries, 1):
            notes += f"## 第{i}章\n"
            notes += f"{summary.get('summary', '')}\n\n"
            
            key_events = summary.get('key_events', [])
            if key_events:
                notes += "关键事件:\n"
                for event in key_events:
                    notes += f"- {event}\n"
                notes += "\n"
            
            character_dev = summary.get('character_development', {})
            if character_dev:
                notes += "人物发展:\n"
                for char, dev in character_dev.items():
                    notes += f"- {char}: {dev}\n"
                notes += "\n"
        
        return notes
    
    def calculate_complexity_score(self, content: str) -> float:
        """
        计算内容复杂度
        
        Args:
            content: 文本内容
            
        Returns:
            复杂度分数 (0-1)
        """
        if not content:
            return 0.0
        
        # 简单复杂度计算
        import re
        
        # 句子数量
        sentences = re.split(r'[。！？]', content)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # 段落数量
        paragraphs = content.split('\n')
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        # 词汇多样性
        words = re.findall(r'[\u4e00-\u9fa5]+', content)
        unique_words = set(words)
        
        if words:
            diversity = len(unique_words) / len(words)
        else:
            diversity = 0
        
        # 计算综合分数
        complexity = min(1.0, (
            (sentence_count / 100) * 0.3 +
            (paragraph_count / 10) * 0.2 +
            diversity * 0.5
        ))
        
        return complexity

# 测试函数
if __name__ == "__main__":
    summarizer = SmartSummarizer()
    
    # 测试数据
    test_content = """
    第一章：穿越
    
    李凡睁开眼睛，发现自己躺在一个陌生的房间里。
    房间的装饰古色古香，窗外的景色更是让他震惊——仙鹤在空中飞翔，远处有修士御剑飞行。
    
    "我这是穿越了？"李凡喃喃自语。
    
    这时，门外传来脚步声。一个穿着道袍的老者推门而入。
    "你醒了？"老者问道，"我是青云宗的掌门，你在后山昏迷了三天。"
    
    李凡意识到，他不仅穿越了，还穿越到了一个修真世界。
    """
    
    # 测试章节摘要
    chapter_summary = summarizer.create_chapter_summary(test_content, 1)
    print("章节摘要:")
    print(json.dumps(chapter_summary, indent=2, ensure_ascii=False))
    
    # 测试关键信息提取
    key_info = summarizer.extract_key_information(test_content)
    print("\n关键信息:")
    print(json.dumps(key_info, indent=2, ensure_ascii=False))
    
    # 测试复杂度计算
    complexity = summarizer.calculate_complexity_score(test_content)
    print(f"\n内容复杂度: {complexity:.2f}")
    
    # 测试阅读笔记
    reading_notes = summarizer.create_reading_notes([chapter_summary])
    print("\n阅读笔记:")
    print(reading_notes[:500])