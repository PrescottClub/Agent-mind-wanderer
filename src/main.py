"""
心绪精灵主入口
使用重构后的模块化架构
"""

import streamlit as st
import random
import time

from config.constants import BUTTON_MESSAGES, LOADING_MESSAGES, QUICK_MOODS
from config.settings import settings
from ui.styles.custom_css import CUSTOM_CSS
from ui.components.sprite_display import SpriteDisplay
from ui.components.gift_display import GiftDisplay
from core.ai_engine import AIEngine
from models.emotion import EmotionResult, MoodRecord


class MindSpriteApp:
    """心绪精灵应用主类"""

    def __init__(self):
        self.ai_engine = None
        self._setup_page()
        self._initialize_session_state()
        self._initialize_ai_engine()

    def _setup_page(self):
        """设置页面配置"""
        st.set_page_config(
            page_title="心绪精灵 ✨",
            page_icon="🧚‍♀️",
            layout="wide"
        )
        # 应用自定义CSS
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    def _initialize_session_state(self):
        """初始化session state"""
        if 'mood_history' not in st.session_state:
            st.session_state.mood_history = []

        if 'current_mood' not in st.session_state:
            st.session_state.current_mood = "平静"

        if 'current_reaction' not in st.session_state:
            st.session_state.current_reaction = ""

        if 'current_gift' not in st.session_state:
            st.session_state.current_gift = {"type": "", "content": ""}

    def _initialize_ai_engine(self):
        """初始化AI引擎"""
        try:
            self.ai_engine = AIEngine()
        except Exception as e:
            st.error(f"❌ AI模型初始化失败: {e}")
            self.ai_engine = None

    def render_header(self):
        """渲染页面头部"""
        st.markdown("""
        <div class="main-title">心绪精灵 ✨</div>
        <div class="subtitle">让可爱的小念陪伴你的每一种心情</div>
        """, unsafe_allow_html=True)

    def render_history_gallery(self):
        """渲染心绪回响画廊"""
        if 'mood_history' in st.session_state and st.session_state.mood_history:
            st.markdown("""
            <div class="history-gallery">
                <h3>💖 心绪回响画廊</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for record in reversed(st.session_state.mood_history):
                timestamp = record.get('timestamp', '刚刚')
                user_input = record.get('user_input', '')
                mood = record.get('mood', '平静')
                sprite_reaction = record.get('sprite_reaction', '')
                gift_type = record.get('gift_type', '')
                gift_content = record.get('gift_content', '')
                
                from config.constants import SPRITE_EMOTIONS
                sprite_emoji = SPRITE_EMOTIONS.get(mood, "( ´ ▽ ` )")
                
                st.markdown(f"""
                <div class="history-card">
                    <div class="timestamp">{timestamp}</div>
                    <p><strong>💭 我说:</strong> {user_input}</p>
                    <p><strong>{sprite_emoji} 小念回应:</strong> {sprite_reaction}</p>
                    <p><strong>🎁 收到礼物:</strong> {gift_type}</p>
                    <p style="background: rgba(240,255,240,0.3); padding: 0.5rem; border-radius: 10px; margin-top: 0.5rem;">
                        {gift_content}
                    </p>
                </div>
                """, unsafe_allow_html=True)

    def process_user_input(self, user_input: str):
        """处理用户输入并更新状态"""
        if not self.ai_engine:
            st.error("AI引擎未初始化")
            return

        # 分析用户情绪
        emotion_result = self.ai_engine.analyze_emotion(user_input)

        # 更新session state
        st.session_state.current_mood = emotion_result.mood_category
        st.session_state.current_reaction = emotion_result.sprite_reaction
        st.session_state.current_gift = {
            "type": emotion_result.gift_type,
            "content": emotion_result.gift_content
        }

        # 添加到历史记录
        record = MoodRecord.create(user_input, emotion_result)
        st.session_state.mood_history.append(record.to_dict())

    def render_chat_interface(self):
        """渲染聊天界面"""
        st.markdown("### 💬 和小念聊天")
        
        # 聊天输入区域
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "💭 和小念分享你的心情吧~",
                placeholder="告诉小念你现在的感受、今天发生的事情，或者任何想说的话... (◕‿◕)♡",
                height=100,
                help="小念会仔细倾听你的每一句话，并送给你专属的心灵礼物哦~ ✨"
            )

            # 随机选择按钮文案和加载消息
            button_text = random.choice(BUTTON_MESSAGES)
            loading_message = random.choice(LOADING_MESSAGES)

            # 提交按钮
            submitted = st.form_submit_button(button_text, type="primary", use_container_width=True)

        if submitted and user_input.strip():
            # 显示加载状态
            with st.spinner(loading_message):
                self.process_user_input(user_input)
                st.rerun()
        elif submitted and not user_input.strip():
            st.warning("记得要告诉小念一些什么哦~ 哪怕只是一个字也好 (◕‿◕)✨")

    def render_quick_mood_buttons(self):
        """渲染快捷心情按钮"""
        st.markdown("##### 🎭 快速表达心情")
        col_a, col_b, col_c = st.columns(3)

        for i, (mood_text, mood_input) in enumerate(QUICK_MOODS):
            col = [col_a, col_b, col_c][i % 3]
            with col:
                if st.button(mood_text, key=f"quick_mood_{i}", type="secondary", use_container_width=True):
                    # 直接处理快捷心情
                    with st.spinner(random.choice(LOADING_MESSAGES)):
                        self.process_user_input(mood_input)
                        st.rerun()

    def render_footer(self):
        """渲染页面底部"""
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #C2185B; font-size: 0.9rem; font-weight: 500; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);">
            愿每一天都有小念陪伴你 ✨
        </div>
        """, unsafe_allow_html=True)

    def run(self):
        """运行应用"""
        # 渲染页面头部
        self.render_header()
        
        # 主要布局
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🧚‍♀️ 小念的家")
            SpriteDisplay.render(st.session_state.current_mood, st.session_state.current_reaction)
        
        with col2:
            self.render_chat_interface()
            self.render_quick_mood_buttons()
            
            # 显示礼物
            if st.session_state.current_gift["type"]:
                GiftDisplay.render(
                    st.session_state.current_gift["type"],
                    st.session_state.current_gift["content"]
                )
        
        # 心绪回响画廊
        self.render_history_gallery()
        
        # 页面底部
        self.render_footer()


def main():
    """主函数"""
    app = MindSpriteApp()
    app.run()


if __name__ == "__main__":
    main() 