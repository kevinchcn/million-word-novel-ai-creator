"""
批量章节生成模块
一次生成多个章节，提高效率
"""

import streamlit as st
import asyncio
import time
from typing import List, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from .generator import NovelGenerator
from .memory_system import SmartMemory
from .consistency import ConsistencyChecker
# Support importing when module is executed as part of the package (relative import)
# and when executed directly as a script (absolute import).
try:
    from ..utils.file_utils import write_file
except Exception:
    # Fallback to absolute import for direct script execution
    from utils.file_utils import write_file

class BatchChapterGenerator:
    """批量章节生成器"""
    
    def __init__(self, generator: NovelGenerator = None, 
                 memory: SmartMemory = None,
                 consistency_checker: ConsistencyChecker = None):
        self.generator = generator
        self.memory = memory
        self.consistency_checker = consistency_checker
        self.max_workers = 3  # 最大并发数
    
    def generate_batch_chapters(self, 
                              start_chapter: int, 
                              chapters_count: int,
                              words_per_chapter: int = 3000,
                              progress_callback: Callable = None,
                              status_callback: Callable = None) -> Dict[str, Any]:
        """
        批量生成多个章节
        
        Args:
            start_chapter: 起始章节
            chapters_count: 章节数量
            words_per_chapter: 每章字数
            progress_callback: 进度回调函数
            status_callback: 状态回调函数
            
        Returns:
            生成结果
        """
        if status_callback:
            status_callback(f"准备生成 {chapters_count} 个章节...")
        
        results = {
            "total_chapters": chapters_count,
            "start_chapter": start_chapter,
            "end_chapter": start_chapter + chapters_count - 1,
            "total_words": 0,
            "total_time": 0,
            "chapters": [],
            "success_count": 0,
            "failed_count": 0
        }
        
        start_time = time.time()
        
        try:
            # 使用线程池并行生成
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                
                for i in range(chapters_count):
                    chapter_num = start_chapter + i
                    
                    future = executor.submit(
                        self._generate_single_chapter,
                        chapter_num,
                        words_per_chapter
                    )
                    futures.append(future)
                
                # 处理完成的任务
                completed_count = 0
                for future in as_completed(futures):
                    try:
                        chapter_result = future.result()
                        
                        if chapter_result['success']:
                            results['chapters'].append(chapter_result)
                            results['success_count'] += 1
                            results['total_words'] += chapter_result.get('word_count', 0)
                            
                            # 更新进度
                            completed_count += 1
                            if progress_callback:
                                progress = completed_count / chapters_count
                                progress_callback(progress)
                            
                            if status_callback:
                                status_callback(f"已完成 {completed_count}/{chapters_count} 章")
                        else:
                            results['failed_count'] += 1
                            print(f"❌ 第{chapter_result['chapter_number']}章生成失败: {chapter_result.get('error', '未知错误')}")
                            
                    except Exception as e:
                        results['failed_count'] += 1
                        print(f"❌ 章节生成异常: {str(e)}")
            
            results['total_time'] = time.time() - start_time
            
            # 保存结果
            self._save_batch_results(results)
            
            return results
            
        except Exception as e:
            if status_callback:
                status_callback(f"批量生成失败: {str(e)}")
            raise
    
    def _generate_single_chapter(self, chapter_number: int, target_words: int) -> Dict[str, Any]:
        """
        生成单个章节
        
        Args:
            chapter_number: 章节编号
            target_words: 目标字数
            
        Returns:
            章节生成结果
        """
        try:
            # 检查必要组件
            if not self.generator or not self.memory:
                raise ValueError("生成器或记忆系统未初始化")
            
            # 获取上下文
            context = self.memory.get_context(chapter_number)
            
            # 获取大纲和人物
            outline = st.session_state.get('generated_outline', {})
            characters = st.session_state.get('characters', [])
            
            if not outline or not characters:
                raise ValueError("请先生成小说框架")
            
            # 生成章节
            chapter = self.generator.generate_chapter(
                chapter_number=chapter_number,
                outline=outline,
                characters=characters,
                context=context,
                target_words=target_words
            )
            
            # 一致性检查
            consistency_result = {}
            if self.consistency_checker:
                consistency_result = self.consistency_checker.check_chapter_consistency(
                    chapter, 
                    {
                        'outline': outline,
                        'characters': characters,
                        'previous_summaries': self.memory._get_recent_summaries(chapter_number, 3)
                    }
                )
            
            # 更新记忆
            self.memory.update_with_chapter(chapter_number, chapter)
            
            # 保存章节文件
            if outline.get('title'):
                title_safe = "".join(c for c in outline['title'] if c.isalnum() or c in " _-")
                chapter_file = f"./outputs/novels/{title_safe}_chapter_{chapter_number}.txt"
                
                # 构建章节内容文本
                chapter_text = f"# 第{chapter_number}章: {chapter.get('title', '')}\n\n"
                chapter_text += chapter.get('content', '')
                
                write_file(chapter_file, chapter_text)
            
            return {
                "success": True,
                "chapter_number": chapter_number,
                "title": chapter.get('title', f"第{chapter_number}章"),
                "word_count": len(chapter.get('content', '')),
                "summary": chapter.get('summary', ''),
                "consistency_check": consistency_result,
                "file_saved": True,
                "generation_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {
                "success": False,
                "chapter_number": chapter_number,
                "error": str(e),
                "generation_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _save_batch_results(self, results: Dict[str, Any]):
        """保存批量生成结果"""
        try:
            import json
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            results_file = f"./outputs/logs/batch_results_{timestamp}.json"
            
            # 确保目录存在
            import os
            os.makedirs("./outputs/logs", exist_ok=True)
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 批量生成结果已保存到: {results_file}")
            
        except Exception as e:
            print(f"⚠️ 保存批量结果失败: {str(e)}")
    
    def generate_batch_with_plan(self, chapter_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        根据章节计划批量生成
        
        Args:
            chapter_plan: 章节计划列表
            
        Returns:
            生成结果
        """
        if not chapter_plan:
            return {"error": "章节计划为空"}
        
        # 提取需要生成的章节
        chapters_to_generate = [
            item['章节'] for item in chapter_plan 
            if item.get('状态') == '待生成'
        ]
        
        if not chapters_to_generate:
            return {"message": "没有需要生成的章节"}
        
        start_chapter = min(chapters_to_generate)
        chapters_count = len(chapters_to_generate)
        
        return self.generate_batch_chapters(
            start_chapter=start_chapter,
            chapters_count=chapters_count
        )
    
    async def async_generate_batch(self, chapters_info: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        异步批量生成章节（可选）
        
        Args:
            chapters_info: 章节信息列表
            
        Returns:
            生成的章节列表
        """
        async def generate_chapter_async(chapter_info: Dict[str, Any]):
            try:
                # 模拟异步生成
                await asyncio.sleep(1)  # 模拟网络延迟
                
                # 这里可以调用真正的异步生成逻辑
                return {
                    "success": True,
                    "chapter_number": chapter_info.get('number'),
                    "title": f"第{chapter_info.get('number')}章"
                }
            except Exception as e:
                return {
                    "success": False,
                    "chapter_number": chapter_info.get('number'),
                    "error": str(e)
                }
        
        # 并发执行所有章节生成任务
        tasks = [generate_chapter_async(info) for info in chapters_info]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return results

# 测试函数
if __name__ == "__main__":
    print("测试批量章节生成器...")
    
    # 创建模拟组件
    class MockGenerator:
        def generate_chapter(self, **kwargs):
            return {
                "title": f"第{kwargs.get('chapter_number')}章",
                "content": "测试内容" * 100,
                "summary": f"第{kwargs.get('chapter_number')}章摘要"
            }
    
    class MockMemory:
        def get_context(self, chapter_num):
            return "测试上下文"
        def update_with_chapter(self, chapter_num, chapter_data):
            pass
    
    generator = MockGenerator()
    memory = MockMemory()
    batch_gen = BatchChapterGenerator(generator, memory)
    
    # 测试批量生成
    try:
        results = batch_gen.generate_batch_chapters(
            start_chapter=1,
            chapters_count=3,
            words_per_chapter=1000
        )
        
        print(f"批量生成结果: {results['success_count']}成功, {results['failed_count']}失败")
        print(f"总字数: {results['total_words']}")
        print(f"总耗时: {results['total_time']:.2f}秒")
        
    except Exception as e:
        print(f"批量生成测试失败: {str(e)}")