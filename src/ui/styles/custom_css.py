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

/* 🎨 心动奶昔统一颜色系统 */
:root {
    --primary: #FF7A9E;                 /* 草莓粉 - 主要交互元素 */
    --secondary: #FFB6C1;               /* 蜜桃粉 - 次要元素 */
    --accent: #E6E6FA;                  /* 丁香紫 - 点缀色 */
    --bg-primary: #FFFBF5;              /* 奶油白 - 主背景 */
    --bg-card: rgba(255, 255, 255, 0.8); /* 卡片背景 */
    --text: #4B4B4B;                    /* 巧克力灰 - 文字 */
    --border: rgba(255, 122, 158, 0.2); /* 统一边框色 */
    --shadow: rgba(255, 122, 158, 0.1); /* 统一阴影色 */
    --focus-ring: rgba(255, 122, 158, 0.3); /* 聚焦环颜色 */
}

/* 🎨 全局样式统一 */
.stApp {
    background: var(--bg-primary);
    font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text);
    min-height: 100vh;
    position: relative;
}

/* 🎯 主内容区域居中 */
.main .block-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
}

/* 🎨 全局字体和颜色统一 */
* {
    font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text) !important;
    transition: all 0.3s ease !important;
}

/* 📝 文字颜色统一 */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
    color: var(--text) !important;
}

.stTextArea label, .stButton label {
    color: var(--primary) !important;
    font-weight: 600 !important;
}

/* 🎨 统一卡片样式 */
.card-base-style, .hover-lift {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px var(--shadow);
    transition: all 0.3s ease;
}

.hover-lift:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--shadow);
}

/* 🎨 标题颜色统一 */
.main-title {
    text-align: center;
    color: var(--primary);
    font-size: 3.5rem;
    font-weight: 800;
    margin: 2rem 0;
    font-family: 'Nunito', sans-serif;
}

.subtitle {
    text-align: center;
    color: var(--secondary);
    font-size: 1.4rem;
    margin-bottom: 2.5rem;
    font-weight: 500;
    font-family: 'Nunito', sans-serif;
}

/* 🎨 聊天气泡 - 精致设计 */
.stChatMessage {
    border-radius: 22px !important;
    padding: 18px 20px !important;
    margin-bottom: 16px !important;
    box-shadow:
        0 4px 15px rgba(255, 122, 158, 0.12),
        0 2px 8px rgba(255, 122, 158, 0.08) !important;
    border: 2px solid rgba(255, 255, 255, 0.6) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    backdrop-filter: blur(5px) !important;
}

.stChatMessage:hover {
    transform: translateY(-1px) !important;
    box-shadow:
        0 6px 20px rgba(255, 122, 158, 0.15),
        0 3px 12px rgba(255, 122, 158, 0.1) !important;
}

/* AI聊天气泡 - 梦幻粉色 */
.stChatMessage[data-testid="assistant-message"] {
    background: linear-gradient(135deg, #FF7A9E 0%, #FF69B4 100%) !important;
    color: white !important;
    margin-right: 3rem !important;
    margin-left: 0 !important;
    border: 2px solid rgba(255, 255, 255, 0.8) !important;
}

.stChatMessage[data-testid="assistant-message"] * {
    color: white !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
}

/* 用户聊天气泡 - 温柔蜜桃色 */
.stChatMessage[data-testid="user-message"] {
    background: linear-gradient(135deg, #FFB6C1 0%, #FFC0CB 100%) !important;
    color: var(--text) !important;
    margin-left: 3rem !important;
    margin-right: 0 !important;
    border: 2px solid rgba(255, 255, 255, 0.9) !important;
}

.stChatMessage[data-testid="user-message"] * {
    color: var(--text) !important;
    font-weight: 500 !important;
}

/* 🎨 统一按钮样式 */
.stButton > button, button {
    background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%) !important;
    border: none !important;
    border-radius: 999px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 15px var(--shadow) !important;
    transition: all 0.3s ease !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1rem !important;
}

.stButton > button:hover, button:hover {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    box-shadow: 0 6px 20px var(--shadow) !important;
    transform: translateY(-1px) !important;
}

/* 🎨 统一输入框样式 */
input, textarea, select, .stTextArea > div > div > textarea, .stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    color: var(--text) !important;
    box-shadow: 0 4px 15px var(--shadow) !important;
    font-size: 1rem !important;
    line-height: 1.5 !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
    font-family: 'Nunito', sans-serif !important;
}

