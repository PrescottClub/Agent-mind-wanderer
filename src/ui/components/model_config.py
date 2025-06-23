"""
模型配置组件
提供DeepSeek模型选择和性能配置的UI界面
"""

import streamlit as st
import os
from typing import Dict, Any


def render_model_config_panel() -> Dict[str, Any]:
    """
    渲染模型配置面板
    
    Returns:
        包含模型配置信息的字典
    """
    
    # 添加CSS样式
    st.markdown("""
    <style>
    .model-config-panel {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 20px rgba(255, 122, 158, 0.1);
        border: 2px solid rgba(255, 122, 158, 0.2);
    }
    
    .model-option {
        background: rgba(255, 251, 245, 0.8);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 182, 193, 0.3);
    }
    
    .speed-indicator {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin-left: 10px;
    }
    
    .speed-fast {
        background: #BFFCC6;
        color: #2d5a3d;
    }
    
    .speed-slow {
        background: #FFE4E1;
        color: #8B4513;
    }
    
    .performance-tip {
        background: rgba(230, 230, 250, 0.6);
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        border-left: 4px solid #FF7A9E;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="model-config-panel">', unsafe_allow_html=True)
    
    st.markdown("### 🚀 模型性能配置")
    
    # 模型选择
    st.markdown("#### 📱 模型选择")
    
    model_options = {
        "deepseek-chat": {
            "name": "DeepSeek V3 (推荐)",
            "description": "快速响应，适合日常对话",
            "speed": "fast",
            "use_case": "💬 日常聊天、情感陪伴、创意写作"
        },
        "deepseek-reasoner": {
            "name": "DeepSeek R1",
            "description": "深度推理，响应较慢",
            "speed": "slow", 
            "use_case": "🧠 复杂推理、数学问题、逻辑分析"
        }
    }
    
    current_model = st.session_state.get('selected_model', 'deepseek-chat')
    
    for model_key, model_info in model_options.items():
        with st.container():
            st.markdown(f'<div class="model-option">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected = st.radio(
                    "选择模型",
                    options=[model_key],
                    format_func=lambda x: f"{model_info['name']} - {model_info['description']}",
                    key=f"radio_{model_key}",
                    index=0 if current_model == model_key else None,
                    label_visibility="collapsed"
                )
                
                if selected:
                    st.session_state.selected_model = model_key
                    current_model = model_key
                
                st.markdown(f"**适用场景:** {model_info['use_case']}")
            
            with col2:
                speed_class = f"speed-{model_info['speed']}"
                speed_text = "⚡ 快速" if model_info['speed'] == 'fast' else "🐌 较慢"
                st.markdown(f'<span class="speed-indicator {speed_class}">{speed_text}</span>', 
                           unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 性能参数配置
    st.markdown("#### ⚙️ 性能参数")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_tokens = st.slider(
            "最大Token数",
            min_value=128,
            max_value=2048,
            value=st.session_state.get('max_tokens', 512),
            step=128,
            help="数值越小响应越快，但回答可能较短"
        )
        st.session_state.max_tokens = max_tokens
    
    with col2:
        temperature = st.slider(
            "创造性温度",
            min_value=0.1,
            max_value=1.0,
            value=st.session_state.get('temperature', 0.5),
            step=0.1,
            help="数值越低响应越快且更稳定"
        )
        st.session_state.temperature = temperature
    
    # 性能提示
    st.markdown('<div class="performance-tip">', unsafe_allow_html=True)
    st.markdown("""
    💡 **性能优化建议:**
    - 选择 **DeepSeek V3** 获得最快响应速度
    - **Token数 ≤ 512** 可显著提升速度
    - **温度 ≤ 0.5** 让回答更快更稳定
    - 如需复杂推理才选择 R1 模型
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 返回配置信息
    return {
        'model': current_model,
        'max_tokens': max_tokens,
        'temperature': temperature,
        'model_info': model_options[current_model]
    }


def apply_model_config(config: Dict[str, Any]) -> bool:
    """
    应用模型配置到环境变量
    
    Args:
        config: 模型配置字典
        
    Returns:
        是否成功应用配置
    """
    try:
        # 更新环境变量
        os.environ['DEEPSEEK_MODEL'] = config['model']
        os.environ['MAX_TOKENS'] = str(config['max_tokens'])
        os.environ['TEMPERATURE'] = str(config['temperature'])
        
        # 更新session state
        st.session_state.model_config_applied = True
        st.session_state.current_model_info = config['model_info']
        
        return True
        
    except Exception as e:
        st.error(f"应用配置失败: {e}")
        return False


def show_current_model_status():
    """显示当前模型状态"""
    current_model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
    max_tokens = os.getenv('MAX_TOKENS', '512')
    temperature = os.getenv('TEMPERATURE', '0.5')
    
    model_name = "DeepSeek V3" if current_model == "deepseek-chat" else "DeepSeek R1"
    speed_emoji = "⚡" if current_model == "deepseek-chat" else "🐌"
    
    st.markdown(f"""
    <div style="background: rgba(255, 251, 245, 0.8); padding: 10px; border-radius: 10px; margin: 5px 0;">
        <small>
        🤖 当前模型: <strong>{model_name}</strong> {speed_emoji} | 
        📊 Token: {max_tokens} | 
        🌡️ 温度: {temperature}
        </small>
    </div>
    """, unsafe_allow_html=True)
