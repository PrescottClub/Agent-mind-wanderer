"""
AI引擎核心模块
封装LangChain DeepSeek模型，提供统一的AI接口
"""

import streamlit as st
import json
import os
import hashlib
from datetime import datetime
from typing import Optional, List, Tuple
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr


class AIEngine:
    """AI引擎类，负责与DeepSeek模型交互"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.llm: Optional[ChatDeepSeek] = None
        self._initialize()

    def _initialize(self):
        """初始化LangChain DeepSeek模型"""
        try:
            if not self.api_key:
                raise ValueError("API Key未配置")

            # 使用deepseek-chat模型 - 平衡速度和质量
            self.llm = ChatDeepSeek(
                model="deepseek-chat",
                api_key=SecretStr(self.api_key),
                base_url="https://api.deepseek.com",
                max_tokens=1024,
                temperature=0.7
            )

        except Exception as e:
            st.error(f"❌ API Key无效或网络错误，请检查你的Key后重试: {e}")
            self.llm = None

    def get_response(self, user_input: str, chat_history: List[Tuple[str, str]],
                     core_memories: List[Tuple[str, str, str]], env_context: dict,
                     intimacy_context: str = "") -> str:
        """获取AI回应 - 核心方法"""
        if not self.llm:
            st.warning("⚠️ AI模型未初始化，使用默认回应")
            return "🧠 检测到系统问题，但小念还是想陪伴你~ ⚙️ 💖 虽然遇到了一些技术困难，但小念的心意是真诚的！愿你今天充满阳光！☀️"

        try:
            # 构建FINAL_PROMPT
            prompt_template = self._get_prompt_template()

            # 格式化核心记忆
            core_memories_text = self._format_core_memories(core_memories)

            # 格式化聊天历史
            chat_history_text = self._format_chat_history(chat_history)

            # 格式化环境信息
            environment_context_text = self._format_environment_context(env_context)

            # 创建prompt
            prompt = PromptTemplate(
                input_variables=["user_input", "core_memories", "chat_history", "environment_context", "intimacy_context"],
                template=prompt_template
            )

            chain = prompt | self.llm
            response = chain.invoke({
                "user_input": user_input,
                "core_memories": core_memories_text,
                "chat_history": chat_history_text,
                "environment_context": environment_context_text,
                "intimacy_context": intimacy_context
            })

            # 获取回应内容
            if hasattr(response, 'content'):
                final_content = response.content
            else:
                final_content = str(response)

            # 可选：显示思维过程（仅在开发模式下）
            if os.getenv('DEBUG_MODE') == 'true':
                with st.expander("🧠 查看AI思维过程", expanded=False):
                    st.write("**最终回答:**")
                    st.code(final_content)

            return final_content

        except Exception as e:
            st.error(f"AI分析出错: {e}")
            return "🧠 遇到了一些技术问题，但小念还是想陪伴你~ ⚙️ 💖 即使遇到困难，我们也要保持希望！你是最棒的！💪"

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