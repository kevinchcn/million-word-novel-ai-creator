"""
智能记忆系统
分层记忆架构解决百万字一致性问题 - 完整实现
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
import hashlib

class SmartMemory:
    """智能记忆系统 - 完整实现"""
    
    def __init__(self, memory_dir: str = "./memory"):
        self.memory_dir = memory_dir
        self.core_settings = {}      # 核心设定（永不遗忘）
        self.characters = {}         # 人物档案
        self.worldview = {}          # 世界观
        self.chapter_summaries = {}  # 章节摘要
        self.relationship_graph = {} # 人物关系图
        self.timeline = []           # 时间线
        self.plots = []              # 情节线
        self.locations = {}          # 地点档案
        
        self._ensure_directories()
        self._load_from_disk()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        directories = [
            self.memory_dir,
            f"{self.memory_dir}/characters",
            f"{self.memory_dir}/summaries",
            f"{self.memory_dir}/relationships",
            f"{self.memory_dir}/plots",
            f"{self.memory_dir}/locations",
            f"{self.memory_dir}/backups"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _load_from_disk(self):
        """从磁盘加载记忆"""
        try:
            # 加载核心设定
            core_file = f"{self.memory_dir}/core_settings.json"
            if os.path.exists(core_file):
                try:
                    with open(core_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():  # 检查文件是否为空
                            self.core_settings = json.loads(content)
                except json.JSONDecodeError:
                    print(f"⚠️ 核心设定文件格式错误，使用默认值")
                    self.core_settings = {}
            
            # 加载人物档案
            characters_dir = f"{self.memory_dir}/characters"
            if os.path.exists(characters_dir):
                for file in os.listdir(characters_dir):
                    if file.endswith('.json'):
                        char_name = file.replace('.json', '')
                        file_path = f"{characters_dir}/{file}"
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if content.strip():
                                    self.characters[char_name] = json.loads(content)
                        except json.JSONDecodeError:
                            print(f"⚠️ 人物文件 {file} 格式错误，跳过")
            
            # 加载章节摘要
            summaries_file = f"{self.memory_dir}/summaries/chapter_summaries.json"
            if os.path.exists(summaries_file):
                try:
                    with open(summaries_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            self.chapter_summaries = json.loads(content)
                except json.JSONDecodeError:
                    print(f"⚠️ 章节摘要文件格式错误，使用默认值")
                    self.chapter_summaries = {}
            
            # 加载世界观
            worldview_file = f"{self.memory_dir}/worldview.json"
            if os.path.exists(worldview_file):
                try:
                    with open(worldview_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            self.worldview = json.loads(content)
                except json.JSONDecodeError:
                    print(f"⚠️ 世界观文件格式错误，使用默认值")
                    self.worldview = {}
            
            # 加载时间线
            timeline_file = f"{self.memory_dir}/timeline.json"
            if os.path.exists(timeline_file):
                try:
                    with open(timeline_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            self.timeline = json.loads(content)
                except json.JSONDecodeError:
                    print(f"⚠️ 时间线文件格式错误，使用默认值")
                    self.timeline = []
            
            # 加载情节线
            plots_dir = f"{self.memory_dir}/plots"
            if os.path.exists(plots_dir):
                for file in os.listdir(plots_dir):
                    if file.endswith('.json'):
                        file_path = f"{plots_dir}/{file}"
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if content.strip():
                                    self.plots.append(json.loads(content))
                        except json.JSONDecodeError:
                            print(f"⚠️ 情节线文件 {file} 格式错误，跳过")
            
            # 加载地点
            locations_dir = f"{self.memory_dir}/locations"
            if os.path.exists(locations_dir):
                for file in os.listdir(locations_dir):
                    if file.endswith('.json'):
                        loc_name = file.replace('.json', '')
                        file_path = f"{locations_dir}/{file}"
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if content.strip():
                                    self.locations[loc_name] = json.loads(content)
                        except json.JSONDecodeError:
                            print(f"⚠️ 地点文件 {file} 格式错误，跳过")
            
            print(f"✅ 记忆系统加载完成: {len(self.characters)}人物, {len(self.chapter_summaries)}章节")
            
        except Exception as e:
            print(f"⚠️ 加载记忆失败: {str(e)}")
            # 初始化默认结构
            self._init_default_structure()
    
    def _save_to_disk(self):
        """保存记忆到磁盘"""
        try:
            # 创建备份
            self._create_backup()
            
            # 保存核心设定
            with open(f"{self.memory_dir}/core_settings.json", 'w', encoding='utf-8') as f:
                json.dump(self.core_settings, f, ensure_ascii=False, indent=2)
            
            # 保存人物档案
            for char_name, char_data in self.characters.items():
                # 清理文件名中的非法字符
                safe_name = "".join(c for c in char_name if c.isalnum() or c in " _-")
                with open(f"{self.memory_dir}/characters/{safe_name}.json", 'w', encoding='utf-8') as f:
                    json.dump(char_data, f, ensure_ascii=False, indent=2)
            
            # 保存章节摘要
            with open(f"{self.memory_dir}/summaries/chapter_summaries.json", 'w', encoding='utf-8') as f:
                json.dump(self.chapter_summaries, f, ensure_ascii=False, indent=2)
            
            # 保存世界观
            with open(f"{self.memory_dir}/worldview.json", 'w', encoding='utf-8') as f:
                json.dump(self.worldview, f, ensure_ascii=False, indent=2)
            
            # 保存时间线
            with open(f"{self.memory_dir}/timeline.json", 'w', encoding='utf-8') as f:
                json.dump(self.timeline, f, ensure_ascii=False, indent=2)
            
            # 保存情节线
            for i, plot in enumerate(self.plots):
                with open(f"{self.memory_dir}/plots/plot_{i+1}.json", 'w', encoding='utf-8') as f:
                    json.dump(plot, f, ensure_ascii=False, indent=2)
            
            # 保存地点
            for loc_name, loc_data in self.locations.items():
                safe_name = "".join(c for c in loc_name if c.isalnum() or c in " _-")
                with open(f"{self.memory_dir}/locations/{safe_name}.json", 'w', encoding='utf-8') as f:
                    json.dump(loc_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ 保存记忆失败: {str(e)}")
            return False
    
    def _create_backup(self):
        """创建备份"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"{self.memory_dir}/backups/{timestamp}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # 复制当前文件到备份目录
            import shutil
            for item in os.listdir(self.memory_dir):
                if item != "backups":
                    src = os.path.join(self.memory_dir, item)
                    if os.path.isfile(src):
                        shutil.copy2(src, backup_dir)
                    elif os.path.isdir(src):
                        shutil.copytree(src, os.path.join(backup_dir, item))
            
            # 清理旧备份（保留最近5个）
            backups = sorted(os.listdir(f"{self.memory_dir}/backups"))
            for backup in backups[:-5]:
                shutil.rmtree(f"{self.memory_dir}/backups/{backup}")
                
        except Exception as e:
            print(f"⚠️ 备份失败: {str(e)}")

    # 在 SmartMemory 类中添加以下方法（大约在第200行附近）
    def save_chapter_plan(self, chapter_plan):
        """保存章节计划 - 简单实现"""
        # 保存到核心设定中
        self.core_settings['chapter_plan'] = chapter_plan
        self._save_to_disk()
        
    def get_chapter_plan(self):
        """获取章节计划 - 简单实现"""
        return self.core_settings.get('chapter_plan', [])

    def save_core_settings(self, settings: Dict[str, Any]):
        """保存核心设定"""
        self.core_settings.update(settings)
        self._save_to_disk()
    
    def save_characters(self, characters: List[Dict[str, Any]]):
        """保存人物设定"""
        for char in characters:
            char_name = char.get('name', 'unknown')
            self.characters[char_name] = char
            
            # 添加时间戳
            if 'created_at' not in self.characters[char_name]:
                self.characters[char_name]['created_at'] = datetime.now().isoformat()
            self.characters[char_name]['updated_at'] = datetime.now().isoformat()
        
        self._save_to_disk()
    
    def save_worldview(self, worldview: Dict[str, Any]):
        """保存世界观"""
        self.worldview = worldview
        
        # 同时保存到核心设定
        if 'worldview' not in self.core_settings:
            self.core_settings['worldview'] = worldview
        
        self._save_to_disk()
    
    def get_context(self, chapter_number: int, window_size: int = 5) -> str:
        """
        获取章节相关上下文
        
        Args:
            chapter_number: 当前章节编号
            window_size: 上下文窗口大小
            
        Returns:
            上下文字符串
        """
        context_parts = []
        
        # 1. 核心设定（总是包含）
        if self.core_settings:
            context_parts.append("## 📚 核心设定")
            for key, value in self.core_settings.items():
                if key not in ['version', 'created_at', 'memory_hierarchy']:
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            context_parts.append(f"- {sub_key}: {sub_value}")
                    else:
                        context_parts.append(f"- {key}: {value}")
        
        # 2. 世界观
        if self.worldview:
            context_parts.append("\n## 🌍 世界观")
            for key, value in self.worldview.items():
                if isinstance(value, list):
                    context_parts.append(f"- {key}: {', '.join(value[:3])}")
                else:
                    context_parts.append(f"- {key}: {value}")
        
        # 3. 相关人物
        relevant_chars = self._get_relevant_characters(chapter_number)
        if relevant_chars:
            context_parts.append("\n## 👥 相关人物")
            for char_name, char_data in relevant_chars.items():
                context_parts.append(f"### {char_name}")
                context_parts.append(f"- 身份: {char_data.get('identity', '')}")
                context_parts.append(f"- 性格: {char_data.get('personality', '')}")
                context_parts.append(f"- 动机: {char_data.get('motivation', '')}")
                
                # 近期发展
                dev_history = char_data.get('development_history', [])
                if dev_history:
                    recent_dev = dev_history[-1] if len(dev_history) > 0 else {}
                    if recent_dev:
                        context_parts.append(f"- 近期发展: {recent_dev.get('development', '')}")
        
        # 4. 最近章节摘要
        recent_summaries = self._get_recent_summaries(chapter_number, window_size)
        if recent_summaries:
            context_parts.append("\n## 📖 最近情节")
            for chap_num, summary in recent_summaries:
                context_parts.append(f"第{chap_num}章: {summary}")
        
        # 5. 时间线关键事件
        timeline_events = self._get_timeline_events(chapter_number)
        if timeline_events:
            context_parts.append("\n## ⏳ 时间线事件")
            for event in timeline_events:
                context_parts.append(f"- {event}")
        
        # 6. 相关地点
        relevant_locations = self._get_relevant_locations(chapter_number)
        if relevant_locations:
            context_parts.append("\n## 🗺️ 相关地点")
            for loc_name, loc_data in relevant_locations.items():
                context_parts.append(f"- {loc_name}: {loc_data.get('description', '')[:100]}...")
        
        # 7. 活跃情节线
        active_plots = self._get_active_plots(chapter_number)
        if active_plots:
            context_parts.append("\n## 🎭 活跃情节线")
            for plot in active_plots[:3]:  # 最多3条
                context_parts.append(f"- {plot.get('name', '未命名')}: {plot.get('current_status', '')}")
        
        return "\n".join(context_parts)
    
    def _get_relevant_characters(self, chapter_number: int) -> Dict[str, Dict]:
        """获取相关人物"""
        relevant_chars = {}
        
        # 规则1: 主角总是在相关人物中
        for name, data in self.characters.items():
            if "主角" in name or data.get('importance', 0) >= 8:
                relevant_chars[name] = data
        
        # 规则2: 根据章节编号选择其他人物
        if chapter_number <= 3:
            # 前3章: 引入主要配角
            for name, data in self.characters.items():
                if data.get('importance', 0) >= 6 and name not in relevant_chars:
                    relevant_chars[name] = data
                    if len(relevant_chars) >= 5:  # 最多5个
                        break
        else:
            # 后续章节: 根据章节编号和人物重要性选择
            for name, data in self.characters.items():
                # 计算人物相关性分数
                relevance_score = self._calculate_character_relevance(name, chapter_number)
                
                if relevance_score >= 0.3 or data.get('importance', 0) >= 7:
                    relevant_chars[name] = data
                
                if len(relevant_chars) >= 8:  # 最多8个
                    break
        
        return relevant_chars
    
    def _calculate_character_relevance(self, character_name: str, chapter_number: int) -> float:
        """计算人物相关性分数"""
        if character_name not in self.characters:
            return 0.0
        
        char_data = self.characters[character_name]
        relevance = 0.0
        
        # 1. 基础重要性
        importance = char_data.get('importance', 5)
        relevance += importance * 0.05
        
        # 2. 上次出现时间
        last_appearance = char_data.get('last_appearance', 0)
        if last_appearance > 0:
            chapters_since = chapter_number - last_appearance
            if chapters_since <= 3:
                relevance += 0.3
            elif chapters_since <= 10:
                relevance += 0.1
        
        # 3. 发展历史长度
        dev_history = char_data.get('development_history', [])
        if dev_history:
            relevance += min(0.2, len(dev_history) * 0.02)
        
        # 4. 与章节编号的哈希关系（确保一致性）
        hash_input = f"{character_name}_{chapter_number}"
        hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        hash_score = (hash_val % 100) / 100.0
        
        # 5. 在最近摘要中的提及
        recent_mentions = self._count_character_mentions(character_name, chapter_number)
        relevance += min(0.2, recent_mentions * 0.05)
        
        return min(1.0, relevance + hash_score * 0.2)
    
    def _count_character_mentions(self, character_name: str, up_to_chapter: int) -> int:
        """统计人物在最近摘要中的提及次数"""
        count = 0
        for chap_num in range(max(1, up_to_chapter - 5), up_to_chapter):
            summary = self.chapter_summaries.get(str(chap_num), "")
            if summary and character_name in summary:
                count += 1
        return count
    
    def _get_recent_summaries(self, current_chapter: int, window_size: int = 5) -> List[Tuple[int, str]]:
        """获取最近章节摘要"""
        recent = []
        
        start_chapter = max(1, current_chapter - window_size)
        
        for chap_num in range(start_chapter, current_chapter):
            summary = self.chapter_summaries.get(str(chap_num))
            if summary:
                # 如果摘要太长，截断
                if isinstance(summary, dict):
                    summary_text = summary.get('summary', '')
                else:
                    summary_text = str(summary)
                
                if len(summary_text) > 200:
                    summary_text = summary_text[:200] + "..."
                
                recent.append((chap_num, summary_text))
        
        return recent
    
    def _get_timeline_events(self, up_to_chapter: int) -> List[str]:
        """获取时间线事件"""
        events = []
        
        for event in self.timeline:
            event_chapter = event.get('chapter', 0)
            if 0 < event_chapter <= up_to_chapter:
                event_desc = event.get('description', '')
                events.append(f"第{event_chapter}章: {event_desc}")
        
        # 按章节排序
        events.sort(key=lambda x: int(x.split('第')[1].split('章')[0]))
        
        return events[-10:]  # 最多返回10个最近事件
    
    def _get_relevant_locations(self, chapter_number: int) -> Dict[str, Dict]:
        """获取相关地点"""
        relevant_locs = {}
        
        # 简单实现：根据章节编号选择
        for name, data in self.locations.items():
            # 根据名称哈希决定是否相关
            hash_input = f"{name}_{chapter_number}"
            hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
            
            if hash_val % 3 == 0:  # 约1/3的地点相关
                relevant_locs[name] = data
            
            if len(relevant_locs) >= 5:  # 最多5个地点
                break
        
        return relevant_locs
    
    def _get_active_plots(self, chapter_number: int) -> List[Dict[str, Any]]:
        """获取活跃情节线"""
        active_plots = []
        
        for plot in self.plots:
            start_chapter = plot.get('start_chapter', 0)
            end_chapter = plot.get('end_chapter', 9999)
            
            if start_chapter <= chapter_number <= end_chapter:
                active_plots.append(plot)
        
        return active_plots[:5]  # 最多5条
    
    def update_with_chapter(self, chapter_number: int, chapter_data: Dict[str, Any]):
        """用章节数据更新记忆系统"""
        
        # 提取章节摘要
        summary = chapter_data.get('summary', '')
        if not summary:
            # 如果没有摘要，从内容中生成简单摘要
            content = chapter_data.get('content', '')
            summary = content[:200] + "..." if len(content) > 200 else content
        
        # 保存章节摘要（智能格式）
        chapter_summary = {
            'summary': summary,
            'chapter_number': chapter_number,
            'word_count': len(chapter_data.get('content', '')),
            'key_events': chapter_data.get('key_events', []),
            'timestamp': datetime.now().isoformat()
        }
        
        self.chapter_summaries[str(chapter_number)] = chapter_summary
        
        # 提取人物发展
        character_development = chapter_data.get('character_development', {})
        for char_name, development in character_development.items():
            if char_name in self.characters:
                # 更新人物最后出现章节
                self.characters[char_name]['last_appearance'] = chapter_number
                
                # 更新人物发展历史
                if 'development_history' not in self.characters[char_name]:
                    self.characters[char_name]['development_history'] = []
                
                self.characters[char_name]['development_history'].append({
                    'chapter': chapter_number,
                    'development': development,
                    'timestamp': datetime.now().isoformat()
                })
        
        # 提取关键事件并添加到时间线
        key_events = chapter_data.get('key_events', [])
        for event in key_events:
            self.timeline.append({
                'chapter': chapter_number,
                'description': event,
                'timestamp': datetime.now().isoformat(),
                'type': 'chapter_event'
            })
        
        # 提取地点信息
        self._extract_locations(chapter_data.get('content', ''), chapter_number)
        
        # 提取情节信息
        self._extract_plots(chapter_data, chapter_number)
        
        # 更新关系图
        self._update_relationships(chapter_data, chapter_number)
        
        # 保存到磁盘
        self._save_to_disk()
        
        print(f"✅ 第{chapter_number}章记忆已更新")
    
    def _extract_locations(self, content: str, chapter_number: int):
        """从内容中提取地点信息"""
        # 简单实现：识别可能的地点名称
        import re
        
        # 识别地点描述模式
        location_patterns = [
            r'在([\u4e00-\u9fa5]{2,6})地?区?',
            r'来到([\u4e00-\u9fa5]{2,6})',
            r'位于([\u4e00-\u9fa5]{2,6})',
            r'([\u4e00-\u9fa5]{2,6})中?'
        ]
        
        locations_found = set()
        for pattern in location_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) >= 2:  # 至少2个字的可能是地点
                    locations_found.add(match)
        
        # 更新地点档案
        for loc_name in locations_found:
            if loc_name not in self.locations:
                self.locations[loc_name] = {
                    'name': loc_name,
                    'first_appearance': chapter_number,
                    'last_appearance': chapter_number,
                    'appearance_count': 1,
                    'description': f"在{loc_name}发生的事件",
                    'created_at': datetime.now().isoformat()
                }
            else:
                self.locations[loc_name]['last_appearance'] = chapter_number
                self.locations[loc_name]['appearance_count'] += 1
    
    def _extract_plots(self, chapter_data: Dict[str, Any], chapter_number: int):
        """从章节中提取情节信息"""
        key_events = chapter_data.get('key_events', [])
        
        if key_events:
            # 检查是否属于现有情节线
            for plot in self.plots:
                plot_keywords = plot.get('keywords', [])
                for event in key_events:
                    if any(keyword in event for keyword in plot_keywords):
                        # 更新现有情节线
                        if 'chapters' not in plot:
                            plot['chapters'] = []
                        plot['chapters'].append(chapter_number)
                        plot['last_updated'] = datetime.now().isoformat()
                        break
            
            # 创建新的情节线（如果事件足够重要）
            if len(key_events) >= 2:
                new_plot = {
                    'name': f"情节线_{len(self.plots)+1}",
                    'start_chapter': chapter_number,
                    'end_chapter': chapter_number,  # 初始值，后续会更新
                    'keywords': key_events[:3],  # 前3个事件作为关键词
                    'chapters': [chapter_number],
                    'created_at': datetime.now().isoformat(),
                    'current_status': '进行中'
                }
                self.plots.append(new_plot)
    
    def _update_relationships(self, chapter_data: Dict[str, Any], chapter_number: int):
        """更新人物关系图"""
        content = chapter_data.get('content', '')
        
        # 简单实现：检测人物互动
        character_interactions = []
        
        for char1 in self.characters:
            for char2 in self.characters:
                if char1 != char2:
                    # 检查两个人物是否在同一段落中被提及
                    if char1 in content and char2 in content:
                        # 计算提及距离
                        pos1 = content.find(char1)
                        pos2 = content.find(char2)
                        
                        if abs(pos1 - pos2) < 500:  # 500字符内视为有关联
                            character_interactions.append((char1, char2))
        
        # 更新关系图
        for char1, char2 in character_interactions:
            relationship_key = f"{char1}-{char2}"
            
            if 'relationships' not in self.relationship_graph:
                self.relationship_graph['relationships'] = {}
            
            if relationship_key not in self.relationship_graph['relationships']:
                self.relationship_graph['relationships'][relationship_key] = {
                    'characters': [char1, char2],
                    'interaction_count': 1,
                    'first_interaction': chapter_number,
                    'last_interaction': chapter_number,
                    'interaction_chapters': [chapter_number]
                }
            else:
                rel = self.relationship_graph['relationships'][relationship_key]
                rel['interaction_count'] += 1
                rel['last_interaction'] = chapter_number
                if chapter_number not in rel['interaction_chapters']:
                    rel['interaction_chapters'].append(chapter_number)
    
    def get_character_profile(self, character_name: str) -> Optional[Dict[str, Any]]:
        """获取人物完整档案"""
        return self.characters.get(character_name)
    
    def update_character(self, character_name: str, updates: Dict[str, Any]):
        """更新人物档案"""
        if character_name in self.characters:
            self.characters[character_name].update(updates)
            self.characters[character_name]['updated_at'] = datetime.now().isoformat()
            self._save_to_disk()
    
    def add_relationship(self, char1: str, char2: str, relationship: str):
        """添加人物关系"""
        if 'relationships' not in self.relationship_graph:
            self.relationship_graph['relationships'] = []
        
        self.relationship_graph['relationships'].append({
            'char1': char1,
            'char2': char2,
            'relationship': relationship,
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_to_disk()
    
    def get_consistency_checklist(self) -> List[str]:
        """获取一致性检查清单"""
        checklist = []
        
        # 人物一致性检查
        for char_name, char_data in self.characters.items():
            # 检查基本属性是否存在
            required_fields = ['name', 'personality', 'motivation']
            for field in required_fields:
                if field not in char_data or not char_data[field]:
                    checklist.append(f"人物'{char_name}'缺少{field}")
            
            # 检查性格一致性
            personality_history = char_data.get('development_history', [])
            if personality_history:
                # 检查性格是否有突变
                recent_personality = None
                for dev in personality_history[-3:]:  # 最近3次发展
                    dev_text = dev.get('development', '')
                    if '性格' in dev_text or '变得' in dev_text:
                        if recent_personality and recent_personality != dev_text:
                            checklist.append(f"人物'{char_name}'性格可能突变")
                        recent_personality = dev_text
        
        # 时间线一致性检查
        chapter_numbers = [int(num) for num in self.chapter_summaries.keys() if num.isdigit()]
        chapter_numbers.sort()
        
        if chapter_numbers:
            # 检查章节编号是否连续
            for i in range(1, len(chapter_numbers)):
                if chapter_numbers[i] != chapter_numbers[i-1] + 1:
                    checklist.append(f"章节编号不连续: 第{chapter_numbers[i-1]}章后应为第{chapter_numbers[i-1]+1}章")
            
            # 检查时间线事件顺序
            timeline_chapters = [event.get('chapter', 0) for event in self.timeline]
            if timeline_chapters:
                if sorted(timeline_chapters) != timeline_chapters:
                    checklist.append("时间线事件顺序可能混乱")
        
        # 世界观一致性检查
        if self.worldview:
            # 检查是否存在矛盾规则
            rules = self.worldview.get('special_rules', [])
            limitations = self.worldview.get('limitations', [])
            
            for rule in rules:
                for limitation in limitations:
                    if rule in limitation or limitation in rule:
                        checklist.append(f"世界观规则可能矛盾: '{rule}' vs '{limitation}'")
        
        return checklist
    
    def get_chapter_plan(self) -> List[Dict[str, Any]]:
        """获取章节计划"""
        # 从核心设定中获取大纲
        outline = self.core_settings.get('outline', {})
        target_words = outline.get('target_words', 100000)
        
        # 简单计算章节数
        estimated_chapters = max(10, target_words // 3000)
        
        plan = []
        for i in range(1, estimated_chapters + 1):
            # 确定属于哪一幕
            if i <= estimated_chapters * 0.3:
                act = "第一幕：建立"
            elif i <= estimated_chapters * 0.7:
                act = "第二幕：对抗"
            else:
                act = "第三幕：解决"
            
            # 检查是否已生成
            status = "已完成" if str(i) in self.chapter_summaries else "待生成"
            
            summary_data = self.chapter_summaries.get(str(i), {})
            if isinstance(summary_data, dict):
                summary = summary_data.get('summary', '')
            else:
                summary = str(summary_data)
            
            plan.append({
                "章节": i,
                "幕": act,
                "目标字数": 3000,
                "状态": status,
                "摘要": summary[:100] + "..." if len(summary) > 100 else summary
            })
        
        return plan
    
    def get_progress_stats(self) -> Dict[str, Any]:
        """获取进度统计"""
        generated_chapters = len(self.chapter_summaries)
        
        # 计算总字数
        total_words = 0
        for chap_num, summary_data in self.chapter_summaries.items():
            if isinstance(summary_data, dict):
                total_words += summary_data.get('word_count', 3000)
            else:
                total_words += 3000  # 默认估算
        
        # 从大纲获取目标字数
        outline = self.core_settings.get('outline', {})
        target_words = outline.get('target_words', 100000)
        
        # 计算进度
        if target_words > 0:
            percentage = min(100, (total_words / target_words) * 100)
        else:
            percentage = 0
        
        # 计算平均一致性（简单估算）
        consistency_scores = []
        for char_data in self.characters.values():
            dev_history = char_data.get('development_history', [])
            if dev_history:
                consistency_scores.append(80)  # 假设有发展历史就是一致的
            else:
                consistency_scores.append(50)  # 默认分数
        
        avg_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0
        
        return {
            'generated_chapters': generated_chapters,
            'total_words': total_words,
            'target_words': target_words,
            'percentage': percentage,
            'characters_count': len(self.characters),
            'timeline_events': len(self.timeline),
            'locations_count': len(self.locations),
            'plots_count': len(self.plots),
            'avg_consistency': avg_consistency,
            'last_updated': datetime.now().isoformat()
        }
    
    def clear_memory(self):
        """清空记忆（谨慎使用）"""
        self.core_settings = {}
        self.characters = {}
        self.worldview = {}
        self.chapter_summaries = {}
        self.relationship_graph = {}
        self.timeline = []
        self.plots = []
        self.locations = {}
        
        # 删除磁盘文件
        import shutil
        if os.path.exists(self.memory_dir):
            shutil.rmtree(self.memory_dir)
        
        self._ensure_directories()
        self._init_default_structure()
        print("✅ 记忆系统已清空")
    
    def export_memory(self, export_path: str = "./memory_export.json"):
        """导出记忆系统"""
        try:
            export_data = {
                'core_settings': self.core_settings,
                'characters': self.characters,
                'worldview': self.worldview,
                'chapter_summaries': self.chapter_summaries,
                'timeline': self.timeline,
                'plots': self.plots,
                'locations': self.locations,
                'export_time': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 记忆系统已导出到: {export_path}")
            return True
            
        except Exception as e:
            print(f"❌ 导出失败: {str(e)}")
            return False
    
    def import_memory(self, import_path: str):
        """导入记忆系统"""
        try:
            if not os.path.exists(import_path):
                print(f"❌ 导入文件不存在: {import_path}")
                return False
            
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # 验证导入数据
            required_keys = ['core_settings', 'characters', 'worldview', 'chapter_summaries']
            for key in required_keys:
                if key not in import_data:
                    print(f"❌ 导入数据缺少必要字段: {key}")
                    return False
            
            # 更新记忆
            self.core_settings = import_data['core_settings']
            self.characters = import_data['characters']
            self.worldview = import_data['worldview']
            self.chapter_summaries = import_data['chapter_summaries']
            self.timeline = import_data.get('timeline', [])
            self.plots = import_data.get('plots', [])
            self.locations = import_data.get('locations', {})
            
            # 保存到磁盘
            self._save_to_disk()
            
            print(f"✅ 记忆系统已从 {import_path} 导入")
            return True
            
        except Exception as e:
            print(f"❌ 导入失败: {str(e)}")
            return False
    
    def search_memory(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索记忆系统"""
        results = []
        
        # 搜索人物
        for char_name, char_data in self.characters.items():
            if query.lower() in char_name.lower() or query in str(char_data).lower():
                results.append({
                    'type': 'character',
                    'name': char_name,
                    'data': char_data,
                    'relevance': 1.0
                })
        
        # 搜索章节摘要
        for chap_num, summary_data in self.chapter_summaries.items():
            if isinstance(summary_data, dict):
                summary_text = summary_data.get('summary', '')
            else:
                summary_text = str(summary_data)
            
            if query in summary_text:
                results.append({
                    'type': 'chapter_summary',
                    'chapter': chap_num,
                    'summary': summary_text,
                    'relevance': 0.8
                })
        
        # 搜索时间线事件
        for event in self.timeline:
            if query in event.get('description', ''):
                results.append({
                    'type': 'timeline_event',
                    'event': event,
                    'relevance': 0.7
                })
        
        # 按相关性排序并限制数量
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:limit]

# 测试函数
if __name__ == "__main__":
    print("🧠 测试智能记忆系统...")
    
    memory = SmartMemory("./test_memory")
    
    # 测试核心设定
    memory.save_core_settings({
        "title": "测试小说",
        "theme": "成长与冒险",
        "target_words": 100000,
        "author": "测试作者",
        "created_at": datetime.now().isoformat()
    })
    
    # 测试人物
    test_characters = [
        {
            "name": "张三",
            "age": "25",
            "gender": "男",
            "identity": "主角",
            "personality": "勇敢、聪明、善良",
            "motivation": "成为最强修士",
            "importance": 10
        },
        {
            "name": "李四",
            "age": "30",
            "gender": "男",
            "identity": "导师",
            "personality": "严肃、博学",
            "motivation": "培养下一代",
            "importance": 8
        }
    ]
    
    memory.save_characters(test_characters)
    
    # 测试世界观
    memory.save_worldview({
        "basic_setting": "修真世界",
        "power_system": "炼气、筑基、金丹、元婴",
        "social_structure": "宗门制度",
        "special_rules": ["灵气是修炼基础", "心魔会影响突破"]
    })
    
    # 测试更新章节
    test_chapter = {
        "summary": "第一章：主角穿越到修真世界，遇到导师李四",
        "content": "张三睁开眼睛，发现自己躺在一个陌生的山洞中。李四站在他面前，神色严肃。",
        "key_events": ["穿越事件", "遇到导师"],
        "character_development": {
            "张三": "适应新世界",
            "李四": "发现可塑之才"
        }
    }
    
    memory.update_with_chapter(1, test_chapter)
    
    # 测试获取上下文
    context = memory.get_context(2)
    print("\n📝 上下文示例（前500字符）:")
    print(context[:500] + "..." if len(context) > 500 else context)
    
    # 测试进度统计
    stats = memory.get_progress_stats()
    print("\n📊 进度统计:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 测试一致性检查
    checklist = memory.get_consistency_checklist()
    print(f"\n🔍 一致性检查清单 ({len(checklist)}个问题):")
    for item in checklist:
        print(f"  ⚠️ {item}")
    
    # 测试搜索
    search_results = memory.search_memory("主角", limit=3)
    print(f"\n🔎 搜索结果 ({len(search_results)}个):")
    for result in search_results:
        print(f"  {result['type']}: {result.get('name', result.get('chapter', ''))}")
    
    # 清理测试目录
    import shutil
    if os.path.exists("./test_memory"):
        shutil.rmtree("./test_memory")
        print("\n🧹 清理测试目录完成")