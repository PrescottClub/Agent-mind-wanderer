"""
情绪相关数据模型
"""

from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime


@dataclass
class EmotionResult:
    """情绪分析结果"""
    mood_category: str
    sprite_reaction: str
    gift_type: str
    gift_content: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmotionResult':
        """从字典创建情绪结果对象"""
        return cls(
            mood_category=data.get('mood_category', '平静'),
            sprite_reaction=data.get('sprite_reaction', ''),
            gift_type=data.get('gift_type', ''),
            gift_content=data.get('gift_content', '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'mood_category': self.mood_category,
            'sprite_reaction': self.sprite_reaction,
            'gift_type': self.gift_type,
            'gift_content': self.gift_content
        }


@dataclass 
class MoodRecord:
    """心情记录"""
    timestamp: str
    user_input: str
    emotion_result: EmotionResult

    @classmethod
    def create(cls, user_input: str, emotion_result: EmotionResult) -> 'MoodRecord':
        """创建新的心情记录"""
        return cls(
            timestamp=datetime.now().strftime("%H:%M:%S"),
            user_input=user_input,
            emotion_result=emotion_result
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式供session_state使用"""
        return {
            'timestamp': self.timestamp,
            'user_input': self.user_input,
            'mood': self.emotion_result.mood_category,
            'sprite_reaction': self.emotion_result.sprite_reaction,
            'gift_type': self.emotion_result.gift_type,
            'gift_content': self.emotion_result.gift_content
        } 