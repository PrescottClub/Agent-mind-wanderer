"""
侧边栏组件
负责渲染API密钥输入界面和会话管理
"""

import streamlit as st
import uuid
from typing import Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.repositories.user_profile_repository import UserProfileRepository
from src.services.intimacy_service import IntimacyService
from .model_config import render_model_config_panel, apply_model_config, show_current_model_status


def render_sidebar() -> Optional[str]:
    """渲染侧边栏API密钥输入界面 - 美化版"""
    with st.sidebar:
        # 自定义样式 - 粉嫩可爱风格
        st.markdown("""
        <style>
        /* 侧边栏整体背景 */
        .stSidebar > div:first-child {
            background: linear-gradient(180deg, #fdf2f8 0%, #fce7f3 50%, #fbcfe8 100%);
        }
        
        .api-config-header {
            background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
            color: white;
            padding: 1.5rem 1rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(236, 72, 153, 0.3);
            border: 2px solid rgba(236, 72, 153, 0.2);
        }
        .api-config-header h2 {
            margin: 0;
            font-size: 1.3rem;
            font-weight: 600;
            color: white;
        }
        .api-config-header p {
            margin: 0.5rem 0 0 0;
            font-size: 0.85rem;
            opacity: 0.9;
            color: rgba(255, 255, 255, 0.8);
        }
        
        /* 美化输入框标题 */
        .stMarkdown h5 {
            color: #be185d !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
        }
        .api-status-card {
            background: rgba(255, 255, 255, 0.7);
            border: 2px solid rgba(236, 72, 153, 0.3);
            border-radius: 12px;
            padding: 1.2rem;
            margin: 1rem 0;
            text-align: center;
            box-shadow: 0 3px 15px rgba(236, 72, 153, 0.1);
            backdrop-filter: blur(10px);
        }
        .api-status-success {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.2) 100%);
            border: 2px solid #22c55e;
            color: #15803d;
        }
        .api-status-success h4 {
            color: #15803d;
            margin: 0 0 0.5rem 0;
        }
        .api-status-warning {
            background: linear-gradient(135deg, rgba(245, 101, 101, 0.1) 0%, rgba(245, 101, 101, 0.2) 100%);
            border: 2px solid #f56565;
            color: #c53030;
        }
        .api-status-warning h4 {
            color: #c53030;
            margin: 0 0 0.5rem 0;
        }
        .help-section {
            background: rgba(255, 255, 255, 0.8);
            border-left: 4px solid #ec4899;
            padding: 1.2rem;
            border-radius: 0 12px 12px 0;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(236, 72, 153, 0.1);
            backdrop-filter: blur(10px);
        }
        .help-section h4 {
            color: #be185d;
            margin-top: 0;
            font-size: 1rem;
            font-weight: 600;
        }
        .help-steps {
            list-style: none;
            padding: 0;
            margin: 0.5rem 0;
        }
        .help-steps li {
            padding: 0.4rem 0;
            position: relative;
            padding-left: 2rem;
            color: #636e72;
        }
        .help-steps li:before {
            content: counter(step-counter);
            counter-increment: step-counter;
            position: absolute;
            left: 0;
            top: 0.4rem;
            background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
            color: white;
            width: 1.4rem;
            height: 1.4rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: bold;
            box-shadow: 0 2px 8px rgba(236, 72, 153, 0.3);
        }
        .help-steps {
            counter-reset: step-counter;
        }
        .help-steps a {
            color: #be185d;
            text-decoration: none;
            font-weight: 500;
        }
        .help-steps a:hover {
            color: #ec4899;
            text-decoration: underline;
        }
        .privacy-note {
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid #22c55e;
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
            font-size: 0.85rem;
            color: #15803d;
            box-shadow: 0 2px 10px rgba(34, 197, 94, 0.1);
            backdrop-filter: blur(10px);
        }
        .privacy-note strong {
            color: #15803d;
        }
        .feature-preview {
            background: rgba(255, 255, 255, 0.8);
            border: 2px solid #ec4899;
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
            box-shadow: 0 2px 10px rgba(236, 72, 153, 0.1);
            backdrop-filter: blur(10px);
        }
        .feature-preview ul {
            margin: 0.5rem 0;
            padding-left: 1rem;
        }
        .feature-preview li {
            color: #374151;
            margin: 0.3rem 0;
            font-size: 0.85rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 美化的头部
        st.markdown("""
        <div class="api-config-header">
            <h2>🔑 API 密钥配置</h2>
            <p>让心绪精灵小念开始陪伴你的旅程</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 优先从 Streamlit Secrets 获取 API 密钥
        api_key_from_secrets = None
        try:
            api_key_from_secrets = st.secrets.get("DEEPSEEK_API_KEY")
        except:
            pass

        # 如果没有从 secrets 获取到，尝试从环境变量获取
        if not api_key_from_secrets:
            api_key_from_secrets = os.getenv("DEEPSEEK_API_KEY")

        # 如果从 secrets 或环境变量获取到了密钥
        if api_key_from_secrets:
            st.session_state.deepseek_api_key = api_key_from_secrets
            st.markdown("""
            <div class="api-status-card api-status-success">
                <h4>✅ API密钥已配置 (来自配置文件)</h4>
                <p>心绪精灵小念已准备好为你服务！</p>
            </div>
            """, unsafe_allow_html=True)
            api_configured = True
        else:
            # 如果没有从配置获取到，显示输入框
            st.markdown("##### 🗝️ 请输入你的 DeepSeek API Key")
            user_api_key = st.text_input(
                "API密钥",
                type="password",
                placeholder="sk-xxxxxxxxxxxxxxxxxxxx",
                help="请在此输入你的DeepSeek API密钥",
                label_visibility="collapsed"
            )

            # 检查用户输入的API密钥
            if user_api_key and user_api_key.strip():
                st.session_state.deepseek_api_key = user_api_key.strip()
                st.markdown("""
                <div class="api-status-card api-status-success">
                    <h4>✅ API密钥已配置</h4>
                    <p>心绪精灵小念已准备好为你服务！</p>
                </div>
                """, unsafe_allow_html=True)
                api_configured = True
            else:
                # 检查session state中是否有密钥
                if hasattr(st.session_state, 'deepseek_api_key') and st.session_state.deepseek_api_key:
                    st.markdown("""
                    <div class="api-status-card api-status-success">
                        <h4>✅ API密钥已配置</h4>
                        <p>心绪精灵小念已准备好为你服务！</p>
                    </div>
                    """, unsafe_allow_html=True)
                    api_configured = True
                else:
                    st.markdown("""
                    <div class="api-status-card api-status-warning">
                        <h4>⚠️ 需要配置API密钥</h4>
                        <p>请输入你的API密钥来开始使用</p>
                    </div>
                    """, unsafe_allow_html=True)
                    api_configured = False
        
        # 美化的帮助文档
        st.markdown("""
        <div class="help-section">
            <h4>📚 如何配置API Key？</h4>
            <ol class="help-steps">
                <li><strong>推荐方式：使用 Streamlit Secrets</strong>
                    <ul>
                        <li>在项目根目录创建 <code>.streamlit/secrets.toml</code> 文件</li>
                        <li>添加：<code>DEEPSEEK_API_KEY = "sk-your-api-key"</code></li>
                        <li>重启应用即可自动加载</li>
                    </ul>
                </li>
                <li><strong>备选方式：环境变量</strong>
                    <ul>
                        <li>设置环境变量：<code>DEEPSEEK_API_KEY=sk-your-api-key</code></li>
                    </ul>
                </li>
                <li><strong>临时方式：手动输入</strong>
                    <ul>
                        <li>在上方输入框中直接输入API密钥</li>
                        <li>仅在当前会话有效</li>
                    </ul>
                </li>
            </ol>
            <p><strong>获取API Key：</strong> 访问 <a href="https://platform.deepseek.com" target="_blank" style="color: #667eea; text-decoration: none;">DeepSeek官网</a> 注册并创建API密钥</p>
        </div>
        """, unsafe_allow_html=True)

        # 隐私保护说明
        st.markdown("""
        <div class="privacy-note">
            🔒 <strong>安全建议</strong><br>
            • <strong>生产部署</strong>：强烈建议使用 Streamlit Secrets 或环境变量<br>
            • <strong>开发测试</strong>：可以使用手动输入方式<br>
            • <strong>隐私保护</strong>：手动输入的密钥仅在浏览器会话中使用，不会存储到服务器
        </div>
        """, unsafe_allow_html=True)
        
        # 可选：显示应用功能预览
        if not api_configured:
            st.markdown("---")
            st.markdown("""
            <div class="feature-preview">
                <h4 style="color: #e84393; margin-top: 0; font-size: 1rem; font-weight: 600;">🌟 应用功能预览</h4>
                <ul>
                    <li>🎭 <strong>智能情绪分析</strong> - 理解你的每种心情</li>
                    <li>🎨 <strong>心情调色盘</strong> - 用颜色表达情感</li>
                    <li>🎁 <strong>宝藏收集盒</strong> - 收藏美好回忆</li>
                    <li>🌙 <strong>主动关怀</strong> - 贴心的陪伴体验</li>
                    <li>🎉 <strong>惊喜彩蛋</strong> - 特殊时刻的小惊喜</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # 【v6.0新增】模型配置部分
        if api_configured:
            st.markdown("---")
            render_model_configuration()

        # 【v5.0新增】亲密度显示部分
        if api_configured:
            st.markdown("---")
            render_intimacy_display()

        # 会话管理部分
        if api_configured:
            st.markdown("---")
            render_session_management()

        return st.session_state.deepseek_api_key if api_configured else None


def render_model_configuration():
    """渲染模型配置部分 - v6.0新增"""
    st.markdown("### 🚀 模型配置")

    # 显示当前模型状态
    show_current_model_status()

    # 模型配置面板
    with st.expander("⚙️ 高级配置", expanded=False):
        config = render_model_config_panel()

        if st.button("✅ 应用配置", type="primary", use_container_width=True):
            if apply_model_config(config):
                st.success("🎉 配置已应用！重新发送消息即可生效")
            else:
                st.error("❌ 配置应用失败")


def render_intimacy_display():
    """渲染亲密度显示部分 - v5.0新增"""
    try:
        # 获取当前会话ID
        session_id = st.session_state.get('session_id', 'unknown')
        if session_id == 'unknown':
            return

        # 初始化服务
        user_profile_repo = UserProfileRepository()
        intimacy_service = IntimacyService(user_profile_repo)

        # 获取亲密度信息
        intimacy_info = intimacy_service.get_intimacy_info(session_id)

        level = intimacy_info["current_level"]
        exp = intimacy_info["current_exp"]
        exp_needed = intimacy_info["exp_needed"]
        progress = intimacy_info["exp_progress"]
        interactions = intimacy_info["total_interactions"]

        # 获取称号
        title = intimacy_service._get_level_title(level)

        st.markdown("### 💖 与小念的羁绊")

        # 羁绊等级显示
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
                    padding: 1rem; border-radius: 12px; text-align: center; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #2d3436;">Lv.{level} ❤️</h4>
            <p style="margin: 0.5rem 0 0 0; color: #636e72; font-size: 0.9rem;">{title}</p>
        </div>
        """, unsafe_allow_html=True)

        # 经验值进度条
        st.write(f"**经验值**: {exp} / {exp_needed} EXP")
        st.progress(progress, text=f"距离下一级还需 {exp_needed - exp} EXP")

        # 互动统计
        st.write(f"**总互动次数**: {interactions} 次")

        # 羁绊状态
        status = intimacy_service._get_intimacy_status(level)
        st.markdown(f"**羁绊状态**: {status}")

    except Exception as e:
        st.error(f"加载羁绊信息失败: {e}")


def render_session_management():
    """渲染会话管理部分"""
    st.markdown("### 🔧 会话管理")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🆕 开始新对话", type="secondary", use_container_width=True):
            # 创建新会话
            new_session_id = str(uuid.uuid4())
            st.session_state.session_id = new_session_id
            st.query_params['session_id'] = new_session_id

            # 清空当前状态
            st.session_state.current_mood = "平静"
            st.session_state.current_reaction = ""
            st.session_state.current_gift = {"type": "", "content": ""}
            st.session_state.mood_history = []
            # 清空聊天消息
            st.session_state.messages = []

            st.success("✨ 新对话已开始！")

    with col_b:
        if st.button("📋 复制会话链接", type="secondary", use_container_width=True):
            session_id = st.session_state.get('session_id', 'unknown')
            # 动态获取当前URL，避免硬编码端口
            try:
                import streamlit.web.server.server as server
                port = server.get_current_server_config().port
                current_url = f"http://localhost:{port}/?session_id={session_id}"
            except:
                current_url = f"http://localhost:8501/?session_id={session_id}"
            st.info(f"🔗 会话链接: {current_url}")
            st.info("💡 保存此链接可以在任何时候回到这个对话！")
