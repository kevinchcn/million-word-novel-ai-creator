"""
一致性检查模块
多维度验证小说内容的一致性
"""

import json
from typing import Dict, List, Any, Tuple
from difflib import SequenceMatcher

class ConsistencyChecker:
    """一致性检查器 - 极简实现"""
    
    def __init__(self):
        self.character_profiles = {}
        self.worldview_rules = {}
        self.timeline = []
    
    def check_character_consistency(self, character_name: str, 
                                   new_content: str, 
                                   existing_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查人物一致性
        
        Args:
            character_name: 人物名称
            new_content: 新内容
            existing_profile: 已有的人物档案
            
        Returns:
            检查结果
        """
        results = {
            "passed": True,
            "score": 100,
            "issues": [],
            "suggestions": []
        }
        
        # 检查性格一致性
        personality = existing_profile.get('personality', '')
        if personality:
            # 简单检查：关键词匹配
            personality_keywords = self._extract_keywords(personality)
            content_keywords = self._extract_keywords(new_content)
            
            matching_keywords = [k for k in personality_keywords if k in content_keywords]
            match_ratio = len(matching_keywords) / max(len(personality_keywords), 1)
            
            if match_ratio < 0.3:
                results["passed"] = False
                results["score"] -= 30
                results["issues"].append(f"人物'{character_name}'的性格表现不一致")
                results["suggestions"].append(f"在描述{character_name}时，请更多体现: {', '.join(personality_keywords[:5])}")
        
        # 检查能力一致性
        abilities = existing_profile.get('abilities', [])
        if abilities:
            # 检查新内容是否出现了未定义的能力
            mentioned_abilities = []
            for ability in abilities:
                if ability in new_content:
                    mentioned_abilities.append(ability)
            
            if len(mentioned_abilities) == 0 and len(abilities) > 0:
                results["issues"].append(f"人物'{character_name}'的能力未在场景中体现")
        
        return results
    
    def check_plot_consistency(self, new_content: str, 
                              previous_summaries: List[str]) -> Dict[str, Any]:
        """
        检查情节一致性
        
        Args:
            new_content: 新内容
            previous_summaries: 之前章节的摘要
            
        Returns:
            检查结果
        """
        results = {
            "passed": True,
            "score": 100,
            "issues": [],
            "suggestions": []
        }
        
        # 检查情节连贯性
        if previous_summaries:
            last_summary = previous_summaries[-1] if previous_summaries else ""
            
            # 简单检查：关键词连续性
            last_keywords = self._extract_keywords(last_summary)
            current_keywords = self._extract_keywords(new_content)
            
            continuity_score = self._calculate_continuity(last_keywords, current_keywords)
            
            if continuity_score < 0.2:
                results["score"] -= 20
                results["issues"].append("情节连贯性较弱")
                results["suggestions"].append("考虑增加与上一章的连接")
        
        # 检查逻辑漏洞
        logical_issues = self._check_logical_issues(new_content)
        if logical_issues:
            results["passed"] = False
            results["score"] -= len(logical_issues) * 10
            results["issues"].extend(logical_issues)
            results["suggestions"].append("检查情节逻辑，修复矛盾之处")
        
        return results
    
    def check_worldview_consistency(self, new_content: str, 
                                   worldview: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查世界观一致性
        
        Args:
            new_content: 新内容
            worldview: 世界观设定
            
        Returns:
            检查结果
        """
        results = {
            "passed": True,
            "score": 100,
            "issues": [],
            "suggestions": []
        }
        
        # 检查世界观规则
        rules = worldview.get('special_rules', '')
        if rules:
            # 检查是否违反特殊规则
            violations = []
            
            # 这里可以添加具体的规则检查逻辑
            # 例如：检查是否有"御剑飞行"但世界观中没有修真体系
            
            if violations:
                results["passed"] = False
                results["score"] -= len(violations) * 15
                results["issues"].extend(violations)
        
        # 检查文化风俗
        culture = worldview.get('culture', '')
        if culture:
            culture_keywords = self._extract_keywords(culture)
            content_keywords = self._extract_keywords(new_content)
            
            # 检查是否有文化元素但未在内容中体现
            culture_match = any(keyword in content_keywords for keyword in culture_keywords[:5])
            
            if not culture_match and culture_keywords:
                results["issues"].append("文化风俗元素未充分体现")
                results["suggestions"].append(f"考虑加入: {', '.join(culture_keywords[:3])}")
        
        return results
    
    def full_consistency_check(self, outline: Dict[str, Any], 
                              characters: List[Dict[str, Any]],
                              chapters: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
        """
        全面一致性检查
        
        Args:
            outline: 小说大纲
            characters: 人物列表
            chapters: 章节数据
            
        Returns:
            全面检查结果
        """
        results = {
            "overall_score": 0,
            "character_consistency": {"score": 0, "issues": []},
            "plot_consistency": {"score": 0, "issues": []},
            "worldview_consistency": {"score": 0, "issues": []},
            "timeline_consistency": {"score": 0, "issues": []}
        }
        
        # 人物一致性检查
        char_scores = []
        char_issues = []
        
        for character in characters:
            char_name = character.get('name', '')
            
            # 检查该人物在所有章节中的表现
            for chapter_num, chapter_data in chapters.items():
                content = chapter_data.get('content', '')
                
                if char_name in content:
                    char_result = self.check_character_consistency(
                        char_name, content, character
                    )
                    
                    char_scores.append(char_result['score'])
                    char_issues.extend(char_result['issues'])
        
        if char_scores:
            results["character_consistency"]["score"] = sum(char_scores) // len(char_scores)
            results["character_consistency"]["issues"] = char_issues[:5]  # 最多显示5个问题
        
        # 情节一致性检查
        plot_scores = []
        plot_issues = []
        
        chapter_numbers = list(chapters.keys())
        chapter_numbers.sort()
        
        for i in range(1, len(chapter_numbers)):
            current_chapter = chapters[chapter_numbers[i]]
            previous_chapter = chapters[chapter_numbers[i-1]]
            
            plot_result = self.check_plot_consistency(
                current_chapter.get('content', ''),
                [previous_chapter.get('summary', '')]
            )
            
            plot_scores.append(plot_result['score'])
            plot_issues.extend(plot_result['issues'])
        
        if plot_scores:
            results["plot_consistency"]["score"] = sum(plot_scores) // len(plot_scores)
            results["plot_consistency"]["issues"] = plot_issues[:5]
        
        # 计算总体评分
        component_scores = [
            results["character_consistency"]["score"],
            results["plot_consistency"]["score"],
            results["worldview_consistency"]["score"],
            results["timeline_consistency"]["score"]
        ]
        
        # 加权平均
        weights = [0.3, 0.4, 0.2, 0.1]
        overall_score = sum(score * weight for score, weight in zip(component_scores, weights))
        results["overall_score"] = int(overall_score)
        
        return results
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """提取关键词"""
        # 简单实现：提取长度大于2的中文字符
        import re
        
        # 提取中文词语
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        
        # 去除常见停用词
        stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        
        keywords = [word for word in chinese_words if word not in stopwords]
        
        # 返回前N个关键词
        return keywords[:max_keywords]
    
    def _calculate_continuity(self, last_keywords: List[str], 
                             current_keywords: List[str]) -> float:
        """计算连续性分数"""
        if not last_keywords or not current_keywords:
            return 0.0
        
        # 计算关键词重叠率
        common_keywords = set(last_keywords) & set(current_keywords)
        continuity = len(common_keywords) / max(len(set(last_keywords)), 1)
        
        return continuity
    
    def _check_logical_issues(self, content: str) -> List[str]:
        """检查逻辑漏洞"""
        issues = []
        
        # 简单检查：时间矛盾
        time_indicators = ['之前', '之后', '刚才', '现在', '未来', '过去']
        time_mentions = []
        
        for indicator in time_indicators:
            if indicator in content:
                time_mentions.append(indicator)
        
        # 如果有多个时间指示词，可能存在时间矛盾
        if len(time_mentions) > 3:
            issues.append("时间描述可能存在矛盾")
        
        # 检查明显矛盾
        contradictions = [
            ('死', '活'),
            ('有', '无'),
            ('存在', '不存在')
        ]
        
        for word1, word2 in contradictions:
            if word1 in content and word2 in content:
                # 检查是否在同一上下文中
                issues.append(f"可能存在'{word1}'和'{word2}'的矛盾")
        
        return issues
    
    def check_chapter_consistency(self, chapter_data: Dict[str, Any], 
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查单个章节的一致性
        
        Args:
            chapter_data: 章节数据
            context: 上下文信息
            
        Returns:
            检查结果
        """
        results = {
            "passed": True,
            "score": 100,
            "detailed_checks": {},
            "issues": [],
            "suggestions": []
        }
        
        content = chapter_data.get('content', '')
        
        # 1. 人物一致性检查
        if 'characters' in context:
            for character in context['characters']:
                char_name = character.get('name', '')
                if char_name in content:
                    char_result = self.check_character_consistency(
                        char_name, content, character
                    )
                    
                    results['detailed_checks'][f'character_{char_name}'] = char_result
                    
                    if not char_result['passed']:
                        results['passed'] = False
                        results['score'] = min(results['score'], char_result['score'])
                        results['issues'].extend(char_result['issues'])
                        results['suggestions'].extend(char_result['suggestions'])
        
        # 2. 情节一致性检查
        if 'previous_summaries' in context:
            plot_result = self.check_plot_consistency(
                content, context['previous_summaries']
            )
            
            results['detailed_checks']['plot'] = plot_result
            
            if not plot_result['passed']:
                results['passed'] = False
                results['score'] = min(results['score'], plot_result['score'])
                results['issues'].extend(plot_result['issues'])
                results['suggestions'].extend(plot_result['suggestions'])
        
        # 3. 世界观一致性检查
        if 'worldview' in context:
            worldview_result = self.check_worldview_consistency(
                content, context['worldview']
            )
            
            results['detailed_checks']['worldview'] = worldview_result
            
            if not worldview_result['passed']:
                results['passed'] = False
                results['score'] = min(results['score'], worldview_result['score'])
                results['issues'].extend(worldview_result['issues'])
                results['suggestions'].extend(worldview_result['suggestions'])
        
        return results

# 测试函数
if __name__ == "__main__":
    checker = ConsistencyChecker()
    
    # 测试数据
    test_character = {
        "name": "张三",
        "personality": "勇敢、聪明、善良",
        "abilities": ["剑法", "法术"]
    }
    
    test_content = "张三是一个胆小的人，他什么都不会。"
    
    # 测试人物一致性
    result = checker.check_character_consistency(
        "张三", test_content, test_character
    )
    
    print("人物一致性检查结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 测试情节一致性
    plot_result = checker.check_plot_consistency(
        "新的章节开始了。",
        ["上一章结束了战斗。"]
    )
    
    print("\n情节一致性检查结果:")
    print(json.dumps(plot_result, indent=2, ensure_ascii=False))
    
    # 测试全面检查
    full_result = checker.full_consistency_check(
        outline={"title": "测试"},
        characters=[test_character],
        chapters={1: {"content": test_content, "summary": "测试章节"}}
    )
    
    print("\n全面一致性检查结果:")
    print(json.dumps(full_result, indent=2, ensure_ascii=False))