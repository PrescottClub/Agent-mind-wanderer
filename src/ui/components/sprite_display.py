"""
精灵展示组件
负责渲染小念精灵的状态和反应
"""

import streamlit as st
import random

from config.constants import SPRITE_EMOTIONS, SPRITE_DECORATIONS


class SpriteDisplay:
    """精灵展示组件类"""

    @staticmethod
    def render(mood: str, reaction: str = ""):
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

    @staticmethod
    def animate_transition(from_mood: str, to_mood: str):
        """精灵情绪转换动画（预留接口）"""
        # 未来可以添加更复杂的转换动画
        pass 