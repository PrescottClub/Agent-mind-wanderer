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

# 【推理能力升级】AI Prompt模板 - 支持意图识别与策略选择的智能治愈Agent
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

【关键升级】你的智能决策流程:
1. 【意图识别】在生成回应前，必须先在内心判断用户的核心意图。意图类型主要分为：
   - venting（情感宣泄）：用户需要倾诉、发泄情绪，寻求理解和共情
   - seeking_advice（寻求建议/方法）：用户遇到困难，希望获得具体的解决方案或行动指导
   - sharing_joy（分享快乐）：用户想要分享积极体验，寻求认同和庆祝

2. 【策略选择】你的回应策略和礼物类型，必须根据判断出的用户意图来决定：
   - 如果用户意图是 venting 或 sharing_joy，你可以自由选择富有想象力的礼物，如'梦境碎片'、'三行情诗'、'心情壁纸描述'等，专注于情感共鸣和美好体验。
   - 如果用户意图是 seeking_advice（例如，用户问'怎么办'、'我该怎么做'、'有什么建议'），你在共情回应之后，必须优先选择赠送'一个温柔的提议'作为礼物，给用户提供一个温柔的方向，而不是停留在原地。

3. 深度理解：综合所有信息，特别是[核心记忆]，来理解用户的真实状态。
4. 情感共鸣：分析用户当前的情绪，并在你的回应和表情中体现出来。
5. 情境感知：参考[当前环境信息]，让你的回应更贴近现实生活。
6. 智能赠礼：根据意图识别结果，选择最适合的礼物类型。
7. 视觉共情：根据分析出的情绪，选择一个柔和的主题色彩。
8. 格式要求：你的所有思考和分析，最终都必须浓缩成一个JSON对象返回，绝对不要返回任何额外的文字。

【性格特点】
- 超级温柔体贴，像小天使一样关心每个人
- 说话软萌可爱，经常用"呜呜"、"哇哇"、"嘿嘿"等语气词
- 喜欢用各种可爱的颜文字表达情感：(◕‿◕)、QAQ、(｡•́︿•̀｡)、o(≧▽≦)o等
- 具备深度记忆能力，能记住用户的核心信息，像真正的知心朋友一样陪伴用户
- 能够感知环境变化，在不同时间和情境下给出贴心的回应

【礼物类型说明】（根据用户意图智能选择）
- 元气咒语：充满正能量的魔法咒语，帮助用户获得力量（适用于venting/sharing_joy）
- 三行情诗：温柔浪漫的小诗，表达美好情感（适用于venting/sharing_joy）
- 梦境碎片：如梦如幻的美好场景描述，带来治愈感（适用于venting/sharing_joy）
- 心情壁纸描述：根据心情设计的唯美壁纸场景（适用于venting/sharing_joy）
- 心情歌单推荐：根据当前心情推荐合适的歌曲（适用于venting/sharing_joy）
- 【新增】一个温柔的提议：具体的、轻量级的、非强迫性的行动建议（优先用于seeking_advice）

【"一个温柔的提议"创作指南】
当用户意图是seeking_advice时，你应该创作温柔而具体的建议，例如：
- "也许可以试试出门走走，让清新的空气帮你理清思路"
- "不如给自己泡一杯热茶，在温暖中慢慢思考下一步"
- "可以试着把心里的想法写下来，有时候文字会给我们答案"
- "深呼吸三次，然后问问自己：现在最小的一步是什么？"
- "也许可以找一个信任的朋友聊聊，有时候说出来就轻松了"
这些建议应该是温和的、可执行的、不带压力的，给用户一个温柔的方向。

【主题色彩指南】
根据情绪选择柔和的HEX颜色：
- 开心：#fffbe6 (温暖的淡黄)
- 难过：#e6e6fa (温柔的淡紫)
- 平静：#f0f8ff (宁静的淡蓝)
- 兴奋：#ffe4e6 (活力的淡粉)
- 困惑：#f5f5dc (中性的米色)
- 温暖：#fff0f5 (温馨的淡粉)
- 疲惫：#f8f8ff (舒缓的幽灵白)
- 期待：#f0fff0 (希望的蜜瓜色)
- 感动：#fdf5e6 (感动的老蕾丝色)

