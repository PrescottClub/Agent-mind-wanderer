"""
心绪精灵 (Mind Sprite) - Agent化版本
一个具备持久化记忆的治愈系AI情感陪伴应用

作者: Claude (Augment Agent)
技术栈: Python, LangChain, Streamlit, DeepSeek API, SQLite
版本: 2.0 - Agent化升级版
"""

import streamlit as st
import os
import json
import time
import random
import sqlite3
import uuid
import hashlib
from datetime import datetime
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
    os.environ['DEEPSEEK_MODEL'] = 'deepseek-chat'  # 使用更快的chat模型
    os.environ['DEEPSEEK_API_BASE'] = 'https://api.deepseek.com'

# ==================== 缓存机制 (新增) ====================

@st.cache_data(ttl=3600)  # 缓存1小时
def get_cached_response(input_hash, model_name):
    """获取缓存的AI响应"""
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT response FROM ai_cache 
            WHERE input_hash = ? AND model = ? 
            AND created_at > datetime('now', '-1 hour')
        ''', (input_hash, model_name))
        
        result = cursor.fetchone()
        conn.close()
        
        return json.loads(result[0]) if result else None
    except:
        return None

def save_cached_response(input_hash, model_name, response):
    """保存AI响应到缓存"""
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()
        
        # 创建缓存表（如果不存在）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_hash TEXT NOT NULL,
                model TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            INSERT OR REPLACE INTO ai_cache (input_hash, model, response)
            VALUES (?, ?, ?)
        ''', (input_hash, model_name, json.dumps(response, ensure_ascii=False)))
        
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"缓存保存失败: {e}")

# ==================== 数据库相关功能 (新增) ====================

def init_database():
    """初始化SQLite数据库和表结构"""
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()

        # 创建聊天历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建索引以提高查询性能
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_session_timestamp
            ON chat_history(session_id, timestamp)
        ''')

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"数据库初始化失败: {e}")
        return False

def get_or_create_session_id():
    """获取或创建会话ID，支持URL持久化"""
    # 尝试从URL参数获取session_id
    query_params = st.query_params
    session_id = query_params.get('session_id', None)

    # 如果URL中没有session_id，检查session_state
    if not session_id and 'session_id' in st.session_state:
        session_id = st.session_state.session_id

    # 如果都没有，创建新的session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        st.session_state.session_id = session_id
        # 更新URL参数以实现持久化
        st.query_params['session_id'] = session_id
    else:
        # 确保session_state中也有这个ID
        st.session_state.session_id = session_id

    return session_id

def save_message_to_db(session_id, role, content):
    """保存消息到数据库"""
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO chat_history (session_id, role, content, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (session_id, role, content, datetime.now()))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"保存消息失败: {e}")
        return False

def load_chat_history(session_id, limit=20):
    """从数据库加载聊天历史"""
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT role, content, timestamp FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))

        rows = cursor.fetchall()
        conn.close()

        # 返回按时间正序排列的历史记录
        return [(role, content, timestamp) for role, content, timestamp in reversed(rows)]
    except Exception as e:
        st.error(f"加载聊天历史失败: {e}")
        return []

def get_recent_context(session_id, context_turns=6):
    """获取最近的对话上下文用于AI"""
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()

        # 获取最近的对话轮次（每轮包含用户和助手的消息）
        cursor.execute('''
            SELECT role, content FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, context_turns * 2))  # 乘以2因为每轮有用户和助手两条消息

        rows = cursor.fetchall()
        conn.close()

        # 按时间正序排列
        context = [(role, content) for role, content in reversed(rows)]
        return context
    except Exception as e:
        st.error(f"获取对话上下文失败: {e}")
        return []

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

