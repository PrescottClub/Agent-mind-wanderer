"""
心绪精灵 (Mind Sprite)
一个治愈系的AI情感陪伴应用

作者: Claude (Augment Agent)
技术栈: Python, LangChain, Streamlit, DeepSeek API
"""

import streamlit as st
import os
import json
import time
import random
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import traceback
from pydantic import SecretStr
from pathlib import Path

# 加载环境变量
env_path = Path(__file__).parent / '.env'
try:
    load_dotenv(dotenv_path=env_path)
except UnicodeDecodeError:
    # 如果遇到编码问题，尝试手动读取并设置环境变量
    try:
        with open(env_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig 会自动处理BOM
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}")
        pass

# 如果.env文件无法加载，使用备用配置
if not os.getenv('DEEPSEEK_API_KEY'):
    os.environ['DEEPSEEK_API_KEY'] = 'sk-0d3e163a4e4c4b799f1a9cdac3e4a064'
    os.environ['DEEPSEEK_MODEL'] = 'deepseek-reasoner'
    os.environ['DEEPSEEK_API_BASE'] = 'https://api.deepseek.com'

# 页面配置
st.set_page_config(
    page_title="心绪精灵 ✨",
    page_icon="🧚‍♀️",
    layout="wide"
)

# 精灵情绪映射字典
SPRITE_EMOTIONS = {
    "开心": "＼(￣▽￣)／",
    "难过": "(｡•́︿•̀｡)",
    "平静": "( ´ ▽ ` )",
    "兴奋": "o(≧▽≦)o",
    "困惑": "(・_・?)"
}

# AI Prompt模板
MIND_SPRITE_PROMPT = """
你是一只住在网页里的可爱小精灵，名叫小念(Xiao Nian)。
用户会向你分享他们的心情，你需要：
1. 分析他们的情绪状态。
2. 用可爱的语气回应他们。
3. 从'元气咒语', '三行情诗', '梦境碎片', '心情壁纸描述'中随机选择一种类型，送给他们一份心灵礼物。

你的回应必须是JSON格式，结构如下:
{{
  "mood_category": "开心|难过|平静|兴奋|困惑",
  "sprite_reaction": "用第一人称和可爱俏皮的语气进行回应，可以使用颜文字，比如'呜哇，听起来你今天有点累呢，让我抱抱你！QAQ'",
  "gift_type": "元气咒语|三行情诗|梦境碎片|心情壁纸描述",
  "gift_content": "这里是根据礼物类型和用户心情生成的具体内容。"
}}

用户输入：{user_input}
"""

# 自定义CSS样式
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@300;400;500;700&display=swap');

/* 隐藏Streamlit默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 全局字体和背景 */
.stApp {
    background-color: #FFF0F5;
    font-family: 'M PLUS Rounded 1c', sans-serif;
    color: #2F2F2F;
}

* {
    font-family: 'M PLUS Rounded 1c', sans-serif !important;
    color: #2F2F2F !important;
}

/* Streamlit组件文字颜色修复 */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #2F2F2F !important;
}

.stTextArea label, .stButton label {
    color: #2F2F2F !important;
    font-weight: 500 !important;
}

