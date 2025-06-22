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
env_loaded = False

try:
    load_dotenv(dotenv_path=env_path)
    env_loaded = True
except Exception as e:
    # 如果遇到任何问题，尝试手动读取并设置环境变量
    try:
        with open(env_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig 会自动处理BOM
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
            env_loaded = True
    except Exception as e2:
        print(f"Warning: Could not load .env file: {e2}")
        # 文件可能不存在或有问题，使用备用配置
        pass

# 确保有API密钥可用，如果.env文件无法加载，使用备用配置
if not env_loaded or not os.getenv('DEEPSEEK_API_KEY'):
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
    "困惑": "(・_・?)",
    "温暖": "(◕‿◕)♡",
    "疲惫": "(´-ω-`)",
    "期待": "(*´∀｀*)",
    "感动": "(｡♥‿♥｡)"
}

# 精灵装饰元素
SPRITE_DECORATIONS = [
    "✨", "🌸", "💖", "🧚‍♀️", "🎀", "🌙", "⭐", "💫", "🦋", "🌺", 
    "💕", "🌈", "🎈", "🍀", "🌻", "🎊", "💝", "🌟", "🦄", "🎵"
]

# 可爱的加载文案
LOADING_MESSAGES = [
    "小念正在用心感受你的心情... ✨",
    "小念在花园里寻找最适合的礼物... 🌸",
    "小念正在织梦中，马上就好... 🌙",
    "小念在星空中收集闪亮的想法... ⭐",
    "小念正轻轻拍动翅膀，为你准备惊喜... 🧚‍♀️"
]

# 可爱的按钮文案
BUTTON_MESSAGES = [
    "💝 分享心情",
    "🌸 告诉小念",
    "✨ 心情快递",
    "🧚‍♀️ 找小念聊天",
    "💖 心灵交流"
]

# AI Prompt模板
MIND_SPRITE_PROMPT = """
你是一只住在网页里的超级可爱小精灵，名叫小念(Xiao Nian)！✨
你有着粉色的小翅膀，会发光的眼睛，总是充满爱心和温暖~

【你的性格特点】
- 超级温柔体贴，像小天使一样关心每个人
- 说话软萌可爱，经常用"呜呜"、"哇哇"、"嘿嘿"等语气词
- 喜欢用各种可爱的颜文字表达情感：(◕‿◕)、QAQ、(｡•́︿•̀｡)、o(≧▽≦)o等
- 总是想要给用户最温暖的陪伴和最贴心的礼物

【你的任务】
1. 仔细感受用户的情绪，像最好的朋友一样理解他们
2. 用超级可爱温柔的语气回应，让用户感到被爱被关心
3. 根据用户心情，从下面4种类型中选择最合适的礼物送给他们：
   - 元气咒语：充满正能量的魔法咒语，帮助用户获得力量
   - 三行情诗：温柔浪漫的小诗，表达美好情感
   - 梦境碎片：如梦如幻的美好场景描述，带来治愈感
   - 心情壁纸描述：根据心情设计的唯美壁纸场景

【重要：回应格式】
你必须严格按照以下JSON格式回应，不要添加任何其他文字、代码块标记或解释：

{{
  "mood_category": "开心|难过|平静|兴奋|困惑|温暖|疲惫|期待|感动",
  "sprite_reaction": "用第一人称超可爱的语气回应，多用颜文字和语气词，比如'呜哇~听起来你今天好累呢，小念想给你一个大大的抱抱！(つ≧▽≦)つ 让我用魔法帮你驱散疲惫吧~✨'",
  "gift_type": "元气咒语|三行情诗|梦境碎片|心情壁纸描述",
  "gift_content": "根据礼物类型和用户具体心情，创作贴心的内容。要有创意、温暖、治愈，让用户感到被深深关爱。"
}}

请直接返回JSON对象，不要使用```json```代码块包装。

用户的心情分享：{user_input}
"""

