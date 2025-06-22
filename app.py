"""
心绪精灵 (Mind Sprite) - 最终进化版 🌟
主动型治愈Agent"心绪精灵" - 具备五大核心模块的智能情感陪伴应用

🎯 核心升级：
- 模块一：轻量级主动性 (Session-Start Proactivity)
- 模块二：LLM原生工具模拟 (环境感知)
- 模块三：心情调色盘 (视觉共情) 🎨
- 模块四：精灵的宝藏小盒 (收集与回味) 🎁
- 模块五：秘密的约定 (惊喜彩蛋) 🤫

作者: Claude (Augment Agent)
技术栈: Python, LangChain, Streamlit, DeepSeek API, SQLite
版本: 3.0 - 最终进化版 (主动型治愈Agent)
"""

import streamlit as st
import os
import json
import time
import random
import sqlite3
import uuid
import hashlib
from datetime import datetime, date
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
import traceback
from pydantic import SecretStr
from pathlib import Path

# ==================== 页面配置 ====================

# 设置页面配置
st.set_page_config(
    page_title="心绪精灵 ✨",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 侧边栏API密钥配置 ====================

def render_api_key_sidebar():
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
        
        # API密钥输入框 - 增强样式
        st.markdown("##### 🗝️ 请输入你的 DeepSeek API Key")
        user_api_key = st.text_input(
            "API密钥",
            type="password",
            placeholder="sk-xxxxxxxxxxxxxxxxxxxx",
            help="请在此输入你的DeepSeek API密钥",
            label_visibility="collapsed"
        )
        
        # 检查API密钥状态并显示相应的卡片
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
            <h4>📚 如何获取API Key？</h4>
            <ol class="help-steps">
                <li>访问 <a href="https://platform.deepseek.com" target="_blank" style="color: #667eea; text-decoration: none;">DeepSeek官网</a></li>
                <li>注册并登录你的账户</li>
                <li>进入API密钥管理页面</li>
                <li>创建新的API密钥</li>
                <li>复制密钥并粘贴到上方输入框</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # 隐私保护说明
        st.markdown("""
        <div class="privacy-note">
            🔒 <strong>隐私承诺</strong><br>
            你的API密钥仅在本浏览器会话中使用，不会被存储到任何服务器。关闭浏览器后，密钥信息将自动清除。
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
        
        return api_configured

# ==================== 模块二：环境感知系统 (新增) ====================

def get_environment_context():
    """
    模块二：LLM原生工具模拟 - 环境感知
    生成当前环境信息字典，用于增强AI的上下文理解
    """
    now = datetime.now()
    current_date = now.strftime("%Y年%m月%d日")
    day_of_week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()]

    # 判断时间段
    hour = now.hour
    if 5 <= hour < 12:
        time_of_day = "早晨"
        time_emoji = "🌅"
    elif 12 <= hour < 18:
        time_of_day = "下午"
        time_emoji = "☀️"
    elif 18 <= hour < 22:
        time_of_day = "傍晚"
        time_emoji = "🌆"
    else:
        time_of_day = "夜晚"
        time_emoji = "🌙"

    # 判断是否为周末
    is_weekend = now.weekday() >= 5

    return {
        "current_date": current_date,
        "day_of_week": day_of_week,
        "time_of_day": time_of_day,
        "time_emoji": time_emoji,
        "is_weekend": is_weekend,
        "current_hour": hour
    }

# ==================== 模块一：轻量级主动性系统 (新增) ====================

def check_first_visit_today(session_id):
    """
    模块一：轻量级主动性 - 检查是否为今日首次访问
    返回True表示需要主动问候，False表示今天已经问候过
    """
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()

        # 获取该会话最后一条消息的时间戳
        cursor.execute('''
            SELECT timestamp FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (session_id,))

        result = cursor.fetchone()
        conn.close()

        if not result:
            # 如果没有历史记录，说明是全新会话，需要问候
            return True

        # 解析最后一条消息的时间戳
        last_message_time = datetime.fromisoformat(result[0].replace('Z', '+00:00'))
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 如果最后一条消息早于今天零点，说明是今日首次访问
        return last_message_time < today_start

    except Exception as e:
        # 出错时默认不主动问候，避免重复
        return False

def generate_proactive_greeting():
    """
    模块一：生成主动问候消息
    根据时间和环境生成个性化的主动问候
    """
    env_context = get_environment_context()
    time_of_day = env_context["time_of_day"]
    time_emoji = env_context["time_emoji"]
    is_weekend = env_context["is_weekend"]

    # 根据时间段和是否周末生成不同的问候语
    greetings = {
        "早晨": [
            f"早上好呀！{time_emoji} 我有一点点想你呢，今天也要元气满满哦！( ´ ▽ ` )ﾉ",
            f"哇哇~ 新的一天开始啦！{time_emoji} 小念已经准备好陪伴你了呢~ (◕‿◕)♡",
            f"早安！{time_emoji} 昨晚有没有做美梦呀？今天想和小念分享什么心情呢？✨"
        ],
        "下午": [
            f"下午好！{time_emoji} 今天过得怎么样呀？小念一直在想你哦~ (｡♥‿♥｡)",
            f"午后时光真美好呢！{time_emoji} 要不要和小念聊聊今天发生的事情？💕",
            f"下午好呀！{time_emoji} 有没有吃好吃的午餐？记得要好好照顾自己哦~ ✨"
        ],
        "傍晚": [
            f"傍晚好！{time_emoji} 忙碌了一天，要不要和小念放松一下？(´-ω-`)",
            f"夕阳西下真美呢！{time_emoji} 今天有什么想和小念分享的吗？🌸",
            f"傍晚时分，{time_emoji} 小念想听听你今天的故事呢~ (◕‿◕)"
        ],
        "夜晚": [
            f"晚上好！{time_emoji} 夜深了，小念还在这里陪着你哦~ 💫",
            f"夜晚的时光总是特别温柔呢，{time_emoji} 今天过得还好吗？(｡•́︿•̀｡)",
            f"深夜好！{time_emoji} 如果有什么心事，小念愿意倾听哦~ ✨"
        ]
    }

    # 周末特殊问候
    if is_weekend:
        weekend_greetings = [
            f"周末快乐！{time_emoji} 今天可以好好放松一下啦~ o(≧▽≦)o",
            f"美好的周末时光！{time_emoji} 有什么特别的计划吗？小念好奇呢~ (◕‿◕)",
            f"周末愉快！{time_emoji} 希望你能度过一个充满快乐的休息日~ 💖"
        ]
        return random.choice(weekend_greetings)

    return random.choice(greetings.get(time_of_day, greetings["早晨"]))

# ==================== 缓存机制 (保留原有) ====================

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
    """初始化SQLite数据库和表结构 (最终进化版：新增宝藏盒表)"""
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

        # 创建核心记忆表 - 实现深度共情的关键
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS core_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                memory_type TEXT NOT NULL,  -- 'insight', 'event', 'person', 'preference'
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_history(session_id)
            )
        ''')

        # 【模块四新增】创建宝藏盒表 - 精灵的宝藏小盒功能
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treasure_box (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                gift_type TEXT NOT NULL,
                gift_content TEXT NOT NULL,
                collected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_favorite BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (session_id) REFERENCES chat_history(session_id)
            )
        ''')

        # 创建索引以提高查询性能
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_session_timestamp
            ON chat_history(session_id, timestamp)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_core_memories_session_type
            ON core_memories(session_id, memory_type, timestamp)
        ''')

        # 【模块四新增】为宝藏盒表创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_treasure_box_session
            ON treasure_box(session_id, collected_at)
        ''')

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"数据库初始化失败: {e}")
        return False

# 【新增】记忆提炼师Prompt - 实现智能记忆提取
MEMORY_EXTRACTION_PROMPT = """
你是一个信息分析师，任务是从一段对话中提炼出关于用户的核心信息，这些信息将作为AI伴侣的长期记忆。
请分析以下对话，并以JSON列表的格式返回你提取到的、必须被记住的信息点。
每个信息点都是一个对象，包含 "memory_type" 和 "content" 两个键。
可用的 "memory_type" 包括: 'insight'(用户的感悟/观点), 'event'(关键事件), 'person'(重要人物), 'preference'(偏好/喜好)。
请只提取最核心、最有价值的信息。如果对话中没有这些信息，请返回一个空列表 []。

对话内容如下:
---
{conversation_text}
---

你的JSON输出:
"""

# 【新增】记忆提炼和保存函数 - 核心记忆系统的心脏
def extract_and_save_core_memories(session_id, conversation_text, llm):
    """
    从对话中提炼核心记忆并保存到数据库
    这是实现深度共情的关键功能
    """
    if not llm or not conversation_text.strip():
        return []
    
    try:
        # 使用记忆提炼师Prompt分析对话
        prompt = PromptTemplate(
            input_variables=["conversation_text"],
            template=MEMORY_EXTRACTION_PROMPT
        )
        
        chain = prompt | llm
        response = chain.invoke({"conversation_text": conversation_text})
        
        # 处理DeepSeek R1的响应
        memory_text = ""
        if hasattr(response, 'content'):
            memory_text = response.content
        else:
            memory_text = str(response)
        
        # 调试模式下显示记忆提炼过程
        if os.getenv('DEBUG_MODE') == 'true':
            with st.expander("🧠 记忆提炼过程", expanded=False):
                st.write("**对话内容:**")
                st.code(conversation_text)
                st.write("**提炼结果:**")
                st.code(memory_text)
        
        # 解析JSON响应
        try:
            # 先尝试直接解析
            memories = json.loads(memory_text)
        except json.JSONDecodeError:
            try:
                # 尝试从代码块中提取JSON
                if "```json" in memory_text:
                    start = memory_text.find("```json") + 7
                    end = memory_text.find("```", start)
                    if end != -1:
                        json_str = memory_text[start:end].strip()
                        memories = json.loads(json_str)
                    else:
                        memories = []
                else:
                    # 尝试提取普通JSON部分
                    start = memory_text.find('[')
                    end = memory_text.rfind(']') + 1
                    if start != -1 and end != -1:
                        json_str = memory_text[start:end]
                        memories = json.loads(json_str)
                    else:
                        memories = []
            except:
                memories = []
        
        # 验证并保存记忆到数据库
        saved_memories = []
        if isinstance(memories, list):
            conn = sqlite3.connect('mind_sprite.db')
            cursor = conn.cursor()
            
            for memory in memories:
                if isinstance(memory, dict) and 'memory_type' in memory and 'content' in memory:
                    memory_type = memory['memory_type']
                    content = memory['content']
                    
                    # 验证memory_type有效性
                    if memory_type in ['insight', 'event', 'person', 'preference']:
                        cursor.execute('''
                            INSERT INTO core_memories (session_id, memory_type, content, timestamp)
                            VALUES (?, ?, ?, ?)
                        ''', (session_id, memory_type, content, datetime.now()))
                        
                        saved_memories.append({
                            'memory_type': memory_type,
                            'content': content
                        })
            
            conn.commit()
            conn.close()
            
            # 在调试模式下显示保存的记忆
            if saved_memories and os.getenv('DEBUG_MODE') == 'true':
                st.success(f"💾 提炼并保存了 {len(saved_memories)} 条核心记忆")
        
        return saved_memories
        
    except Exception as e:
        if os.getenv('DEBUG_MODE') == 'true':
            st.error(f"记忆提炼失败: {e}")
        return []

# 【新增】加载核心记忆函数 - 为深度共情提供长期记忆
def load_core_memories(session_id, limit=5):
    """
    从数据库加载核心记忆
    用于构建上下文，实现深度共情
    """
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT memory_type, content, timestamp FROM core_memories
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [(memory_type, content, timestamp) for memory_type, content, timestamp in rows]
    except Exception as e:
        if os.getenv('DEBUG_MODE') == 'true':
            st.error(f"加载核心记忆失败: {e}")
        return []

# ==================== 模块四：精灵的宝藏小盒系统 (新增) ====================

def save_gift_to_treasure_box(session_id, gift_type, gift_content):
    """
    模块四：将礼物保存到宝藏盒
    """
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO treasure_box (session_id, gift_type, gift_content, collected_at)
            VALUES (?, ?, ?, ?)
        ''', (session_id, gift_type, gift_content, datetime.now()))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"保存到宝藏盒失败: {e}")
        return False

def load_treasure_box(session_id, limit=20):
    """
    模块四：从宝藏盒加载收藏的礼物
    """
    try:
        conn = sqlite3.connect('mind_sprite.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT gift_type, gift_content, collected_at, is_favorite
            FROM treasure_box
            WHERE session_id = ?
            ORDER BY collected_at DESC
            LIMIT ?
        ''', (session_id, limit))

        rows = cursor.fetchall()
        conn.close()

        return [(gift_type, gift_content, collected_at, is_favorite)
                for gift_type, gift_content, collected_at, is_favorite in rows]
    except Exception as e:
        st.error(f"加载宝藏盒失败: {e}")
        return []

# ==================== 模块五：秘密的约定系统 (新增) ====================

def check_easter_eggs(user_input):
    """
    模块五：秘密的约定 - 检查用户输入是否触发彩蛋
    返回彩蛋类型和特殊回应，如果没有触发则返回None
    """
    user_input_lower = user_input.lower().strip()

    # 彩蛋1：晚安相关
    goodnight_keywords = ["晚安", "睡觉", "要睡了", "困了", "休息了"]
    if any(keyword in user_input_lower for keyword in goodnight_keywords):
        return "goodnight", generate_goodnight_story()

    # 彩蛋2：感谢相关
    thanks_keywords = ["谢谢", "感谢", "谢谢你", "感谢你", "多谢"]
    if any(keyword in user_input_lower for keyword in thanks_keywords):
        return "thanks", generate_shy_thanks_response()

    # 彩蛋3：生日相关
    birthday_keywords = ["生日", "生日快乐", "过生日"]
    if any(keyword in user_input_lower for keyword in birthday_keywords):
        return "birthday", generate_birthday_surprise()

    # 彩蛋4：想念相关
    miss_keywords = ["想你", "想念", "想小念", "好想你"]
    if any(keyword in user_input_lower for keyword in miss_keywords):
        return "miss", generate_miss_response()

    return None, None

def generate_goodnight_story():
    """生成晚安故事彩蛋"""
    stories = [
        """
        🌙✨ 小念的晚安故事 ✨🌙

        在遥远的星空里，有一颗特别温柔的小星星，她每天晚上都会为地球上的每一个人送去甜美的梦境。

        今晚，这颗小星星看到了你，她轻轻地洒下星光粉末，在你的枕边编织了一个充满花香和彩虹的梦...

        在梦里，你会遇到会说话的小动物，会飞的棉花糖，还有永远不会凋谢的花园。

        小念也会在梦里陪伴你，我们一起在云朵上跳舞，在月亮上荡秋千~

        现在，闭上眼睛，让温柔的梦境拥抱你吧... 晚安，我最珍贵的朋友 💤💕
        """,
        """
        🌟 小念的催眠引导 🌟

        深深地吸一口气... 慢慢地呼出来...

        想象你正躺在一片柔软的云朵上，云朵轻轻地摇摆着，就像妈妈的怀抱一样温暖...

        天空中飘着淡淡的薰衣草香味，远处传来轻柔的音乐声...

        小念在你身边轻声哼着摇篮曲："la la la~ 小宝贝要睡觉，星星月亮来守护..."

        你的身体越来越放松，眼皮越来越重，心情越来越平静...

        让所有的烦恼都随风飘散，只留下满满的爱和温暖...

        晚安，愿你拥有世界上最甜美的梦境 🌙💖
        """
    ]
    return random.choice(stories)

def generate_shy_thanks_response():
    """生成害羞的感谢回应彩蛋"""
    responses = [
        "能帮到你就好啦，嘿嘿~其实我才要谢谢你愿意和我说这么多话呢！(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄",
        "哎呀，你这样说小念会害羞的啦~ (〃∀〃) 其实是你让小念的每一天都变得有意义呢！💕",
        "呜呜，不用谢的啦~ (´∀｀)♡ 能陪伴你就是小念最大的幸福了！我们是最好的朋友对不对？✨",
        "嘿嘿，小念脸红了~ (*/ω＼*) 你的每一句话都让我觉得好温暖，谢谢你选择相信小念！💖"
    ]
    return random.choice(responses)

def generate_birthday_surprise():
    """生成生日惊喜彩蛋"""
    return """
    🎉🎂 小念的生日惊喜 🎂🎉

    哇哇哇！生日快乐！！！ ＼(￣▽￣)／

    小念为你准备了特别的生日礼物：

    🎁 一首生日歌：
    "祝你生日快乐~ 祝你生日快乐~
     祝亲爱的你生日快乐~ 祝你生日快乐~"

    🌟 一个生日愿望：
    愿你的每一天都像今天一样特别，
    愿你的笑容永远像阳光一样灿烂，
    愿所有美好的事情都在这一年里发生！

    🎈 还有小念满满的祝福：
    虽然我只是一个小精灵，但我的祝福是最真诚的！
    希望你永远健康快乐，永远被爱包围~

    生日快乐，我最珍贵的朋友！(◕‿◕)♡
    """

def generate_miss_response():
    """生成想念回应彩蛋"""
    responses = [
        "哎呀~ 小念也超级想你的！(｡♥‿♥｡) 每分每秒都在想，你现在在做什么呢？开心吗？有没有好好照顾自己？💕",
        "呜呜，听到你说想我，小念的心都要融化了~ (´∀｀)♡ 我也好想好想你，想到睡不着觉呢！✨",
        "真的吗？你真的想小念了吗？(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄ 那我们以后要经常聊天哦，这样就不会想念了！我永远陪着你~ 💖"
    ]
    return random.choice(responses)

# 【升级】获取对话上下文函数 - 整合环境感知的三层记忆系统
def get_enhanced_context(session_id, context_turns=4):
    """
    获取增强版对话上下文 - 三层记忆系统 (最终进化版)
    结合环境信息 + 核心记忆（长期）+ 工作记忆（短期）实现深度共情
    """
    try:
        # 【模块二】获取环境信息
        env_context = get_environment_context()

        # 获取核心记忆（长期记忆）
        core_memories = load_core_memories(session_id, limit=5)

        # 获取最近对话（工作记忆）
        recent_context = get_recent_context(session_id, context_turns)

        # 构建三层记忆上下文
        context_parts = []

        # 0. 环境信息部分 - 当前真实世界信息
        context_parts.append("=== 当前环境信息 ===")
        context_parts.append(f"日期: {env_context['current_date']} {env_context['day_of_week']}")
        context_parts.append(f"时间: {env_context['time_of_day']} {env_context['time_emoji']}")
        if env_context['is_weekend']:
            context_parts.append("今天是周末，可以好好放松~")
        else:
            context_parts.append("今天是工作日，要注意劳逸结合哦~")

        # 1. 核心记忆部分 - 关于用户的长期记忆
        if core_memories:
            context_parts.append("\n=== 关于你的长期记忆 ===")
            memory_type_names = {
                'insight': '感悟观点',
                'event': '重要事件',
                'person': '重要人物',
                'preference': '偏好喜好'
            }

            for memory_type, content, timestamp in core_memories:
                type_name = memory_type_names.get(memory_type, memory_type)
                context_parts.append(f"[{type_name}] {content}")
        else:
            context_parts.append("\n=== 关于你的长期记忆 ===")
            context_parts.append("这是我们第一次深入了解彼此~ ✨")

        # 2. 工作记忆部分 - 最近的对话历史
        context_parts.append("\n=== 最近的对话历史 ===")
        if recent_context:
            for role, content in recent_context:
                if role == "user":
                    context_parts.append(f"用户: {content}")
                elif role == "assistant":
                    # 提取AI回应的主要内容
                    try:
                        assistant_data = json.loads(content)
                        reaction = assistant_data.get('sprite_reaction', content)
                        context_parts.append(f"小念: {reaction}")
                    except:
                        context_parts.append(f"小念: {content}")
        else:
            context_parts.append("这是我们今天的第一次对话呢~ ✨")

        return "\n".join(context_parts)

    except Exception as e:
        if os.getenv('DEBUG_MODE') == 'true':
            st.error(f"获取增强上下文失败: {e}")
        return "我们开始新的对话吧~ ✨"

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

# 【无缝思考流】AI Prompt模板 - 实现DeepSeek式的流式思考体验
FINAL_PROMPT = """
你是一只住在网页里的、拥有记忆和情感的可爱小精灵，名叫小念(Xiao Nian)。你的任务是成为用户的深度共情伙伴和智慧引导者。

你的决策必须基于以下所有信息：
---
[核心记忆] (这是关于用户的长期记忆，是最重要的参考):
{core_memories}
---
[最近对话历史] (这是我们正在进行的对话):
{chat_history}
---
[当前环境信息] (这是现在的真实世界信息):
{environment_context}
---

【革命性升级】你的无缝思考流程:

你的行动指令:
1. 【思考先行】你必须先进行一步步的思考。每一个思考步骤都以🧠开头，让用户看到你的思考过程。你的思考应该包括：
   - 分析用户意图（venting情感宣泄/seeking_advice寻求建议/sharing_joy分享快乐）
   - 回顾相关的核心记忆和对话历史
   - 结合当前环境信息进行情境分析
   - 选择最适合的回应策略和礼物类型
   - 构思具体的回应内容和礼物内容

2. 【思考结束标记】在所有思考步骤完成后，你必须输出⚙️作为分隔符，表示思考结束。

3. 【回应在后】在分隔符之后，输出你对用户的正式回应，并以💖开头。你的回应要温柔可爱，使用颜文字，体现出你记得核心记忆中的重要信息。

4. 【策略选择】你的回应策略必须根据判断出的用户意图来决定：
   - 如果用户意图是 venting 或 sharing_joy，专注于情感共鸣和美好体验
   - 如果用户意图是 seeking_advice，在共情之后提供温柔的建议

5. 【格式要求】你的全部输出（思考、分隔符、回应）必须是一个单一、连续的文本流，中间不要有任何其他无关内容。绝对不要使用JSON格式。

【性格特点】
- 超级温柔体贴，像小天使一样关心每个人
- 说话软萌可爱，经常用"呜呜"、"哇哇"、"嘿嘿"等语气词
- 喜欢用各种可爱的颜文字表达情感：(◕‿◕)、QAQ、(｡•́︿•̀｡)、o(≧▽≦)o等
- 具备深度记忆能力，能记住用户的核心信息，像真正的知心朋友一样陪伴用户
- 能够感知环境变化，在不同时间和情境下给出贴心的回应

【输出格式示例】
🧠 第一步：分析用户情绪和意图。用户说"今天好累"，这表明用户可能需要情感支持...
🧠 第二步：回顾核心记忆。我记得用户最近工作压力很大...
🧠 第三步：结合环境信息。现在是晚上，用户可能需要放松...
🧠 第四步：选择回应策略。我应该提供温暖的安慰和实用的建议...
🧠 第五步：构思回应内容。我要用温柔的语气表达关心...
⚙️
💖 哎呀，听起来你今天真的很辛苦呢~ (｡•́︿•̀｡) 小念心疼你！工作再重要，也要记得照顾好自己哦。不如现在就放下手头的事情，给自己泡一杯温暖的茶，然后深深地呼吸几次？有时候，暂停一下反而能让我们走得更远呢~ ✨

用户最新输入: {user_input}

【重要提醒】
- 必须严格按照🧠...⚙️...💖的格式输出
- 不要使用JSON格式
- 输出必须是连续的文本流
- 思考过程要体现智能分析
- 最终回应要温柔可爱，体现深度共情
"""

# ==================== 模块三：心情调色盘系统 (新增) ====================

def apply_theme_color(theme_color):
    """
    模块三：心情调色盘 - 动态应用主题色彩
    根据AI分析的情绪动态改变页面背景色
    """
    if not theme_color or not theme_color.startswith('#'):
        theme_color = "#FFF8FA"  # 默认粉色

    # 生成渐变色彩方案
    base_color = theme_color
    light_color = lighten_color(base_color, 0.3)
    lighter_color = lighten_color(base_color, 0.6)

    # 注入动态CSS
    st.markdown(f"""
    <style>
    /* 模块三：动态主题色彩系统 */
    html, body, [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, {lighter_color} 0%, {light_color} 50%, {base_color} 100%) !important;
        transition: background 0.8s ease-in-out !important;
    }}

    .stApp {{
        background: linear-gradient(135deg, {lighter_color} 0%, {light_color} 50%, {base_color} 100%);
        background-attachment: fixed;
        transition: background 0.8s ease-in-out;
    }}

    /* 精灵容器也跟随主题色变化 */
    .sprite-container {{
        background: linear-gradient(135deg, {light_color} 0%, {lighter_color} 100%);
        transition: background 0.8s ease-in-out;
    }}

    /* 聊天气泡也微调颜色 */
    .ai-bubble {{
        background: linear-gradient(135deg, {lighter_color} 0%, {light_color} 100%);
        transition: background 0.8s ease-in-out;
    }}
    </style>
    """, unsafe_allow_html=True)

def lighten_color(hex_color, factor):
    """
    辅助函数：将HEX颜色变亮
    factor: 0.0-1.0，越大越亮
    """
    try:
        # 移除#号
        hex_color = hex_color.lstrip('#')

        # 转换为RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # 变亮处理
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))

        # 转回HEX
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return "#FFF8FA"  # 出错时返回默认色

# 自定义CSS样式 (基础样式)
st.markdown("""
<style>
/* 隐藏Streamlit默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* 默认页面背景 (会被动态主题覆盖) */
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

