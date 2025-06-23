"""
主页面信息组件
整合原来侧边栏的功能到主页面
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.repositories.user_profile_repository import UserProfileRepository
from src.services.intimacy_service import IntimacyService


def render_user_profile(session_id: str):
    """渲染用户档案信息"""
    user_profile_repo = UserProfileRepository()
    intimacy_service = IntimacyService(user_profile_repo)
    
    # 获取用户档案
    profile = user_profile_repo.get_profile(session_id)
    if not profile:
        profile = user_profile_repo.find_or_create_profile(session_id)
    
    # 用三列布局显示信息
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FFE4E1 0%, #FFF0F5 100%);
            border: 2px solid rgba(255, 122, 158, 0.3);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 122, 158, 0.1);
        ">
            <h4 style="color: #FF7A9E; margin: 0 0 10px 0;">💖 羁绊等级</h4>
            <div style="font-size: 2rem; font-weight: bold; color: #FF69B4;">
                {level}
            </div>
            <div style="color: #666; font-size: 0.9rem;">
                {level_name}
            </div>
        </div>
        """.format(
            level=profile['intimacy_level'],
            level_name=intimacy_service._get_level_title(profile['intimacy_level'])
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #F0F8FF 0%, #E6F3FF 100%);
            border: 2px solid rgba(176, 196, 222, 0.4);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(176, 196, 222, 0.1);
        ">
            <h4 style="color: #4682B4; margin: 0 0 10px 0;">💬 互动次数</h4>
            <div style="font-size: 2rem; font-weight: bold; color: #4169E1;">
                {interactions}
            </div>
            <div style="color: #666; font-size: 0.9rem;">
                总对话数
            </div>
        </div>
        """.format(interactions=profile['total_interactions']), unsafe_allow_html=True)
    
    with col3:
        if profile.get('nickname'):
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #F0E6FF 0%, #E6F3FF 100%);
                border: 2px solid rgba(147, 112, 219, 0.4);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(147, 112, 219, 0.1);
            ">
                <h4 style="color: #9370DB; margin: 0 0 10px 0;">🏷️ 昵称</h4>
                <div style="font-size: 1.2rem; font-weight: bold; color: #8A2BE2;">
                    {nickname}
                </div>
                <div style="color: #666; font-size: 0.9rem;">
                    小念这样称呼你
                </div>
            </div>
            """.format(nickname=profile['nickname']), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #FFF8DC 0%, #FFFACD 100%);
                border: 2px solid rgba(255, 215, 0, 0.4);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.1);
            ">
                <h4 style="color: #DAA520; margin: 0 0 10px 0;">✨ 新朋友</h4>
                <div style="font-size: 1rem; color: #B8860B;">
                    还没有昵称
                </div>
                <div style="color: #666; font-size: 0.9rem;">
                    继续聊天解锁
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_quick_actions():
    """渲染快捷操作"""
    st.markdown("### 🚀 快捷操作")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎭 情绪分析", use_container_width=True):
            st.session_state.show_emotion_analysis = True
    
    with col2:
        if st.button("🔍 搜索资源", use_container_width=True):
            st.session_state.show_search = True
    
    with col3:
        if st.button("📊 数据统计", use_container_width=True):
            st.session_state.show_stats = True
    
    with col4:
        if st.button("🔄 新会话", use_container_width=True):
            if 'session_id' in st.session_state:
                del st.session_state.session_id
            st.rerun()


def render_app_features():
    """渲染应用功能说明"""
    with st.expander("📱 应用功能介绍", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🎨 核心功能**
            - 💬 智能对话陪伴
            - 🎭 深度情感理解
            - 💖 羁绊等级系统
            - 🎁 专属礼物生成
            - 📝 记忆联想机制
            """)
        
        with col2:
            st.markdown("""
            **🌟 增强功能**
            - 🆘 情绪急救包
            - 🔍 心理健康资源搜索
            - 📊 情绪趋势分析
            - ⏰ 主动关怀提醒
            - 🎪 精灵状态展示
            """)


def render_session_info(session_id: str):
    """渲染会话信息"""
    with st.expander("📋 会话信息", expanded=False):
        st.markdown(f"""
        **当前会话ID**: `{session_id[:8]}...`  
        **会话状态**: 🟢 活跃中  
        **创建时间**: {st.session_state.get('session_start_time', '未知')}
        """)
        
        if st.button("🗑️ 清空聊天记录", type="secondary"):
            # 这里可以添加清空逻辑
            st.warning("此功能将在后续版本中实现")


def render_main_info_panel(session_id: str):
    """渲染主页面信息面板"""
    st.markdown("---")
    
    # 用户档案
    render_user_profile(session_id)
    
    st.markdown("---")
    
    # 快捷操作
    render_quick_actions()
    
    st.markdown("---")
    
    # 应用功能介绍和会话信息
    col1, col2 = st.columns(2)
    
    with col1:
        render_app_features()
    
    with col2:
        render_session_info(session_id) 