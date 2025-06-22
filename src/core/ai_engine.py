"""
AI引擎核心模块
封装LangChain DeepSeek模型，提供统一的AI接口
"""

import streamlit as st
import json
from typing import Optional
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from config.settings import settings
from config.prompts import MIND_SPRITE_PROMPT
from models.emotion import EmotionResult


class AIEngine:
    """AI引擎类，负责与DeepSeek模型交互"""

    def __init__(self):
        self.llm: Optional[ChatDeepSeek] = None
        self._initialize()

    def _initialize(self):
        """初始化LangChain DeepSeek模型"""
        try:
            if not settings.deepseek_api_key:
                st.error("请在.env文件中配置DEEPSEEK_API_KEY")
                return

            # 使用deepseek-reasoner (R1)模型 - 强大的推理能力
            # 注意：R1不支持temperature等参数，但支持JSON输出
            self.llm = ChatDeepSeek(
                model=settings.deepseek_model,
                api_key=SecretStr(settings.deepseek_api_key),
                base_url=settings.deepseek_api_base,
                max_tokens=settings.max_tokens
            )

        except Exception as e:
            st.error(f"初始化AI模型失败: {e}")
            self.llm = None

    def safe_parse_json(self, response_text: str) -> dict:
        """安全解析AI返回的JSON，包含容错机制"""
        try:
            # 尝试直接解析JSON
            result = json.loads(response_text)
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
                        return result

                # 尝试提取普通JSON部分
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end != -1:
                    json_str = response_text[start:end]
                    result = json.loads(json_str)
                    return result
            except:
                pass
            
            # 如果都失败了，返回默认回应
            return {
                "mood_category": "平静",
                "sprite_reaction": "哎呀，小念有点confused了呢... 不过没关系，我还是很开心能陪伴你！(◕‿◕)✨",
                "gift_type": "元气咒语",
                "gift_content": "虽然我有点迷糊，但我的心意是真诚的！愿你今天充满阳光！☀️"
            }
        except Exception as e:
            st.error(f"解析AI回应时出错: {e}")
            return {
                "mood_category": "平静",
                "sprite_reaction": "呜呜，小念遇到了一些技术问题... 但我还是想陪伴你！(｡•́︿•̀｡)",
                "gift_type": "元气咒语",
                "gift_content": "即使遇到困难，我们也要保持希望！你是最棒的！💪"
            }

    def analyze_emotion(self, user_input: str) -> EmotionResult:
        """分析用户情绪并生成精灵回应"""
        if not self.llm:
            st.warning("⚠️ AI模型未初始化，使用默认回应")
            return EmotionResult.from_dict({})

        try:
            prompt = PromptTemplate(
                input_variables=["user_input"],
                template=MIND_SPRITE_PROMPT
            )

            chain = prompt | self.llm
            response = chain.invoke({"user_input": user_input})

            # DeepSeek R1 特殊处理：获取思维链和最终回答
            reasoning_content = ""
            final_content = ""

            # 安全获取回复内容
            if hasattr(response, 'content'):
                final_content = str(response.content)
            else:
                final_content = str(response)

            # 可选：显示R1的思维过程（仅在开发模式下）
            if settings.debug_mode and reasoning_content:
                with st.expander("🧠 查看R1思维过程", expanded=False):
                    st.write("**最终回答:**")
                    st.code(final_content)

            # 使用最终回答进行JSON解析
            result_dict = self.safe_parse_json(final_content)
            return EmotionResult.from_dict(result_dict)

        except Exception as e:
            st.error(f"AI分析出错: {e}")
            return EmotionResult.from_dict({}) 