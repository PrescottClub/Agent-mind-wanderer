"""
工具函数模块
提供环境感知、主动性检查等辅助功能
"""

import random
from datetime import datetime
from typing import Dict, List
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.repositories.chat_repository import ChatRepository


def get_environment_context() -> Dict:
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


def check_first_visit_today(session_id: str) -> bool:
    """
    模块一：轻量级主动性 - 检查是否为今日首次访问
    返回True表示需要主动问候，False表示今天已经问候过
    """
    try:
        chat_repo = ChatRepository()
        last_timestamp = chat_repo.get_last_message_timestamp(session_id)
        
        if not last_timestamp:
            # 如果没有历史记录，说明是全新会话，需要问候
            return True

        # 解析最后一条消息的时间戳
        last_message_time = datetime.fromisoformat(last_timestamp.replace('Z', '+00:00'))
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 如果最后一条消息早于今天零点，说明是今日首次访问
        return last_message_time < today_start

    except Exception:
        # 出错时默认不主动问候，避免重复
        return False


def generate_proactive_greeting() -> str:
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


def parse_enhanced_ai_response(response_data: Dict) -> Dict:
    """
    解析增强版AI回应的JSON格式
    返回包含所有必要信息的字典
    """
    try:
        return {
            "mood_category": response_data.get("mood_category", "温暖"),
            "memory_association": response_data.get("memory_association"),
            "sprite_reaction": response_data.get("sprite_reaction", "小念想和你分享温暖~"),
            "emotional_resonance": response_data.get("emotional_resonance", "温暖的情感共鸣"),
            "gift_type": response_data.get("gift_type", "元气咒语"),
            "gift_content": response_data.get("gift_content", "小念的温暖陪伴~"),
            "search_summary": response_data.get("search_summary"),  # 搜索结果时才有
            "is_emergency": response_data.get("is_emergency", False)  # 急救包模式标识
        }
    except Exception as e:
        # 如果解析失败，返回降级版本
        return {
            "mood_category": "温暖",
            "memory_association": None,
            "sprite_reaction": "呜呜~ 小念有点困惑，但还是想陪伴你~",
            "emotional_resonance": "即使在困难时刻，陪伴依然珍贵",
            "gift_type": "元气咒语",
            "gift_content": "✨ 愿我们的友谊永远温暖如初 ✨",
            "search_summary": None,
            "is_emergency": False
        }


def parse_ai_response(response_text: str) -> Dict:
    """
    解析AI回应，提取思考过程和最终回答
    """
    # 查找思考结束标记
    if "⚙️" in response_text:
        parts = response_text.split("⚙️", 1)
        thinking_steps = parts[0].strip()
        final_response = parts[1].strip() if len(parts) > 1 else ""
        
        # 提取思考步骤
        thinking_lines = []
        for line in thinking_steps.split('\n'):
            if line.strip().startswith('🧠'):
                thinking_lines.append(line.strip())
        
        # 提取最终回应（去掉💖前缀）
        if final_response.startswith('💖'):
            final_response = final_response[1:].strip()
        
        return {
            "thinking_steps": thinking_lines,
            "final_response": final_response,
            "has_thinking": len(thinking_lines) > 0
        }
    else:
        # 如果没有标准格式，直接返回原文
        return {
            "thinking_steps": [],
            "final_response": response_text,
            "has_thinking": False
        }


def extract_gift_from_response(response_text: str) -> Dict:
    """
    从AI回应中提取礼物信息
    这是一个简化版本，实际应用中可能需要更复杂的解析逻辑
    """
    # 简单的关键词匹配来确定礼物类型
    gift_keywords = {
        "元气咒语": ["元气", "咒语", "魔法", "祝福"],
        "温暖拥抱": ["拥抱", "温暖", "抱抱", "怀抱"],
        "彩虹糖果": ["糖果", "彩虹", "甜蜜", "甜甜"],
        "星光祝福": ["星光", "星星", "祝福", "闪闪"],
        "心灵花束": ["花束", "花朵", "鲜花", "花儿"]
    }
    
    response_lower = response_text.lower()
    
    for gift_type, keywords in gift_keywords.items():
        if any(keyword in response_lower for keyword in keywords):
            return {
                "type": gift_type,
                "content": f"小念为你准备的{gift_type}~ ✨"
            }
    
    # 默认礼物
    return {
        "type": "元气咒语",
        "content": "小念的温暖陪伴就是最好的礼物~ 💖"
    }