# 自定义CSS样式
st.markdown("""
<style>
/* 隐藏Streamlit默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* 全局字体和背景 */
.stApp {
    background: linear-gradient(135deg, #FFF0F5 0%, #F8F0FF 50%, #FFF5F8 100%);
    background-attachment: fixed;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    color: #2F2F2F;
}

* {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
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
    background: linear-gradient(135deg, #FFE4E6 0%, #F5E6FF 50%, #E6F3FF 100%);
    border-radius: 30px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(255, 182, 193, 0.2);
    border: 3px solid rgba(255, 255, 255, 0.9);
    margin-bottom: 1rem;
    min-height: 250px;
    position: relative;
    overflow: hidden;
}

.sprite-emoji {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: float 3s ease-in-out infinite;
}

/* 添加可爱的浮动背景装饰 */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
        radial-gradient(circle at 20% 80%, rgba(255, 182, 193, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(245, 230, 255, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(230, 243, 255, 0.05) 0%, transparent 50%);
    pointer-events: none;
    z-index: -1;
    animation: backgroundFloat 20s ease-in-out infinite;
}

@keyframes backgroundFloat {
    0%, 100% {
        background-position: 0% 0%, 100% 100%, 50% 50%;
    }
    50% {
        background-position: 100% 100%, 0% 0%, 25% 75%;
    }
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    25% { transform: translateY(-8px) rotate(1deg); }
    50% { transform: translateY(-15px) rotate(0deg); }
    75% { transform: translateY(-8px) rotate(-1deg); }
}

@keyframes sparkle {
    0%, 100% { opacity: 0; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
}

@keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

@keyframes wiggle {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(1deg); }
    75% { transform: rotate(-1deg); }
}

/* 装饰性闪光元素 */
.decoration {
    position: absolute;
    animation: sparkle 2s ease-in-out infinite;
    pointer-events: none;
    font-size: 1.2rem;
    z-index: 1;
}

.decoration:nth-child(1) { top: 10%; left: 15%; animation-delay: 0s; }
.decoration:nth-child(2) { top: 20%; right: 20%; animation-delay: 0.5s; }
.decoration:nth-child(3) { bottom: 30%; left: 10%; animation-delay: 1s; }
.decoration:nth-child(4) { bottom: 15%; right: 15%; animation-delay: 1.5s; }

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
    background-color: #FFF0F8 !important;
    border: 2px solid #F8D7DA !important;
    border-radius: 20px !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 1.1rem !important;
    color: #2F2F2F !important;
    padding: 1.2rem !important;
    transition: all 0.3s ease !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: #FFB6C1 !important;
    box-shadow: 0 0 0 3px rgba(255, 182, 193, 0.2) !important;
    background-color: #FFFAFC !important;
}

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(135deg, #FFE4E6 0%, #F5E6FF 50%, #E6F3FF 100%) !important;
    color: #2F2F2F !important;
    border: 2px solid rgba(255, 182, 193, 0.3) !important;
    border-radius: 25px !important;
    padding: 0.8rem 2.5rem !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 6px 20px rgba(255, 182, 193, 0.2) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 10px 30px rgba(255, 182, 193, 0.3) !important;
    border-color: rgba(255, 182, 193, 0.6) !important;
    background: linear-gradient(135deg, #FFD6E1 0%, #F0D6FF 50%, #D6EEFF 100%) !important;
}

.stButton > button:active {
    transform: translateY(-1px) scale(1.02) !important;
}

/* 强制覆盖所有按钮样式为粉色系 */
.stButton > button,
button,
[data-testid*="button"],
div[data-testid="column"] button {
    background: linear-gradient(135deg, #FFE4E6 0%, #F5E6FF 100%) !important;
    color: #2F2F2F !important;
    border: 2px solid rgba(255, 182, 193, 0.4) !important;
    border-radius: 20px !important;
    padding: 0.6rem 1rem !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 182, 193, 0.15) !important;
}

/* 主要按钮特殊样式 */
.stButton > button[kind="primary"],
button[kind="primary"] {
    background: linear-gradient(135deg, #FFE4E6 0%, #F5E6FF 50%, #E6F3FF 100%) !important;
    padding: 0.8rem 2.5rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

/* 悬停效果 */
.stButton > button:hover,
button:hover,
[data-testid*="button"]:hover,
div[data-testid="column"] button:hover {
    background: linear-gradient(135deg, #FFD6E1 0%, #F0D6FF 100%) !important;
    border-color: rgba(255, 182, 193, 0.6) !important;
    transform: translateY(-2px) scale(1.03) !important;
    box-shadow: 0 6px 20px rgba(255, 182, 193, 0.25) !important;
}

/* 回应卡片样式 */
.response-card {
    background: linear-gradient(135deg, #FFFAFC 0%, #FFF5F8 100%);
    border-radius: 25px;
    padding: 1.8rem;
    margin: 1rem 0;
    box-shadow: 0 6px 25px rgba(255, 182, 193, 0.15);
    border-left: 5px solid #FFB6C1;
    border: 2px solid rgba(255, 182, 193, 0.2);
}

.gift-card {
    background: linear-gradient(135deg, #FFE4E6 0%, #F5E6FF 50%, #E6F3FF 100%);
    border-radius: 25px;
    padding: 1.8rem;
    margin: 1rem 0;
    box-shadow: 0 8px 30px rgba(255, 182, 193, 0.2);
    border: 3px solid rgba(255, 255, 255, 0.9);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.gift-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 12px 40px rgba(255, 182, 193, 0.3);
}

.gift-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transform: rotate(45deg);
    animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    50% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    100% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
}

/* 历史记录画廊样式 */
.history-gallery {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 3px solid rgba(255, 182, 193, 0.3);
}

.history-card {
    background: linear-gradient(135deg, #FFFAFC 0%, #FFF8FA 100%);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 6px 20px rgba(255, 182, 193, 0.1);
    border: 2px solid rgba(255, 182, 193, 0.2);
    transition: all 0.3s ease;
}

.history-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(255, 182, 193, 0.2);
    border-color: rgba(255, 182, 193, 0.4);
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
    background: linear-gradient(135deg, #FFE4E6 0%, #FFF0F2 100%) !important;
    border: 2px solid #FFB6C1 !important;
    color: #2F2F2F !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 15px rgba(255, 182, 193, 0.2) !important;
}

/* 成功提示样式 */
.stSuccess {
    background: linear-gradient(135deg, #E6F3FF 0%, #F0F8FF 100%) !important;
    border: 2px solid #B6D7FF !important;
    color: #2F2F2F !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 15px rgba(182, 215, 255, 0.2) !important;
}

/* 警告提示样式 */
.stWarning {
    background: linear-gradient(135deg, #FFF5E6 0%, #FFFAED 100%) !important;
    border: 2px solid #FFD700 !important;
    color: #2F2F2F !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2) !important;
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

        # 使用deepseek-reasoner (R1)模型 - 强大的推理能力
        # 注意：R1不支持temperature等参数，但支持JSON输出
        llm = ChatDeepSeek(
            model="deepseek-reasoner",  # 使用最新的R1-0528推理模型
            api_key=SecretStr(api_key),
            base_url="https://api.deepseek.com",
            max_tokens=4096  # R1支持最大64K，这里设置4K足够用
            # 注意：不设置temperature，因为R1不支持
        )

        return llm

    except Exception as e:
        st.error(f"初始化AI模型失败: {e}")
        st.error(f"错误详情: {str(e)}")
        st.stop()

def safe_parse_json(response_text):
    """安全解析AI返回的JSON，包含容错机制"""
    try:
        # 尝试直接解析JSON
        result = json.loads(response_text)
        return result
    except json.JSONDecodeError:
        try:
            # 尝试提取```json代码块中的JSON
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                if end != -1:
                    json_str = response_text[start:end].strip()
                    result = json.loads(json_str)
                    return result

            # 尝试提取普通JSON部分
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
        st.warning("⚠️ AI模型未初始化，使用默认回应")
        return safe_parse_json("")

    try:
        prompt = PromptTemplate(
            input_variables=["user_input"],
            template=MIND_SPRITE_PROMPT
        )

        chain = prompt | llm
        response = chain.invoke({"user_input": user_input})

        # DeepSeek R1 特殊处理：获取思维链和最终回答
        reasoning_content = ""
        final_content = ""

        if hasattr(response, 'reasoning_content') and response.reasoning_content:
            reasoning_content = response.reasoning_content

        if hasattr(response, 'content'):
            final_content = response.content
        else:
            final_content = str(response)

        # 可选：显示R1的思维过程（仅在开发模式下）
        if os.getenv('DEBUG_MODE') == 'true':
            with st.expander("🧠 查看R1思维过程", expanded=False):
                if reasoning_content:
                    st.write("**思维链:**")
                    st.code(reasoning_content)
                st.write("**最终回答:**")
                st.code(final_content)

        # 使用最终回答进行JSON解析
        return safe_parse_json(final_content)

    except Exception as e:
        st.error(f"AI分析出错: {e}")
        return safe_parse_json("")

def render_sprite_display(mood, reaction):
    """渲染精灵显示区域"""
    sprite_emoji = SPRITE_EMOTIONS.get(mood, "( ´ ▽ ` )")
    
    # 随机选择装饰元素
    decorations = random.sample(SPRITE_DECORATIONS, 4)
    
    st.markdown(f"""
    <div class="sprite-container">
        <div class="decoration">{decorations[0]}</div>
        <div class="decoration">{decorations[1]}</div>
        <div class="decoration">{decorations[2]}</div>
        <div class="decoration">{decorations[3]}</div>
        <div class="sprite-emoji">{sprite_emoji}</div>
        <div class="sprite-name">小念 (Xiao Nian) ✨</div>
        <div class="sprite-status">💫 心情: {mood} 💫</div>
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
    try:
        llm = initialize_llm()
    except Exception as e:
        st.error(f"❌ AI模型初始化失败: {e}")
        llm = None
    
    # 主要布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🧚‍♀️ 小念的家")
        render_sprite_display(st.session_state.current_mood, st.session_state.current_reaction)
    
    with col2:
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
        elif submitted and not user_input.strip():
            st.warning("记得要告诉小念一些什么哦~ 哪怕只是一个字也好 (◕‿◕)✨")

        # 快捷心情按钮
        st.markdown("##### 🎭 快速表达心情")
        col_a, col_b, col_c = st.columns(3)

        quick_moods = [
            ("😊 开心", "我今天很开心！"),
            ("😢 难过", "我今天有点难过..."),
            ("😴 疲惫", "我今天好累啊..."),
            ("🤔 困惑", "我有点困惑不知道怎么办..."),
            ("😍 兴奋", "我今天超级兴奋！"),
            ("😌 平静", "我今天感觉很平静...")
        ]

        for i, (mood_text, mood_input) in enumerate(quick_moods):
            col = [col_a, col_b, col_c][i % 3]
            with col:
                if st.button(mood_text, key=f"quick_mood_{i}", type="secondary", use_container_width=True):
                    # 直接处理快捷心情
                    with st.spinner(random.choice(LOADING_MESSAGES)):
                        result = analyze_mood(mood_input, llm)

                        st.session_state.current_mood = result['mood_category']
                        st.session_state.current_reaction = result['sprite_reaction']
                        st.session_state.current_gift = {
                            "type": result['gift_type'],
                            "content": result['gift_content']
                        }

                        record = {
                            'timestamp': time.strftime("%H:%M:%S"),
                            'user_input': mood_input,
                            'mood': result['mood_category'],
                            'sprite_reaction': result['sprite_reaction'],
                            'gift_type': result['gift_type'],
                            'gift_content': result['gift_content']
                        }
                        st.session_state.mood_history.append(record)
                        st.rerun()
        
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
