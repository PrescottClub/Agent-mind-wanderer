"""
心绪精灵 (Mind Sprite) - 重构版主入口
主动型治愈Agent"心绪精灵" - 模块化架构版本

作者: Claude (Augment Agent)
技术栈: Python, LangChain, Streamlit, DeepSeek API, SQLite
版本: 4.0 - 模块化重构版
"""

import streamlit as st
import time
import uuid
from datetime import datetime

# 导入重构后的模块
from src.data.database import init_db
from src.data.repositories.chat_repository import ChatRepository
from src.data.repositories.user_profile_repository import UserProfileRepository
from src.services.intimacy_service import IntimacyService
from src.core.ai_engine import AIEngine
from src.core.session_manager import SessionManager
from src.ui.components.sidebar import render_sidebar
from src.utils.helpers import (
    get_environment_context,
    check_first_visit_today,
    generate_proactive_greeting,
    parse_ai_response,
    extract_gift_from_response
)

# ==================== 页面配置 ====================

st.set_page_config(
    page_title="心绪精灵 ✨",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用甜美马卡龙CSS样式
from src.ui.styles.custom_css import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==================== 主应用类 ====================

class MindSpriteApp:
    """心绪精灵主应用类"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.chat_repo = ChatRepository()
        self.user_profile_repo = UserProfileRepository()
        self.intimacy_service = IntimacyService(self.user_profile_repo)
        self.ai_engine = None
        
    def initialize_ai_engine(self, api_key: str):
        """初始化AI引擎"""
        self.ai_engine = AIEngine(api_key)
    
    def render_header(self):
        """渲染页面头部"""
        st.markdown("""
        <div class="main-title">心绪精灵 ✨</div>
        <div class="subtitle">你的专属情感陪伴小精灵 💖</div>
        """, unsafe_allow_html=True)
    
    def handle_proactive_greeting(self):
        """处理主动问候"""
        session_id = self.session_manager.session_id
        
        # 检查是否需要主动问候
        if (not st.session_state.get('proactive_greeting_shown', False) and 
            check_first_visit_today(session_id)):
            
            # 生成主动问候
            greeting = generate_proactive_greeting()
            
            # 保存到数据库
            self.chat_repo.add_message(session_id, "assistant", greeting)
            
            # 显示主动问候
            with st.chat_message("assistant"):
                st.markdown(f"💖 {greeting}")
            
            # 标记已显示
            st.session_state.proactive_greeting_shown = True
    
    def render_chat_history(self):
        """渲染聊天历史"""
        session_id = self.session_manager.session_id
        history = self.chat_repo.get_history(session_id, limit=20)
        
        for role, content, timestamp in history:
            with st.chat_message(role):
                if role == "assistant":
                    # 解析AI回应
                    parsed = parse_ai_response(content)
                    
                    # 显示思考过程
                    if parsed["has_thinking"]:
                        with st.expander("🧠 小念的思考过程", expanded=False):
                            for step in parsed["thinking_steps"]:
                                st.write(step)
                    
                    # 显示最终回应
                    st.markdown(f"💖 {parsed['final_response']}")
                else:
                    st.markdown(content)
    
    def handle_user_input(self, user_input: str):
        """处理用户输入"""
        session_id = self.session_manager.session_id

        # 保存用户消息
        self.chat_repo.add_message(session_id, "user", user_input)

        # 获取上下文信息
        env_context = get_environment_context()
        core_memories = self.chat_repo.get_core_memories(session_id, limit=5)
        recent_context = self.chat_repo.get_recent_context(session_id, context_turns=4)

        # 【v5.0新增】获取亲密度上下文
        intimacy_context = self.intimacy_service.get_intimacy_context_for_ai(session_id)

        # 获取AI回应
        with st.spinner("小念正在思考中..."):
            ai_response = self.ai_engine.get_response(
                user_input, recent_context, core_memories, env_context, intimacy_context
            )

        # 保存AI回应
        self.chat_repo.add_message(session_id, "assistant", ai_response)

        # 提取并处理礼物
        gift_info = extract_gift_from_response(ai_response)
        if gift_info["type"]:
            st.session_state.current_gift = gift_info
            self.chat_repo.add_treasure(
                session_id, gift_info["type"], gift_info["content"]
            )

        # 【v5.0新增】添加经验值和处理升级
        exp_result = self.intimacy_service.add_exp(session_id, exp_to_add=10)

        # 检查是否升级
        if exp_result["leveled_up"]:
            # 升级庆祝效果
            st.balloons()

            # 升级提示
            new_level = exp_result["new_level"]
            st.toast(f"🎉 恭喜！与小念的羁绊提升到 Lv.{new_level} 啦！", icon="🎉")

            # 显示升级奖励
            if exp_result["level_rewards"]:
                st.success("🎁 解锁新奖励：")
                for reward in exp_result["level_rewards"]:
                    st.info(f"✨ {reward['content']}")

        # 显示经验值获得提示（小字提示）
        exp_gained = exp_result["exp_gained"]
        st.caption(f"💫 获得 {exp_gained} EXP！")

        # 刷新页面以显示新消息
        st.rerun()
    
    def render_treasure_box(self):
        """渲染宝藏盒"""
        session_id = self.session_manager.session_id
        treasures = self.chat_repo.get_treasures(session_id, limit=5)

        # 初始化会话状态
        if "show_treasure_modal" not in st.session_state:
            st.session_state.show_treasure_modal = False
        if "selected_treasure" not in st.session_state:
            st.session_state.selected_treasure = None

        if treasures:
            st.markdown('<h3 class="treasure-box-title">🎁 小念的宝藏盒</h3>', unsafe_allow_html=True)

            cols = st.columns(min(len(treasures), 3))
            for i, (gift_type, gift_content, collected_at, is_favorite) in enumerate(treasures):
                with cols[i % 3]:
                    favorite_icon = "⭐" if is_favorite else ""

                    # 渲染宝藏卡片（使用新的CSS类）
                    st.markdown(f"""
                    <div class="treasure-card">
                        <h4>{favorite_icon} {gift_type}</h4>
                        <p>{gift_content}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # 添加"查看详情"按钮
                    if st.button("✨ 查看详情", key=f"view_treasure_{i}", help="点击查看宝藏详细信息"):
                        # 设置选中的宝藏数据
                        st.session_state.selected_treasure = {
                            "gift_type": gift_type,
                            "gift_content": gift_content,
                            "collected_at": collected_at,
                            "is_favorite": is_favorite
                        }
                        st.session_state.show_treasure_modal = True
                        st.rerun()

        # 条件渲染宝藏详情（使用expander代替modal）
        if st.session_state.show_treasure_modal and st.session_state.selected_treasure:
            treasure = st.session_state.selected_treasure

            # 使用expander作为模态框的替代方案
            with st.expander("🎁 宝藏详情", expanded=True):
                # 模态框内容
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <h2 style="color: var(--primary); margin-bottom: 1rem;">
                        {'⭐' if treasure['is_favorite'] else '💎'} {treasure['gift_type']}
                    </h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background: var(--bg-card);
                           border-radius: 15px;
                           padding: 1.5rem;
                           margin: 1rem 0;
                           border: 2px solid var(--border);">
                    <h4 style="color: var(--primary); margin-bottom: 0.8rem;">💝 宝藏内容</h4>
                    <p style="font-size: 1.1rem; line-height: 1.6; color: var(--text);">
                        {treasure['gift_content']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background: var(--accent);
                           border-radius: 15px;
                           padding: 1rem;
                           margin: 1rem 0;
                           text-align: center;">
                    <h4 style="color: var(--text); margin-bottom: 0.5rem;">⏰ 收集时间</h4>
                    <p style="color: var(--text); font-size: 0.95rem;">
                        {treasure['collected_at']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # 关闭按钮
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("💖 关闭", key="close_treasure_modal", use_container_width=True):
                        st.session_state.show_treasure_modal = False
                        st.session_state.selected_treasure = None
                        st.rerun()
    
    def run(self):
        """运行应用"""
        # 初始化数据库
        if not init_db():
            st.error("❌ 数据库初始化失败，应用可能无法正常工作")
            return
        
        # 渲染侧边栏并获取API密钥
        api_key = render_sidebar()
        
        # 检查API密钥
        if not api_key:
            st.info("👈 请在左侧侧边栏输入你的DeepSeek API Key以开始聊天。")
            st.markdown("""
            ### 欢迎来到心绪精灵！✨
            
            心绪精灵是一个主动型治愈Agent，具备五大核心模块：
            
            - 🌟 **轻量级主动性** - 主动关心问候
            - 🌍 **环境感知** - 了解时间和情境
            - 🎨 **心情调色盘** - 视觉化情感共鸣
            - 🎁 **宝藏小盒** - 收集美好回忆
            - 🤫 **秘密约定** - 特殊彩蛋惊喜
            
            配置你的API密钥后即可开始与小念的温暖对话~ 💕
            """)
            st.stop()
        
        # 初始化AI引擎
        self.initialize_ai_engine(api_key)
        
        # 渲染页面头部
        self.render_header()
        
        # 处理主动问候
        self.handle_proactive_greeting()
        
        # 渲染聊天历史
        self.render_chat_history()
        
        # 处理用户输入
        if user_input := st.chat_input("和小念分享你的心情吧~ 💭"):
            self.handle_user_input(user_input)
        
        # 渲染宝藏盒
        self.render_treasure_box()


def main():
    """主函数"""
    app = MindSpriteApp()
    app.run()


if __name__ == "__main__":
    main()
