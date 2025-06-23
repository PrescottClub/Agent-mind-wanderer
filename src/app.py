"""
心绪精灵主应用类 - 重构版
负责应用的整体流程控制和UI渲染
"""

import streamlit as st
import time
import uuid
from datetime import datetime
from typing import Optional

# 导入重构后的模块
from .data.database import init_db
from .data.repositories.chat_repository import ChatRepository
from .data.repositories.user_profile_repository import UserProfileRepository
from .services.intimacy_service import IntimacyService
from .services.chat_service import ChatService
from .core.ai_engine import AIEngine
from .core.session_manager import SessionManager
from .ui.components.api_config import render_api_config, render_compact_status
from .ui.components.main_info import render_main_info_panel
from .config.settings import settings
from .utils.helpers import (
    get_environment_context,
    check_first_visit_today,
    generate_proactive_greeting,
    parse_ai_response,
    parse_enhanced_ai_response,
    clean_markdown_text
)


class MindSpriteApp:
    """心绪精灵主应用类 - 重构版"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.chat_repo = ChatRepository()
        self.user_profile_repo = UserProfileRepository()
        self.intimacy_service = IntimacyService(self.user_profile_repo)
        self.ai_engine = None
        self.chat_service = None
        
        # 初始化聊天消息状态
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
    def initialize_ai_engine(self, api_key: str, serp_api_key: Optional[str] = None):
        """初始化AI引擎和聊天服务"""
        self.ai_engine = AIEngine(api_key, serp_api_key)
        self.chat_service = ChatService(
            ai_engine=self.ai_engine,
            chat_repo=self.chat_repo,
            intimacy_service=self.intimacy_service
        )
    
    def render_header(self):
        """渲染页面头部"""
        st.markdown("""
        <div class="main-title">心绪精灵 ✨</div>
        <div class="subtitle">你的专属情感陪伴小精灵 💖</div>
        """, unsafe_allow_html=True)
    
    def handle_proactive_greeting(self):
        """处理主动问候和关怀任务"""
        session_id = self.session_manager.session_id
        
        # 【v5.1新增】优先检查关怀任务
        if self.ai_engine:
            try:
                care_tasks = self.ai_engine.get_pending_care_tasks(session_id)
                if care_tasks and not st.session_state.get('care_task_shown', False):
                    # 显示第一个关怀任务
                    care_task = care_tasks[0]
                    
                    # 添加关怀消息到session state
                    care_message = clean_markdown_text(care_task.get('care_message', '小念想起你了~'))
                    care_response = f"💝 小念想起: {care_message}"
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": care_response
                    })
                    
                    # 保存到数据库
                    self.chat_repo.add_message(session_id, "assistant", care_response)
                    
                    # 标记关怀任务为已完成
                    task_id = care_task.get('id')
                    if task_id:
                        self.ai_engine.complete_care_task(task_id)
                    
                    # 标记已显示，避免重复
                    st.session_state.care_task_shown = True
                    return  # 显示关怀任务后就不显示普通问候了
            except Exception as e:
                print(f"关怀任务检查错误: {e}")
        
        # 检查是否需要主动问候
        if (not st.session_state.get('proactive_greeting_shown', False) and 
            check_first_visit_today(session_id)):
            
            # 生成主动问候
            greeting = generate_proactive_greeting()
            
            # 保存到session state（清理后的文本）
            cleaned_greeting = clean_markdown_text(greeting)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"💖 {cleaned_greeting}"
            })
            
            # 保存到数据库
            self.chat_repo.add_message(session_id, "assistant", cleaned_greeting)
            
            # 标记已显示
            st.session_state.proactive_greeting_shown = True
    
    def render_chat_history(self):
        """渲染聊天历史 - 使用session state优先"""
        session_id = self.session_manager.session_id
        
        # 如果session state为空，从数据库加载历史记录
        if not st.session_state.messages:
            history = self.chat_repo.get_history(session_id, limit=20)
            for role, content, timestamp in history:
                st.session_state.messages.append({
                    "role": role,
                    "content": content
                })
        
        # 渲染所有消息
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    # 检查是否是最后一条AI消息且内容为空（需要流式处理）
                    if i == len(st.session_state.messages) - 1 and not message["content"]:
                        # 这是最新的空AI消息，需要进行流式处理
                        self._handle_streaming_response(i)
                    else:
                        # 直接显示已解析的内容
                        cleaned_content = clean_markdown_text(message["content"])
                        st.markdown(cleaned_content)
                else:
                    st.markdown(message["content"])
    
    def handle_user_input(self, user_input: str):
        """处理用户输入 - 使用流式响应实现打字机效果"""
        session_id = self.session_manager.session_id

        # 添加用户消息到session state
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # 保存用户消息到数据库
        message_id = self.chat_repo.add_message(session_id, "user", user_input)
        if message_id is None:
            st.error("保存消息失败")
            return

        # 使用聊天服务处理消息（流式响应）
        if not self.chat_service:
            st.error("聊天服务未初始化")
            return

        # 添加空的AI消息占位符到session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": ""
        })

        # 重新渲染整个聊天历史以显示新消息
        st.rerun()

        # 注意：流式响应将在下次渲染时处理

    def _handle_streaming_response(self, message_index: int):
        """处理流式响应显示"""
        session_id = self.session_manager.session_id

        # 获取对应的用户消息
        if message_index > 0:
            user_message = st.session_state.messages[message_index - 1]
            user_input = user_message["content"]

            # 获取最新的消息ID（从数据库）
            recent_messages = self.chat_repo.get_recent_context(session_id, context_turns=1)
            if recent_messages:
                message_id = recent_messages[0][0]  # 获取最新消息的ID

                # 创建占位符用于流式显示
                message_placeholder = st.empty()
                full_response = ""

                try:
                    # 流式处理用户消息
                    for current_content in self.chat_service.process_user_message_stream(session_id, user_input, message_id):
                        # 实时更新显示内容（打字机效果）
                        cleaned_content = clean_markdown_text(current_content)
                        message_placeholder.markdown(cleaned_content)
                        full_response = current_content

                    # 更新session state中的消息内容
                    st.session_state.messages[message_index]["content"] = full_response

                    # 保存完整回应到数据库
                    self.chat_repo.add_message(session_id, "assistant", full_response)

                    # 处理后续逻辑（礼物、经验值等）
                    self._handle_post_response_logic(session_id, user_input, message_id, full_response)

                except Exception as e:
                    st.error(f"流式处理出错: {e}")
                    error_response = "💖 小念遇到了一些技术问题，但还是想陪伴你~ 请稍后再试试吧！"
                    st.session_state.messages[message_index]["content"] = error_response
                    self.chat_repo.add_message(session_id, "assistant", error_response)

    def _handle_post_response_logic(self, session_id: str, user_input: str, message_id: int, full_response: str):
        """处理响应后的逻辑（礼物、经验值等）"""
        try:
            # 获取完整的处理结果来处理礼物和经验值
            result = self.chat_service.process_user_message(session_id, user_input, message_id)

            if result["success"]:
                gift_info = result["gift_info"]
                exp_result = result["exp_result"]

                # 处理礼物
                if gift_info["type"]:
                    st.success(f"🎁 **{gift_info['type']}**\n\n{gift_info['content']}")

                # 处理升级效果
                if exp_result["leveled_up"]:
                    st.balloons()
                    st.toast(f"🎉 恭喜！与小念的羁绊提升到 Lv.{exp_result['new_level']} 啦！", icon="🎉")

                    # 显示升级奖励
                    if exp_result["level_rewards"]:
                        st.success("🎁 解锁新奖励：")
                        for reward in exp_result["level_rewards"]:
                            st.info(f"✨ {reward['content']}")

                # 显示经验值获得提示
                exp_gained = exp_result["exp_gained"]
                st.caption(f"💫 获得 {exp_gained} EXP！")

        except Exception as e:
            print(f"后续逻辑处理错误: {e}")
    
    def render_treasure_box(self):
        """渲染宝藏盒"""
        session_id = self.session_manager.session_id
        treasures = self.chat_repo.get_treasures(session_id, limit=6)
        
        # 如果有当前礼物，从历史中移除（避免重复显示）
        current_gift = st.session_state.get('current_gift')
        if current_gift and treasures:
            # 过滤掉可能重复的最新礼物
            filtered_treasures = []
            for treasure in treasures:
                if not (treasure[0] == current_gift['type'] and treasure[1] == current_gift['content']):
                    filtered_treasures.append(treasure)
            treasures = filtered_treasures[:5]  # 只保留5个历史礼物

        # 初始化会话状态
        if "show_treasure_modal" not in st.session_state:
            st.session_state.show_treasure_modal = False
        if "selected_treasure" not in st.session_state:
            st.session_state.selected_treasure = None

        if treasures:
            st.markdown("💝 **小念为你珍藏的美好回忆**")

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

    def run(self):
        """运行应用"""
        # 初始化数据库
        if not init_db():
            st.error("❌ 数据库初始化失败，应用可能无法正常工作")
            return

        # 渲染浮动API配置面板
        api_configured = render_api_config()

        # 检查API密钥
        if not api_configured:
            # 渲染页面头部
            self.render_header()

            # 显示API配置提示
            render_compact_status()

            st.markdown("""
            ### 欢迎来到心绪精灵！✨

            心绪精灵是一个主动型治愈Agent，具备五大核心模块：

            - 🌟 **轻量级主动性** - 主动关心问候
            - 🌍 **环境感知** - 了解时间和情境
            - 🎨 **心情调色盘** - 视觉化情感共鸣
            - 🎁 **宝藏小盒** - 收集美好回忆
            - 🤫 **秘密约定** - 特殊彩蛋惊喜

            请在右上角配置你的API密钥后即可开始与小念的温暖对话~ 💕
            """)

            # 显示主页面信息
            render_main_info_panel(self.session_manager.session_id)
            st.stop()

        # 初始化AI引擎
        api_key = st.session_state.get('deepseek_api_key', '')
        if api_key:
            self.initialize_ai_engine(api_key, settings.serp_api_key)

        # 渲染页面头部
        self.render_header()

        # 显示API状态（紧凑版）
        render_compact_status()

        # 渲染聊天历史
        self.render_chat_history()

        # 处理主动问候（在历史之后，避免重复显示）
        self.handle_proactive_greeting()

        # 【v5.0】性能优化重构版：流式响应 + 状态管理优化
        st.caption("🚀 v5.0重构版：流式响应 + 无刷新交互 + 模块化架构")

        # 处理用户输入
        if user_input := st.chat_input("和小念分享你的心情吧~ 💭"):
            self.handle_user_input(user_input)

        # 渲染宝藏盒（折叠显示历史礼物，避免与当前礼物重复）
        with st.expander("🎁 小念的宝藏盒（点击查看历史礼物）", expanded=False):
            self.render_treasure_box()

        # 渲染主页面信息面板
        render_main_info_panel(self.session_manager.session_id)