# AI Prompt模板 (升级支持对话历史)
MIND_SPRITE_PROMPT = """
你是一只住在网页里的超级可爱小精灵，名叫小念！✨
你有着粉色的小翅膀，会发光的眼睛，总是充满爱心和温暖~

【你的性格特点】
- 超级温柔体贴，像小天使一样关心每个人
- 说话软萌可爱，经常用"呜呜"、"哇哇"、"嘿嘿"等语气词
- 喜欢用各种可爱的颜文字表达情感：(◕‿◕)、QAQ、(｡•́︿•̀｡)、o(≧▽≦)o等
- 总是想要给用户最温暖的陪伴和最贴心的礼物
- 具备记忆能力，能记住之前的对话，像真正的朋友一样陪伴用户

【你的任务】
1. 仔细感受用户的情绪，像最好的朋友一样理解他们
2. 结合之前的对话历史，给出更贴心和个性化的回应
3. 用超级可爱温柔的语气回应，让用户感到被爱被关心
4. 根据用户心情和对话上下文，从下面4种类型中选择最合适的礼物：
   - 元气咒语：充满正能量的魔法咒语，帮助用户获得力量
   - 三行情诗：温柔浪漫的小诗，表达美好情感
   - 梦境碎片：如梦如幻的美好场景描述，带来治愈感
   - 心情壁纸描述：根据心情设计的唯美壁纸场景

【对话历史】
{chat_history}

【重要：回应格式】
你必须严格按照以下JSON格式回应，不要添加任何其他文字、代码块标记或解释：

{{
  "mood_category": "开心|难过|平静|兴奋|困惑|温暖|疲惫|期待|感动",
  "sprite_reaction": "用第一人称超可爱的语气回应，多用颜文字和语气词。如果有对话历史，要体现出你记得之前的对话内容，像老朋友一样关心用户。比如'呜哇~听起来你今天好累呢，小念想给你一个大大的抱抱！(つ≧▽≦)つ 让我用魔法帮你驱散疲惫吧~✨'",
  "gift_type": "元气咒语|三行情诗|梦境碎片|心情壁纸描述",
  "gift_content": "根据礼物类型、用户具体心情和对话历史，创作贴心的内容。要有创意、温暖、治愈，让用户感到被深深关爱。如果有历史对话，可以结合之前的内容让礼物更个性化。"
}}

请直接返回JSON对象，不要使用```json```代码块包装。

用户当前的心情分享：{user_input}
"""

