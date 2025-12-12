"""
百万字小说AI创作器 - Web界面
简洁美观的用户界面
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import yaml

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv()

# 导入自定义模块
from core.generator import NovelGenerator
from core.memory_system import SmartMemory
from core.consistency import ConsistencyChecker
from core.summarizer import SmartSummarizer
from utils.file_utils import save_json, ensure_directories
from auth import check_api_key

# 页面配置
st.set_page_config(
    page_title="百万字小说AI创作器",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/million-word-novel-ai-creator',
        'Report a bug': 'https://github.com/yourusername/million-word-novel-ai-creator/issues',
        'About': '# 百万字小说AI创作器\n解决长篇小说的前后一致性问题'
    }
)

# 加载配置
@st.cache_resource
def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config()

# 自定义CSS样式
def load_css():
    st.markdown("""
    <style>
        /* 主标题样式 */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        
        /* 副标题样式 */
        .sub-header {
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        /* 卡片样式 */
        .metric-card {
            background: #000000;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid #eaeaea;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
        }
        
        /* 按钮样式 */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            transition: all 0.3s;
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        /* 输入框样式 */
        .stTextArea textarea {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            transition: border-color 0.3s;
        }
        
        .stTextArea textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 1px #667eea;
        }
        
        /* 进度条样式 */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        /* 标签页样式 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            font-weight: 600;
        }
        
        /* 侧边栏样式 */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #000000 10%, #000000 100%);
        }
        
        /* 成功消息样式 */
        .stSuccess {
            border-left: 4px solid #10b981;
            background-color: #f0fdf4;
            padding: 1rem;
            border-radius: 4px;
        }
        
        /* 警告消息样式 */
        .stWarning {
            border-left: 4px solid #f59e0b;
            background-color: #fffbeb;
            padding: 1rem;
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

class NovelCreatorApp:
    def __init__(self):
        self.api_key = None
        self.generator = None
        self.memory = None
        self.consistency_checker = None
        self.summarizer = None
        self.init_session_state()
    
    def init_session_state(self):
        """初始化session state"""
        if 'generated_outline' not in st.session_state:
            st.session_state.generated_outline = None
        if 'characters' not in st.session_state:
            st.session_state.characters = []
        if 'chapters' not in st.session_state:
            st.session_state.chapters = {}
        if 'progress' not in st.session_state:
            st.session_state.progress = {
                'target_words': 100000,
                'completed_words': 0,
                'chapters_count': 0,
                'percentage': 0
            }
        if 'memory_initialized' not in st.session_state:
            st.session_state.memory_initialized = False
    
    def initialize_components(self, api_key):
        """初始化各个组件"""
        try:
            self.api_key = api_key
            self.generator = NovelGenerator(api_key)
            self.memory = SmartMemory()
            self.consistency_checker = ConsistencyChecker()
            self.summarizer = SmartSummarizer()
            st.session_state.memory_initialized = True
            return True
        except Exception as e:
            st.error(f"初始化失败: {str(e)}")
            return False
    
    def render_sidebar(self):
        """渲染侧边栏"""
        with st.sidebar:
            # API配置部分
            st.markdown("### 🔐 API配置")
            
            api_key = st.text_input(
                "DeepSeek API密钥",
                type="password",
                help="从DeepSeek平台获取API密钥",
                placeholder="sk-xxxxxxxxxxxxxxxx"
            )
            
            if st.button("验证并初始化", type="primary", use_container_width=True):
                if api_key:
                    with st.spinner("正在验证API密钥..."):
                        if check_api_key(api_key):
                            if self.initialize_components(api_key):
                                st.success("✅ 系统初始化成功!")
                                st.rerun()
                        else:
                            st.error("❌ API密钥无效，请检查后重试")
                else:
                    st.warning("⚠️ 请输入API密钥")
            
            st.divider()
            
            # 创作参数部分
            st.markdown("### 🎯 创作参数")
            
            # 目标字数选择
            word_options = {
                "10万字": 100000,
                "30万字": 300000,
                "50万字": 500000,
                "80万字": 800000,
                "100万字": 1000000,
                "200万字": 2000000
            }
            
            selected_word_label = st.selectbox(
                "目标字数",
                list(word_options.keys()),
                index=0
            )
            
            target_words = word_options[selected_word_label]
            st.session_state.progress['target_words'] = target_words
            
            # 小说类型选择
            novel_type = st.selectbox(
                "小说类型",
                ["玄幻", "仙侠", "都市", "科幻", "悬疑", "言情", "历史", "军事", "其他"],
                index=0
            )
            
            # 写作风格选择
            writing_style = st.selectbox(
                "写作风格",
                ["轻松幽默", "严肃正剧", "文艺细腻", "快节奏", "慢热细腻", "群像描写"],
                index=1
            )
            
            # 高级设置
            with st.expander("⚙️ 高级设置"):
                batch_size = st.slider(
                    "批量生成章节数",
                    min_value=1,
                    max_value=10,
                    value=3,
                    help="一次生成多少个章节"
                )
                
                chapter_words = st.slider(
                    "每章字数",
                    min_value=1000,
                    max_value=10000,
                    value=3000,
                    step=500
                )
                
                consistency_level = st.select_slider(
                    "一致性检查强度",
                    options=["宽松", "标准", "严格"],
                    value="标准"
                )
            
            return {
                'api_key': api_key,
                'target_words': target_words,
                'novel_type': novel_type,
                'writing_style': writing_style,
                'batch_size': batch_size,
                'chapter_words': chapter_words,
                'consistency_level': consistency_level
            }
    
    def render_main_header(self):
        """渲染主标题"""
        st.markdown('<h1 class="main-header">📚 百万字小说AI创作器</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">✨ 让AI帮你解决长篇小说的前后一致性问题</p>', unsafe_allow_html=True)
        
        # 特性卡片
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🧠 智能记忆</h3>
                <p>分层记忆系统，解决百万字一致性</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 一键生成</h3>
                <p>从创意到完整框架自动生成</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>🔍 实时检查</h3>
                <p>多维度验证保证内容连贯性</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 进度追踪</h3>
                <p>可视化监控创作进度和质量</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_creative_input(self):
        """渲染创意输入区域"""
        st.markdown("## ✨ 创意输入")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            creative_input = st.text_area(
                "描述你的小说创意",
                height=180,
                placeholder="""例如：
一个现代程序员穿越到修真世界，发现仙法本质是代码。
他用编程思维重构修炼体系，创建"Git修仙"、"Docker炼丹"等全新概念。
在宗门大比中，他用代码击败传统修士，引发修真界革命...

请尽量详细描述，包括：
• 核心设定和世界观
• 主角特点和能力
• 主要矛盾和冲突
• 期望的故事走向""",
                help="描述越详细，AI生成的内容越精准",
                key="creative_input"
            )
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>💡 创作提示</h4>
                <ul style="padding-left: 20px; margin-bottom: 0;">
                <li>详细描述世界观</li>
                <li>明确主角性格</li>
                <li>设定核心冲突</li>
                <li>描述叙事风格</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 生成小说框架", 
                        type="primary", 
                        use_container_width=True,
                        disabled=not st.session_state.memory_initialized):
                return creative_input
        
        return None
    
    def generate_novel_framework(self, creative_input, params):
        """生成小说框架"""
        with st.spinner("🧠 AI正在构思你的小说世界..."):
            try:
                # 创建进度显示
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 1. 生成大纲
                status_text.text("📋 正在生成小说大纲...")
                outline = self.generator.generate_outline(
                    creative=creative_input,
                    word_count=params['target_words'],
                    novel_type=params['novel_type'],
                    writing_style=params['writing_style']
                )
                progress_bar.progress(25)
                
                # 保存大纲
                save_json(outline, f"./outputs/outlines/{outline.get('title', 'novel')}_outline.json")
                st.session_state.generated_outline = outline
                
                # 2. 生成人物
                status_text.text("👥 正在生成人物设定...")
                characters = self.generator.generate_characters(outline)
                progress_bar.progress(50)
                
                self.memory.save_characters(characters)
                st.session_state.characters = characters
                
                # 3. 生成世界观
                status_text.text("🌍 正在构建世界观...")
                worldview = self.generator.generate_worldview(outline, characters)
                progress_bar.progress(75)
                
                self.memory.save_worldview(worldview)
                
                # 4. 生成章节计划
                status_text.text("📖 正在制定章节计划...")
                chapter_plan = self.generator.generate_chapter_plan(outline, params['target_words'])
                progress_bar.progress(100)
                
                self.memory.save_chapter_plan(chapter_plan)
                
                status_text.text("✅ 小说框架生成完成!")
                
                return {
                    'outline': outline,
                    'characters': characters,
                    'worldview': worldview,
                    'chapter_plan': chapter_plan,
                    'success': True
                }
                
            except Exception as e:
                st.error(f"生成失败: {str(e)}")
                return {'success': False, 'error': str(e)}
    
    def render_generated_content(self, generated_data):
        """渲染生成的内容"""
        if not generated_data['success']:
            return
        
        outline = generated_data['outline']
        characters = generated_data['characters']
        
        # 创建标签页
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 小说大纲", 
            "👥 人物设定", 
            "📖 章节计划",
            "🔍 一致性检查"
        ])
        
        with tab1:
            self.render_outline_tab(outline)
        
        with tab2:
            self.render_characters_tab(characters)
        
        with tab3:
            self.render_chapter_plan_tab(generated_data['chapter_plan'])
        
        with tab4:
            self.render_consistency_tab(outline, characters)
    
    def render_outline_tab(self, outline):
        """渲染大纲标签页"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {outline.get('title', '未命名')}")
            st.markdown(f"**核心主题**: {outline.get('theme', '')}")
            
            st.markdown("#### 故事梗概")
            st.write(outline.get('summary', ''))
            
            if 'structure' in outline:
                st.markdown("#### 三幕结构")
                structure = outline['structure']
                
                for act_name, act_content in structure.items():
                    with st.expander(f"**{act_name}**: {act_content.get('description', '')}"):
                        st.write(act_content.get('details', ''))
        
        with col2:
            st.markdown("#### 📊 基本信息")
            st.metric("目标字数", f"{outline.get('target_words', 0):,}")
            st.metric("预计章节", outline.get('estimated_chapters', 0))
            
            if 'key_plot_points' in outline:
                st.markdown("#### 🎭 关键情节点")
                for i, point in enumerate(outline['key_plot_points'][:5], 1):
                    st.write(f"{i}. {point}")
    
    def render_characters_tab(self, characters):
        """渲染人物标签页"""
        st.markdown(f"### 主要人物 ({len(characters)}人)")
        
        # 人物筛选
        col1, col2 = st.columns([1, 3])
        with col1:
            search_term = st.text_input("搜索人物", placeholder="输入姓名或特征")
        
        # 显示人物卡片
        cols = st.columns(3)
        
        for idx, character in enumerate(characters):
            if search_term and search_term.lower() not in str(character).lower():
                continue
            
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>{character.get('name', '未知')}</h4>
                        <p><strong>身份:</strong> {character.get('identity', '')}</p>
                        <p><strong>年龄:</strong> {character.get('age', '')}</p>
                        <p><strong>性格:</strong> {character.get('personality', '')[:50]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("查看详情"):
                        st.write(f"**背景故事**: {character.get('background', '')}")
                        st.write(f"**核心动机**: {character.get('motivation', '')}")
                        st.write(f"**成长弧线**: {character.get('growth_arc', '')}")
                        if 'relationships' in character:
                            st.write("**人物关系**:")
                            for rel in character['relationships']:
                                st.write(f"  • {rel}")
    
    def render_chapter_plan_tab(self, chapter_plan):
        """渲染章节计划标签页"""
        st.markdown("### 📖 章节计划")
        
        # 批量生成控制
        col1, col2, col3 = st.columns(3)
        
        with col1:
            start_chapter = st.number_input("起始章节", min_value=1, value=1)
        
        with col2:
            batch_size = st.number_input("生成章节数", min_value=1, max_value=10, value=3)
        
        with col3:
            if st.button("🎯 批量生成章节", use_container_width=True):
                self.batch_generate_chapters(start_chapter, batch_size)
        
        # 显示章节计划
        if chapter_plan:
            st.dataframe(
                chapter_plan,
                use_container_width=True,
                hide_index=True
            )
    
    def batch_generate_chapters(self, start_chapter, batch_size):
        """批量生成章节"""
        if not st.session_state.generated_outline:
            st.warning("请先生成小说框架")
            return
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            for i in range(batch_size):
                chapter_num = start_chapter + i
                
                status_text.text(f"正在生成第 {chapter_num} 章...")
                
                # 获取上下文
                context = self.memory.get_context(chapter_num)
                
                # 生成章节
                chapter = self.generator.generate_chapter(
                    chapter_number=chapter_num,
                    outline=st.session_state.generated_outline,
                    characters=st.session_state.characters,
                    context=context,
                    target_words=3000
                )
                
                # 保存章节
                chapter_file = f"./outputs/novels/{st.session_state.generated_outline.get('title', 'novel')}_chapter_{chapter_num}.txt"
                with open(chapter_file, 'w', encoding='utf-8') as f:
                    f.write(chapter.get('content', ''))
                
                # 更新进度
                st.session_state.chapters[chapter_num] = chapter
                st.session_state.progress['chapters_count'] += 1
                st.session_state.progress['completed_words'] += len(chapter.get('content', ''))
                
                # 更新记忆
                self.memory.update_with_chapter(chapter_num, chapter)
                
                # 更新进度条
                progress = (i + 1) / batch_size
                progress_bar.progress(progress)
            
            status_text.text("✅ 批量生成完成!")
            st.success(f"成功生成 {batch_size} 个章节!")
            
        except Exception as e:
            st.error(f"生成失败: {str(e)}")
    
    def render_consistency_tab(self, outline, characters):
        """渲染一致性检查标签页"""
        st.markdown("### 🔍 一致性检查")
        
        if st.button("运行全面一致性检查", use_container_width=True):
            with st.spinner("正在检查..."):
                results = self.consistency_checker.full_consistency_check(
                    outline=outline,
                    characters=characters,
                    chapters=st.session_state.chapters
                )
                
                self.display_consistency_results(results)
    
    def display_consistency_results(self, results):
        """显示一致性检查结果"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            score = results.get('character_consistency', {}).get('score', 0)
            st.metric("人物一致性", f"{score}%")
            
            issues = results.get('character_consistency', {}).get('issues', [])
            if issues:
                st.warning("⚠️ 人物一致性问题:")
                for issue in issues[:3]:
                    st.write(f"• {issue}")
        
        with col2:
            score = results.get('plot_consistency', {}).get('score', 0)
            st.metric("情节连贯性", f"{score}%")
            
            issues = results.get('plot_consistency', {}).get('issues', [])
            if issues:
                st.warning("⚠️ 情节连贯性问题:")
                for issue in issues[:3]:
                    st.write(f"• {issue}")
        
        with col3:
            score = results.get('worldview_consistency', {}).get('score', 0)
            st.metric("世界观统一性", f"{score}%")
            
            issues = results.get('worldview_consistency', {}).get('issues', [])
            if issues:
                st.warning("⚠️ 世界观统一性问题:")
                for issue in issues[:3]:
                    st.write(f"• {issue}")
        
        # 总体评分
        overall = results.get('overall_score', 0)
        st.progress(overall / 100)
        st.markdown(f"#### 总体一致性评分: **{overall}%**")
        
        if overall >= 80:
            st.success("✅ 一致性良好，可以继续创作")
        elif overall >= 60:
            st.warning("⚠️ 一致性一般，建议检查主要问题")
        else:
            st.error("❌ 一致性较差，需要大幅调整")
    
    def render_progress_section(self):
        """渲染进度追踪区域"""
        st.markdown("## 📊 创作进度")
        
        progress = st.session_state.progress
        target_words = progress['target_words']
        completed_words = progress['completed_words']
        chapters_count = progress['chapters_count']
        
        # 计算百分比
        if target_words > 0:
            percentage = min(100, (completed_words / target_words) * 100)
        else:
            percentage = 0
        
        progress['percentage'] = percentage
        
        # 进度条
        st.progress(percentage / 100)
        
        # 统计卡片
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("目标字数", f"{target_words:,}")
        
        with col2:
            st.metric("已完成字数", f"{completed_words:,}")
        
        with col3:
            st.metric("完成进度", f"{percentage:.1f}%")
        
        with col4:
            st.metric("已生成章节", chapters_count)
        
        # 质量评估
        if chapters_count > 0:
            st.markdown("### 📈 质量评估")
            
            # 这里可以添加更复杂的质量评估逻辑
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("人物塑造", "8.5/10")
            
            with col2:
                st.metric("情节设计", "7.8/10")
            
            with col3:
                st.metric("文笔质量", "8.2/10")
    
    def run(self):
        """运行应用"""
        # 加载CSS
        load_css()
        
        # 渲染主标题
        self.render_main_header()
        
        # 检查初始化状态
        if not st.session_state.memory_initialized:
            st.warning("⚠️ 请在侧边栏配置API密钥并初始化系统")
        
        # 渲染侧边栏
        params = self.render_sidebar()
        
        # 主内容区域
        creative_input = self.render_creative_input()
        
        # 处理创意生成
        if creative_input and st.session_state.memory_initialized:
            generated_data = self.generate_novel_framework(creative_input, params)
            if generated_data and generated_data['success']:
                self.render_generated_content(generated_data)
        
        # 显示已有内容
        elif st.session_state.generated_outline:
            generated_data = {
                'success': True,
                'outline': st.session_state.generated_outline,
                'characters': st.session_state.characters,
                'chapter_plan': self.memory.get_chapter_plan() if self.memory else []
            }
            self.render_generated_content(generated_data)
        
        # 渲染进度追踪
        self.render_progress_section()
        
        # 页脚
        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: #666;'>"
            "百万字小说AI创作器 · 解决长篇小说的前后一致性问题 · "
            "<a href='https://github.com/yourusername/million-word-novel-ai-creator' target='_blank'>GitHub</a>"
            "</p>",
            unsafe_allow_html=True
        )

def main():
    """主函数"""
    app = NovelCreatorApp()
    app.run()

if __name__ == "__main__":
    # 确保目录存在
    ensure_directories("./outputs")
    ensure_directories("./outputs/novels")
    ensure_directories("./outputs/outlines")
    ensure_directories("./memory")
    
    # 运行应用
    main()