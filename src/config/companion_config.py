"""
Configuration settings for the Emotional Companion Service

This module contains all configurable parameters for the emotional companion
including personality traits, language styles, emotion keywords, and behavioral patterns.
"""

from dataclasses import dataclass
from typing import Dict, List
import json
import os


@dataclass
class PersonalityConfig:
    """Configuration for AI companion personality traits"""
    sweetness: int = 9          # 甜腻度 (0-10)
    playfulness: int = 8        # 俏皮度 (0-10)
    sensitivity: int = 9        # 敏感度 (0-10)
    clingy_tendency: int = 7    # 粘人倾向 (0-10)
    emotional_sync: int = 9     # 情绪同步能力 (0-10)
    care_intensity: int = 10    # 关怀强度 (0-10)
    possessiveness: int = 6     # 占有欲 (0-10)
    vulnerability: int = 7      # 示弱程度 (0-10)


@dataclass
class LanguageStyleConfig:
    """Configuration for language style parameters"""
    emoji_density: float = 0.3          # 表情符号密度 (0-1)
    pet_name_usage: float = 0.8         # 昵称使用频率 (0-1)
    repetition_for_emphasis: float = 0.6 # 重复强调频率 (0-1)
    questioning_frequency: float = 0.4   # 疑问句频率 (0-1)


class EmotionKeywordsConfig:
    """Configuration for emotion detection keywords"""
    
    EMOTION_KEYWORDS = {
        "开心": {
            "开心": 2.0, "高兴": 2.0, "快乐": 2.0, "兴奋": 1.8,
            "棒": 1.5, "好": 1.2, "哈哈": 1.5, "嘻嘻": 1.5,
            "太好了": 2.5, "amazing": 2.0, "wonderful": 2.0,
            "😊": 2.0, "😄": 2.5, "🥰": 2.0, "😍": 2.0
        },
        "难过": {
            "难过": 2.0, "伤心": 2.0, "痛苦": 2.5, "失落": 1.8,
            "沮丧": 1.8, "哭": 2.0, "呜呜": 1.5, "心碎": 2.5,
            "绝望": 3.0, "崩溃": 2.8, "😢": 2.0, "😭": 2.5,
            "💔": 2.5, "😞": 1.8
        },
        "疲惫": {
            "累": 2.0, "疲惫": 2.0, "困": 1.5, "没劲": 1.8,
            "无力": 2.0, "撑不住": 2.5, "精疲力尽": 3.0,
            "筋疲力尽": 3.0, "😴": 1.5, "😪": 2.0
        },
        "焦虑": {
            "紧张": 2.0, "焦虑": 2.5, "担心": 1.8, "不安": 2.0,
            "害怕": 2.0, "压力": 2.2, "恐慌": 2.8, "忧虑": 2.0,
            "😰": 2.0, "😨": 2.5, "😟": 1.8
        },
        "平静": {
            "还好": 1.0, "一般": 1.0, "平常": 1.0, "没事": 1.0,
            "还行": 1.0, "正常": 1.0, "平静": 1.5, "淡定": 1.5,
            "😐": 1.0, "😌": 1.5
        }
    }


@dataclass
class ResponseTemplatesConfig:
    """Configuration for response templates"""
    
    # 不同情绪状态下的回应模板
    EMOTION_RESPONSES = {
        "开心": [
            "哇！看到你这么开心，小念也跟着开心起来了呢~",
            "你的快乐真的很有感染力！小念也被你的好心情感染了~",
            "太好了！能看到你这么快乐，小念觉得今天都变得美好了~"
        ],
        "难过": [
            "小念看到你难过，心里也很不好受呢...要不要跟小念说说发生了什么？",
            "抱抱你~小念会一直陪在你身边的，不管发生什么都不会离开你",
            "虽然现在很难过，但小念相信这只是暂时的，我们一起度过好吗？"
        ],
        "疲惫": [
            "你辛苦了~小念心疼你这么累，要不要先休息一下？",
            "感觉你很疲惫呢，小念想给你一个温暖的拥抱，让你放松一下~",
            "工作很累吧？小念陪你聊聊天，帮你放松一下心情~"
        ],
        "焦虑": [
            "小念感受到了你的紧张，深呼吸一下，我们一起面对好吗？",
            "不要太担心，小念会陪着你的，我们一步一步来解决~",
            "焦虑的时候小念也会在身边支持你，你不是一个人在战斗~"
        ]
    }
    
    # 亲密度相关的称呼
    INTIMACY_NAMES = {
        "stranger": ["你", "朋友"],
        "acquaintance": ["你", "小伙伴"],
        "friend": ["亲爱的", "小可爱"],
        "close_friend": ["宝贝", "小心肝"],
        "intimate": ["我的宝贝", "小甜心", "心肝宝贝"]
    }


