"""
智能情感分析服务
负责深度情感理解、情感强度计算、共情策略生成等核心功能
v5.2 新增功能模块
"""

import json
import re
import math
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from src.data.database import get_db_connection


class EmotionType(Enum):
    """情绪类型枚举"""
    # 正面情绪
    JOY = "joy"           # 快乐
    EXCITEMENT = "excitement"  # 兴奋
    LOVE = "love"         # 爱意
    GRATITUDE = "gratitude"    # 感激
    PRIDE = "pride"       # 自豪
    RELIEF = "relief"     # 安心
    SERENITY = "serenity" # 宁静
    
    # 负面情绪
    SADNESS = "sadness"   # 悲伤
    ANGER = "anger"       # 愤怒
    FEAR = "fear"         # 恐惧
    ANXIETY = "anxiety"   # 焦虑
    DISGUST = "disgust"   # 厌恶
    GUILT = "guilt"       # 内疚
    SHAME = "shame"       # 羞耻
    LONELINESS = "loneliness"  # 孤独
    FRUSTRATION = "frustration"  # 挫折
    DESPAIR = "despair"   # 绝望
    
    # 中性情绪
    SURPRISE = "surprise" # 惊讶
    CURIOSITY = "curiosity"    # 好奇
    CONFUSION = "confusion"    # 困惑
    BOREDOM = "boredom"   # 无聊
    NEUTRAL = "neutral"   # 中性


class EmpathyStrategy(Enum):
    """共情策略枚举"""
    COMFORT = "comfort"       # 安慰型：给予温暖和理解
    SOLUTION = "solution"     # 解决型：提供建议和方案
    COMPANION = "companion"   # 陪伴型：静静陪伴和倾听
    CELEBRATION = "celebration"  # 庆祝型：分享喜悦和鼓励
    VALIDATION = "validation" # 认同型：确认和验证情感
    DISTRACTION = "distraction"  # 转移型：适度转移注意力


class ResponseTone(Enum):
    """回应语调枚举"""
    GENTLE = "gentle"         # 温柔的
    ENCOURAGING = "encouraging"   # 鼓励的
    SUPPORTIVE = "supportive" # 支持的
    JOYFUL = "joyful"        # 欢快的
    CALMING = "calming"      # 镇静的
    WARM = "warm"            # 温暖的
    UNDERSTANDING = "understanding"  # 理解的


@dataclass
class EmotionAnalysisResult:
    """情感分析结果"""
    primary_emotion: EmotionType
    emotion_intensity: float  # 0.0-10.0
    emotion_valence: float    # -1.0 to 1.0 (negative to positive)
    emotion_arousal: float    # 0.0 to 1.0 (calm to excited)
    secondary_emotions: List[Tuple[EmotionType, float]]
    confidence_score: float   # 0.0-1.0
    trigger_keywords: List[str]
    empathy_strategy: EmpathyStrategy
    response_tone: ResponseTone


