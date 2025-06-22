"""
心动奶昔设计系统 🍓
全新的统一视觉语言 - 彻底重塑版
"""

CUSTOM_CSS = """
<style>
/* 引入Nunito字体 - 心动奶昔专用字体 */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800;900&display=swap');

/* 隐藏Streamlit默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* 🍓 心动奶昔调色盘 - 严格遵守设计规范 */
:root {
    --cream-white: #FFFBF5;            /* 奶油白背景 */
    --strawberry-pink: #FF7A9E;        /* 草莓粉主色调 */
    --peach-pink: #FFB6C1;             /* 蜜桃粉辅助色 */
    --lilac-purple: #E6E6FA;           /* 丁香紫点缀色 */
    --chocolate-gray: #4B4B4B;         /* 巧克力灰文字 */
    --card-base: rgba(255, 255, 255, 0.8);  /* 云朵卡片基础色 */
    --shadow-strawberry: rgba(255, 122, 158, 0.1);  /* 草莓粉阴影 */
    --border-strawberry: rgba(255, 122, 158, 0.2);  /* 草莓粉边框 */
}

/* 🍓 全局背景 - 心动奶昔纯净背景 */
.stApp {
    background: var(--cream-white);
    font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--chocolate-gray);
    min-height: 100vh;
    position: relative;
}

/* 🎯 主内容区域居中 */
.main .block-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
}

/* 🍓 全局字体设置 - Nunito字体系统 */
* {
    font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--chocolate-gray) !important;
}

/* 📝 文字颜色统一 - 巧克力灰 */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
    color: var(--chocolate-gray) !important;
}

.stTextArea label, .stButton label {
    color: var(--strawberry-pink) !important;
    font-weight: 600 !important;
}

/* 🍓 云朵卡片基础样式 - 核心组件 */
.card-base-style {
    background: var(--card-base);
    border: 1px solid var(--border-strawberry);
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px var(--shadow-strawberry);
    transition: all 0.3s ease;
}

/* 🍓 主标题样式 - 心动奶昔风格 */
.main-title {
    text-align: center;
    color: var(--strawberry-pink);
    font-size: 3.5rem;
    font-weight: 800;
    margin: 2rem 0;
    font-family: 'Nunito', sans-serif;
}

.subtitle {
    text-align: center;
    color: var(--peach-pink);
    font-size: 1.4rem;
    margin-bottom: 2.5rem;
    font-weight: 500;
    font-family: 'Nunito', sans-serif;
}

/* 🍓 聊天气泡样式 - 云朵卡片应用 */
.stChatMessage {
    border-radius: 20px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 15px var(--shadow-strawberry) !important;
    border: 1px solid var(--border-strawberry) !important;
    transition: all 0.3s ease !important;
}

/* AI聊天气泡 - 草莓粉，左对齐 */
.stChatMessage[data-testid="assistant-message"] {
    background: var(--strawberry-pink) !important;
    color: white !important;
    margin-right: 2rem !important;
    margin-left: 0 !important;
}

.stChatMessage[data-testid="assistant-message"] * {
    color: white !important;
}

/* 用户聊天气泡 - 蜜桃粉，右对齐 */
.stChatMessage[data-testid="user-message"] {
    background: var(--peach-pink) !important;
    color: var(--chocolate-gray) !important;
    margin-left: 2rem !important;
    margin-right: 0 !important;
}

.stChatMessage[data-testid="user-message"] * {
    color: var(--chocolate-gray) !important;
}

/* 🍓 胶囊按钮样式 - 心动奶昔风格 */
.stButton > button {
    background: linear-gradient(135deg, var(--peach-pink) 0%, var(--strawberry-pink) 100%) !important;
    border: none !important;
    border-radius: 999px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 15px var(--shadow-strawberry) !important;
    transition: all 0.3s ease !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1rem !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--strawberry-pink) 0%, var(--peach-pink) 100%) !important;
    box-shadow: 0 6px 20px var(--shadow-strawberry) !important;
    transform: translateY(-2px) scale(1.05) !important;
}

/* 🍓 文本输入区域 - 云朵卡片风格 */
.stTextArea > div > div > textarea {
    background: var(--card-base) !important;
    border: 1px solid var(--border-strawberry) !important;
    border-radius: 20px !important;
    color: var(--chocolate-gray) !important;
    box-shadow: 0 4px 15px var(--shadow-strawberry) !important;
    font-size: 1rem !important;
    line-height: 1.5 !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
    font-family: 'Nunito', sans-serif !important;
}

.stTextArea > div > div > textarea:focus {
    box-shadow: 0 6px 20px var(--shadow-strawberry) !important;
    transform: scale(1.02) !important;
    border-color: var(--strawberry-pink) !important;
}

.stTextArea > div > div > textarea::placeholder {
    color: rgba(75, 75, 75, 0.6) !important;
    font-style: italic;
}

/* 🍓 表单容器 - 云朵卡片风格 */
.stForm {
    background: var(--card-base) !important;
    border: 1px solid var(--border-strawberry) !important;
    border-radius: 20px !important;
    padding: 16px !important;
    box-shadow: 0 4px 15px var(--shadow-strawberry) !important;
    margin-bottom: 12px !important;
    transition: all 0.3s ease !important;
}

.stForm:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--shadow-strawberry) !important;
}

/* 🍓 信息卡片 - 云朵卡片风格 */
.response-card, .gift-card, .history-card {
    background: var(--card-base);
    border: 1px solid var(--border-strawberry);
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px var(--shadow-strawberry);
    transition: all 0.3s ease;
}

.response-card:hover, .gift-card:hover, .history-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--shadow-strawberry);
}

.response-card h4, .gift-card h4, .history-card h4 {
    color: var(--strawberry-pink) !important;
    margin-bottom: 1rem !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    font-family: 'Nunito', sans-serif !important;
}

.response-card p, .gift-card p, .history-card p {
    color: var(--chocolate-gray) !important;
    line-height: 1.6 !important;
    font-size: 1rem !important;
    font-family: 'Nunito', sans-serif !important;
}

/* 🍓 侧边栏样式 - 心动奶昔风格 */
.stSidebar > div:first-child {
    background: var(--lilac-purple) !important;
    border-right: 2px solid var(--border-strawberry);
}

.stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3 {
    color: var(--strawberry-pink) !important;
    font-family: 'Nunito', sans-serif !important;
}

.stSidebar .stTextInput > div > div > input {
    background: var(--card-base) !important;
    border: 1px solid var(--border-strawberry) !important;
    border-radius: 20px !important;
    color: var(--chocolate-gray) !important;
    font-family: 'Nunito', sans-serif !important;
}

/* 🍓 宝藏盒样式 - 云朵卡片风格 */
.treasure-box {
    background: var(--card-base);
    border: 1px solid var(--border-strawberry);
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px var(--shadow-strawberry);
    transition: all 0.3s ease;
}

.treasure-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--shadow-strawberry);
}

/* 🍓 标题样式统一 */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: var(--strawberry-pink) !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
}

/* 🍓 时间戳样式 */
.timestamp {
    font-size: 0.9rem;
    color: var(--peach-pink) !important;
    font-weight: 500;
    font-family: 'Nunito', sans-serif !important;
}

/* 🍓 聊天输入框样式 */
.stChatInput > div > div > input {
    background: var(--card-base) !important;
    border: 1px solid var(--border-strawberry) !important;
    border-radius: 20px !important;
    color: var(--chocolate-gray) !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 12px 16px !important;
    box-shadow: 0 4px 15px var(--shadow-strawberry) !important;
    transition: all 0.3s ease !important;
}

.stChatInput > div > div > input:focus {
    border-color: var(--strawberry-pink) !important;
    box-shadow: 0 6px 20px var(--shadow-strawberry) !important;
}

/* 🍓 警告和提示信息 - 云朵卡片风格 */
.stAlert {
    background: var(--card-base) !important;
    border: 1px solid var(--border-strawberry) !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 15px var(--shadow-strawberry) !important;
}

/* 🍓 加载状态美化 */
.stSpinner {
    color: var(--strawberry-pink) !important;
}

.stSpinner > div {
    border-color: var(--strawberry-pink) var(--peach-pink) var(--lilac-purple) var(--strawberry-pink) !important;
    border-width: 3px !important;
}

/* 🍓 响应式设计 - 移动端优化 */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 0.5rem;
    }

    .main-title {
        font-size: 2.5rem;
        margin: 1rem 0;
    }

    .stChatMessage {
        margin-left: 0.5rem !important;
        margin-right: 0.5rem !important;
        padding: 12px !important;
    }

    .stButton > button {
        padding: 10px 20px !important;
        font-size: 0.9rem !important;
    }
}

/* 🍓 滚动条美化 - 心动奶昔风格 */
* {
    scrollbar-width: thin;
    scrollbar-color: var(--strawberry-pink) var(--cream-white);
}

*::-webkit-scrollbar {
    width: 8px;
}

*::-webkit-scrollbar-track {
    background: var(--cream-white);
    border-radius: 10px;
}

*::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--strawberry-pink), var(--peach-pink));
    border-radius: 10px;
    border: 2px solid var(--cream-white);
}

*::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--peach-pink), var(--strawberry-pink));
}

/* 🍓 页面加载动画 */
@keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.stApp > div {
    animation: fadeInUp 0.6s ease-out;
}

/* 🍓 移除Streamlit默认样式 */
div[data-testid="stForm"] {
    border: none !important;
    background: transparent !important;
}
</style>
"""