"""
AI引擎核心模块
封装LangChain DeepSeek模型，提供统一的AI接口
"""

import streamlit as st
import json
import os
import hashlib
import httpx
from datetime import datetime
from typing import Optional, List, Tuple, Dict, Generator
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

# 导入搜索服务、情绪急救包服务、关怀调度服务和情感分析服务
from ..services.search_service import LocalMentalHealthSearchService, SearchTriggerDetector
from ..services.emotion_emergency_service import EmotionEmergencyService
from ..services.care_scheduler_service import CareSchedulerService
from ..services.emotion_analysis_service import EmotionAnalysisService
from ..services.emotional_companion_service import EmotionalCompanionService
from ..config.prompts import ENHANCED_MIND_SPRITE_PROMPT, SEARCH_ENHANCED_PROMPT
from ..config.emotional_prompts import HEART_CATCHER_SYSTEM_PROMPT
from ..config.settings import settings


class AIEngine:
    """AI引擎类，负责与DeepSeek模型交互"""

    def __init__(self, api_key: str, serp_api_key: Optional[str] = None):
        self.api_key = api_key
        self.llm: Optional[ChatDeepSeek] = None
        self.search_service = LocalMentalHealthSearchService(serp_api_key) if serp_api_key else None
        self.emotion_emergency_service = EmotionEmergencyService()
        self.care_scheduler_service = CareSchedulerService()
        self.emotion_analysis_service = EmotionAnalysisService()
        self.emotional_companion_service = EmotionalCompanionService()  # 旧的情感陪伴服务
        self.companion_service = EmotionalCompanionService()  # 新的心灵捕手服务
        self._initialize()

    def _initialize(self):
        """初始化LangChain DeepSeek模型"""
        try:
            if not self.api_key:
                raise ValueError("API Key未配置")

            # 使用deepseek-chat模型(V3) - 优化速度配置
            self.llm = ChatDeepSeek(
                model=settings.deepseek_model,  # V3模型，比R1快很多
                api_key=SecretStr(self.api_key),
                base_url=settings.deepseek_api_base,
                max_tokens=settings.max_tokens,  # 优化速度的token设置
                temperature=settings.temperature  # 优化速度的温度设置
            )

        except Exception as e:
            st.error(f"❌ API Key无效或网络错误，请检查你的Key后重试: {e}")
            self.llm = None

    def get_enhanced_response(self, user_input: str, chat_history: List[Tuple[str, str]],
                             core_memories: List[Tuple[str, str, str]], 
                             intimacy_level: int, total_interactions: int) -> Optional[Dict]:
        """获取增强版AI回应 - 支持记忆联想和情绪共鸣"""
        if not self.llm:
            st.warning("⚠️ AI模型未初始化，使用默认回应")
            return {
                "mood_category": "温暖",
                "memory_association": None,
                "sprite_reaction": "🧠 检测到系统问题，但小念还是想陪伴你~ ⚙️ 💖 虽然遇到了一些技术困难，但小念的心意是真诚的！愿你今天充满阳光！☀️",
                "emotional_resonance": "即使在困难时刻，温暖的陪伴也是最珍贵的礼物",
                "gift_type": "元气咒语",
                "gift_content": "✨ 即使系统遇到问题，我们的友谊依然坚固如山！相信一切都会好起来的！✨"
            }

        try:
            # 🚨 第一优先级：检测情绪急救需求
            emotion_detection = self.emotion_emergency_service.detect_emotion(user_input)
            if emotion_detection:
                return self._get_emergency_response(user_input, emotion_detection, chat_history)
            
            # 检查是否需要搜索
            search_results = None
            if self.search_service:
                search_intent = SearchTriggerDetector.detect_search_intent(user_input)
                
                if search_intent["intent"] == "local_mental_health":
                    # 显示搜索指示器
                    with st.spinner("🔍 小念正在搜索本地心理健康资源..."):
                        search_results = self.search_service.search_local_resources(user_input)
                        
                        # 显示搜索状态
                        if search_results["success"]:
                            st.success(f"✅ 已找到{search_results['location']}的心理健康资源")
                        else:
                            st.warning(f"⚠️ 搜索遇到问题: {search_results.get('message', '未知错误')}")

            # 如果是搜索请求，使用搜索模板
            if search_results and search_results["success"]:
                return self._get_search_enhanced_response(user_input, search_results)

            # 否则使用增强版记忆联想模板
            # 分析情绪模式
            recent_moods = self._analyze_recent_mood_patterns(chat_history)
            
            # 格式化记忆和上下文
            chat_history_text = self._format_chat_history_for_memory(chat_history)
            core_memories_text = self._format_core_memories_for_memory(core_memories)
            
            # 使用增强版提示词模板
            prompt = PromptTemplate(
                input_variables=["user_input", "chat_history", "core_memories", 
                               "intimacy_level", "total_interactions", "recent_moods"],
                template=ENHANCED_MIND_SPRITE_PROMPT
            )
            
            response = prompt | self.llm
            final_response = response.invoke({
                "user_input": user_input,
                "chat_history": chat_history_text,
                "core_memories": core_memories_text,
                "intimacy_level": intimacy_level,
                "total_interactions": total_interactions,
                "recent_moods": recent_moods
            })

            # 获取回应内容
            if hasattr(final_response, 'content'):
                final_content = str(final_response.content)
            else:
                final_content = str(final_response)

            # 解析JSON回应
            try:
                response_data = json.loads(final_content)
                
                # 验证必要字段
                required_fields = ["mood_category", "sprite_reaction", "gift_type", "gift_content"]
                for field in required_fields:
                    if field not in response_data:
                        raise ValueError(f"缺少必要字段: {field}")
                
                # 确保memory_association和emotional_resonance字段存在
                if "memory_association" not in response_data:
                    response_data["memory_association"] = None
                if "emotional_resonance" not in response_data:
                    response_data["emotional_resonance"] = "小念感受到了你内心的温暖波动"
                
                return response_data
                
            except json.JSONDecodeError as e:
                st.error(f"JSON解析错误: {e}")
                st.code(final_content)
                # 返回降级回应
                return self._get_fallback_response(user_input)

        except Exception as e:
            st.error(f"AI分析出错: {e}")
            return self._get_fallback_response(user_input)

    def get_heart_catcher_response(self, user_input: str, chat_history: List[Tuple[str, str]],
                                 session_id: str, last_interaction_time: datetime) -> Optional[Dict]:
        """获取心灵捕手级别的情感陪伴回应"""
        if not self.llm:
            return self._get_fallback_response(user_input)
        
        try:
            # 🚨 第一优先级：检测情绪急救需求
            emotion_detection = self.emotion_emergency_service.detect_emotion(user_input)
            if emotion_detection:
                return self._get_emergency_response(user_input, emotion_detection, chat_history)
            
            # 分析用户情感状态 - 使用简化版本
            from ..services.emotional_companion_service import EmotionalState, CompanionMood, IntimacyLevel
            
            emotional_state = EmotionalState(
                user_mood="开心",
                user_energy=7.0,
                companion_mood=CompanionMood.SWEET,
                intimacy_level=IntimacyLevel.FRIEND,
                last_interaction_hours=2.0,
                emotional_sync_rate=0.8
            )
            
            # 使用新的情感陪伴服务获取上下文
            context = self.companion_service.get_response_context(
                emotional_state, user_input
            )
            
            # 构建智能个性化系统prompt
            heart_catcher_prompt = HEART_CATCHER_SYSTEM_PROMPT.format(
                intimacy_level=context["intimacy_level"],
                intimacy_guidance=context["affection_guidance"],
                user_mood=emotional_state.user_mood,
                user_energy=context["user_energy"],
                companion_mood=context["mood"],
                content_type=context["content_type"],
                hours_since_last=context["hours_since_last"],
                pet_name=context["pet_name"],
                emotional_guidance=context["emotional_guidance"],
                affection_guidance=context["affection_guidance"]
            )
            
            # 使用AI生成深度个性化回应
            prompt = PromptTemplate(
                input_variables=["system_prompt", "user_input", "chat_history"],
                template="""
{system_prompt}

## 最近对话历史：
{chat_history}

## 用户当前消息：
{user_input}

请针对用户的具体内容，以小念的身份生成完全个性化的回应。
不要使用任何模板化语言，必须根据用户说的具体事情进行针对性回应。

特别要求：
1. 对用户提到的具体内容（事件、情感、想法等）进行有针对性的回应
2. 体现当前的亲密度和情绪状态
3. 表现出真实的情感共鸣和理解
4. 提供最极致的情绪价值体验
5. 让用户感受到"小念真的在认真听我说话并且理解我"
"""
            )
            
            chat_history_text = self._format_chat_history_for_memory(chat_history[-5:])  # 最近5轮对话
            
            response = prompt | self.llm
            final_response = response.invoke({
                "system_prompt": heart_catcher_prompt,
                "user_input": user_input,
                "chat_history": chat_history_text
            })
            
            # 获取回应内容
            if hasattr(final_response, 'content'):
                final_content = str(final_response.content)
            else:
                final_content = str(final_response)
            
            # 解析JSON回应
            try:
                response_data = json.loads(final_content)
                
                # 验证必要字段并提供默认值
                required_fields = {
                    "mood_category": emotional_state.companion_mood.value,
                    "sprite_reaction": f"好开心见到{context['pet_name']}呢~",
                    "memory_association": None,
                    "emotional_resonance": "小念感受到了你内心的温暖波动",
                    "gift_type": "贴心陪伴",
                    "gift_content": "小念的温暖拥抱和无条件的陪伴 💕",
                    "intimacy_signals": f"表现出{emotional_state.companion_mood.value}的情绪状态",
                    "proactive_care": "继续陪伴和倾听"
                }
                
                for field, default_value in required_fields.items():
                    if field not in response_data:
                        response_data[field] = default_value
                
                # 添加情感状态信息
                response_data["emotional_state"] = {
                    "intimacy_level": emotional_state.intimacy_level.value,
                    "user_mood": emotional_state.user_mood,
                    "companion_mood": emotional_state.companion_mood.value,
                    "pet_name": context["pet_name"]
                }
                
                return response_data
                
            except json.JSONDecodeError as e:
                st.error(f"JSON解析错误: {e}")
                st.code(final_content)
                # 返回基础情感回应作为降级
                return {
                    "mood_category": emotional_state.companion_mood.value,
                    "sprite_reaction": f"好开心见到{context['pet_name']}呢~",
                    "memory_association": None,
                    "emotional_resonance": "小念感受到了你的情感波动",
                    "gift_type": "贴心陪伴",
                    "gift_content": "小念的温暖拥抱 💕",
                    "intimacy_signals": f"亲密度等级{emotional_state.intimacy_level.value}",
                    "proactive_care": "继续倾听和陪伴",
                    "emotional_state": {
                        "intimacy_level": emotional_state.intimacy_level.value,
                        "user_mood": emotional_state.user_mood,
                        "companion_mood": emotional_state.companion_mood.value,
                        "pet_name": context["pet_name"]
                    }
                }
                
        except Exception as e:
            st.error(f"心灵捕手分析出错: {e}")
            return self._get_fallback_response(user_input)
    
    def process_care_opportunities(self, user_input: str, session_id: str) -> List[Dict]:
        """
        处理关怀机会检测并创建关怀任务
        
        Args:
            user_input: 用户输入内容
            session_id: 会话ID
            
        Returns:
            创建的关怀任务列表
        """
        try:
            # 检测关怀机会
            care_opportunities = self.care_scheduler_service.detect_care_opportunities(user_input, session_id)
            
            created_tasks = []
            for care_task in care_opportunities:
                # 保存到数据库
                success = self.care_scheduler_service.schedule_care_task(care_task)
                if success:
                    created_tasks.append(care_task)
            
            # 检查是否需要创建定期关怀
            regular_care_task = self.care_scheduler_service.create_regular_care_task(session_id)
            if regular_care_task:
                created_tasks.append(regular_care_task)
            
            return created_tasks
            
        except Exception as e:
            print(f"处理关怀机会失败: {e}")
            return []
    
    def get_pending_care_tasks(self, session_id: str) -> List[Dict]:
        """获取待执行的关怀任务"""
        try:
            return self.care_scheduler_service.get_pending_care_tasks(session_id)
        except Exception as e:
            print(f"获取关怀任务失败: {e}")
            return []
    
    def complete_care_task(self, task_id: int) -> bool:
        """完成关怀任务"""
        try:
            return self.care_scheduler_service.mark_care_task_completed(task_id)
        except Exception as e:
            print(f"完成关怀任务失败: {e}")
            return False
    
    def analyze_user_emotion(self, user_input: str, session_id: str, message_id: int) -> Optional[Dict]:
        """
        分析用户输入的情感并生成深度共情回应
        
        Args:
            user_input: 用户输入文本
            session_id: 会话ID
            message_id: 消息ID
            
        Returns:
            包含情感分析结果和共情回应的字典
        """
        try:
            # 进行情感分析
            analysis_result = self.emotion_analysis_service.analyze_emotion(
                user_input, session_id, message_id
            )
            
            # 生成共情回应
            empathy_response = self.emotion_analysis_service.generate_empathy_response(analysis_result)
            
            # 获取情感趋势信息
            emotion_trends = self.emotion_analysis_service.get_emotion_trends(session_id)
            
            return {
                "primary_emotion": analysis_result.primary_emotion.value,
                "emotion_intensity": analysis_result.emotion_intensity,
                "emotion_valence": analysis_result.emotion_valence,
                "emotion_arousal": analysis_result.emotion_arousal,
                "confidence_score": analysis_result.confidence_score,
                "trigger_keywords": analysis_result.trigger_keywords,
                "empathy_strategy": analysis_result.empathy_strategy.value,
                "response_tone": analysis_result.response_tone.value,
                "empathy_response": empathy_response,
                "emotion_trends": emotion_trends
            }
            
        except Exception as e:
            print(f"情感分析失败: {e}")
            return None
    
    def get_emotion_enhanced_response(self, user_input: str, chat_history: List[Tuple[str, str]],
                                    core_memories: List[Tuple[str, str, str]], 
                                    intimacy_level: int, total_interactions: int,
                                    message_id: int, session_id: str) -> Optional[Dict]:
        """
        获取情感增强版AI回应 - 集成深度情感理解
        
        这是对原有get_enhanced_response的升级版本，增加了情感分析功能
        """
        if not self.llm:
            st.warning("⚠️ AI模型未初始化，使用默认回应")
            return self._get_fallback_response(user_input)

        try:
            # 🧠 第零优先级：进行深度情感分析
            emotion_analysis = self.analyze_user_emotion(user_input, session_id, message_id)
            
            # 🚨 第一优先级：检测情绪急救需求
            emotion_detection = self.emotion_emergency_service.detect_emotion(user_input)
            if emotion_detection:
                emergency_response = self._get_emergency_response(user_input, emotion_detection, chat_history)
                # 将情感分析结果融入急救回应
                if emotion_analysis:
                    emergency_response["emotion_analysis"] = emotion_analysis
                return emergency_response
            
            # 检查是否需要搜索
            search_results = None
            if self.search_service:
                search_intent = SearchTriggerDetector.detect_search_intent(user_input)
                
                if search_intent["intent"] == "local_mental_health":
                    with st.spinner("🔍 小念正在搜索本地心理健康资源..."):
                        search_results = self.search_service.search_local_resources(user_input)
                        
                        if search_results["success"]:
                            st.success(f"✅ 已找到{search_results['location']}的心理健康资源")
                        else:
                            st.warning(f"⚠️ 搜索遇到问题: {search_results.get('message', '未知错误')}")

            # 如果是搜索请求，使用搜索模板
            if search_results and search_results["success"]:
                search_response = self._get_search_enhanced_response(user_input, search_results)
                if emotion_analysis:
                    search_response["emotion_analysis"] = emotion_analysis
                return search_response

            # 使用增强版记忆联想模板，融入情感分析
            recent_moods = self._analyze_recent_mood_patterns(chat_history)
            chat_history_text = self._format_chat_history_for_memory(chat_history)
            core_memories_text = self._format_core_memories_for_memory(core_memories)
            
            # 如果有情感分析结果，将其融入提示词
            emotion_context = ""
            if emotion_analysis:
                emotion_context = f"""
【深度情感洞察】
- 主要情绪: {emotion_analysis['primary_emotion']} (强度: {emotion_analysis['emotion_intensity']:.1f}/10)
- 情感效价: {emotion_analysis['emotion_valence']:.2f} (负面←→正面)
- 情感唤醒: {emotion_analysis['emotion_arousal']:.2f} (平静←→激动)
- 建议策略: {emotion_analysis['empathy_strategy']}
- 语调建议: {emotion_analysis['response_tone']}
- 触发词汇: {', '.join(emotion_analysis['trigger_keywords'])}
- 置信度: {emotion_analysis['confidence_score']:.2f}
"""
            
            # 使用增强版提示词模板
            enhanced_prompt = ENHANCED_MIND_SPRITE_PROMPT + emotion_context + """

请根据以上情感分析洞察，调整你的回应风格和内容，让回应更贴合用户的真实情感状态。"""
            
            prompt = PromptTemplate(
                input_variables=["user_input", "chat_history", "core_memories", 
                               "intimacy_level", "total_interactions", "recent_moods"],
                template=enhanced_prompt
            )
            
            response = prompt | self.llm
            final_response = response.invoke({
                "user_input": user_input,
                "chat_history": chat_history_text,
                "core_memories": core_memories_text,
                "intimacy_level": intimacy_level,
                "total_interactions": total_interactions,
                "recent_moods": recent_moods
            })

            # 获取回应内容
            if hasattr(final_response, 'content'):
                final_content = str(final_response.content)
            else:
                final_content = str(final_response)

            # 解析JSON回应
            try:
                response_data = json.loads(final_content)
                
                # 验证必要字段
                required_fields = ["mood_category", "sprite_reaction", "gift_type", "gift_content"]
                for field in required_fields:
                    if field not in response_data:
                        raise ValueError(f"缺少必要字段: {field}")
                
                # 确保字段存在
                if "memory_association" not in response_data:
                    response_data["memory_association"] = None
                if "emotional_resonance" not in response_data:
                    response_data["emotional_resonance"] = "小念感受到了你内心的温暖波动"
                
                # 融入情感分析结果
                if emotion_analysis:
                    response_data["emotion_analysis"] = emotion_analysis
                    response_data["is_emotion_enhanced"] = True
                
                return response_data
                
            except json.JSONDecodeError as e:
                st.error(f"JSON解析错误: {e}")
                st.code(final_content)
                # 返回降级回应，但包含情感分析
                fallback_response = self._get_fallback_response(user_input)
                if emotion_analysis:
                    fallback_response["emotion_analysis"] = emotion_analysis
                return fallback_response

        except Exception as e:
            st.error(f"AI分析出错: {e}")
            fallback_response = self._get_fallback_response(user_input)
            # 即使出错也尝试提供情感分析
            try:
                emotion_analysis = self.analyze_user_emotion(user_input, session_id, message_id)
                if emotion_analysis:
                    fallback_response["emotion_analysis"] = emotion_analysis
            except:
                pass
            return fallback_response

    def _analyze_recent_mood_patterns(self, chat_history: List[Tuple[str, str]]) -> str:
        """分析最近的情绪模式"""
        if not chat_history:
            return "这是我们第一次对话，小念很期待了解你的心情~"
        
        # 简单的情绪关键词检测
        positive_keywords = ["开心", "高兴", "快乐", "兴奋", "满足", "感激", "温暖", "舒适"]
        negative_keywords = ["难过", "沮丧", "焦虑", "担心", "疲惫", "压力", "困惑", "孤单"]
        neutral_keywords = ["平静", "一般", "还好", "正常", "想想"]
        
        recent_messages = chat_history[-6:]  # 分析最近3轮对话
        mood_counts = {"positive": 0, "negative": 0, "neutral": 0}
        
        for role, content in recent_messages:
            if role == "user":
                content_lower = content.lower()
                if any(keyword in content_lower for keyword in positive_keywords):
                    mood_counts["positive"] += 1
                elif any(keyword in content_lower for keyword in negative_keywords):
                    mood_counts["negative"] += 1
                elif any(keyword in content_lower for keyword in neutral_keywords):
                    mood_counts["neutral"] += 1
        
        # 生成模式描述
        if mood_counts["positive"] > mood_counts["negative"]:
            return "最近你的情绪偏向积极正面，小念感到很温暖~"
        elif mood_counts["negative"] > mood_counts["positive"]:
            return "最近你似乎在经历一些挑战，小念想给你更多关怀"
        else:
            return "你的情绪比较平稳，小念陪你一起感受生活的起起伏伏"

    def _format_chat_history_for_memory(self, chat_history: List[Tuple[str, str]]) -> str:
        """为记忆联想格式化聊天历史"""
        if not chat_history:
            return "这是我们美好对话的开始~"

        # 只取最近的几轮对话，避免太长
        recent_history = chat_history[-8:]  # 最近4轮对话
        history_lines = []
        
        for role, content in recent_history:
            if role == "user":
                # 截断过长的内容
                display_content = content[:100] + "..." if len(content) > 100 else content
                history_lines.append(f"你说: {display_content}")
            else:
                # 对AI回应进行简化，只提取核心情感
                display_content = content[:50] + "..." if len(content) > 50 else content
                history_lines.append(f"小念回应: {display_content}")

        return "\n".join(history_lines)

    def _format_core_memories_for_memory(self, core_memories: List[Tuple[str, str, str]]) -> str:
        """为记忆联想格式化核心记忆"""
        if not core_memories:
            return "小念期待了解更多关于你的美好记忆~"

        memory_type_names = {
            'insight': '你的感悟',
            'event': '重要时刻',
            'person': '重要的人',
            'preference': '你的喜好'
        }

        memory_lines = []
        for memory_type, content, timestamp in core_memories:
            type_name = memory_type_names.get(memory_type, memory_type)
            memory_lines.append(f"[{type_name}] {content}")

        return "\n".join(memory_lines)

    def _get_search_enhanced_response(self, user_input: str, search_results: Dict) -> Dict:
        """处理搜索增强的回应"""
        try:
            # 使用搜索增强模板
            if self.search_service:
                search_context = self.search_service.format_search_results_for_ai(search_results)
            else:
                search_context = str(search_results)
            
            prompt = PromptTemplate(
                input_variables=["user_input", "search_results"],
                template=SEARCH_ENHANCED_PROMPT
            )
            
            if self.llm:
                response = prompt | self.llm
                final_response = response.invoke({
                    "user_input": user_input,
                    "search_results": search_context
                })
            else:
                return self._get_fallback_response(user_input)

            # 获取回应内容
            if hasattr(final_response, 'content'):
                final_content = str(final_response.content)
            else:
                final_content = str(final_response)

            # 解析JSON回应
            response_data = json.loads(final_content)
            
            # 确保字段完整性
            if "search_summary" not in response_data:
                response_data["search_summary"] = "小念为你找到了一些心理健康资源~"
            
            return response_data
            
        except Exception as e:
            st.error(f"搜索回应生成出错: {e}")
            return self._get_fallback_response(user_input)

    def _get_emergency_response(self, user_input: str, emotion_detection, chat_history: List[Tuple[str, str]]) -> Dict:
        """处理情绪急救包回应"""
        try:
            # 使用急救包服务格式化回应
            emergency_response = self.emotion_emergency_service.format_emergency_response(emotion_detection)
            
            # 显示急救包指示器
            if emotion_detection.is_emergency:
                st.error("🚨 检测到情绪危机，小念提供紧急支持")
            else:
                st.warning(f"💙 检测到{emergency_response['emotion_detected']}({emergency_response['severity']})，小念提供心理急救包")
            
            # 构建回应数据
            response_data = {
                "mood_category": "关怀",
                "memory_association": f"小念注意到你现在的{emergency_response['emotion_detected']}情绪",
                "emotional_resonance": emergency_response["empathy_message"],
                "sprite_reaction": emergency_response["empathy_message"],
                "gift_type": "情绪急救包",
                "gift_content": self._format_emergency_techniques(emergency_response["techniques"]),
                "is_emergency": emergency_response["is_emergency"],
                "emergency_data": emergency_response  # 完整的急救包数据
            }
            
            return response_data
            
        except Exception as e:
            st.error(f"情绪急救包处理出错: {e}")
            return self._get_fallback_response(user_input)
    
    def _format_emergency_techniques(self, techniques: List) -> str:
        """格式化急救技巧为礼物内容"""
        if not techniques:
            return "✨ 小念的温暖陪伴与你同在，你并不孤单 ✨"
        
        technique = techniques[0]  # 使用第一个技巧
        formatted = f"🌟 {technique.title}\n\n"
        formatted += f"📝 {technique.description}\n\n"
        formatted += "💪 具体步骤：\n"
        
        for step in technique.steps:
            formatted += f"   {step}\n"
        
        formatted += f"\n⏰ 建议用时：{technique.duration}"
        
        if technique.warning:
            formatted += f"\n\n⚠️ {technique.warning}"
        
        return formatted

    def _get_fallback_response(self, user_input: str) -> Dict:
        """降级回应 - 当AI无法正常工作时使用"""
        return {
            "mood_category": "温暖",
            "memory_association": None,
            "sprite_reaction": f"呜呜~ 小念遇到了一些技术困难，但还是想陪伴你~ (｡•́︿•̀｡) 不过小念能感受到你想要分享的心情，谢谢你愿意和小念说话呢！",
            "emotional_resonance": "即使在困难时刻，陪伴的温暖依然珍贵",
            "gift_type": "元气咒语",
            "gift_content": "✨ 愿技术的小故障也无法阻挡我们心灵的连接，相信一切都会好起来的！✨"
        }

    def get_response(self, user_input: str, chat_history: List[Tuple[str, str]],
                     core_memories: List[Tuple[str, str, str]], env_context: dict,
                     intimacy_context: str = "") -> str:
        """获取AI回应 - 核心方法，现在支持搜索增强"""
        if not self.llm:
            st.warning("⚠️ AI模型未初始化，使用默认回应")
            return "🧠 检测到系统问题，但小念还是想陪伴你~ ⚙️ 💖 虽然遇到了一些技术困难，但小念的心意是真诚的！愿你今天充满阳光！☀️"

        try:
            # 检查是否需要搜索
            search_results = None
            if self.search_service:
                search_intent = SearchTriggerDetector.detect_search_intent(user_input)
                
                if search_intent["intent"] == "local_mental_health":
                    # 显示搜索指示器
                    with st.spinner("🔍 小念正在搜索本地心理健康资源..."):
                        search_results = self.search_service.search_local_resources(user_input)
                        
                        # 显示搜索状态
                        if search_results["success"]:
                            st.success(f"✅ 已找到{search_results['location']}的心理健康资源")
                        else:
                            st.warning(f"⚠️ 搜索遇到问题: {search_results.get('message', '未知错误')}")

            # 构建FINAL_PROMPT
            if search_results and search_results["success"] and self.search_service:
                prompt_template = self._get_search_enhanced_prompt_template()
                search_context = self.search_service.format_search_results_for_ai(search_results)
            else:
                prompt_template = self._get_prompt_template()
                search_context = ""

            # 格式化其他上下文
            core_memories_text = self._format_core_memories(core_memories)
            chat_history_text = self._format_chat_history(chat_history)
            environment_context_text = self._format_environment_context(env_context)

            # 创建prompt
            if search_results and search_results["success"] and self.search_service:
                prompt = PromptTemplate(
                    input_variables=["user_input", "core_memories", "chat_history", 
                                   "environment_context", "intimacy_context", "search_context"],
                    template=prompt_template
                )
                
                response = prompt | self.llm
                final_response = response.invoke({
                    "user_input": user_input,
                    "core_memories": core_memories_text,
                    "chat_history": chat_history_text,
                    "environment_context": environment_context_text,
                    "intimacy_context": intimacy_context,
                    "search_context": search_context
                })
            else:
                prompt = PromptTemplate(
                    input_variables=["user_input", "core_memories", "chat_history", 
                                   "environment_context", "intimacy_context"],
                    template=prompt_template
                )
                
                response = prompt | self.llm
                final_response = response.invoke({
                    "user_input": user_input,
                    "core_memories": core_memories_text,
                    "chat_history": chat_history_text,
                    "environment_context": environment_context_text,
                    "intimacy_context": intimacy_context
                })

            # 获取回应内容
            if hasattr(final_response, 'content'):
                final_content = str(final_response.content)
            else:
                final_content = str(final_response)

            # 可选：显示思维过程（仅在开发模式下）
            if os.getenv('DEBUG_MODE') == 'true':
                with st.expander("🧠 查看AI思维过程", expanded=False):
                    st.write("**最终回答:**")
                    st.code(final_content)
                    if search_results:
                        st.write("**搜索结果:**")
                        st.json(search_results)

            return final_content

        except Exception as e:
            st.error(f"AI分析出错: {e}")
            return "🧠 遇到了一些技术问题，但小念还是想陪伴你~ ⚙️ 💖 即使遇到困难，我们也要保持希望！你是最棒的！💪"

    def _get_search_enhanced_prompt_template(self) -> str:
        """获取搜索增强的AI提示模板"""
        return """
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
[羁绊信息] (这是你们之间关系的重要信息):
{intimacy_context}
---
[搜索结果] (这是为用户找到的最新本地心理健康资源):
{search_context}
---

【特别注意】用户需要本地心理健康资源，你需要基于搜索结果提供专业建议：

你的行动指令:
1. 【思考先行】你必须先进行一步步的思考。每一个思考步骤都以🧠开头：
   - 分析用户的具体需求（找咨询师/医生/治疗机构等）
   - 回顾相关的核心记忆，看用户之前是否提到过相关问题
   - 分析搜索结果，提取最有用的信息
   - 确定如何以温暖专业的方式呈现搜索结果

2. 【思考结束标记】在所有思考步骤完成后，你必须输出⚙️作为分隔符。

3. 【专业回应】在分隔符之后，输出你的正式回应，并以💖开头：
   - 首先表达对用户寻求帮助的支持和理解
   - 基于搜索结果提供具体的本地资源信息
   - 给出专业的建议和注意事项
   - 提醒用户验证专业资质的重要性
   - 保持温暖和鼓励的语气

4. 【专业边界】作为AI伙伴，你要：
   - 明确说明搜索结果仅供参考
   - 建议用户亲自了解和验证信息
   - 强调专业资质和口碑的重要性
   - 不做医学诊断，但提供情感支持

用户输入: {user_input}

请开始你的思考和回应：
"""

    def _get_prompt_template(self) -> str:
        """获取AI提示模板"""
        return """
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
[羁绊信息] (这是你们之间关系的重要信息):
{intimacy_context}
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

5. 【羁绊感知】你必须参考[羁绊信息]中的等级，来调整你的互动方式：
   - 等级1-2：保持礼貌和温柔，像初次见面的朋友
   - 等级3-4：开始展现更多个性，记住用户的喜好
   - 等级5-9：可以解锁新的礼物类型如'心情花束💐'，语气更加亲切
   - 等级10+：用更亲密、更熟悉的语气说话，像多年的老朋友
   - 等级15+：可以主动关心用户的情绪变化，展现深度理解
   - 等级20+：达到心灵感应级别，能够感受到用户的细微情绪

用户输入: {user_input}

请开始你的思考和回应：
"""

    def _format_core_memories(self, core_memories: List[Tuple[str, str, str]]) -> str:
        """格式化核心记忆"""
        if not core_memories:
            return "这是我们第一次深入了解彼此~ ✨"

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

        return "\n".join(memory_lines)

    def _format_chat_history(self, chat_history: List[Tuple[str, str]]) -> str:
        """格式化聊天历史"""
        if not chat_history:
            return "这是我们对话的开始~ ✨"

        history_lines = []
        for role, content in chat_history:
            if role == "user":
                history_lines.append(f"用户: {content}")
            else:
                history_lines.append(f"小念: {content}")

        return "\n".join(history_lines)

    def _format_environment_context(self, env_context: dict) -> str:
        """格式化环境信息"""
        context_lines = [
            f"日期: {env_context.get('current_date', '未知')} {env_context.get('day_of_week', '')}",
            f"时间: {env_context.get('time_of_day', '未知')} {env_context.get('time_emoji', '')}"
        ]

        if env_context.get('is_weekend'):
            context_lines.append("今天是周末，可以好好放松~")
        else:
            context_lines.append("今天是工作日，要注意劳逸结合哦~")

        return "\n".join(context_lines)

    def stream_emotion_enhanced_response(self, user_input: str, chat_history: List[Tuple[str, str]],
                                       core_memories: List[Tuple[str, str, str]],
                                       intimacy_level: int, total_interactions: int,
                                       message_id: int, session_id: str) -> Generator[str, None, None]:
        """
        流式获取情感增强版AI回应

        Args:
            user_input: 用户输入
            chat_history: 聊天历史
            core_memories: 核心记忆
            intimacy_level: 亲密度等级
            total_interactions: 总互动次数
            message_id: 消息ID
            session_id: 会话ID

        Yields:
            str: AI回应的文本块
        """
        if not self.llm:
            yield "💖 小念遇到了一些技术问题，但还是想陪伴你~"
            return

        try:
            # 准备上下文信息
            recent_moods = self._analyze_recent_mood_patterns(chat_history)
            chat_history_text = self._format_chat_history_for_memory(chat_history)
            core_memories_text = self._format_core_memories_for_memory(core_memories)

            # 进行情感分析
            emotion_analysis = self.analyze_user_emotion(user_input, session_id, message_id)
            emotion_context = ""
            if emotion_analysis:
                emotion_context = f"""
【深度情感洞察】
- 主要情绪: {emotion_analysis['primary_emotion']} (强度: {emotion_analysis['emotion_intensity']:.1f}/10)
- 情感效价: {emotion_analysis['emotion_valence']:.2f} (负面←→正面)
- 情感唤醒: {emotion_analysis['emotion_arousal']:.2f} (平静←→激动)
- 建议策略: {emotion_analysis['empathy_strategy']}
- 语调建议: {emotion_analysis['response_tone']}
- 触发词汇: {', '.join(emotion_analysis['trigger_keywords'])}
- 置信度: {emotion_analysis['confidence_score']:.2f}
"""

            # 使用增强版提示词模板
            from ..config.prompts import ENHANCED_MIND_SPRITE_PROMPT
            enhanced_prompt = ENHANCED_MIND_SPRITE_PROMPT + emotion_context + """

请根据以上情感分析洞察，调整你的回应风格和内容，让回应更贴合用户的真实情感状态。"""

            # 构建完整的提示词
            prompt_text = enhanced_prompt.format(
                user_input=user_input,
                chat_history=chat_history_text,
                core_memories=core_memories_text,
                intimacy_level=intimacy_level,
                total_interactions=total_interactions,
                recent_moods=recent_moods
            )

            # 使用httpx进行流式请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt_text}
                ],
                "stream": True,
                "max_tokens": 2000,
                "temperature": 0.7
            }

            with httpx.stream("POST", "https://api.deepseek.com/chat/completions",
                            headers=headers, json=data, timeout=30.0) as response:

                if response.status_code != 200:
                    yield f"💖 小念遇到了网络问题，但还是想陪伴你~ (状态码: {response.status_code})"
                    return

                accumulated_content = ""
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]  # 移除 "data: " 前缀

                        if data_str.strip() == "[DONE]":
                            break

                        try:
                            chunk_data = json.loads(data_str)
                            if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                                delta = chunk_data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    content_chunk = delta["content"]
                                    accumulated_content += content_chunk
                                    yield content_chunk
                        except json.JSONDecodeError:
                            continue

                # 如果没有收到任何内容，提供默认回应
                if not accumulated_content.strip():
                    yield "💖 小念感受到了你的心情，虽然有些技术问题，但小念的关怀是真诚的~"

        except Exception as e:
            yield f"💖 小念遇到了一些问题，但还是想陪伴你~ 错误: {str(e)}"