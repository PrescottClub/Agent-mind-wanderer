"""
礼物展示组件
负责渲染小念送给用户的心灵礼物
"""

import streamlit as st

from config.constants import GIFT_ICONS


class GiftDisplay:
    """礼物展示组件类"""

    @staticmethod
    def render(gift_type: str, gift_content: str):
        """渲染礼物展示区域"""
        if gift_type and gift_content:
            icon = GIFT_ICONS.get(gift_type, "🎁")
            
            st.markdown(f"""
            <div class="gift-card">
                <h4>{icon} 小念的礼物: {gift_type}</h4>
                <p>{gift_content}</p>
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def render_with_animation(gift_type: str, gift_content: str):
        """带动画效果的礼物展示（预留接口）"""
        # 未来可以添加礼物展示动画
        GiftDisplay.render(gift_type, gift_content) 