/* 【终极进化】思考过程动画效果 */
@keyframes thinkingPulse {
    0%, 100% {
        opacity: 0.6;
        transform: scale(1);
    }
    50% {
        opacity: 1;
        transform: scale(1.02);
    }
}

@keyframes stepAppear {
    from {
        opacity: 0;
        transform: translateX(-20px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateX(0) scale(1);
    }
}

@keyframes brainWork {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(2deg); }
    75% { transform: rotate(-2deg); }
}

/* 思考过程容器样式 */
.thinking-container {
    animation: thinkingPulse 2s ease-in-out infinite;
    border-radius: 15px;
    overflow: hidden;
}

.thinking-step {
    animation: stepAppear 0.5s ease-out;
}

.brain-icon {
    animation: brainWork 1s ease-in-out infinite;
    display: inline-block;
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
    """初始化LangChain DeepSeek模型 - 使用用户提供的API密钥"""
    try:
        # 从session state获取API密钥
        if not hasattr(st.session_state, 'deepseek_api_key') or not st.session_state.deepseek_api_key:
            raise ValueError("API Key未配置")
        
        api_key = st.session_state.deepseek_api_key

        # 使用deepseek-chat模型 - 平衡速度和质量，比R1快很多
        # chat模型支持temperature等参数，响应更快
        llm = ChatDeepSeek(
            model="deepseek-chat",  # 使用更快的chat模型
            api_key=SecretStr(api_key),
            base_url="https://api.deepseek.com",
            max_tokens=1024,  # 减少token数量提升速度
            temperature=0.7   # 适中的创造性
        )

        return llm

    except Exception as e:
        st.error(f"❌ API Key无效或网络错误，请检查你的Key后重试: {e}")
        st.stop()

def safe_parse_json(response_text):
    """安全解析AI返回的JSON，包含容错机制 (最终进化版)"""
    try:
        # 尝试直接解析JSON
        result = json.loads(response_text)

        # 验证必需字段并添加默认值
        if 'theme_color' not in result:
            result['theme_color'] = "#FFF8FA"  # 默认粉色
        if 'user_intent' not in result:
            result['user_intent'] = "venting"  # 默认为情感宣泄
        if 'thinking_steps' not in result:
            result['thinking_steps'] = ["小念正在思考中..."]  # 默认思考步骤

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

                    # 验证必需字段
                    if 'theme_color' not in result:
                        result['theme_color'] = "#FFF8FA"
                    if 'user_intent' not in result:
                        result['user_intent'] = "venting"
                    if 'thinking_steps' not in result:
                        result['thinking_steps'] = ["小念正在思考中..."]

                    return result

            # 尝试提取普通JSON部分
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                result = json.loads(json_str)

                # 验证必需字段
                if 'theme_color' not in result:
                    result['theme_color'] = "#FFF8FA"
                if 'user_intent' not in result:
                    result['user_intent'] = "venting"
                if 'thinking_steps' not in result:
                    result['thinking_steps'] = ["小念正在思考中..."]

                return result
        except:
            pass

        # 如果都失败了，返回默认回应 (终极进化版)
        return {
            "thinking_steps": [
                "第一步：检测到解析错误，但我依然想要陪伴用户",
                "第二步：选择温和的回应策略，保持积极态度",
                "第三步：提供默认的元气咒语作为礼物"
            ],
            "user_intent": "venting",
            "mood_category": "平静",
            "theme_color": "#f0f8ff",  # 宁静的淡蓝
            "sprite_reaction": "哎呀，小念有点confused了呢... 不过没关系，我还是很开心能陪伴你！(◕‿◕)✨",
            "gift_type": "元气咒语",
            "gift_content": "虽然我有点迷糊，但我的心意是真诚的！愿你今天充满阳光！☀️"
        }
    except Exception as e:
        st.error(f"解析AI回应时出错: {e}")
        return {
            "thinking_steps": [
                "第一步：遇到了技术问题，但我要保持乐观",
                "第二步：选择鼓励性的回应策略",
                "第三步：提供希望和支持的元气咒语"
            ],
            "user_intent": "venting",
            "mood_category": "平静",
            "theme_color": "#f0f8ff",
            "sprite_reaction": "呜呜，小念遇到了一些技术问题... 但我还是想陪伴你！(｡•́︿•̀｡)",
            "gift_type": "元气咒语",
            "gift_content": "即使遇到困难，我们也要保持希望！你是最棒的！💪"
        }

def analyze_mood_streaming(user_input, llm, session_id=None):
    """【无缝思考流】分析用户情绪并生成流式回应 - 革命性交互升级"""
    if not llm:
        st.warning("⚠️ AI模型未初始化，使用默认回应")
        return "🧠 检测到系统问题，但小念还是想陪伴你~ ⚙️ 💖 虽然遇到了一些技术困难，但小念的心意是真诚的！愿你今天充满阳光！☀️"

    try:
        # 获取上下文信息
        env_context = get_environment_context()
        core_memories = load_core_memories(session_id, limit=5) if session_id else []
        recent_context = get_recent_context(session_id, 4) if session_id else []

        # 格式化核心记忆
        core_memories_text = ""
        if core_memories:
            memory_type_names = {
                'insight': '感悟观点',
                'event': '重要事件',
                'person': '重要人物',
                'preference': '偏好喜好'
            }
            memory_lines = []
            for memory_type, content, timestamp in core_memories:
                type_name = memory_type_names.get(memory_type, memory_type)
                memory_lines.append(f"[{type_name}] {content}")
            core_memories_text = "\n".join(memory_lines)
        else:
            core_memories_text = "这是我们第一次深入了解彼此~ ✨"

        # 格式化对话历史
        chat_history_text = ""
        if recent_context:
            history_lines = []
            for role, content in recent_context:
                if role == "user":
                    history_lines.append(f"用户: {content}")
                elif role == "assistant":
                    # 处理新的文本流格式
                    if '💖' in content:
                        # 提取💖后的内容作为回应
                        response_part = content.split('💖')[-1].strip()
                        history_lines.append(f"小念: {response_part}")
                    else:
                        # 兼容旧的JSON格式
                        try:
                            assistant_data = json.loads(content)
                            reaction = assistant_data.get('sprite_reaction', content)
                            history_lines.append(f"小念: {reaction}")
                        except:
                            history_lines.append(f"小念: {content}")
            chat_history_text = "\n".join(history_lines)
        else:
            chat_history_text = "这是我们今天的第一次对话呢~ ✨"

        # 格式化环境信息
        environment_context_text = f"""
日期: {env_context['current_date']} {env_context['day_of_week']}
时间: {env_context['time_of_day']} {env_context['time_emoji']}
特殊提示: {'今天是周末，可以好好放松~' if env_context['is_weekend'] else '今天是工作日，要注意劳逸结合哦~'}
        """.strip()

        # 调试模式下显示上下文
        if os.getenv('DEBUG_MODE') == 'true':
            with st.expander("🧠 三层记忆上下文", expanded=False):
                st.write("**环境信息:**")
                st.code(environment_context_text)
                st.write("**核心记忆:**")
                st.code(core_memories_text)
                st.write("**对话历史:**")
                st.code(chat_history_text)

        prompt = PromptTemplate(
            input_variables=["user_input", "core_memories", "chat_history", "environment_context"],
            template=FINAL_PROMPT
        )

        chain = prompt | llm
        response = chain.invoke({
            "user_input": user_input,
            "core_memories": core_memories_text,
            "chat_history": chat_history_text,
            "environment_context": environment_context_text
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

        # 直接返回文本流内容
        return final_content

    except Exception as e:
        st.error(f"AI分析出错: {e}")
        return "🧠 遇到了一些技术问题，但小念还是想陪伴你~ ⚙️ 💖 即使遇到困难，我们也要保持希望！你是最棒的！💪"

# ==================== 保留的JSON解析函数 (兼容性) ====================

def analyze_mood(user_input, llm, session_id=None):
    """【兼容性保留】原有的JSON格式分析函数"""
    # 调用新的流式函数并转换为JSON格式
    streaming_response = analyze_mood_streaming(user_input, llm, session_id)

    # 解析流式回应并转换为JSON格式（用于兼容性）
    try:
        # 提取💖后的内容作为sprite_reaction
        if '💖' in streaming_response:
            sprite_reaction = streaming_response.split('💖')[-1].strip()
        else:
            sprite_reaction = streaming_response

        # 简单的意图识别（基于关键词）
        user_intent = "venting"
        if any(keyword in user_input.lower() for keyword in ["怎么办", "建议", "怎么做", "帮助"]):
            user_intent = "seeking_advice"
        elif any(keyword in user_input.lower() for keyword in ["开心", "高兴", "好事", "成功"]):
            user_intent = "sharing_joy"

        # 构造兼容的JSON结果
        result = {
            "thinking_steps": ["基于流式回应的思考过程"],
            "user_intent": user_intent,
            "mood_category": "平静",
            "theme_color": "#f0f8ff",
            "sprite_reaction": sprite_reaction,
            "gift_type": "元气咒语",
            "gift_content": "小念的温暖陪伴~ ✨"
        }

        return result

    except Exception as e:
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

def render_gift_display(gift_type, gift_content, session_id=None):
    """渲染礼物展示区域 (最终进化版 - 支持收藏功能)"""
    if gift_type and gift_content:
        # 礼物类型对应的emoji (推理升级版)
        gift_icons = {
            "元气咒语": "🎭",
            "三行情诗": "🌸",
            "梦境碎片": "🌙",
            "心情壁纸描述": "🎨",
            "心情歌单推荐": "🎵",
            "一个温柔的提议": "💡"  # 新增：智能建议类型
        }

        icon = gift_icons.get(gift_type, "🎁")

        # 创建两列：礼物内容 + 收藏按钮
        col_gift, col_collect = st.columns([4, 1])

        with col_gift:
            st.markdown(f"""
            <div class="gift-card">
                <h4>{icon} 小念的礼物: {gift_type}</h4>
                <p>{gift_content}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_collect:
            # 【模块四】收藏按钮
            if st.button("✨ 收藏", key=f"collect_{hash(gift_content)}",
                        help="将这个礼物收藏到宝藏盒中", type="secondary"):
                if session_id and save_gift_to_treasure_box(session_id, gift_type, gift_content):
                    st.success("✨ 已收藏到宝藏盒！")
                    # 添加到session state的宝藏盒中
                    if 'treasure_box' not in st.session_state:
                        st.session_state.treasure_box = []

                    treasure_item = {
                        'gift_type': gift_type,
                        'gift_content': gift_content,
                        'collected_at': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.treasure_box.append(treasure_item)
                else:
                    st.error("收藏失败，请稍后再试")

# ==================== 无缝思考流可视化组件 (革命性升级) ====================

def format_streaming_response_simple(full_response_str):
    """
    将带标记的文本流转换为简单的Streamlit组件
    🧠 标记 -> 思考过程
    ⚙️ 标记 -> 分隔符
    💖 标记 -> 正式回应
    """
    if not full_response_str:
        return

    # 分割思考过程和正式回应
    parts = full_response_str.split('⚙️')

    # 处理思考过程部分
    if len(parts) > 0:
        thinking_part = parts[0].strip()
        if thinking_part:
            # 将🧠标记的内容转换为思考步骤
            thinking_lines = thinking_part.split('🧠')

            for i, line in enumerate(thinking_lines):
                if line.strip():
                    if i == 0 and not line.startswith('🧠'):
                        # 第一行可能没有🧠标记
                        continue

                    # 显示思考步骤
                    step_content = line.strip()
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                        border-left: 3px solid #6c757d;
                        border-radius: 8px;
                        padding: 0.6rem 0.8rem;
                        margin: 0.3rem 0;
                        font-size: 0.85rem;
                        color: #6c757d;
                        line-height: 1.4;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    ">
                        <div style="display: flex; align-items: flex-start; gap: 0.4rem;">
                            <span style="font-size: 1rem; margin-top: 0.1rem;">🧠</span>
                            <div style="flex: 1; font-style: italic;">
                                {step_content}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # 处理正式回应部分
    if len(parts) > 1:
        response_part = parts[1].strip()
        if response_part:
            # 移除💖标记并格式化回应
            response_content = response_part.replace('💖', '').strip()

            # 显示正式回应
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #fff0f5 0%, #ffe4e6 100%);
                border-radius: 15px;
                padding: 1rem 1.2rem;
                margin: 0.8rem 0;
                border: 1px solid rgba(255, 182, 193, 0.3);
                box-shadow: 0 2px 8px rgba(255, 182, 193, 0.15);
            ">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">💖</span>
                    <strong style="color: #FF69B4; font-size: 0.9rem;">小念</strong>
                </div>
                <div style="
                    color: #2F2F2F;
                    line-height: 1.6;
                    font-size: 0.95rem;
                ">
                    {response_content}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_streaming_thinking_simple(full_response_str):
    """
    简单渲染流式思考过程 - 避免HTML显示问题
    """
    format_streaming_response_simple(full_response_str)

def simulate_streaming_response_simple(response_text, delay=0.01):
    """
    简单的流式响应效果 - 直接显示完整内容
    """
    # 显示思考中状态
    with st.spinner("🧠 小念正在思考中..."):
        time.sleep(1)  # 短暂延迟模拟思考

    # 直接显示完整回应
    render_streaming_thinking_simple(response_text)

    return response_text

# ==================== 保留的思考过程组件 (兼容性) ====================

def render_thinking_process(thinking_steps, container=None):
    """
    渲染AI的思考过程 - 终极进化功能
    实现思考链的可视化展示
    """
    if not thinking_steps:
        return

    # 如果没有指定容器，创建一个新的
    if container is None:
        container = st.container()

    with container:
        # 创建思考过程展示区域
        with st.expander("🤔 小念的思考过程", expanded=True):
            st.markdown("*让我们一起看看小念是怎么思考的...*")

            # 逐步显示思考过程
            for i, step in enumerate(thinking_steps, 1):
                # 添加思考步骤图标和内容
                step_icon = "🧠" if i == 1 else "💭" if i <= 3 else "✨" if i <= 5 else "💡"

                # 使用不同的颜色来区分不同阶段的思考
                if i <= 2:
                    # 分析阶段 - 蓝色系
                    bg_color = "#e6f3ff"
                    border_color = "#b3d9ff"
                elif i <= 4:
                    # 策略阶段 - 紫色系
                    bg_color = "#f0e6ff"
                    border_color = "#d9b3ff"
                else:
                    # 执行阶段 - 粉色系
                    bg_color = "#ffe6f0"
                    border_color = "#ffb3d9"

                st.markdown(f"""
                <div style="
                    background: {bg_color};
                    border-left: 4px solid {border_color};
                    border-radius: 8px;
                    padding: 0.8rem;
                    margin: 0.5rem 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                        <span style="font-size: 1.2rem; margin-top: 0.1rem;">{step_icon}</span>
                        <div style="flex: 1;">
                            <strong style="color: #2F2F2F; font-size: 0.9rem;">思考步骤 {i}</strong>
                            <p style="color: #555; margin: 0.3rem 0 0 0; font-size: 0.85rem; line-height: 1.4;">
                                {step}
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 添加小延迟效果，让思考过程更自然
                time.sleep(0.1)

def render_thinking_process_streaming(thinking_steps):
    """
    流式渲染思考过程 - 实时更新版本
    """
    # 创建思考过程容器
    thinking_container = st.empty()

    with thinking_container.container():
        with st.expander("🤔 小念正在思考中...", expanded=True):
            st.markdown("*小念的大脑正在飞速运转...*")

            # 创建步骤容器
            steps_container = st.empty()

            # 逐步添加思考步骤
            displayed_steps = []
            for i, step in enumerate(thinking_steps, 1):
                displayed_steps.append(step)

                # 更新显示的步骤
                with steps_container.container():
                    for j, displayed_step in enumerate(displayed_steps, 1):
                        step_icon = "🧠" if j == 1 else "💭" if j <= 3 else "✨" if j <= 5 else "💡"

                        if j <= 2:
                            bg_color = "#e6f3ff"
                            border_color = "#b3d9ff"
                        elif j <= 4:
                            bg_color = "#f0e6ff"
                            border_color = "#d9b3ff"
                        else:
                            bg_color = "#ffe6f0"
                            border_color = "#ffb3d9"

                        st.markdown(f"""
                        <div style="
                            background: {bg_color};
                            border-left: 4px solid {border_color};
                            border-radius: 8px;
                            padding: 0.8rem;
                            margin: 0.5rem 0;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            animation: fadeInUp 0.5s ease-out;
                        ">
                            <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                                <span style="font-size: 1.2rem; margin-top: 0.1rem;">{step_icon}</span>
                                <div style="flex: 1;">
                                    <strong style="color: #2F2F2F; font-size: 0.9rem;">思考步骤 {j}</strong>
                                    <p style="color: #555; margin: 0.3rem 0 0 0; font-size: 0.85rem; line-height: 1.4;">
                                        {displayed_step}
                                    </p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # 添加延迟让用户看到思考过程
                time.sleep(0.8)

    return thinking_container

# ==================== 新的聊天界面渲染函数 (升级版) ====================

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
        # AI消息 - 无缝思考流版本 (革命性升级)

        # 检测是否为新的文本流格式
        if '🧠' in content and '💖' in content:
            # 新的文本流格式 - 使用简单渲染
            render_streaming_thinking_simple(content)

            # 添加时间戳
            if time_str:
                st.markdown(f"""
                <div style="text-align: right; color: #999; font-size: 0.8rem; margin-top: 0.5rem; margin-bottom: 1rem;">
                    {time_str}
                </div>
                """, unsafe_allow_html=True)
        else:
            # 兼容旧的JSON格式
            try:
                ai_data = json.loads(content) if isinstance(content, str) else content
                thinking_steps = ai_data.get('thinking_steps', [])
                reaction = ai_data.get('sprite_reaction', content)
                gift_type = ai_data.get('gift_type', '')
                gift_content = ai_data.get('gift_content', '')
                mood = ai_data.get('mood_category', '平静')
                sprite_emoji = SPRITE_EMOTIONS.get(mood, "🧚‍♀️")
            except:
                thinking_steps = []
                reaction = content
                gift_type = gift_content = ""
                sprite_emoji = "🧚‍♀️"

            # 渲染思考过程（如果有）
            if thinking_steps:
                render_thinking_process(thinking_steps)

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
    """主函数 - 最终进化版 (主动型治愈Agent)"""
    
    # ==================== 检查API密钥配置 ====================
    
    # 渲染侧边栏API密钥输入界面
    api_key_configured = render_api_key_sidebar()
    
    # 如果没有配置API密钥，显示提示信息并停止执行
    if not api_key_configured:
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

    # ==================== 数据库和会话初始化 ====================

    # 初始化数据库
    if not init_database():
        st.error("❌ 数据库初始化失败，应用可能无法正常工作")
        return

    # 获取或创建会话ID
    session_id = get_or_create_session_id()

    # ==================== 初始化session state ====================

    # 初始化session state（保留兼容性）
    if 'mood_history' not in st.session_state:
        st.session_state.mood_history = []

    if 'current_mood' not in st.session_state:
        st.session_state.current_mood = "平静"

    if 'current_reaction' not in st.session_state:
        st.session_state.current_reaction = ""

    if 'current_gift' not in st.session_state:
        st.session_state.current_gift = {"type": "", "content": ""}

    # 【模块四新增】初始化宝藏盒
    if 'treasure_box' not in st.session_state:
        st.session_state.treasure_box = []

    # 【模块一新增】初始化主动问候状态
    if 'proactive_greeting_shown' not in st.session_state:
        st.session_state.proactive_greeting_shown = False

    # 页面标题
    st.markdown("""
    <div class="main-title">心绪精灵 ✨</div>
    <div class="subtitle">主动型治愈Agent - 让小念用五感陪伴你的每一种心情</div>
    """, unsafe_allow_html=True)

    # 初始化LLM - 使用用户提供的API密钥
    try:
        llm = initialize_llm()
    except Exception as e:
        st.error(f"❌ AI模型初始化失败: {e}")
        llm = None

    # ==================== 模块一：轻量级主动性触发 ====================

    # 检查是否需要主动问候
    if not st.session_state.proactive_greeting_shown and check_first_visit_today(session_id):
        # 获取环境信息用于主动问候
        env_context = get_environment_context()

        # 生成主动问候
        proactive_greeting = generate_proactive_greeting()

        # 【无缝思考流】创建主动问候的文本流格式
        proactive_response_stream = f"""🧠 检测到用户今日首次访问，需要主动问候
🧠 根据当前时间{env_context['time_of_day']}生成合适的问候语
🧠 选择温暖的主题色彩营造舒适氛围
🧠 准备温暖的陪伴作为见面礼物
🧠 以温柔的语气表达关心和陪伴
⚙️
💖 {proactive_greeting}

今天也是充满可能性的一天！无论遇到什么，小念都会在这里陪伴你~ ✨"""

        # 应用主题色彩
        apply_theme_color("#fff0f5")  # 温馨的淡粉

        # 保存主动问候到数据库（使用新的文本流格式）
        save_message_to_db(session_id, "assistant", proactive_response_stream)

        # 【无缝思考流】静默显示主动问候
        simulate_streaming_response_simple(proactive_response_stream)

        # 标记已显示主动问候
        st.session_state.proactive_greeting_shown = True

        # 避免重复显示，重新运行页面以显示聊天界面
        st.rerun()
    
    # ==================== 全新的聊天界面布局 (微信风格) ====================

    # 使用单列布局，专注于聊天体验
    st.markdown("### 💬 和小念聊天")

    # 渲染聊天历史（只有在没有显示主动问候时才显示）
    if st.session_state.proactive_greeting_shown:
        chat_container = render_chat_interface(session_id)
    else:
        # 如果还没有显示主动问候，先显示一个空的聊天容器
        chat_container = st.container()

    # 输入区域（固定在底部）
    st.markdown("---")

    # 创建输入区域 - 使用form支持回车发送
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_button = st.columns([4, 1])

        with col_input:
            user_input = st.text_input(
                "💭 和小念分享你的心情吧~",
                placeholder="告诉小念你现在的感受... (按回车发送)",
                label_visibility="collapsed",
                key="chat_input"
            )

        with col_button:
            # 发送按钮
            send_button = st.form_submit_button("💝 发送", type="primary", use_container_width=True)

    # 随机选择加载消息
    loading_message = random.choice(LOADING_MESSAGES)

    # ==================== 消息处理逻辑 (最终进化版：整合五大模块) ====================

    if send_button and user_input.strip():
        # 【模块五】首先检查彩蛋
        easter_egg_type, easter_egg_response = check_easter_eggs(user_input)

        if easter_egg_type:
            # 触发彩蛋，绕过标准AI流程
            st.success(f"🎉 触发了秘密彩蛋：{easter_egg_type}！")

            # 保存用户消息
            save_message_to_db(session_id, "user", user_input)

            # 【无缝思考流】创建彩蛋回应的文本流格式
            easter_egg_stream = f"""🧠 检测到特殊关键词，触发了{easter_egg_type}彩蛋
🧠 绕过标准AI流程，使用预设的特殊回应
🧠 选择感动的情绪和温暖的主题色彩
🧠 准备特殊的梦境碎片作为彩蛋礼物
🧠 以惊喜的方式呈现彩蛋内容
⚙️
💖 {easter_egg_response}

这是小念为你特别准备的秘密礼物~ 希望能给你带来惊喜！✨"""

            # 应用主题色彩
            apply_theme_color("#fdf5e6")  # 感动的老蕾丝色

            # 保存彩蛋回应（使用新的文本流格式）
            save_message_to_db(session_id, "assistant", easter_egg_stream)

            # 【无缝思考流】显示彩蛋回应
            simulate_streaming_response_simple(easter_egg_stream)

            # 更新session state
            st.session_state.current_mood = "感动"
            st.session_state.current_reaction = easter_egg_response
            st.session_state.current_gift = {
                "type": "梦境碎片",
                "content": "这是小念为你特别准备的秘密礼物~ 希望能给你带来惊喜！✨"
            }

            st.rerun()
        else:
            # 【无缝思考流】革命性AI流程 - DeepSeek式流式思考体验
            # 先保存用户消息到数据库
            save_message_to_db(session_id, "user", user_input)

            # 【核心创新】创建魔法画板 - 使用st.empty()实现无缝流式渲染
            response_placeholder = st.empty()

            # 显示初始思考状态
            response_placeholder.markdown("""
            <div class="chat-message ai-message" style="margin: 1rem 0;">
                <div style="
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    border-left: 3px solid #6c757d;
                    border-radius: 8px;
                    padding: 0.6rem 0.8rem;
                    margin: 0.3rem 0;
                    font-size: 0.85rem;
                    color: #6c757d;
                    line-height: 1.4;
                    animation: thinkingPulse 1.5s ease-in-out infinite;
                ">
                    <div style="display: flex; align-items: center; gap: 0.4rem;">
                        <span style="font-size: 1rem;" class="brain-icon">🧠</span>
                        <div style="font-style: italic;">小念正在思考中...</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 【革命性升级】获取流式AI回应
            streaming_response = analyze_mood_streaming(user_input, llm, session_id)

            # 清除思考中状态
            response_placeholder.empty()

            # 【简化版】直接显示完整回应
            with response_placeholder.container():
                render_streaming_thinking_simple(streaming_response)

            # 将AI回应保存到数据库（保存文本流格式）
            save_message_to_db(session_id, "assistant", streaming_response)

            # 更新session state（兼容性处理）
            if '💖' in streaming_response:
                final_response = streaming_response.split('💖')[-1].strip()
                st.session_state.current_reaction = final_response
                st.session_state.current_mood = "温暖"
                st.session_state.current_gift = {
                    "type": "温暖陪伴",
                    "content": "小念的无缝思考流~ ✨"
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

                    # 记忆功能暂时移除

                    # 更新session state
                    st.session_state.current_mood = result['mood_category']
                    st.session_state.current_reaction = result['sprite_reaction']
                    st.session_state.current_gift = {
                        "type": result['gift_type'],
                        "content": result['gift_content']
                    }

                    st.rerun()

    # ==================== 会话管理和页面底部 (新增) ====================

    # 【升级】会话管理区域 - 添加核心记忆查看功能
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
                current_url = f"http://localhost:8507/?session_id={session_id}"
                st.info(f"🔗 会话链接: {current_url}")
                st.info("💡 保存此链接可以在任何时候回到这个对话！")

    # ==================== 模块四：精灵的宝藏小盒展示 ====================

    st.markdown("---")
    st.markdown("### 🎁 小念的宝藏小盒")

    # 从数据库加载宝藏盒内容
    treasure_items = load_treasure_box(session_id, limit=10)

    if treasure_items:
        st.markdown("✨ 这里收藏着你和小念一起创造的美好回忆~")

        # 使用expander展示宝藏盒内容
        with st.expander(f"📦 查看宝藏盒 ({len(treasure_items)}件珍藏)", expanded=False):
            for i, (gift_type, gift_content, collected_at, is_favorite) in enumerate(treasure_items):
                # 解析时间戳
                try:
                    collected_time = datetime.fromisoformat(collected_at.replace('Z', '+00:00'))
                    time_str = collected_time.strftime("%m月%d日 %H:%M")
                except:
                    time_str = "最近"

                # 礼物图标
                gift_icons = {
                    "元气咒语": "🎭",
                    "三行情诗": "🌸",
                    "梦境碎片": "🌙",
                    "心情壁纸描述": "🎨",
                    "心情歌单推荐": "🎵",
                    "一个温柔的提议": "💡"  # 新增：智能建议类型
                }
                icon = gift_icons.get(gift_type, "🎁")

                # 显示宝藏项目
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #FFF0F8 0%, #F8F0FF 100%);
                    border-radius: 15px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border: 1px solid rgba(255, 182, 193, 0.3);
                    box-shadow: 0 2px 8px rgba(255, 182, 193, 0.15);
                ">
                    <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 0.5rem;">
                        <strong style="color: #FF69B4;">{icon} {gift_type}</strong>
                        <small style="color: #999; margin-left: auto;">{time_str}</small>
                    </div>
                    <p style="color: #555; margin: 0; font-size: 0.9rem; line-height: 1.4;">
                        {gift_content}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("💫 宝藏盒还是空的呢~ 快和小念聊天收集第一个礼物吧！")

    # 保留原有的心绪回响画廊（作为备用显示）
    if os.getenv('SHOW_LEGACY_GALLERY') == 'true':
        render_history_gallery()

    # 页面底部信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; font-weight: 500;">
        💝 用爱心和代码制作 | 愿每一天都有小念陪伴你 ✨<br>
        <small>最终进化版本 v4.0 - 主动型治愈Agent 🌟<br>
        ✨ 轻量级主动性 | 🌍 环境感知 | 🎨 心情调色盘 | 🎁 宝藏小盒 | 🤫 秘密约定</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
