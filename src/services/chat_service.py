"""
聊天服务类 - 重构版
负责处理聊天业务逻辑，分离UI和业务逻辑
"""

import streamlit as st
import json
import httpx
from typing import Generator, Dict, Optional, List, Tuple
from ..core.ai_engine import AIEngine
from ..data.repositories.chat_repository import ChatRepository
from ..services.intimacy_service import IntimacyService
from ..utils.helpers import (
    parse_enhanced_ai_response,
    clean_markdown_text
)


class ChatService:
    """聊天服务类 - 负责处理聊天相关的业务逻辑"""
    
    def __init__(self, ai_engine: AIEngine, chat_repo: ChatRepository, intimacy_service: IntimacyService):
        self.ai_engine = ai_engine
        self.chat_repo = chat_repo
        self.intimacy_service = intimacy_service
    
    def process_user_message_stream(self, session_id: str, user_input: str, message_id: int) -> Generator[str, None, None]:
        """
        流式处理用户消息 - 返回用户友好的内容

        Args:
            session_id: 会话ID
            user_input: 用户输入
            message_id: 消息ID

        Yields:
            str: 解析后的AI回应文本块
        """
        try:
            # 先获取完整的非流式响应来解析结构化数据
            result = self.process_user_message(session_id, user_input, message_id)

            if not result["success"]:
                yield "💖 小念遇到了一些技术问题，但还是想陪伴你~"
                return

            parsed_response = result["parsed_response"]
            gift_info = result["gift_info"]

            # 构建要流式显示的内容
            content_parts = []

            # 添加记忆联想（如果有）
            memory_association = parsed_response["memory_association"]
            if memory_association and memory_association != "null" and memory_association.strip():
                content_parts.append(f"💭 记忆联想: {memory_association}")

            # 添加情绪共鸣
            emotional_resonance = parsed_response["emotional_resonance"]
            if emotional_resonance:
                content_parts.append(f"💕 {emotional_resonance}")

            # 添加主要回应
            sprite_reaction = parsed_response["sprite_reaction"]
            content_parts.append(f"💖 {sprite_reaction}")

            # 添加礼物信息（如果有）
            if gift_info["type"]:
                content_parts.append(f"🎁 **{gift_info['type']}**")
                content_parts.append(gift_info['content'])

            # 将所有内容合并
            full_content = "\n\n".join(content_parts)

            # 模拟打字机效果 - 逐字符流式输出
            current_text = ""
            for char in full_content:
                current_text += char
                yield current_text

        except Exception as e:
            st.error(f"流式处理出错: {e}")
            yield f"💖 小念遇到了一些技术问题，但还是想陪伴你~"
    
    def process_user_message(self, session_id: str, user_input: str, message_id: int) -> Dict:
        """
        处理用户消息（非流式版本，用于后处理）
        
        Args:
            session_id: 会话ID
            user_input: 用户输入
            message_id: 消息ID
            
        Returns:
            Dict: 处理结果，包含AI回应和相关信息
        """
        try:
            # 获取上下文信息
            core_memories = self.chat_repo.get_core_memories(session_id, limit=5)
            recent_context = self.chat_repo.get_recent_context(session_id, context_turns=4)
            
            # 获取亲密度信息
            from ..data.repositories.user_profile_repository import UserProfileRepository
            user_profile_repo = UserProfileRepository()
            profile = user_profile_repo.get_profile(session_id)
            if not profile:
                profile = user_profile_repo.find_or_create_profile(session_id)
            
            intimacy_level = profile["intimacy_level"]
            total_interactions = profile["total_interactions"]
            
            # 🎯 使用心灵捕手模式获取AI回应
            from datetime import datetime, timedelta
            last_interaction_time = datetime.now() - timedelta(hours=1)  # 默认1小时前，实际应从数据库获取
            
            response_data = self.ai_engine.get_heart_catcher_response(
                user_input=user_input,
                chat_history=recent_context,
                session_id=session_id,
                last_interaction_time=last_interaction_time
            )
            
            # 如果心灵捕手失败，降级到情感增强回应
            if not response_data:
                response_data = self.ai_engine.get_emotion_enhanced_response(
                    user_input, recent_context, core_memories, intimacy_level, total_interactions,
                    message_id, session_id
                )
            
            if not response_data:
                return {
                    "success": False,
                    "error": "获取AI回应失败"
                }
            
            # 解析增强版回应
            parsed_response = parse_enhanced_ai_response(response_data)
            
            # 构建完整的回应文本用于保存
            full_response = parsed_response["sprite_reaction"]
            memory_association = parsed_response["memory_association"]
            if memory_association and memory_association != "null" and memory_association.strip():
                full_response = f"💭 记忆联想: {memory_association}\n\n{full_response}"
            
            # 处理礼物
            gift_info = {
                "type": parsed_response["gift_type"],
                "content": parsed_response["gift_content"]
            }
            
            if gift_info["type"]:
                st.session_state.current_gift = gift_info
                self.chat_repo.add_treasure(
                    session_id, gift_info["type"], gift_info["content"]
                )
            
            # 添加经验值和处理升级
            exp_result = self.intimacy_service.add_exp(session_id, exp_to_add=15)
            
            # 处理关怀机会检测
            care_tasks = []
            try:
                care_tasks = self.ai_engine.process_care_opportunities(user_input, session_id)
            except Exception as e:
                print(f"关怀任务处理错误: {e}")
            
            return {
                "success": True,
                "parsed_response": parsed_response,
                "response_data": response_data,
                "full_response": full_response,
                "gift_info": gift_info,
                "exp_result": exp_result,
                "care_tasks": care_tasks
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"处理消息时出错: {e}"
            }
    
    def display_ai_response(self, result: Dict):
        """
        显示AI回应（UI渲染逻辑）
        
        Args:
            result: process_user_message的返回结果
        """
        if not result["success"]:
            st.error(result["error"])
            return
        
        parsed_response = result["parsed_response"]
        response_data = result["response_data"]
        gift_info = result["gift_info"]
        exp_result = result["exp_result"]
        care_tasks = result["care_tasks"]
        
        # 检查是否为急救包回应
        is_emergency = parsed_response.get("is_emergency", False)
        
        # 检查是否有情感分析结果
        emotion_analysis = response_data.get("emotion_analysis")
        is_emotion_enhanced = response_data.get("is_emotion_enhanced", False)
        
        # 显示回应
        with st.chat_message("assistant"):
            # 显示情感洞察（如果有深度情感分析）
            if is_emotion_enhanced and emotion_analysis:
                st.markdown("### 🧠 深度情感洞察")
                
                # 情感分析概览
                primary_emotion = emotion_analysis["primary_emotion"]
                intensity = emotion_analysis["emotion_intensity"]
                valence = emotion_analysis["emotion_valence"]
                empathy_strategy = emotion_analysis["empathy_strategy"]
                
                # 情绪强度条
                intensity_color = "🔴" if intensity > 7 else "🟡" if intensity > 4 else "🟢"
                st.markdown(f"💫 **主要情绪**: {primary_emotion} {intensity_color} ({intensity:.1f}/10)")
                
                # 情感效价指示
                valence_emoji = "😊" if valence > 0.3 else "😔" if valence < -0.3 else "😐"
                st.markdown(f"🎭 **情感倾向**: {valence_emoji} ({valence:.2f})")
                
                # 共情策略
                strategy_emoji = {"comfort": "🤗", "solution": "💡", "companion": "🫶", 
                                "celebration": "🎉", "validation": "✅"}.get(empathy_strategy, "💝")
                st.markdown(f"🎯 **关怀策略**: {strategy_emoji} {empathy_strategy}")
                
                # 共情回应
                if "empathy_response" in emotion_analysis:
                    empathy_response = clean_markdown_text(emotion_analysis['empathy_response'])
                    st.info(f"💙 {empathy_response}")
                
                st.markdown("---")
            
            if is_emergency:
                # 急救包特殊显示
                st.markdown("### 🚨 情绪关怀模式")
                st.error("小念检测到你需要额外的关怀和支持")
                st.markdown("---")
                
                # 显示情绪共鸣
                st.markdown("### 💙 深度理解")
                emotional_resonance = clean_markdown_text(parsed_response['emotional_resonance'])
                st.markdown(f"🫂 {emotional_resonance}")
                st.markdown("---")
                
                # 显示主要回应
                sprite_reaction = clean_markdown_text(parsed_response['sprite_reaction'])
                st.markdown(f"💖 {sprite_reaction}")
            else:
                # 普通增强版回应
                # 显示记忆联想（如果有）
                memory_association = parsed_response["memory_association"]
                if memory_association and memory_association != "null" and memory_association.strip():
                    st.markdown("### 💭 记忆联想")
                    cleaned_memory = clean_markdown_text(memory_association)
                    st.info(f"🌟 {cleaned_memory}")
                    st.markdown("---")
                
                # 显示情绪共鸣
                st.markdown("### 💕 情感共鸣")
                emotional_resonance = clean_markdown_text(parsed_response['emotional_resonance'])
                st.markdown(f"🫶 {emotional_resonance}")
                st.markdown("---")
                
                # 显示主要回应
                sprite_reaction = clean_markdown_text(parsed_response['sprite_reaction'])
                st.markdown(f"💖 {sprite_reaction}")

        # 显示礼物
        if gift_info["type"]:
            if is_emergency:
                st.markdown("### 🆘 情绪急救包")
                with st.container():
                    st.error(f"**{gift_info['type']}**")
                    cleaned_gift_content = clean_markdown_text(gift_info['content'])
                    st.markdown(cleaned_gift_content)
                    
                    # 显示危机资源（如果有）
                    if parsed_response.get("emergency_data", {}).get("crisis_resources"):
                        st.markdown("---")
                        st.markdown("### 📞 紧急联系方式")
                        crisis_resources = parsed_response["emergency_data"]["crisis_resources"]
                        for resource_name, contact_info in crisis_resources.items():
                            if resource_name != "温馨提醒":
                                st.info(f"**{resource_name}**: {contact_info}")
                            else:
                                st.warning(f"💙 {contact_info}")
                                
                    # 支持信息
                    if parsed_response.get("emergency_data", {}).get("support_message"):
                        st.markdown("---")
                        support_msg = parsed_response["emergency_data"]["support_message"]
                        st.info(support_msg)
            else:
                st.markdown("### 🎁 小念的礼物")
                cleaned_gift_content = clean_markdown_text(gift_info['content'])
                st.success(f"**{gift_info['type']}**\n\n{cleaned_gift_content}")

        # 检查是否升级
        if exp_result["leveled_up"]:
            # 升级庆祝效果
            st.balloons()

            # 升级提示
            new_level = exp_result["new_level"]
            st.toast(f"🎉 恭喜！与小念的羁绊提升到 Lv.{new_level} 啦！", icon="🎉")

            # 显示升级奖励
            if exp_result["level_rewards"]:
                st.success("🎁 解锁新奖励：")
                for reward in exp_result["level_rewards"]:
                    st.info(f"✨ {reward['content']}")

        # 显示经验值获得提示（小字提示）
        exp_gained = exp_result["exp_gained"]
        st.caption(f"💫 获得 {exp_gained} EXP！（记忆联想奖励）")

        # 处理关怀任务显示
        if care_tasks:
            for task in care_tasks:
                care_type_names = {
                    "emotion_followup": "情绪跟进",
                    "event_followup": "事件跟进", 
                    "regular_care": "定期关怀"
                }
                type_name = care_type_names.get(task['care_type'], task['care_type'])
                # 安全地处理时间显示
                scheduled_time = task.get('scheduled_time', '')
                if isinstance(scheduled_time, str) and len(scheduled_time) >= 16:
                    time_display = scheduled_time[:16]
                elif hasattr(scheduled_time, 'strftime') and not isinstance(scheduled_time, str):
                    # 如果是datetime对象，格式化为字符串
                    time_display = scheduled_time.strftime('%Y-%m-%d %H:%M')
                else:
                    time_display = str(scheduled_time)
                st.caption(f"💝 小念已为你安排 {type_name} （{time_display}）")