/* 🎨 统一聚焦效果 */
input:focus, textarea:focus, select:focus,
.stTextArea > div > div > textarea:focus,
.stTextInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--focus-ring) !important;
    outline: none !important;
}

input::placeholder, textarea::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: rgba(75, 75, 75, 0.6) !important;
    font-style: italic;
}

/* 🎨 统一容器和卡片样式 */
.stForm, .response-card, .gift-card, .history-card, .treasure-box {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 16px !important;
    box-shadow: 0 4px 15px var(--shadow) !important;
    margin-bottom: 12px !important;
    transition: all 0.3s ease !important;
}

.stForm:hover, .response-card:hover, .gift-card:hover, .history-card:hover, .treasure-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--shadow) !important;
}

/* 🎨 统一标题颜色 */
.response-card h4, .gift-card h4, .history-card h4,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: var(--primary) !important;
    margin-bottom: 1rem !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    font-family: 'Nunito', sans-serif !important;
}

/* 🎨 统一文本颜色 */
.response-card p, .gift-card p, .history-card p {
    color: var(--text) !important;
    line-height: 1.6 !important;
    font-size: 1rem !important;
    font-family: 'Nunito', sans-serif !important;
}

/* 🎨 侧边栏 - 精致设计 */
.stSidebar > div:first-child {
    background: linear-gradient(180deg, #E6E6FA 0%, #F0E6FF 100%) !important;
    border-right: 3px solid rgba(255, 122, 158, 0.2) !important;
    box-shadow: 2px 0 15px rgba(255, 122, 158, 0.1) !important;
}

.stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3 {
    color: var(--primary) !important;
    font-family: 'Nunito', sans-serif !important;
}

/* 🎨 侧边栏过渡效果 */
.stSidebar {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stSidebar > div {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 🎨 侧边栏输入框统一样式 */
.stSidebar .stTextInput > div > div > input,
.stSidebar input[type="text"],
.stSidebar input[type="password"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    color: var(--text) !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 12px 16px !important;
    box-shadow: 0 2px 8px var(--shadow) !important;
    transition: all 0.3s ease !important;
    font-size: 0.95rem !important;
}

.stSidebar .stTextInput > div > div > input:focus,
.stSidebar input[type="text"]:focus,
.stSidebar input[type="password"]:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--focus-ring) !important;
    outline: none !important;
}

.stSidebar .stTextInput > div > div > input::placeholder,
.stSidebar input::placeholder {
    color: rgba(75, 75, 75, 0.6) !important;
    font-style: italic !important;
}

/* 🎨 时间戳颜色统一 */
.timestamp {
    font-size: 0.9rem;
    color: var(--secondary) !important;
    font-weight: 500;
    font-family: 'Nunito', sans-serif !important;
}

/* 🎨 聊天输入框 - 精致设计 */
.stChatInput {
    position: fixed !important;
    bottom: 20px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: calc(100% - 40px) !important;
    max-width: 760px !important;
    z-index: 1000 !important;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 251, 245, 0.9)) !important;
    border-radius: 25px !important;
    box-shadow:
        0 10px 30px rgba(255, 122, 158, 0.15),
        0 4px 15px rgba(255, 122, 158, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    padding: 8px 12px !important;
    margin: 0 !important;
    backdrop-filter: blur(15px) !important;
    border: 2px solid rgba(255, 122, 158, 0.3) !important;
}