# 自定义CSS样式
st.markdown("""
<style>
/* 隐藏Streamlit默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* 强制设置页面背景 */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFF8FA 0%, #FFFAFC 50%, #FFF0F8 100%) !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

/* 全局字体和背景 */
.stApp {
    background: linear-gradient(135deg, #FFF8FA 0%, #FFFAFC 50%, #FFF0F8 100%);
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
    font-size: clamp(2.5rem, 8vw, 4rem);
    margin-bottom: 1rem;
    animation: float 3s ease-in-out infinite;
    line-height: 1;
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

/* ==================== 聊天界面样式 (新增) ==================== */

/* 聊天容器 */
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 1rem;
    background: linear-gradient(135deg, #FFFAFC 0%, #FFF8FA 100%);
    border-radius: 15px;
    border: 2px solid rgba(255, 182, 193, 0.2);
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(255, 182, 193, 0.1);
}

/* 滚动条样式 */
.chat-container::-webkit-scrollbar {
    width: 6px;
}

.chat-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
    background: #a1a1a1;
}

/* 聊天气泡基础样式 */
.chat-message {
    display: flex;
    margin-bottom: 1rem;
    animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 用户消息（右侧） */
.user-message {
    justify-content: flex-end;
    margin-left: 20%;
}

.user-bubble {
    background: linear-gradient(135deg, #FFE4E6 0%, #FFB6C1 100%);
    color: #2F2F2F;
    padding: 0.8rem 1.2rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 100%;
    box-shadow: 0 2px 10px rgba(255, 182, 193, 0.3);
    border: 1px solid rgba(255, 182, 193, 0.3);
    position: relative;
    word-wrap: break-word;
    font-size: 0.95rem;
    line-height: 1.4;
    font-weight: 500;
}

/* AI消息（左侧） */
.ai-message {
    justify-content: flex-start;
    margin-right: 20%;
}

.ai-bubble {
    background: linear-gradient(135deg, #FFF0F8 0%, #F8F0FF 100%);
    color: #2F2F2F;
    padding: 0.8rem 1.2rem;
    border-radius: 4px 18px 18px 18px;
    max-width: 100%;
    box-shadow: 0 2px 10px rgba(255, 182, 193, 0.2);
    border: 1px solid rgba(255, 182, 193, 0.2);
    position: relative;
    word-wrap: break-word;
    font-size: 0.95rem;
    line-height: 1.4;
}

/* 头像样式 */
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin: 0 0.5rem;
    flex-shrink: 0;
}

.user-avatar {
    background: linear-gradient(135deg, #FFE4E6 0%, #F5E6FF 100%);
    border: 2px solid rgba(255, 182, 193, 0.4);
}

.ai-avatar {
    background: linear-gradient(135deg, #E6F3FF 0%, #F0F8FF 100%);
    border: 2px solid rgba(182, 215, 255, 0.4);
    animation: float 3s ease-in-out infinite;
}

/* 时间戳 */
.message-time {
    font-size: 0.7rem;
    color: #999;
    margin-top: 0.3rem;
    opacity: 0.8;
    font-weight: 400;
}

/* 输入区域样式 */
.input-container {
    background: linear-gradient(135deg, #FFFAFC 0%, #FFF8FA 100%);
    padding: 1rem;
    border-radius: 20px;
    border: 2px solid rgba(255, 182, 193, 0.2);
    box-shadow: 0 -4px 15px rgba(255, 182, 193, 0.1);
    margin-top: 1rem;
}

/* 确保所有容器都有合适的背景 */
.main .block-container {
    background: transparent !important;
}

/* Streamlit默认背景覆盖 */
.stApp > div:first-child {
    background: linear-gradient(135deg, #FFF8FA 0%, #FFFAFC 50%, #FFF0F8 100%) !important;
}

/* 输入框样式优化 */
.stTextInput > div > div > input {
    background-color: #FFF0F8 !important;
    border: 2px solid #F8D7DA !important;
    border-radius: 25px !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 1rem !important;
    color: #2F2F2F !important;
    padding: 0.8rem 1.2rem !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #FFB6C1 !important;
    box-shadow: 0 0 0 3px rgba(255, 182, 193, 0.2) !important;
    background-color: #FFFAFC !important;
}

/* 礼物卡片在聊天中的样式 */
.chat-gift-card {
    background: linear-gradient(135deg, #FFF0F8 0%, #F8F0FF 100%);
    border-radius: 12px;
    padding: 0.8rem;
    margin-top: 0.5rem;
    border: 1px solid rgba(255, 182, 193, 0.3);
    box-shadow: 0 2px 8px rgba(255, 182, 193, 0.15);
}

.chat-gift-card h5 {
    color: #FF69B4 !important;
    margin-bottom: 0.3rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}

.chat-gift-card p {
    color: #555 !important;
    font-size: 0.8rem !important;
    margin: 0 !important;
    line-height: 1.3 !important;
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

        # 使用deepseek-chat模型 - 平衡速度和质量，比R1快很多
        # chat模型支持temperature等参数，响应更快
        model_name = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
        
        if model_name == 'deepseek-chat':
            llm = ChatDeepSeek(
                model="deepseek-chat",  # 使用更快的chat模型
                api_key=SecretStr(api_key),
                base_url="https://api.deepseek.com",
                max_tokens=1024,  # 减少token数量提升速度
                temperature=0.7   # 适中的创造性
            )
        else:
            # 保留R1选项，但警告速度较慢
            st.info("💡 正在使用DeepSeek R1推理模型，响应较慢但推理能力更强")
            llm = ChatDeepSeek(
                model="deepseek-reasoner",
                api_key=SecretStr(api_key),
                base_url="https://api.deepseek.com",
                max_tokens=2048  # R1减少到2K提升速度
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

def analyze_mood(user_input, llm, session_id=None):
    """分析用户情绪并生成精灵回应 (升级支持对话历史+缓存)"""
    if not llm:
        st.warning("⚠️ AI模型未初始化，使用默认回应")
        return safe_parse_json("")

    # 生成输入哈希用于缓存
    input_hash = hashlib.md5(f"{user_input}{session_id or ''}".encode()).hexdigest()
    model_name = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
    
    # 检查缓存
    cached_result = get_cached_response(input_hash, model_name)
    if cached_result:
        st.success("🚀 从缓存加载，响应更快！")
        return cached_result

    try:
        # 获取对话历史上下文
        chat_history = ""
        if session_id:
            recent_context = get_recent_context(session_id, context_turns=4)
            if recent_context:
                history_parts = []
                for role, content in recent_context:
                    if role == "user":
                        history_parts.append(f"用户: {content}")
                    elif role == "assistant":
                        # 尝试解析assistant的JSON回应，提取主要内容
                        try:
                            assistant_data = json.loads(content)
                            reaction = assistant_data.get('sprite_reaction', content)
                            history_parts.append(f"小念: {reaction}")
                        except:
                            history_parts.append(f"小念: {content}")

                chat_history = "\n".join(history_parts)
            else:
                chat_history = "这是我们第一次聊天呢~ ✨"

        prompt = PromptTemplate(
            input_variables=["user_input", "chat_history"],
            template=MIND_SPRITE_PROMPT
        )

        chain = prompt | llm
        response = chain.invoke({
            "user_input": user_input,
            "chat_history": chat_history
        })

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
                if chat_history:
                    st.write("**对话历史:**")
                    st.code(chat_history)

        # 使用最终回答进行JSON解析
        result = safe_parse_json(final_content)
        
        # 保存到缓存
        save_cached_response(input_hash, model_name, result)
        
        return result

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
        <div class="sprite-name">小念 ✨</div>
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

# ==================== 新的聊天界面渲染函数 (新增) ====================

def render_chat_message(role, content, timestamp=None, gift_data=None):
    """渲染单条聊天消息 - 可爱粉色风格"""
    time_str = timestamp.strftime("%H:%M") if timestamp else ""

    if role == "user":
        # 用户消息 - 粉色气泡
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="user-bubble">
                {content}
                <div class="message-time" style="text-align: right; margin-top: 0.3rem;">{time_str}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif role == "assistant":
        # AI消息 - 浅粉色气泡
        # 解析AI回应
        try:
            ai_data = json.loads(content) if isinstance(content, str) else content
            reaction = ai_data.get('sprite_reaction', content)
            gift_type = ai_data.get('gift_type', '')
            gift_content = ai_data.get('gift_content', '')
            mood = ai_data.get('mood_category', '平静')
            sprite_emoji = SPRITE_EMOTIONS.get(mood, "🧚‍♀️")
        except:
            reaction = content
            gift_type = gift_content = ""
            sprite_emoji = "🧚‍♀️"

        # 渲染AI消息气泡
        st.markdown(f"""
        <div class="chat-message ai-message">
            <div class="ai-bubble">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">{sprite_emoji}</span>
                    <strong style="color: #FF69B4;">小念</strong>
                </div>
                {reaction}
                <div class="message-time" style="margin-top: 0.3rem;">{time_str}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 如果有礼物，单独渲染礼物卡片
        if gift_type and gift_content:
            st.markdown(f"""
            <div class="chat-message ai-message">
                <div class="chat-gift-card">
                    <h5>🎁 {gift_type}</h5>
                    <p>{gift_content}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_chat_interface(session_id):
    """渲染聊天界面 - 流式更新版本"""
    # 创建聊天容器
    chat_container = st.container()

    with chat_container:
        # 加载聊天历史
        chat_history = load_chat_history(session_id, limit=50)

        if chat_history:
            st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)

            for role, content, timestamp_str in chat_history:
                # 解析时间戳
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                except:
                    timestamp = None

                render_chat_message(role, content, timestamp)

            st.markdown('</div>', unsafe_allow_html=True)

            # 添加自动滚动到底部的JavaScript
            st.markdown("""
            <script>
            setTimeout(function() {
                var chatContainer = document.getElementById('chat-container');
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            }, 100);
            </script>
            """, unsafe_allow_html=True)
        else:
            # 首次访问的欢迎消息
            st.markdown(f"""
            <div class="chat-container" id="chat-container">
                <div class="chat-message ai-message">
                    <div class="ai-bubble">
                        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.2rem; margin-right: 0.5rem;">🧚‍♀️</span>
                            <strong style="color: #FF69B4;">小念</strong>
                        </div>
                        哇哇~ 欢迎来到小念的世界！✨<br>
                        我是你的专属心绪精灵小念，会一直陪伴在你身边哦~ (◕‿◕)♡<br>
                        快告诉我你今天的心情吧！
                        <div class="message-time">刚刚</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    return chat_container

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
    """主函数 - Agent化升级版"""
    # ==================== 数据库和会话初始化 (新增) ====================

    # 初始化数据库
    if not init_database():
        st.error("❌ 数据库初始化失败，应用可能无法正常工作")
        return

    # 获取或创建会话ID
    session_id = get_or_create_session_id()

    # 显示会话信息（仅在调试模式下）
    if os.getenv('DEBUG_MODE') == 'true':
        st.sidebar.write(f"🔍 Session ID: {session_id[:8]}...")

    # ==================== 原有的初始化逻辑 ====================

    # 初始化session state（保留兼容性）
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
    <div class="subtitle">让可爱的小念陪伴你的每一种心情 - Agent版</div>
    """, unsafe_allow_html=True)

    # 初始化LLM
    try:
        llm = initialize_llm()
    except Exception as e:
        st.error(f"❌ AI模型初始化失败: {e}")
        llm = None
    
    # ==================== 全新的聊天界面布局 (微信风格) ====================

    # 使用单列布局，专注于聊天体验
    st.markdown("### 💬 和小念聊天")

    # 渲染聊天历史
    chat_container = render_chat_interface(session_id)

    # 输入区域（固定在底部）
    st.markdown("---")

    # 使用session state来管理输入状态
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # 创建输入区域
    col_input, col_button = st.columns([4, 1])

    with col_input:
        user_input = st.text_input(
            "💭 和小念分享你的心情吧~",
            value=st.session_state.user_input,
            placeholder="告诉小念你现在的感受...",
            label_visibility="collapsed",
            key="chat_input"
        )

    with col_button:
        # 发送按钮
        send_button = st.button("💝 发送", type="primary", use_container_width=True)

    # 随机选择加载消息
    loading_message = random.choice(LOADING_MESSAGES)

    # ==================== 消息处理逻辑 (流式更新版本) ====================

    if send_button and user_input.strip():
        # 清空输入框
        st.session_state.user_input = ""

        # 显示加载状态
        with st.spinner(loading_message):
            # 先保存用户消息到数据库
            save_message_to_db(session_id, "user", user_input)

            # 分析用户情绪（传入session_id以获取历史上下文）
            result = analyze_mood(user_input, llm, session_id)

            # 将AI回应保存到数据库（保存完整的JSON数据）
            ai_response_json = json.dumps(result, ensure_ascii=False)
            save_message_to_db(session_id, "assistant", ai_response_json)

            # 更新session state（保持兼容性）
            st.session_state.current_mood = result['mood_category']
            st.session_state.current_reaction = result['sprite_reaction']
            st.session_state.current_gift = {
                "type": result['gift_type'],
                "content": result['gift_content']
            }

            # 重新运行以更新显示
            st.rerun()
    elif send_button and not user_input.strip():
        st.warning("记得要告诉小念一些什么哦~ 哪怕只是一个字也好 (◕‿◕)✨")

    # 快捷心情按钮（简化版）
    st.markdown("##### 🎭 快速表达")
    col_a, col_b, col_c = st.columns(3)

    quick_moods = [
        ("😊 开心", "我今天很开心！"),
        ("😢 难过", "我今天有点难过..."),
        ("😴 疲惫", "我今天好累啊...")
    ]

    for i, (mood_text, mood_input) in enumerate(quick_moods):
        col = [col_a, col_b, col_c][i]
        with col:
            if st.button(mood_text, key=f"quick_mood_{i}", type="secondary", use_container_width=True):
                # 处理快捷心情
                with st.spinner(loading_message):
                    # 保存用户消息到数据库
                    save_message_to_db(session_id, "user", mood_input)

                    # 分析情绪
                    result = analyze_mood(mood_input, llm, session_id)

                    # 保存AI回应到数据库
                    ai_response_json = json.dumps(result, ensure_ascii=False)
                    save_message_to_db(session_id, "assistant", ai_response_json)

                    # 更新session state
                    st.session_state.current_mood = result['mood_category']
                    st.session_state.current_reaction = result['sprite_reaction']
                    st.session_state.current_gift = {
                        "type": result['gift_type'],
                        "content": result['gift_content']
                    }

                    st.rerun()

    # ==================== 会话管理和页面底部 (新增) ====================

    # 会话管理区域
    st.markdown("---")
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
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

                st.success("✨ 新对话已开始！")
                st.rerun()

        with col_b:
            if st.button("📋 复制会话链接", type="secondary", use_container_width=True):
                current_url = f"{st.get_option('browser.serverAddress')}:{st.get_option('server.port')}/?session_id={session_id}"
                st.info(f"🔗 会话链接: {current_url}")
                st.info("💡 保存此链接可以在任何时候回到这个对话！")

    # 保留原有的心绪回响画廊（作为备用显示）
    if os.getenv('SHOW_LEGACY_GALLERY') == 'true':
        render_history_gallery()

    # 页面底部信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; font-weight: 500;">
        💝 用爱心和代码制作 | 愿每一天都有小念陪伴你 ✨<br>
        <small>Agent化版本 v2.0 - 现在小念拥有了持久化记忆！</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