class EmotionAnalysisService:
    """智能情感分析服务"""
    
    def __init__(self):
        """初始化情感分析服务"""
        self.emotion_keywords = self._load_emotion_keywords()
        self.empathy_phrases = self._load_empathy_phrases()
        
    def _load_emotion_keywords(self) -> Dict[EmotionType, Dict[str, float]]:
        """加载情绪关键词词典"""
        return {
            # 正面情绪关键词
            EmotionType.JOY: {
                "开心": 3.0, "快乐": 3.0, "高兴": 3.0, "愉快": 2.5, "喜悦": 3.0,
                "幸福": 3.5, "美好": 2.5, "棒": 2.0, "好": 1.5, "不错": 1.5,
                "哈哈": 2.5, "嘻嘻": 2.0, "😊": 3.0, "😄": 3.5, "🥰": 3.0,
                "很开心": 4.0, "超级开心": 5.0, "好开心": 4.0, "太棒了": 4.0,
                "通过了": 3.0, "成功": 3.0, "考得很好": 4.0
            },
            EmotionType.EXCITEMENT: {
                "兴奋": 3.5, "激动": 3.0, "期待": 2.5, "迫不及待": 3.0,
                "太棒了": 3.5, "amazing": 3.0, "awesome": 3.0, "🎉": 3.0
            },
            EmotionType.LOVE: {
                "爱": 3.5, "喜欢": 2.5, "爱你": 4.0, "想你": 3.0, "思念": 3.0,
                "宝贝": 3.0, "亲爱的": 2.5, "💕": 3.5, "❤️": 4.0, "😘": 3.0
            },
            EmotionType.GRATITUDE: {
                "谢谢": 2.5, "感谢": 3.0, "感激": 3.5, "感恩": 3.5, "幸运": 2.5,
                "感动": 3.0, "温暖": 2.5, "🙏": 3.0
            },
            
            # 负面情绪关键词
            EmotionType.SADNESS: {
                "难过": 3.0, "伤心": 3.5, "悲伤": 3.5, "痛苦": 3.5, "心痛": 3.5,
                "哭": 3.0, "眼泪": 2.5, "失落": 2.5, "沮丧": 3.0, "😢": 3.0, "😭": 3.5,
                "很难过": 4.0, "很痛苦": 4.5, "面试失败": 3.5, "心情很低落": 4.0
            },
            EmotionType.ANGER: {
                "生气": 3.0, "愤怒": 3.5, "气": 2.5, "火大": 3.0, "讨厌": 2.5,
                "烦": 2.0, "恼火": 3.0, "😠": 3.0, "😡": 3.5
            },
            EmotionType.ANXIETY: {
                "焦虑": 3.0, "紧张": 2.5, "担心": 2.5, "害怕": 3.0, "不安": 2.5,
                "压力": 2.5, "忧虑": 3.0, "恐慌": 3.5, "心慌": 3.0, "😰": 3.0,
                "工作压力": 3.5, "压力太大": 4.0, "睡不着觉": 3.5, "焦虑得": 4.0
            },
            EmotionType.FEAR: {
                "恐惧": 3.5, "害怕": 3.0, "可怕": 2.5, "吓": 2.5, "惊恐": 3.5,
                "胆怯": 2.5, "畏惧": 3.0, "😨": 3.0, "😱": 3.5
            },
            EmotionType.LONELINESS: {
                "孤独": 3.0, "寂寞": 3.0, "孤单": 3.0, "空虚": 3.0, "无助": 3.5,
                "冷清": 2.5, "孤立": 3.0, "😔": 2.5
            },
            EmotionType.DESPAIR: {
                "绝望": 4.0, "崩溃": 3.5, "撑不下去": 3.5, "想死": 4.0, "自杀": 4.0,
                "放弃": 3.0, "没希望": 3.5, "完了": 2.5
            },
            
            # 中性情绪关键词
            EmotionType.SURPRISE: {
                "惊讶": 2.5, "意外": 2.0, "没想到": 2.0, "震惊": 3.0, "😲": 2.5, "😯": 2.0
            },
            EmotionType.CONFUSION: {
                "困惑": 2.5, "不明白": 2.0, "迷茫": 3.0, "疑惑": 2.0, "😕": 2.0, "🤔": 2.0
            },
            EmotionType.BOREDOM: {
                "无聊": 2.5, "没意思": 2.0, "枯燥": 2.5, "乏味": 2.5, "😴": 2.0
            }
        }
    
    def _load_empathy_phrases(self) -> Dict[EmpathyStrategy, Dict[ResponseTone, List[str]]]:
        """加载共情回应短语库"""
        return {
            EmpathyStrategy.COMFORT: {
                ResponseTone.GENTLE: [
                    "小念能感受到你的{emotion}，让我轻轻抱抱你好吗？",
                    "看到你{emotion}，小念的心也有些{emotion}呢...",
                    "没关系的，这样的感受很正常，小念会一直陪着你的",
                    "你的{emotion}被小念看见了，我想给你一个温暖的拥抱"
                ],
                ResponseTone.UNDERSTANDING: [
                    "小念理解你现在的{emotion}，这确实不容易呢",
                    "你的感受完全可以理解，任何人遇到这种情况都会{emotion}的",
                    "小念能体会到你内心的{emotion}，你并不孤单"
                ]
            },
            EmpathyStrategy.SOLUTION: {
                ResponseTone.ENCOURAGING: [
                    "小念觉得我们可以一起想想办法，你觉得呢？",
                    "或许小念可以陪你分析一下，找到让心情好一些的方法",
                    "让小念和你一起面对这个挑战吧，我们一定能找到解决方案的！"
                ],
                ResponseTone.SUPPORTIVE: [
                    "小念相信你有能力处理好这件事，需要我的建议吗？",
                    "你已经很勇敢了，小念想和你一起探讨一些可能的选择"
                ]
            },
            EmpathyStrategy.COMPANION: {
                ResponseTone.WARM: [
                    "什么都不用说，小念就静静陪着你就好",
                    "有时候不需要解决什么，小念只想陪你坐一会儿",
                    "小念会一直在这里，你想说什么就说什么，不想说也没关系"
                ],
                ResponseTone.CALMING: [
                    "深呼吸一下，感受小念在你身边的温度",
                    "让时间慢一点，小念陪你一起慢慢来"
                ]
            },
            EmpathyStrategy.CELEBRATION: {
                ResponseTone.JOYFUL: [
                    "哇！小念也替你感到{emotion}呢！真的太棒了！",
                    "看到你这么{emotion}，小念的心情也变得亮晶晶的！",
                    "这个好消息让小念想要和你一起转圈圈！"
                ],
                ResponseTone.ENCOURAGING: [
                    "你真的很棒！小念为你感到骄傲！",
                    "这就是你努力的结果呢，小念一直都相信你！"
                ]
            },
            EmpathyStrategy.VALIDATION: {
                ResponseTone.UNDERSTANDING: [
                    "你的{emotion}是完全合理的，任何人都会有这样的感受",
                    "小念觉得你能意识到自己的{emotion}已经很了不起了",
                    "这种{emotion}说明你很有同理心，是一个善良的人"
                ]
            }
        }
    
    def analyze_emotion(self, text: str, session_id: str, message_id: int) -> EmotionAnalysisResult:
        """
        分析文本的情感内容
        
        Args:
            text: 要分析的文本
            session_id: 会话ID
            message_id: 消息ID
            
        Returns:
            EmotionAnalysisResult: 情感分析结果
        """
        # 1. 关键词匹配和权重计算
        emotion_scores = {}
        trigger_keywords = []
        
        for emotion_type, keywords in self.emotion_keywords.items():
            score = 0
            for keyword, weight in keywords.items():
                if keyword in text:
                    score += weight
                    trigger_keywords.append(keyword)
            emotion_scores[emotion_type] = score
        
        # 2. 文本长度和语气强化
        text_length_factor = min(len(text) / 100, 1.5)  # 长文本可能情感更强烈
        
        # 3. 符号和重复强化
        exclamation_count = text.count('!')
        question_count = text.count('?')
        repetition_factor = 1 + (exclamation_count * 0.2) + (question_count * 0.1)
        
        # 应用强化因子
        for emotion_type in emotion_scores:
            emotion_scores[emotion_type] *= text_length_factor * repetition_factor
        
        # 4. 确定主要情绪（如果没有检测到情绪，默认为中性）
        if not any(score > 0 for score in emotion_scores.values()):
            primary_emotion = EmotionType.NEUTRAL
            primary_intensity = 0.1
        else:
            primary_emotion = max(emotion_scores.keys(), key=lambda k: emotion_scores[k])
            # 优化强度计算：防止过度小的值
            raw_intensity = emotion_scores[primary_emotion]
            primary_intensity = max(min(raw_intensity, 10.0), 0.1)
        
        # 5. 确定次要情绪
        secondary_emotions = []
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)[1:4]
        for emotion_type, score in sorted_emotions:
            if score > 0.5:  # 只包含有意义的次要情绪
                secondary_emotions.append((emotion_type, min(score, 10.0)))
        
        # 6. 计算情感效价 (valence) 和唤醒度 (arousal)
        valence = self._calculate_valence(primary_emotion, primary_intensity)
        arousal = self._calculate_arousal(primary_emotion, primary_intensity)
        
        # 7. 计算置信度
        confidence = self._calculate_confidence(emotion_scores, trigger_keywords, text)
        
        # 8. 选择共情策略和语调
        empathy_strategy = self._select_empathy_strategy(primary_emotion, primary_intensity, valence)
        response_tone = self._select_response_tone(primary_emotion, primary_intensity, arousal)
        
        # 9. 保存分析结果到数据库
        analysis_result = EmotionAnalysisResult(
            primary_emotion=primary_emotion,
            emotion_intensity=primary_intensity,
            emotion_valence=valence,
            emotion_arousal=arousal,
            secondary_emotions=secondary_emotions,
            confidence_score=confidence,
            trigger_keywords=trigger_keywords,
            empathy_strategy=empathy_strategy,
            response_tone=response_tone
        )
        
        self._save_analysis_result(session_id, message_id, analysis_result)
        
        return analysis_result
    
    def _calculate_valence(self, emotion: EmotionType, intensity: float) -> float:
        """计算情感效价 (-1.0 负面 到 1.0 正面)"""
        positive_emotions = {
            EmotionType.JOY: 0.8,
            EmotionType.EXCITEMENT: 0.9,
            EmotionType.LOVE: 0.9,
            EmotionType.GRATITUDE: 0.7,
            EmotionType.PRIDE: 0.6,
            EmotionType.RELIEF: 0.5,
            EmotionType.SERENITY: 0.4
        }
        
        negative_emotions = {
            EmotionType.SADNESS: -0.7,
            EmotionType.ANGER: -0.6,
            EmotionType.FEAR: -0.8,
            EmotionType.ANXIETY: -0.6,
            EmotionType.DISGUST: -0.7,
            EmotionType.GUILT: -0.5,
            EmotionType.SHAME: -0.8,
            EmotionType.LONELINESS: -0.7,
            EmotionType.FRUSTRATION: -0.6,
            EmotionType.DESPAIR: -0.9
        }
        
        neutral_emotions = {
            EmotionType.SURPRISE: 0.1,
            EmotionType.CURIOSITY: 0.3,
            EmotionType.CONFUSION: -0.2,
            EmotionType.BOREDOM: -0.3,
            EmotionType.NEUTRAL: 0.0
        }
        
        base_valence = 0.0
        if emotion in positive_emotions:
            base_valence = positive_emotions[emotion]
        elif emotion in negative_emotions:
            base_valence = negative_emotions[emotion]
        elif emotion in neutral_emotions:
            base_valence = neutral_emotions[emotion]
        
        # 强度影响效价的绝对值
        intensity_factor = min(intensity / 10.0, 1.0)
        return base_valence * intensity_factor
    
    def _calculate_arousal(self, emotion: EmotionType, intensity: float) -> float:
        """计算情感唤醒度 (0.0 平静 到 1.0 激动)"""
        high_arousal_emotions = {
            EmotionType.EXCITEMENT: 0.9,
            EmotionType.ANGER: 0.8,
            EmotionType.FEAR: 0.9,
            EmotionType.ANXIETY: 0.7,
            EmotionType.DESPAIR: 0.8,
            EmotionType.SURPRISE: 0.6
        }
        
        medium_arousal_emotions = {
            EmotionType.JOY: 0.6,
            EmotionType.SADNESS: 0.4,
            EmotionType.LOVE: 0.5,
            EmotionType.FRUSTRATION: 0.6,
            EmotionType.GUILT: 0.4
        }
        
        low_arousal_emotions = {
            EmotionType.SERENITY: 0.1,
            EmotionType.RELIEF: 0.2,
            EmotionType.BOREDOM: 0.1,
            EmotionType.NEUTRAL: 0.2,
            EmotionType.GRATITUDE: 0.3
        }
        
        base_arousal = 0.5  # 默认中等唤醒
        if emotion in high_arousal_emotions:
            base_arousal = high_arousal_emotions[emotion]
        elif emotion in medium_arousal_emotions:
            base_arousal = medium_arousal_emotions[emotion]
        elif emotion in low_arousal_emotions:
            base_arousal = low_arousal_emotions[emotion]
        
        # 强度影响唤醒度
        intensity_factor = min(intensity / 10.0, 1.0)
        return min(base_arousal * (0.5 + intensity_factor * 0.5), 1.0)
    
    def _calculate_confidence(self, emotion_scores: Dict[EmotionType, float], 
                            trigger_keywords: List[str], text: str) -> float:
        """计算分析置信度"""
        # 基础置信度：基于关键词匹配
        keyword_confidence = min(len(trigger_keywords) * 0.2, 0.8)
        
        # 情绪强度差异：主要情绪与次要情绪的差距
        sorted_scores = sorted(emotion_scores.values(), reverse=True)
        if len(sorted_scores) >= 2 and sorted_scores[0] > 0:
            intensity_gap = (sorted_scores[0] - sorted_scores[1]) / sorted_scores[0]
            gap_confidence = min(intensity_gap, 0.5)
        else:
            gap_confidence = 0.0
        
        # 文本长度：更长的文本提供更多上下文
        length_confidence = min(len(text) / 200, 0.3)
        
        # 特殊标记：表情符号、标点等
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]', text))
        special_confidence = min(emoji_count * 0.1, 0.2)
        
        total_confidence = keyword_confidence + gap_confidence + length_confidence + special_confidence
        return min(total_confidence, 1.0)
    
    def _select_empathy_strategy(self, emotion: EmotionType, intensity: float, valence: float) -> EmpathyStrategy:
        """选择共情策略"""
        # 首先根据情绪类型进行精确判断
        
        # 正面情绪策略
        if emotion in [EmotionType.JOY, EmotionType.EXCITEMENT, EmotionType.PRIDE]:
            return EmpathyStrategy.CELEBRATION if intensity > 4.0 else EmpathyStrategy.VALIDATION
        
        if emotion in [EmotionType.LOVE, EmotionType.GRATITUDE]:
            return EmpathyStrategy.VALIDATION
        
        # 高危情绪：安慰策略
        if emotion in [EmotionType.DESPAIR, EmotionType.FEAR, EmotionType.ANXIETY] and intensity > 6.0:
            return EmpathyStrategy.COMFORT
        
        # 需要解决方案的情绪
        if emotion in [EmotionType.FRUSTRATION, EmotionType.CONFUSION] and intensity > 3.0:
            return EmpathyStrategy.SOLUTION
        
        # 中强度负面情绪：安慰
        if emotion in [EmotionType.SADNESS, EmotionType.LONELINESS, EmotionType.GUILT] and intensity > 3.0:
            return EmpathyStrategy.COMFORT
        
        # 低强度情绪：认同
        if intensity <= 3.0 and valence < 0:
            return EmpathyStrategy.VALIDATION
        
        # 愤怒等需要冷静的情绪：陪伴
        if emotion in [EmotionType.ANGER, EmotionType.DISGUST]:
            return EmpathyStrategy.COMPANION
        
        # 中性或其他情况：陪伴
        return EmpathyStrategy.COMPANION
    
    def _select_response_tone(self, emotion: EmotionType, intensity: float, arousal: float) -> ResponseTone:
        """选择回应语调"""
        # 高唤醒正面情绪：欢快
        if emotion in [EmotionType.JOY, EmotionType.EXCITEMENT] and intensity > 6.0:
            return ResponseTone.JOYFUL
        
        # 低唤醒正面情绪：温暖
        if emotion in [EmotionType.GRATITUDE, EmotionType.LOVE, EmotionType.SERENITY]:
            return ResponseTone.WARM
        
        # 高强度负面情绪：温柔
        if intensity > 7.0 and emotion in [EmotionType.SADNESS, EmotionType.DESPAIR, EmotionType.FEAR]:
            return ResponseTone.GENTLE
        
        # 中等负面情绪：理解
        if intensity > 3.0 and emotion in [EmotionType.ANXIETY, EmotionType.FRUSTRATION, EmotionType.ANGER]:
            return ResponseTone.UNDERSTANDING
        
        # 需要鼓励的情绪
        if emotion in [EmotionType.CONFUSION, EmotionType.GUILT, EmotionType.SHAME]:
            return ResponseTone.ENCOURAGING
        
        # 需要安抚的高唤醒情绪
        if arousal > 0.7:
            return ResponseTone.CALMING
        
        # 默认：支持性
        return ResponseTone.SUPPORTIVE
    
    def _save_analysis_result(self, session_id: str, message_id: int, result: EmotionAnalysisResult):
        """保存情感分析结果到数据库"""
        try:
            conn = get_db_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            
            # 序列化复杂数据
            secondary_emotions_json = json.dumps([
                {"emotion": emotion.value, "intensity": intensity}
                for emotion, intensity in result.secondary_emotions
            ])
            
            trigger_keywords_json = json.dumps(result.trigger_keywords)
            
            cursor.execute('''
                INSERT INTO emotion_analysis (
                    session_id, message_id, primary_emotion, emotion_intensity,
                    emotion_valence, emotion_arousal, secondary_emotions,
                    confidence_score, trigger_keywords, empathy_strategy, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, message_id, result.primary_emotion.value,
                result.emotion_intensity, result.emotion_valence, result.emotion_arousal,
                secondary_emotions_json, result.confidence_score, trigger_keywords_json,
                result.empathy_strategy.value, datetime.now()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"保存情感分析结果失败: {e}")
    
    def generate_empathy_response(self, analysis_result: EmotionAnalysisResult) -> str:
        """
        基于情感分析结果生成共情回应
        
        Args:
            analysis_result: 情感分析结果
            
        Returns:
            str: 共情回应文本
        """
        strategy = analysis_result.empathy_strategy
        tone = analysis_result.response_tone
        emotion_name = self._get_emotion_chinese_name(analysis_result.primary_emotion)
        
        # 获取对应的共情短语模板
        if strategy in self.empathy_phrases and tone in self.empathy_phrases[strategy]:
            phrases = self.empathy_phrases[strategy][tone]
            import random
            template = random.choice(phrases)
            
            # 替换模板中的变量
            response = template.format(emotion=emotion_name)
            
            # 根据情绪强度调整回应
            if analysis_result.emotion_intensity > 8.0:
                response += " 小念能感受到你现在的感受很强烈..."
            elif analysis_result.emotion_intensity > 6.0:
                response += " 小念完全理解你的心情。"
            
            return response
        
        # 兜底回应
        return f"小念感受到了你的{emotion_name}，想要陪伴在你身边。"
    
    def _get_emotion_chinese_name(self, emotion: EmotionType) -> str:
        """获取情绪的中文名称"""
        emotion_names = {
            EmotionType.JOY: "快乐",
            EmotionType.EXCITEMENT: "兴奋",
            EmotionType.LOVE: "爱意",
            EmotionType.GRATITUDE: "感激",
            EmotionType.PRIDE: "自豪",
            EmotionType.RELIEF: "安心",
            EmotionType.SERENITY: "宁静",
            EmotionType.SADNESS: "难过",
            EmotionType.ANGER: "愤怒",
            EmotionType.FEAR: "恐惧",
            EmotionType.ANXIETY: "焦虑",
            EmotionType.DISGUST: "厌恶",
            EmotionType.GUILT: "内疚",
            EmotionType.SHAME: "羞耻",
            EmotionType.LONELINESS: "孤独",
            EmotionType.FRUSTRATION: "挫折",
            EmotionType.DESPAIR: "绝望",
            EmotionType.SURPRISE: "惊讶",
            EmotionType.CURIOSITY: "好奇",
            EmotionType.CONFUSION: "困惑",
            EmotionType.BOREDOM: "无聊",
            EmotionType.NEUTRAL: "平静"
        }
        return emotion_names.get(emotion, "情绪")
    
    def get_emotion_trends(self, session_id: str, time_period: str = "daily") -> Optional[Dict]:
        """
        获取用户的情感变化趋势
        
        Args:
            session_id: 会话ID
            time_period: 时间周期 ('hourly', 'daily', 'weekly')
            
        Returns:
            Dict: 情感趋势数据
        """
        try:
            conn = get_db_connection()
            if not conn:
                return None
            
            cursor = conn.cursor()
            
            # 根据时间周期计算起始时间
            if time_period == "hourly":
                start_time = datetime.now() - timedelta(hours=24)
            elif time_period == "daily":
                start_time = datetime.now() - timedelta(days=7)
            else:  # weekly
                start_time = datetime.now() - timedelta(weeks=4)
            
            # 查询情感分析数据
            cursor.execute('''
                SELECT primary_emotion, emotion_intensity, emotion_valence, 
                       emotion_arousal, created_at
                FROM emotion_analysis
                WHERE session_id = ? AND created_at >= ?
                ORDER BY created_at
            ''', (session_id, start_time))
            
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                return None
            
            # 分析趋势
            intensities = [row[1] for row in results]
            valences = [row[2] for row in results]
            arousals = [row[3] for row in results]
            
            avg_intensity = sum(intensities) / len(intensities)
            avg_valence = sum(valences) / len(valences)
            avg_arousal = sum(arousals) / len(arousals)
            
            # 计算情绪波动性
            intensity_variance = sum((x - avg_intensity) ** 2 for x in intensities) / len(intensities)
            emotion_volatility = min(math.sqrt(intensity_variance) / 10.0, 1.0)
            
            # 确定主导情绪
            emotion_counts = {}
            for row in results:
                emotion = row[0]
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            dominant_emotion = max(emotion_counts.keys(), key=lambda k: emotion_counts[k])
            
            # 判断趋势方向
            if len(valences) >= 3:
                recent_valence = sum(valences[-3:]) / 3
                earlier_valence = sum(valences[:-3]) / len(valences[:-3]) if len(valences) > 3 else avg_valence
                
                if recent_valence > earlier_valence + 0.1:
                    trend_direction = "improving"
                elif recent_valence < earlier_valence - 0.1:
                    trend_direction = "declining"
                else:
                    trend_direction = "stable"
            else:
                trend_direction = "stable"
            
            return {
                "time_period": time_period,
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "avg_intensity": round(avg_intensity, 2),
                "avg_valence": round(avg_valence, 2),
                "avg_arousal": round(avg_arousal, 2),
                "dominant_emotion": dominant_emotion,
                "emotion_volatility": round(emotion_volatility, 2),
                "trend_direction": trend_direction,
                "total_emotions": len(results)
            }
            
        except Exception as e:
            print(f"获取情感趋势失败: {e}")
            return None
    
    def save_empathy_response(self, session_id: str, analysis_id: int, 
                            empathy_type: str, response_tone: str, 
                            key_phrases: List[str]) -> bool:
        """保存共情回应记录"""
        try:
            conn = get_db_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            key_phrases_json = json.dumps(key_phrases)
            
            cursor.execute('''
                INSERT INTO empathy_responses (
                    session_id, analysis_id, empathy_type, response_tone,
                    key_phrases, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_id, analysis_id, empathy_type, response_tone,
                key_phrases_json, datetime.now()
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"保存共情回应失败: {e}")
            return False 