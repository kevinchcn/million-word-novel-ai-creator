"""
一体化调整模块
统一调整叙事风格、情节节奏、人物关系等
"""

import json
from typing import Dict, List, Any, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class UnifiedAdjuster:
    """一体化调整器"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self._init_templates()
    
    def _init_templates(self):
        """初始化调整模板"""
        
        # 叙事风格调整模板
        self.style_adjustment_template = PromptTemplate(
            input_variables=["current_content", "adjustment_instruction", "novel_type"],
            template="""
            请根据以下调整指令，修改文本的叙事风格：
            
            原文：
            {current_content}
            
            调整指令：
            {adjustment_instruction}
            
            小说类型：
            {novel_type}
            
            要求：
            1. 保持情节和人物不变
            2. 只调整叙事风格和语言表达
            3. 确保调整后的文本连贯自然
            4. 根据小说类型保持适当的风格
            
            输出调整后的文本。
            """
        )
        
        # 情节节奏调整模板
        self.pace_adjustment_template = PromptTemplate(
            input_variables=["current_content", "adjustment_instruction"],
            template="""
            请根据以下调整指令，修改文本的情节节奏：
            
            原文：
            {current_content}
            
            调整指令：
            {adjustment_instruction}
            
            要求：
            1. 保持核心情节和人物关系
            2. 调整叙事节奏（加快或放缓）
            3. 适当增加或减少细节描写
            4. 保持文本的连贯性
            
            输出调整后的文本。
            """
        )
        
        # 人物关系调整模板
        self.relationship_adjustment_template = PromptTemplate(
            input_variables=["current_content", "adjustment_instruction", "character_profiles"],
            template="""
            请根据以下调整指令，修改文本中的人物关系：
            
            原文：
            {current_content}
            
            调整指令：
            {adjustment_instruction}
            
            人物档案：
            {character_profiles}
            
            要求：
            1. 保持人物基本性格不变
            2. 调整人物之间的互动和关系
            3. 确保关系变化合理自然
            4. 保持情节逻辑性
            
            输出调整后的文本。
            """
        )
        
        # 世界观调整模板
        self.worldview_adjustment_template = PromptTemplate(
            input_variables=["current_content", "adjustment_instruction", "worldview"],
            template="""
            请根据以下调整指令，修改文本中的世界观表现：
            
            原文：
            {current_content}
            
            调整指令：
            {adjustment_instruction}
            
            世界观设定：
            {worldview}
            
            要求：
            1. 保持世界观核心规则不变
            2. 调整世界观的表现方式和细节
            3. 确保调整后的世界观更加鲜明
            4. 保持文本的连贯性
            
            输出调整后的文本。
            """
        )
        
        # 整体优化模板
        self.overall_optimization_template = PromptTemplate(
            input_variables=["current_content", "adjustment_instruction", "novel_context"],
            template="""
            请根据以下调整指令，对文本进行整体优化：
            
            原文：
            {current_content}
            
            调整指令：
            {adjustment_instruction}
            
            小说上下文：
            {novel_context}
            
            要求：
            1. 综合优化叙事、节奏、人物、世界观
            2. 保持原作的精髓和特色
            3. 提升文本的整体质量
            4. 确保优化后的文本更加吸引人
            
            输出优化后的文本。
            """
        )
    
    def unified_adjustment(self, adjustment_type: str, 
                          adjustment_instruction: str,
                          content: str,
                          context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行一体化调整
        
        Args:
            adjustment_type: 调整类型
            adjustment_instruction: 调整指令
            content: 要调整的内容
            context: 上下文信息
            
        Returns:
            调整结果
        """
        if not self.llm:
            return {
                "success": False,
                "error": "语言模型未初始化",
                "adjusted_content": content
            }
        
        try:
            # 根据调整类型选择模板
            if adjustment_type == "叙事风格":
                template = self.style_adjustment_template
                input_vars = {
                    "current_content": content,
                    "adjustment_instruction": adjustment_instruction,
                    "novel_type": context.get('novel_type', '') if context else ''
                }
                
            elif adjustment_type == "情节节奏":
                template = self.pace_adjustment_template
                input_vars = {
                    "current_content": content,
                    "adjustment_instruction": adjustment_instruction
                }
                
            elif adjustment_type == "人物关系":
                template = self.relationship_adjustment_template
                input_vars = {
                    "current_content": content,
                    "adjustment_instruction": adjustment_instruction,
                    "character_profiles": json.dumps(
                        context.get('characters', []), 
                        ensure_ascii=False
                    ) if context else "[]"
                }
                
            elif adjustment_type == "世界观设定":
                template = self.worldview_adjustment_template
                input_vars = {
                    "current_content": content,
                    "adjustment_instruction": adjustment_instruction,
                    "worldview": json.dumps(
                        context.get('worldview', {}), 
                        ensure_ascii=False
                    ) if context else "{}"
                }
                
            elif adjustment_type == "整体优化":
                template = self.overall_optimization_template
                input_vars = {
                    "current_content": content,
                    "adjustment_instruction": adjustment_instruction,
                    "novel_context": json.dumps(
                        context, 
                        ensure_ascii=False
                    ) if context else "{}"
                }
                
            else:
                return {
                    "success": False,
                    "error": f"不支持的调整类型: {adjustment_type}",
                    "adjusted_content": content
                }
            
            # 执行调整
            chain = LLMChain(llm=self.llm, prompt=template)
            adjusted_content = chain.run(**input_vars)
            
            # 分析调整效果
            effect_analysis = self._analyze_adjustment_effect(
                original=content,
                adjusted=adjusted_content,
                adjustment_type=adjustment_type
            )
            
            return {
                "success": True,
                "adjustment_type": adjustment_type,
                "original_length": len(content),
                "adjusted_length": len(adjusted_content),
                "adjusted_content": adjusted_content,
                "effect_analysis": effect_analysis,
                "change_percentage": self._calculate_change_percentage(content, adjusted_content)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "adjusted_content": content
            }
    
    def _analyze_adjustment_effect(self, original: str, adjusted: str, 
                                 adjustment_type: str) -> Dict[str, Any]:
        """
        分析调整效果
        
        Args:
            original: 原文
            adjusted: 调整后文本
            adjustment_type: 调整类型
            
        Returns:
            效果分析
        """
        # 简单分析：计算变化指标
        analysis = {
            "word_count_change": len(adjusted) - len(original),
            "sentence_count_change": self._count_sentences(adjusted) - self._count_sentences(original),
            "adjustment_type": adjustment_type,
            "estimated_impact": "轻微"
        }
        
        # 计算相似度
        similarity = self._calculate_similarity(original, adjusted)
        analysis["similarity_score"] = similarity
        
        # 评估影响程度
        if similarity < 0.7:
            analysis["estimated_impact"] = "重大"
        elif similarity < 0.9:
            analysis["estimated_impact"] = "中等"
        
        return analysis
    
    def _count_sentences(self, text: str) -> int:
        """统计句子数量"""
        import re
        sentences = re.split(r'[。！？.!?]', text)
        return len([s for s in sentences if s.strip()])
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _calculate_change_percentage(self, original: str, adjusted: str) -> float:
        """计算变化百分比"""
        if not original:
            return 100.0
        
        diff_count = sum(1 for a, b in zip(original, adjusted) if a != b)
        max_len = max(len(original), len(adjusted))
        
        if max_len == 0:
            return 0.0
        
        return (diff_count / max_len) * 100
    
    def batch_adjust_chapters(self, chapters: List[Dict[str, Any]], 
                            adjustment_type: str, 
                            adjustment_instruction: str,
                            context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        批量调整章节
        
        Args:
            chapters: 章节列表
            adjustment_type: 调整类型
            adjustment_instruction: 调整指令
            context: 上下文信息
            
        Returns:
            调整后的章节列表
        """
        adjusted_chapters = []
        
        for i, chapter in enumerate(chapters):
            print(f"正在调整第{i+1}/{len(chapters)}章...")
            
            content = chapter.get('content', '')
            if not content:
                adjusted_chapters.append(chapter)
                continue
            
            # 执行调整
            result = self.unified_adjustment(
                adjustment_type=adjustment_type,
                adjustment_instruction=adjustment_instruction,
                content=content,
                context=context
            )
            
            if result['success']:
                # 更新章节内容
                chapter['adjusted_content'] = result['adjusted_content']
                chapter['adjustment_analysis'] = result['effect_analysis']
                chapter['original_length'] = len(content)
                chapter['adjusted_length'] = len(result['adjusted_content'])
            else:
                chapter['adjustment_error'] = result['error']
            
            adjusted_chapters.append(chapter)
        
        return adjusted_chapters
    
    def generate_adjustment_suggestions(self, content: str, 
                                      context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        生成调整建议
        
        Args:
            content: 待调整的内容
            context: 上下文信息
            
        Returns:
            调整建议列表
        """
        suggestions = []
        
        # 分析内容特征
        content_features = self._analyze_content_features(content)
        
        # 生成风格调整建议
        if content_features.get('sentence_length_avg', 0) > 30:
            suggestions.append({
                "type": "叙事风格",
                "suggestion": "句子偏长，建议简化句式，使阅读更流畅",
                "priority": "中",
                "estimated_effect": "提升可读性"
            })
        
        if content_features.get('dialogue_ratio', 0) < 0.2:
            suggestions.append({
                "type": "情节节奏",
                "suggestion": "对话比例较低，建议增加人物对话，增强互动性",
                "priority": "高",
                "estimated_effect": "增强人物表现力"
            })
        
        if content_features.get('descriptive_ratio', 0) > 0.5:
            suggestions.append({
                "type": "情节节奏",
                "suggestion": "描述性内容过多，建议增加情节推进速度",
                "priority": "中",
                "estimated_effect": "加快节奏"
            })
        
        # 根据上下文生成建议
        if context:
            if context.get('novel_type') == '玄幻':
                suggestions.append({
                    "type": "世界观设定",
                    "suggestion": "建议增加修真体系的细节描写，增强世界真实感",
                    "priority": "中",
                    "estimated_effect": "深化世界观"
                })
            
            if context.get('writing_style') == '快节奏':
                suggestions.append({
                    "type": "情节节奏",
                    "suggestion": "当前节奏符合快节奏风格，建议保持",
                    "priority": "低",
                    "estimated_effect": "维持风格"
                })
        
        return suggestions
    
    def _analyze_content_features(self, content: str) -> Dict[str, float]:
        """分析内容特征"""
        import re
        
        features = {
            "word_count": len(content),
            "sentence_count": 0,
            "paragraph_count": 0,
            "sentence_length_avg": 0,
            "dialogue_ratio": 0,
            "descriptive_ratio": 0
        }
        
        if not content:
            return features
        
        # 统计句子
        sentences = re.split(r'[。！？.!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        features['sentence_count'] = len(sentences)
        
        # 计算平均句子长度
        if sentences:
            features['sentence_length_avg'] = sum(len(s) for s in sentences) / len(sentences)
        
        # 统计段落
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        features['paragraph_count'] = len(paragraphs)
        
        # 估算对话比例（包含引号的内容）
        dialogue_pattern = r'["「][^"」]+["」]'
        dialogue_matches = re.findall(dialogue_pattern, content)
        dialogue_chars = sum(len(match) for match in dialogue_matches)
        
        if len(content) > 0:
            features['dialogue_ratio'] = dialogue_chars / len(content)
        
        # 估算描述比例（包含描写性词汇）
        descriptive_words = ['的', '地', '得', '着', '了', '过', '在', '是']
        descriptive_count = sum(content.count(word) for word in descriptive_words)
        
        if len(content) > 0:
            features['descriptive_ratio'] = descriptive_count / len(content)
        
        return features

# 测试函数
if __name__ == "__main__":
    print("测试一体化调整器...")
    
    adjuster = UnifiedAdjuster()
    
    # 测试文本
    test_content = """
    张三站在山顶，眺望远方的云海。他的心情很复杂，既有对未来的期待，也有对过去的留恋。
    风吹过他的脸庞，带来一丝凉意。他想起了师父的教诲，心中涌起一股力量。
    """
    
    # 测试调整
    test_context = {
        "novel_type": "玄幻",
        "writing_style": "文艺细腻",
        "characters": [{"name": "张三", "personality": "坚毅、深思"}]
    }
    
    # 生成建议
    suggestions = adjuster.generate_adjustment_suggestions(test_content, test_context)
    print(f"生成 {len(suggestions)} 条调整建议:")
    for suggestion in suggestions:
        print(f"  [{suggestion['priority']}] {suggestion['type']}: {suggestion['suggestion']}")
    
    # 如果没有LLM，显示模拟结果
    if not adjuster.llm:
        print("\n（模拟）执行风格调整...")
        adjusted = test_content + "\n（此处为模拟的调整结果）"
        
        # 分析效果
        effect = adjuster._analyze_adjustment_effect(
            original=test_content,
            adjusted=adjusted,
            adjustment_type="叙事风格"
        )
        
        print(f"调整效果分析: {effect}")