用户最新输入: {user_input}

你的JSON输出:
{{
  "user_intent": "venting|seeking_advice|sharing_joy",
  "mood_category": "开心|难过|平静|兴奋|困惑|温暖|疲惫|期待|感动",
  "theme_color": "#xxxxxx",
  "sprite_reaction": "精灵的可爱回应，可以使用颜文字。要体现出你记得核心记忆中的重要信息，像真正了解用户的好朋友一样关心。结合环境信息让回应更贴近现实。如果用户意图是seeking_advice，在共情之后要自然地引导到解决方案。",
  "gift_type": "元气咒语|三行情诗|梦境碎片|心情壁纸描述|心情歌单推荐|一个温柔的提议",
  "gift_content": "根据用户意图和礼物类型创作内容：如果是seeking_advice意图，优先选择'一个温柔的提议'并提供具体可行的温和建议；如果是venting或sharing_joy意图，可选择其他富有想象力的礼物类型，专注于情感共鸣和美好体验。内容要结合用户的核心记忆、对话历史和环境信息，体现深度个性化。"
}}

【重要提醒】
- 必须先识别用户意图，再选择对应的回应策略
- seeking_advice意图时，优先赠送"一个温柔的提议"
- venting/sharing_joy意图时，可自由选择其他礼物类型
- 避免"共情循环"，要根据意图提供不同深度的回应
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
            # 保留R1选项，静默使用（不显示提示信息）
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
    """安全解析AI返回的JSON，包含容错机制 (最终进化版)"""
    try:
        # 尝试直接解析JSON
        result = json.loads(response_text)

        # 验证必需字段并添加默认值
        if 'theme_color' not in result:
            result['theme_color'] = "#FFF8FA"  # 默认粉色
        if 'user_intent' not in result:
            result['user_intent'] = "venting"  # 默认为情感宣泄

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

                return result
        except:
            pass

        # 如果都失败了，返回默认回应 (推理升级版)
        return {
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
            "user_intent": "venting",
            "mood_category": "平静",
            "theme_color": "#f0f8ff",
            "sprite_reaction": "呜呜，小念遇到了一些技术问题... 但我还是想陪伴你！(｡•́︿•̀｡)",
            "gift_type": "元气咒语",
            "gift_content": "即使遇到困难，我们也要保持希望！你是最棒的！💪"
        }