.stChatInput > div {
    background: transparent !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

.stChatInput > div > div {
    background: transparent !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

.stChatInput > div > div > input {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(255, 122, 158, 0.25) !important;
    border-radius: 20px !important;
    color: var(--text) !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 14px 20px !important;
    box-shadow:
        inset 0 2px 6px rgba(255, 122, 158, 0.08),
        0 2px 8px rgba(255, 122, 158, 0.05) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-size: 1rem !important;
    width: 100% !important;
    font-weight: 500 !important;
}

.stChatInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow:
        inset 0 2px 6px rgba(255, 122, 158, 0.1),
        0 0 0 3px rgba(255, 122, 158, 0.15),
        0 4px 12px rgba(255, 122, 158, 0.1) !important;
    outline: none !important;
    transform: translateY(-1px) !important;
}

.stChatInput > div > div > input::placeholder {
    color: rgba(255, 122, 158, 0.6) !important;
    font-style: normal !important;
    font-weight: 400 !important;
}

/* 🎨 聊天输入框发送按钮 - 可爱设计 */
.stChatInput button {
    background: linear-gradient(135deg, #FF7A9E 0%, #FF69B4 100%) !important;
    border: none !important;
    border-radius: 50% !important;
    color: white !important;
    width: 44px !important;
    height: 44px !important;
    box-shadow:
        0 4px 15px rgba(255, 122, 158, 0.3),
        0 2px 8px rgba(255, 105, 180, 0.2) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    margin-left: 10px !important;
    position: relative !important;
    overflow: hidden !important;
}

.stChatInput button::before {
    content: '💖' !important;
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    font-size: 16px !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}

.stChatInput button:hover {
    background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%) !important;
    box-shadow:
        0 6px 20px rgba(255, 122, 158, 0.4),
        0 3px 12px rgba(255, 20, 147, 0.3) !important;
    transform: translateY(-2px) scale(1.05) !important;
}

.stChatInput button:hover::before {
    opacity: 1 !important;
}

.stChatInput button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* 🎨 警告和提示信息颜色统一 */
.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 15px var(--shadow) !important;
}

/* 🎨 加载状态颜色统一 */
.stSpinner {
    color: var(--primary) !important;
}

.stSpinner > div {
    border-color: var(--primary) var(--secondary) var(--accent) var(--primary) !important;
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

/* 🎨 滚动条颜色统一 */
* {
    scrollbar-width: thin;
    scrollbar-color: var(--primary) var(--bg-primary);
}

*::-webkit-scrollbar {
    width: 8px;
}

*::-webkit-scrollbar-track {
    background: var(--bg-primary);
    border-radius: 10px;
}

*::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 10px;
    border: 2px solid var(--bg-primary);
}

*::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--secondary), var(--primary));
}

/* 🎨 页面加载动画 - 可爱效果 */
@keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(30px) scale(0.95);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes heartbeat {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

@keyframes float {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-5px);
    }
}

.stApp > div {
    animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 🎨 主标题动画 */
.main-title {
    animation: heartbeat 3s ease-in-out infinite;
}

/* 🎨 聊天气泡微妙浮动 */
.stChatMessage {
    animation: float 4s ease-in-out infinite;
}

.stChatMessage:nth-child(even) {
    animation-delay: 0.5s;
}

.stChatMessage:nth-child(odd) {
    animation-delay: 1s;
}

/* 🎨 聊天消息头像 - 超可爱设计 */
.stChatMessage .stAvatar {
    background: linear-gradient(135deg, #FFE4E1 0%, #FFF0F5 100%) !important;
    color: var(--primary) !important;
    border: 3px solid rgba(255, 182, 193, 0.6) !important;
    box-shadow:
        0 4px 12px rgba(255, 122, 158, 0.2),
        inset 0 2px 4px rgba(255, 255, 255, 0.8) !important;
    width: 45px !important;
    height: 45px !important;
    border-radius: 50% !important;
    position: relative !important;
    overflow: hidden !important;
}

/* AI头像 - 小精灵图标 */
.stChatMessage[data-testid="assistant-message"] .stAvatar {
    background: linear-gradient(135deg, #FFB6C1 0%, #FFC0CB 100%) !important;
    border: 3px solid rgba(255, 255, 255, 0.9) !important;
}

.stChatMessage[data-testid="assistant-message"] .stAvatar::before {
    content: '✨' !important;
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    font-size: 20px !important;
    animation: sparkle 2s ease-in-out infinite !important;
}

/* 用户头像 - 可爱表情 */
.stChatMessage[data-testid="user-message"] .stAvatar {
    background: linear-gradient(135deg, #E6E6FA 0%, #F0E6FF 100%) !important;
}

.stChatMessage[data-testid="user-message"] .stAvatar::before {
    content: '😊' !important;
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    font-size: 18px !important;
}

/* 隐藏原始SVG图标 */
.stChatMessage .stAvatar svg {
    display: none !important;
}

/* 闪烁动画 */
@keyframes sparkle {
    0%, 100% {
        transform: translate(-50%, -50%) scale(1) rotate(0deg);
        opacity: 0.8;
    }
    50% {
        transform: translate(-50%, -50%) scale(1.1) rotate(180deg);
        opacity: 1;
    }
}

/* 🎨 所有组件颜色统一 */
.stApp, .main, .block-container {
    background: var(--bg-primary) !important;
}

.stToolbar {
    background: var(--bg-card) !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 15px var(--shadow) !important;
}

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    color: var(--text) !important;
}

.stCheckbox, .stRadio {
    color: var(--text) !important;
}

.stCheckbox > label, .stRadio > label {
    color: var(--text) !important;
    font-family: 'Nunito', sans-serif !important;
}

.stSlider > div > div > div {
    background: var(--secondary) !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, var(--secondary), var(--primary)) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 20px !important;
    padding: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text) !important;
    border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important;
}

.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
}