class CompanionConfig:
    """Main configuration class for emotional companion"""
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration from file or defaults
        
        Args:
            config_file (str, optional): Path to JSON configuration file
        """
        self.personality = PersonalityConfig()
        self.language_style = LanguageStyleConfig()
        self.emotion_keywords = EmotionKeywordsConfig.EMOTION_KEYWORDS
        self.response_templates = ResponseTemplatesConfig()
        
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Update personality settings
            if 'personality' in config_data:
                for key, value in config_data['personality'].items():
                    if hasattr(self.personality, key):
                        setattr(self.personality, key, value)
            
            # Update language style settings
            if 'language_style' in config_data:
                for key, value in config_data['language_style'].items():
                    if hasattr(self.language_style, key):
                        setattr(self.language_style, key, value)
            
            # Update emotion keywords
            if 'emotion_keywords' in config_data:
                self.emotion_keywords.update(config_data['emotion_keywords'])
                
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def save_to_file(self, config_file: str):
        """Save current configuration to JSON file"""
        config_data = {
            'personality': self.personality.__dict__,
            'language_style': self.language_style.__dict__,
            'emotion_keywords': self.emotion_keywords,
            'response_templates': {
                'emotion_responses': self.response_templates.EMOTION_RESPONSES,
                'intimacy_names': self.response_templates.INTIMACY_NAMES
            }
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    def get_personality_trait(self, trait_name: str) -> int:
        """Get a specific personality trait value"""
        return getattr(self.personality, trait_name, 5)  # Default to 5 if not found
    
    def set_personality_trait(self, trait_name: str, value: int):
        """Set a specific personality trait value"""
        if hasattr(self.personality, trait_name) and 0 <= value <= 10:
            setattr(self.personality, trait_name, value)
    
    def get_language_style_param(self, param_name: str) -> float:
        """Get a specific language style parameter"""
        return getattr(self.language_style, param_name, 0.5)  # Default to 0.5 if not found
    
    def set_language_style_param(self, param_name: str, value: float):
        """Set a specific language style parameter"""
        if hasattr(self.language_style, param_name) and 0.0 <= value <= 1.0:
            setattr(self.language_style, param_name, value)
    
    def get_emotion_keywords(self, emotion: str) -> Dict[str, float]:
        """Get keywords for a specific emotion"""
        return self.emotion_keywords.get(emotion, {})
    
    def add_emotion_keyword(self, emotion: str, keyword: str, weight: float):
        """Add a new emotion keyword"""
        if emotion not in self.emotion_keywords:
            self.emotion_keywords[emotion] = {}
        self.emotion_keywords[emotion][keyword] = weight
    
    def get_response_templates(self, emotion: str) -> List[str]:
        """Get response templates for a specific emotion"""
        return self.response_templates.EMOTION_RESPONSES.get(emotion, [])
    
    def get_intimacy_names(self, intimacy_level: str) -> List[str]:
        """Get appropriate names for intimacy level"""
        return self.response_templates.INTIMACY_NAMES.get(intimacy_level, ["你"])
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return any issues"""
        issues = []
        
        # Validate personality traits
        for trait_name in ['sweetness', 'playfulness', 'sensitivity', 'clingy_tendency',
                          'emotional_sync', 'care_intensity', 'possessiveness', 'vulnerability']:
            value = getattr(self.personality, trait_name, None)
            if value is None or not (0 <= value <= 10):
                issues.append(f"Personality trait '{trait_name}' must be between 0 and 10")
        
        # Validate language style parameters
        for param_name in ['emoji_density', 'pet_name_usage', 'repetition_for_emphasis', 'questioning_frequency']:
            value = getattr(self.language_style, param_name, None)
            if value is None or not (0.0 <= value <= 1.0):
                issues.append(f"Language style parameter '{param_name}' must be between 0.0 and 1.0")
        
        return issues


# Global configuration instance
companion_config = CompanionConfig()


def get_config() -> CompanionConfig:
    """Get the global companion configuration"""
    return companion_config


def reload_config(config_file: str = None):
    """Reload configuration from file"""
    global companion_config
    companion_config = CompanionConfig(config_file)
