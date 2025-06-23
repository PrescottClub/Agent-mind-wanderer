"""
心绪精灵 (Mind Sprite) - 重构版主入口
主动型治愈Agent"心绪精灵" - 性能优化版本

作者: Claude (Augment Agent)
技术栈: Python, LangChain, Streamlit, DeepSeek API, SQLite
版本: 5.0 - 性能优化重构版
"""

import streamlit as st
from src.ui.styles.custom_css import CUSTOM_CSS
from src.app import MindSpriteApp

# ==================== 页面配置 ====================

st.set_page_config(
    page_title="心绪精灵 ✨",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 应用甜美马卡龙CSS样式
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==================== 主函数 ====================

def main():
    """主函数"""
    app = MindSpriteApp()
    app.run()


if __name__ == "__main__":
    main()
