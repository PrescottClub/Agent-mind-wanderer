"""
情绪急救包服务
检测用户的负面情绪，提供专业的心理急救技巧和引导
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class EmotionType(Enum):
    """负面情绪类型枚举"""
    ANXIETY = "焦虑"
    DEPRESSION = "抑郁"
    ANGER = "愤怒"
    PANIC = "恐慌"
    GRIEF = "悲伤"
    STRESS = "压力"
    LONELINESS = "孤独"
    DESPAIR = "绝望"
    SELF_HARM = "自伤倾向"  # 高危情况
    SUICIDAL = "自杀倾向"  # 紧急情况


class SeverityLevel(Enum):
    """情绪严重程度"""
    MILD = "轻度"
    MODERATE = "中度"
    SEVERE = "重度"
    CRITICAL = "危机"  # 需要专业干预


@dataclass
class EmotionDetectionResult:
    """情绪检测结果"""
    emotion_type: EmotionType
    severity: SeverityLevel
    confidence: float  # 检测置信度 0-1
    trigger_keywords: List[str]  # 触发的关键词
    is_emergency: bool  # 是否为紧急情况


@dataclass
class EmergencyTechnique:
    """急救技巧"""
    title: str
    description: str
    steps: List[str]
    duration: str  # 建议用时
    warning: Optional[str] = None  # 警告信息


class EmotionEmergencyService:
    """情绪急救包服务"""
    
    def __init__(self):
        self._init_emotion_patterns()
        self._init_emergency_techniques()
    
    def _init_emotion_patterns(self):
        """初始化情绪识别模式"""
        self.emotion_patterns = {
            EmotionType.ANXIETY: {
                "keywords": [
                    "焦虑", "紧张", "担心", "不安", "害怕", "恐惧", "心慌", "出汗",
                    "失眠", "睡不着", "心跳快", "呼吸困难", "胸闷", "手抖",
                    "考试", "面试", "压力大", "忐忑", "坐立不安", "心神不宁"
                ],
                "severity_patterns": {
                    SeverityLevel.MILD: ["有点担心", "稍微紧张", "轻微不安"],
                    SeverityLevel.MODERATE: ["很焦虑", "非常担心", "睡不好"],
                    SeverityLevel.SEVERE: ["极度焦虑", "恐慌发作", "无法控制"],
                    SeverityLevel.CRITICAL: ["无法呼吸", "觉得要死了", "完全失控"]
                }
            },
            
            EmotionType.DEPRESSION: {
                "keywords": [
                    "抑郁", "沮丧", "绝望", "无助", "无意义", "空虚", "麻木",
                    "不想动", "没兴趣", "没动力", "疲惫", "想哭", "难过",
                    "人生没意思", "活着累", "看不到希望", "黑暗", "孤独"
                ],
                "severity_patterns": {
                    SeverityLevel.MILD: ["有点沮丧", "心情不好", "没精神"],
                    SeverityLevel.MODERATE: ["很抑郁", "非常难过", "不想见人"],
                    SeverityLevel.SEVERE: ["极度绝望", "生活没意义", "完全失去希望"],
                    SeverityLevel.CRITICAL: ["想死", "不想活", "结束一切"]
                }
            },
            
            EmotionType.ANGER: {
                "keywords": [
                    "愤怒", "生气", "火大", "暴躁", "愤恨", "恼火", "烦躁",
                    "想打人", "想破坏", "控制不住", "暴力", "发脾气", "爆发"
                ],
                "severity_patterns": {
                    SeverityLevel.MILD: ["有点生气", "轻微不满"],
                    SeverityLevel.MODERATE: ["很愤怒", "非常生气"],
                    SeverityLevel.SEVERE: ["极度愤怒", "失去理智"],
                    SeverityLevel.CRITICAL: ["想伤害", "暴力冲动", "控制不住"]
                }
            },
            
            EmotionType.SELF_HARM: {
                "keywords": [
                    "自伤", "自残", "割腕", "伤害自己", "自我惩罚", "割伤",
                    "想伤害自己", "自虐", "自我摧残"
                ],
                "severity_patterns": {
                    SeverityLevel.CRITICAL: ["所有自伤相关都是危机"]
                }
            },
            
            EmotionType.SUICIDAL: {
                "keywords": [
                    "自杀", "结束生命", "死了算了", "不想活", "离开这个世界",
                    "一了百了", "解脱", "轻生", "自尽", "想死"
                ],
                "severity_patterns": {
                    SeverityLevel.CRITICAL: ["所有自杀相关都是紧急情况"]
                }
            }
        }
    
    def _init_emergency_techniques(self):
        """初始化急救技巧库"""
        self.emergency_techniques = {
            EmotionType.ANXIETY: [
                EmergencyTechnique(
                    title="4-7-8 呼吸法",
                    description="通过调节呼吸来缓解焦虑，这是最有效的快速放松技巧之一",
                    steps=[
                        "1. 舒适地坐着或躺着，脊椎挺直",
                        "2. 用鼻子吸气4秒，感受空气进入肺部",
                        "3. 屏住呼吸7秒，让氧气充分循环",
                        "4. 用嘴巴慢慢呼气8秒，想象紧张离开身体",
                        "5. 重复3-4次，感受身体的放松"
                    ],
                    duration="3-5分钟"
                ),
                EmergencyTechnique(
                    title="5-4-3-2-1 接地技巧",
                    description="通过感官觉察来缓解焦虑，帮助回到当下",
                    steps=[
                        "1. 说出5样你能看到的东西",
                        "2. 说出4样你能触摸到的东西", 
                        "3. 说出3样你能听到的声音",
                        "4. 说出2样你能闻到的气味",
                        "5. 说出1样你能品尝到的味道"
                    ],
                    duration="5-10分钟"
                )
            ],
            
            EmotionType.DEPRESSION: [
                EmergencyTechnique(
                    title="积极行为激活",
                    description="通过小步骤的积极行动来提升情绪",
                    steps=[
                        "1. 选择一个非常简单的活动（如洗脸、喝水）",
                        "2. 专注完成这个小任务",
                        "3. 给自己一个小小的赞美",
                        "4. 如果感觉好一些，再尝试下一个小任务",
                        "5. 记录自己完成的每一件小事"
                    ],
                    duration="每次5-10分钟"
                ),
                EmergencyTechnique(
                    title="三件好事练习",
                    description="专注发现生活中的积极面，重建希望感",
                    steps=[
                        "1. 回想今天发生的三件好事（再小都可以）",
                        "2. 写下为什么这些事情是好的",
                        "3. 感受这些好事带来的温暖感觉",
                        "4. 对自己说：'我值得拥有好事'",
                        "5. 每天坚持这个练习"
                    ],
                    duration="10-15分钟"
                )
            ],
            
            EmotionType.ANGER: [
                EmergencyTechnique(
                    title="愤怒冷却技巧",
                    description="安全地释放愤怒能量，避免伤害自己和他人",
                    steps=[
                        "1. 立即离开引发愤怒的环境",
                        "2. 进行剧烈的身体运动（如快走、做俯卧撑）",
                        "3. 大声说出'停止'或'冷静'",
                        "4. 用冷水洗脸或洗手",
                        "5. 等待至少20分钟再做重要决定"
                    ],
                    duration="20-30分钟"
                )
            ],
            
            EmotionType.PANIC: [
                EmergencyTechnique(
                    title="恐慌发作应对",
                    description="在恐慌发作时保持安全和镇定",
                    steps=[
                        "1. 提醒自己：这是恐慌，不是危险，会过去的",
                        "2. 找一个安全的地方坐下",
                        "3. 专注于缓慢深呼吸，不要过度换气",
                        "4. 握紧拳头再放松，重复几次",
                        "5. 等待感觉自然消退（通常10-20分钟）"
                    ],
                    duration="15-20分钟",
                    warning="如果症状持续或频繁发作，请寻求专业帮助"
                )
            ]
        }
    
    def detect_emotion(self, text: str) -> Optional[EmotionDetectionResult]:
        """
        检测文本中的负面情绪
        返回最匹配的情绪检测结果
        """
        text_lower = text.lower()
        best_match = None
        highest_confidence = 0.0
        
        for emotion_type, patterns in self.emotion_patterns.items():
            # 计算关键词匹配度
            matched_keywords = []
            for keyword in patterns["keywords"]:
                if keyword in text_lower:
                    matched_keywords.append(keyword)
            
            if not matched_keywords:
                continue
            
            # 计算置信度（匹配关键词数量 / 总关键词数量）
            confidence = len(matched_keywords) / len(patterns["keywords"])
            
            # 如果有多个关键词匹配，增加置信度
            if len(matched_keywords) > 1:
                confidence += 0.2
            
            # 检测严重程度
            severity = self._detect_severity(text_lower, patterns["severity_patterns"])
            
            # 高危情况直接标记为紧急
            is_emergency = (emotion_type in [EmotionType.SELF_HARM, EmotionType.SUICIDAL] or 
                          severity == SeverityLevel.CRITICAL)
            
            if confidence > highest_confidence:
                highest_confidence = confidence
                best_match = EmotionDetectionResult(
                    emotion_type=emotion_type,
                    severity=severity,
                    confidence=confidence,
                    trigger_keywords=matched_keywords,
                    is_emergency=is_emergency
                )
        
        # 只有置信度足够高才返回结果
        if highest_confidence >= 0.1:  # 至少10%的关键词匹配
            return best_match
        
        return None
    
    def _detect_severity(self, text: str, severity_patterns: Dict) -> SeverityLevel:
        """检测情绪严重程度"""
        for severity, patterns in reversed(list(severity_patterns.items())):
            for pattern in patterns:
                if pattern in text:
                    return severity
        
        # 默认为轻度
        return SeverityLevel.MILD
    
    def get_emergency_techniques(self, emotion_type: EmotionType) -> List[EmergencyTechnique]:
        """获取特定情绪的急救技巧"""
        return self.emergency_techniques.get(emotion_type, [])
    
    def get_crisis_resources(self) -> Dict[str, str]:
        """获取危机干预资源"""
        return {
            "中国心理危机干预热线": "400-161-9995",
            "北京危机干预热线": "400-161-9995",
            "上海心理援助热线": "021-64387777",
            "广州心理危机干预热线": "020-81899120",
            "全国通用": "拨打120急救电话或前往最近的医院急诊科",
            "温馨提醒": "如果有自伤或自杀想法，请立即寻求专业帮助，你的生命很珍贵"
        }
    
    def format_emergency_response(self, detection_result: EmotionDetectionResult) -> Dict:
        """格式化急救回应"""
        techniques = self.get_emergency_techniques(detection_result.emotion_type)
        
        response = {
            "emotion_detected": detection_result.emotion_type.value,
            "severity": detection_result.severity.value,
            "is_emergency": detection_result.is_emergency,
            "empathy_message": self._get_empathy_message(detection_result),
            "techniques": techniques[:2],  # 提供最多2个技巧，避免信息过载
            "support_message": self._get_support_message(detection_result),
            "crisis_resources": self.get_crisis_resources() if detection_result.is_emergency else None
        }
        
        return response
    
    def _get_empathy_message(self, result: EmotionDetectionResult) -> str:
        """获取共情信息"""
        empathy_messages = {
            EmotionType.ANXIETY: f"小念感受到了你的{result.emotion_type.value}，这种感觉很不舒服，但你并不孤单。焦虑是可以缓解的，让我们一起来处理它。",
            EmotionType.DEPRESSION: f"小念看到你正在经历{result.emotion_type.value}，这一定很痛苦。请记住，这些感觉会过去的，你比你想象的更坚强。",
            EmotionType.ANGER: f"小念理解你现在很{result.emotion_type.value}，愤怒是正常的情绪，关键是要安全地处理它。",
            EmotionType.PANIC: "小念知道恐慌的感觉很可怕，但请记住：你是安全的，这种感觉会过去。",
            EmotionType.SELF_HARM: "小念很担心你，你的痛苦是真实的，但伤害自己不是解决办法。让我们找到更好的应对方式。",
            EmotionType.SUICIDAL: "小念非常关心你的安全。你现在的痛苦是暂时的，但选择离开是永久的。请让专业人士帮助你度过这个困难时期。"
        }
        
        return empathy_messages.get(result.emotion_type, "小念感受到了你的痛苦，让我们一起面对这个困难。")
    
    def _get_support_message(self, result: EmotionDetectionResult) -> str:
        """获取支持信息"""
        if result.is_emergency:
            return "🚨 如果你现在有伤害自己的想法，请立即联系专业帮助热线或身边的亲友。你的生命很宝贵，总有人愿意帮助你。"
        elif result.severity in [SeverityLevel.SEVERE, SeverityLevel.CRITICAL]:
            return "💙 小念建议你考虑寻求专业心理咨询师的帮助。专业支持可以更好地帮助你应对这些困难情绪。"
        else:
            return "💕 小念会一直陪伴你。如果这些技巧没有帮助，或者感觉更糟，请不要犹豫寻求更多支持。" 