/* 🍓 确保页面底部有足够空间给悬浮输入框 */
.main .block-container {
    padding-bottom: 120px !important;
}

/* 🍓 移除Streamlit默认样式 */
div[data-testid="stForm"] {
    border: none !important;
    background: transparent !important;
}

/* 🎨 代码块颜色统一 */
.stMarkdown code {
    background: var(--focus-ring) !important;
    color: var(--primary) !important;
    border-radius: 8px !important;
    padding: 2px 6px !important;
}

.stCode {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 15px !important;
}

/* 🎨 侧边栏切换按钮 - 真正可用的版本 */
.sidebar-toggle-btn {
    position: fixed !important;
    top: 20px !important;
    left: 20px !important;
    z-index: 9999 !important;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    color: white !important;
    width: 50px !important;
    height: 50px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 20px !important;
    cursor: pointer !important;
    box-shadow:
        0 4px 15px rgba(255, 122, 158, 0.3),
        0 2px 8px rgba(255, 122, 158, 0.2) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 3px solid rgba(255, 255, 255, 0.9) !important;
    user-select: none !important;
}

.sidebar-toggle-btn:hover {
    transform: translateY(-2px) scale(1.05) !important;
    box-shadow:
        0 6px 20px rgba(255, 122, 158, 0.4),
        0 3px 12px rgba(255, 122, 158, 0.3) !important;
}

.sidebar-toggle-btn:active {
    transform: translateY(0) scale(0.98) !important;
}
</style>

<script>
// 🎨 侧边栏切换功能
document.addEventListener('DOMContentLoaded', function() {
    // 创建切换按钮
    function createToggleButton() {
        const existingBtn = document.querySelector('.sidebar-toggle-btn');
        if (existingBtn) return;

        const toggleBtn = document.createElement('div');
        toggleBtn.className = 'sidebar-toggle-btn';
        toggleBtn.innerHTML = '⚙️';
        toggleBtn.title = '打开/关闭设置面板';

        // 点击事件
        toggleBtn.addEventListener('click', function() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            const sidebarContent = document.querySelector('.stSidebar > div');

            if (sidebar && sidebarContent) {
                const isCollapsed = sidebar.getAttribute('aria-expanded') === 'false';

                if (isCollapsed) {
                    // 展开侧边栏
                    sidebar.setAttribute('aria-expanded', 'true');
                    sidebarContent.style.width = '21rem';
                    sidebarContent.style.transform = 'translateX(0)';
                    toggleBtn.style.left = '240px';
                    toggleBtn.innerHTML = '✖️';
                } else {
                    // 收起侧边栏
                    sidebar.setAttribute('aria-expanded', 'false');
                    sidebarContent.style.width = '0';
                    sidebarContent.style.transform = 'translateX(-100%)';
                    toggleBtn.style.left = '20px';
                    toggleBtn.innerHTML = '⚙️';
                }
            }
        });

        document.body.appendChild(toggleBtn);
    }

    // 监听页面变化
    const observer = new MutationObserver(function(mutations) {
        createToggleButton();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // 初始创建
    createToggleButton();
});
</script>
"""