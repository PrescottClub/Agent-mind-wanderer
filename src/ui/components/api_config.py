"""
API配置组件 - 浮动面板版
用小的浮动面板替代复杂的侧边栏
"""

import streamlit as st


def render_api_config():
    """渲染API配置浮动面板"""
    # 检查API密钥状态
    api_configured = bool(st.session_state.get('deepseek_api_key'))
    
    # 浮动配置面板样式
    st.markdown("""
    <style>
    .api-float-panel {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 248, 240, 0.9) 100%);
        border: 2px solid rgba(255, 122, 158, 0.3);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 10px 30px rgba(255, 122, 158, 0.2);
        backdrop-filter: blur(15px);
        z-index: 900;
        min-width: 280px;
        max-width: 320px;
    }
    
    .api-status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 10px;
    }
    
    .api-status-success {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.2) 100%);
        border: 1px solid #22c55e;
        color: #15803d;
    }
    
    .api-status-warning {
        background: linear-gradient(135deg, rgba(245, 101, 101, 0.1) 0%, rgba(245, 101, 101, 0.2) 100%);
        border: 1px solid #f56565;
        color: #c53030;
    }
    
    .api-input-compact {
        margin: 10px 0;
    }
    
    .api-input-compact input {
        font-size: 0.85rem !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
    }
    
    .help-link {
        color: #FF7A9E;
        text-decoration: none;
        font-size: 0.8rem;
        opacity: 0.8;
        transition: opacity 0.3s ease;
    }
    
    .help-link:hover {
        opacity: 1;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 浮动面板容器
    with st.container():
        if api_configured:
            st.markdown("""
            <div class="api-float-panel">
                <div class="api-status-badge api-status-success">
                    ✅ API已配置
                </div>
                <div style="font-size: 0.8rem; color: #666;">
                    小念已准备好为你服务~ 💖
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="api-float-panel">
                <div class="api-status-badge api-status-warning">
                    ⚠️ 需要配置API
                </div>
            """, unsafe_allow_html=True)
            
            # API密钥输入
            with st.container():
                user_api_key = st.text_input(
                    "DeepSeek API Key",
                    type="password",
                    placeholder="sk-xxxxxxxxxxxxxxxxxxxx",
                    key="api_input_float",
                    help="请输入你的DeepSeek API密钥"
                )
                
                if user_api_key and user_api_key.strip():
                    st.session_state.deepseek_api_key = user_api_key.strip()
                    st.rerun()
            
            st.markdown("""
                <div style="margin-top: 10px; text-align: center;">
                    <a href="https://platform.deepseek.com" target="_blank" class="help-link">
                        📚 如何获取API Key？
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    return api_configured


def render_compact_status():
    """渲染紧凑状态显示 - 用于主页面顶部"""
    api_configured = bool(st.session_state.get('deepseek_api_key'))
    
    if api_configured:
        st.success("🔑 API已配置 - 小念随时待命！")
    else:
        st.warning("⚠️ 请先配置API密钥才能开始聊天")
    
    return api_configured 