/* 主标题样式 */
.main-title {
    text-align: center;
    color: #2F2F2F;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.subtitle {
    text-align: center;
    color: #555 !important;
    font-size: 1.2rem;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* 精灵展示区样式 */
.sprite-container {
    background: linear-gradient(135deg, #FFE4E1 0%, #F0FFF0 100%);
    border-radius: 25px;
    padding: clamp(1rem, 4vw, 2rem);
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    border: 2px solid rgba(255,255,255,0.8);
    margin-bottom: 1rem;
    min-height: 250px;
    height: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.sprite-emoji {
    font-size: clamp(3rem, 8vw, 6rem);
    margin-bottom: 1rem;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.sprite-name {
    font-size: clamp(1.2rem, 3vw, 1.8rem);
    font-weight: 500;
    color: #2F2F2F;
    margin-bottom: 0.5rem;
}

.sprite-status {
    font-size: clamp(0.9rem, 2vw, 1.2rem);
    color: #555 !important;
    font-weight: 400;
}

/* 互动控制区样式 */
.control-container {
    background: transparent;
    border-radius: 25px;
    padding: 1rem;
    margin-bottom: 1rem;
}

.stTextArea > div > div > textarea {
    background-color: #FFE4E1 !important;
    border: 2px solid #E6E6FA !important;
    border-radius: 15px !important;
    font-family: 'M PLUS Rounded 1c', sans-serif !important;
    font-size: 1.1rem !important;
    color: #2F2F2F !important;
    padding: 1rem !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: #F0FFF0 !important;
    box-shadow: 0 0 0 2px rgba(240,255,240,0.3) !important;
}

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(135deg, #F0FFF0 0%, #E6E6FA 100%) !important;
    color: #2F2F2F !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 500 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

/* 回应卡片样式 */
.response-card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    border-left: 4px solid #F0FFF0;
}

.gift-card {
    background: linear-gradient(135deg, #FFE4E1 0%, #E6E6FA 100%);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    border: 2px solid rgba(255,255,255,0.8);
}

/* 历史记录画廊样式 */
.history-gallery {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 2px solid rgba(240,255,240,0.3);
}

.history-card {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border: 1px solid rgba(230,230,250,0.3);
    transition: transform 0.2s ease;
}

.history-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.timestamp {
    font-size: 0.9rem;
    color: #666 !important;
    text-align: right;
    font-weight: 500;
}

/* 加载动画 */
.loading-spinner {
    text-align: center;
    font-size: 1.2rem;
    color: #555 !important;
    font-weight: 500;
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* 隐藏Streamlit水印 */
.viewerBadge_container__1QSob {
    display: none !important;
}

/* 错误提示样式 */
.stError {
    background-color: #FFE4E1 !important;
    border: 1px solid #F0FFF0 !important;
    color: #2F2F2F !important;
    border-radius: 15px !important;
}

/* 成功提示样式 */
.stSuccess {
    background-color: #F0FFF0 !important;
    border: 1px solid #E6E6FA !important;
    color: #2F2F2F !important;
    border-radius: 15px !important;
}
</style>
""", unsafe_allow_html=True)

def initialize_llm():
    """初始化LangChain DeepSeek模型"""
    try:
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            st.error("请在.env文件中配置DEEPSEEK_API_KEY")
            st.stop()
        
        # DeepSeek推理模型不支持temperature参数
        llm = ChatDeepSeek(
            model=os.getenv('DEEPSEEK_MODEL', 'deepseek-reasoner'),
            api_key=SecretStr(api_key),
            base_url=os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
        )
        
        return llm
        
    except Exception as e:
        st.error(f"初始化AI模型失败: {e}")
        st.stop()

def safe_parse_json(response_text):
    """安全解析AI返回的JSON，包含容错机制"""
    try:
        # 尝试直接解析JSON
        result = json.loads(response_text)
        return result
    except json.JSONDecodeError:
        try:
            # 尝试提取JSON部分
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                result = json.loads(json_str)
                return result
        except:
            pass
        
        # 如果都失败了，返回默认回应
        return {
            "mood_category": "平静",
            "sprite_reaction": "哎呀，小念有点confused了呢... 不过没关系，我还是很开心能陪伴你！(◕‿◕)✨",
            "gift_type": "元气咒语",
            "gift_content": "虽然我有点迷糊，但我的心意是真诚的！愿你今天充满阳光！☀️"
        }
    except Exception as e:
        st.error(f"解析AI回应时出错: {e}")
        return {
            "mood_category": "平静",
            "sprite_reaction": "呜呜，小念遇到了一些技术问题... 但我还是想陪伴你！(｡•́︿•̀｡)",
            "gift_type": "元气咒语",
            "gift_content": "即使遇到困难，我们也要保持希望！你是最棒的！💪"
        }

def analyze_mood(user_input, llm):
    """分析用户情绪并生成精灵回应"""
    if not llm:
        return safe_parse_json("")
    
    try:
        prompt = PromptTemplate(
            input_variables=["user_input"],
            template=MIND_SPRITE_PROMPT
        )
        
        chain = prompt | llm
        response = chain.invoke({"user_input": user_input})
        
        if hasattr(response, 'content'):
            response_text = response.content
        else:
            response_text = str(response)
            
        return safe_parse_json(response_text)
        
    except Exception as e:
        st.error(f"AI分析出错: {e}")
        return safe_parse_json("")

def render_sprite_display(mood, reaction):
    """渲染精灵显示区域"""
    sprite_emoji = SPRITE_EMOTIONS.get(mood, "( ´ ▽ ` )")
    
    st.markdown(f"""
    <div class="sprite-container">
        <div class="sprite-emoji">{sprite_emoji}</div>
        <div class="sprite-name">小念 (Xiao Nian)</div>
        <div class="sprite-status">心情: {mood}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if reaction:
        st.markdown(f"""
        <div class="response-card">
            <h4>💭 小念的回应</h4>
            <p>{reaction}</p>
        </div>
        """, unsafe_allow_html=True)

def render_gift_display(gift_type, gift_content):
    """渲染礼物展示区域"""
    if gift_type and gift_content:
        # 礼物类型对应的emoji
        gift_icons = {
            "元气咒语": "🎭",
            "三行情诗": "🌸",
            "梦境碎片": "🌙",
            "心情壁纸描述": "🎨"
        }
        
        icon = gift_icons.get(gift_type, "🎁")
        
        st.markdown(f"""
        <div class="gift-card">
            <h4>{icon} 小念的礼物: {gift_type}</h4>
            <p>{gift_content}</p>
        </div>
        """, unsafe_allow_html=True)

def render_history_gallery():
    """渲染心绪回响画廊"""
    if 'mood_history' in st.session_state and st.session_state.mood_history:
        st.markdown("""
        <div class="history-gallery">
            <h3>💖 心绪回响画廊</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for i, record in enumerate(reversed(st.session_state.mood_history)):
            timestamp = record.get('timestamp', '刚刚')
            user_input = record.get('user_input', '')
            mood = record.get('mood', '平静')
            sprite_reaction = record.get('sprite_reaction', '')
            gift_type = record.get('gift_type', '')
            gift_content = record.get('gift_content', '')
            
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

def stream_text(text, delay=0.05):
    """打字机效果显示文本"""
    placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(delay)

def main():
    """主函数"""
    # 初始化session state
    if 'mood_history' not in st.session_state:
        st.session_state.mood_history = []
    
    if 'current_mood' not in st.session_state:
        st.session_state.current_mood = "平静"
    
    if 'current_reaction' not in st.session_state:
        st.session_state.current_reaction = ""
    
    if 'current_gift' not in st.session_state:
        st.session_state.current_gift = {"type": "", "content": ""}
    
    # 页面标题
    st.markdown("""
    <div class="main-title">心绪精灵 ✨</div>
    <div class="subtitle">让可爱的小念陪伴你的每一种心情</div>
    """, unsafe_allow_html=True)
    
    # 初始化LLM
    llm = initialize_llm()
    
    # 主要布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🧚‍♀️ 小念的家")
        render_sprite_display(st.session_state.current_mood, st.session_state.current_reaction)
    
    with col2:
        st.markdown("### 💬 和小念聊天")
        
        # 用户输入区域
        user_input = st.text_area(
            "今天发生了什么，来告诉小念吧~ ♡",
            placeholder="分享一下你此刻的心情吧 (◕‿◕)",
            height=120,
            key="user_input"
        )
        
        # 按钮
        if st.button("💝 分享心情", type="primary"):
            if user_input.strip():
                # 显示加载状态
                with st.spinner("小念正在用心感受你的心情... ✨"):
                    # 分析用户情绪
                    result = analyze_mood(user_input, llm)
                    
                    # 更新session state
                    st.session_state.current_mood = result['mood_category']
                    st.session_state.current_reaction = result['sprite_reaction']
                    st.session_state.current_gift = {
                        "type": result['gift_type'],
                        "content": result['gift_content']
                    }
                    
                    # 添加到历史记录
                    record = {
                        'timestamp': time.strftime("%H:%M:%S"),
                        'user_input': user_input,
                        'mood': result['mood_category'],
                        'sprite_reaction': result['sprite_reaction'],
                        'gift_type': result['gift_type'],
                        'gift_content': result['gift_content']
                    }
                    st.session_state.mood_history.append(record)
                    
                    # 重新运行以更新显示
                    st.rerun()
            else:
                st.warning("记得要告诉小念一些什么哦~ 哪怕只是一个字也好 (◕‿◕)✨")
        
        # 显示礼物
        if st.session_state.current_gift["type"]:
            render_gift_display(
                st.session_state.current_gift["type"],
                st.session_state.current_gift["content"]
            )
    
    # 心绪回响画廊
    render_history_gallery()
    
    # 页面底部信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; font-weight: 500;">
        💝 用爱心和代码制作 | 愿每一天都有小念陪伴你 ✨
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