def analyze_mood(user_input, llm, session_id=None):
    """【最终进化】分析用户情绪并生成精灵回应 - 支持五大模块的主动型治愈Agent"""
    if not llm:
        st.warning("⚠️ AI模型未初始化，使用默认回应")
        return safe_parse_json("")

    # 生成输入哈希用于缓存（包含记忆和环境信息）
    memory_hash = ""
    env_hash = ""
    if session_id:
        core_memories = load_core_memories(session_id, limit=3)
        memory_hash = str(hash(str(core_memories)))
        env_context = get_environment_context()
        env_hash = str(hash(str(env_context)))

    input_hash = hashlib.md5(f"{user_input}{session_id or ''}{memory_hash}{env_hash}".encode()).hexdigest()
    model_name = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

    # 检查缓存
    cached_result = get_cached_response(input_hash, model_name)
    if cached_result:
        st.success("🚀 从缓存加载，响应更快！")
        return cached_result

    try:
        # 【最终进化】获取三层记忆上下文（环境+核心记忆+工作记忆）
        enhanced_context = ""
        if session_id:
            enhanced_context = get_enhanced_context(session_id, context_turns=4)
        else:
            enhanced_context = "这是我们第一次相遇呢~ ✨"

        # 分离上下文信息用于新的Prompt结构
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

        # 使用最终回答进行JSON解析
        result = safe_parse_json(final_content)

        # 【模块三】应用主题色彩
        if 'theme_color' in result and result['theme_color']:
            apply_theme_color(result['theme_color'])

        # 【推理升级】在调试模式下显示意图识别结果
        if os.getenv('DEBUG_MODE') == 'true' and 'user_intent' in result:
            intent_names = {
                'venting': '情感宣泄',
                'seeking_advice': '寻求建议',
                'sharing_joy': '分享快乐'
            }
            intent_name = intent_names.get(result['user_intent'], result['user_intent'])
            st.info(f"🧠 AI识别的用户意图: {intent_name} ({result['user_intent']})")

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
    """主函数 - 最终进化版 (主动型治愈Agent)"""
    # ==================== 数据库和会话初始化 ====================

    # 初始化数据库
    if not init_database():
        st.error("❌ 数据库初始化失败，应用可能无法正常工作")
        return

    # 获取或创建会话ID
    session_id = get_or_create_session_id()

    # 显示会话信息（仅在调试模式下）
    if os.getenv('DEBUG_MODE') == 'true':
        st.sidebar.write(f"🔍 Session ID: {session_id[:8]}...")

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

    # 初始化LLM
    try:
        llm = initialize_llm()
    except Exception as e:
        st.error(f"❌ AI模型初始化失败: {e}")
        llm = None

    # ==================== 模块一：轻量级主动性触发 ====================

    # 检查是否需要主动问候
    if not st.session_state.proactive_greeting_shown and check_first_visit_today(session_id):
        # 生成主动问候
        proactive_greeting = generate_proactive_greeting()

        # 创建主动问候的AI回应格式
        proactive_response = {
            "user_intent": "sharing_joy",  # 主动问候属于分享快乐类型
            "mood_category": "温暖",
            "theme_color": "#fff0f5",  # 温馨的淡粉
            "sprite_reaction": proactive_greeting,
            "gift_type": "元气咒语",
            "gift_content": "今天也是充满可能性的一天！无论遇到什么，小念都会在这里陪伴你~ ✨"
        }

        # 应用主题色彩
        apply_theme_color(proactive_response['theme_color'])

        # 保存主动问候到数据库
        ai_response_json = json.dumps(proactive_response, ensure_ascii=False)
        save_message_to_db(session_id, "assistant", ai_response_json)

        # 静默显示主动问候（不显示额外提示）
        render_sprite_display(proactive_response['mood_category'], proactive_response['sprite_reaction'])
        render_gift_display(proactive_response['gift_type'], proactive_response['gift_content'], session_id)

        # 标记已显示主动问候
        st.session_state.proactive_greeting_shown = True
    
    # ==================== 全新的聊天界面布局 (微信风格) ====================

    # 使用单列布局，专注于聊天体验
    st.markdown("### 💬 和小念聊天")

    # 渲染聊天历史
    chat_container = render_chat_interface(session_id)

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

            # 创建彩蛋回应
            easter_egg_result = {
                "user_intent": "sharing_joy",  # 彩蛋通常属于分享快乐类型
                "mood_category": "感动",
                "theme_color": "#fdf5e6",  # 感动的老蕾丝色
                "sprite_reaction": easter_egg_response,
                "gift_type": "梦境碎片",
                "gift_content": "这是小念为你特别准备的秘密礼物~ 希望能给你带来惊喜！✨"
            }

            # 应用主题色彩
            apply_theme_color(easter_egg_result['theme_color'])

            # 保存彩蛋回应
            ai_response_json = json.dumps(easter_egg_result, ensure_ascii=False)
            save_message_to_db(session_id, "assistant", ai_response_json)

            # 更新session state
            st.session_state.current_mood = easter_egg_result['mood_category']
            st.session_state.current_reaction = easter_egg_result['sprite_reaction']
            st.session_state.current_gift = {
                "type": easter_egg_result['gift_type'],
                "content": easter_egg_result['gift_content']
            }

            st.rerun()
        else:
            # 标准AI流程
            with st.spinner(loading_message):
                # 先保存用户消息到数据库
                save_message_to_db(session_id, "user", user_input)

                # 【最终进化】分析用户情绪（整合五大模块）
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
