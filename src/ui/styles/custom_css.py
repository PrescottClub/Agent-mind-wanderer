"""
甜美马卡龙风格CSS样式 🍰
完全重塑的可爱治愈系UI设计
"""

CUSTOM_CSS = """
<style>
/* 引入可爱字体 - 站酷快乐体 */
@import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');

/* 隐藏Streamlit默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* 🌈 全局设计语言 - 甜美马卡龙调色盘 */
:root {
    --primary-pink: #FFC0CB;           /* 主色调 - 少女粉 */
    --background-cream: #FFF5E1;       /* 背景基色 - 淡奶白 */
    --accent-lavender: #E6E6FA;        /* 辅助色1 - 薰衣草紫 */
    --accent-mint: #BFFCC6;            /* 辅助色2 - 薄荷绿 */
    --highlight-peach: #FFB6C1;        /* 强调色 - 蜜桃粉 */
    --text-soft-gray: #5D5D5D;         /* 文字主色 - 深灰 */
    --shadow-pink: rgba(255, 182, 193, 0.4);  /* 粉色阴影 */
    --glow-pink: rgba(255, 105, 180, 0.3);    /* 粉色光晕 */
}

/* 🎨 全局背景 - 梦幻马卡龙渐变 */
.stApp {
    background: linear-gradient(135deg,
        var(--background-cream) 0%,
        var(--primary-pink) 25%,
        var(--accent-lavender) 50%,
        var(--accent-mint) 75%,
        var(--highlight-peach) 100%);
    background-attachment: fixed;
    font-family: 'ZCOOL KuaiLe', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-soft-gray);
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

/* ✨ 梦幻泡泡背景装饰 */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
        radial-gradient(circle at 15% 85%, var(--shadow-pink) 0%, transparent 35%),
        radial-gradient(circle at 85% 15%, rgba(230, 230, 250, 0.2) 0%, transparent 40%),
        radial-gradient(circle at 45% 45%, rgba(191, 252, 198, 0.15) 0%, transparent 30%),
        radial-gradient(circle at 75% 75%, var(--glow-pink) 0%, transparent 45%);
    pointer-events: none;
    z-index: -1;
    animation: dreamyFloat 20s ease-in-out infinite;
}

@keyframes dreamyFloat {
    0%, 100% {
        background-position: 0% 0%, 100% 100%, 50% 50%, 25% 75%;
        opacity: 0.6;
    }
    33% {
        background-position: 30% 70%, 70% 30%, 80% 20%, 90% 10%;
        opacity: 0.8;
    }
    66% {
        background-position: 70% 30%, 30% 70%, 20% 80%, 60% 40%;
        opacity: 0.7;
    }
}

/* 🎭 全局字体设置 - 可爱风格 */
* {
    font-family: 'ZCOOL KuaiLe', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-soft-gray) !important;
    letter-spacing: 0.5px;
}

/* 📝 文字颜色统一 - 柔和色调 */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
    color: var(--text-soft-gray) !important;
}

.stTextArea label, .stButton label {
    color: #C2185B !important;
    font-weight: 600 !important;
}

/* 🌟 主标题样式 - 梦幻马卡龙渐变 */
.main-title {
    text-align: center;
    background: linear-gradient(45deg,
        var(--primary-pink),
        var(--highlight-peach),
        var(--accent-lavender),
        var(--accent-mint));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.5rem;
    font-weight: 700;
    margin: 2rem 0;
    text-shadow: 2px 2px 8px var(--shadow-pink);
    animation: titleShimmer 4s ease-in-out infinite;
    position: relative;
}

.main-title::before {
    content: '✨';
    position: absolute;
    left: -2rem;
    top: 50%;
    transform: translateY(-50%);
    animation: sparkleLeft 2s ease-in-out infinite;
}

.main-title::after {
    content: '✨';
    position: absolute;
    right: -2rem;
    top: 50%;
    transform: translateY(-50%);
    animation: sparkleRight 2s ease-in-out infinite 0.5s;
}

@keyframes titleShimmer {
    0%, 100% {
        background: linear-gradient(45deg, var(--primary-pink), var(--highlight-peach), var(--accent-lavender));
        -webkit-background-clip: text;
        background-clip: text;
    }
    50% {
        background: linear-gradient(45deg, var(--accent-mint), var(--primary-pink), var(--highlight-peach));
        -webkit-background-clip: text;
        background-clip: text;
    }
}

@keyframes sparkleLeft {
    0%, 100% { transform: translateY(-50%) scale(1) rotate(0deg); opacity: 0.7; }
    50% { transform: translateY(-50%) scale(1.3) rotate(180deg); opacity: 1; }
}

@keyframes sparkleRight {
    0%, 100% { transform: translateY(-50%) scale(1) rotate(0deg); opacity: 0.7; }
    50% { transform: translateY(-50%) scale(1.3) rotate(-180deg); opacity: 1; }
}

.subtitle {
    text-align: center;
    color: #C2185B !important;
    font-size: 1.4rem;
    margin-bottom: 2.5rem;
    font-weight: 500;
    text-shadow: 1px 1px 4px var(--shadow-pink);
    position: relative;
}

.subtitle::before {
    content: '🎀';
    margin-right: 0.5rem;
}

.subtitle::after {
    content: '🎀';
    margin-left: 0.5rem;
}

/* 🧚‍♀️ 精灵展示区 - 软糖般的可爱容器 */
.sprite-container {
    background: linear-gradient(135deg,
        var(--background-cream) 0%,
        var(--primary-pink) 30%,
        var(--accent-lavender) 70%,
        var(--accent-mint) 100%);
    border-radius: 30px;
    padding: 2.5rem;
    text-align: center;
    box-shadow:
        0 20px 40px var(--shadow-pink),
        inset 0 4px 15px rgba(255, 255, 255, 0.7),
        0 0 30px var(--glow-pink);
    border: 4px solid rgba(255, 255, 255, 0.9);
    margin-bottom: 2rem;
    min-height: 280px;
    position: relative;
    overflow: hidden;
    animation: containerBreath 5s ease-in-out infinite;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.sprite-container:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow:
        0 25px 50px var(--shadow-pink),
        inset 0 6px 20px rgba(255, 255, 255, 0.8),
        0 0 40px var(--glow-pink);
}

@keyframes containerBreath {
    0%, 100% {
        box-shadow:
            0 20px 40px var(--shadow-pink),
            inset 0 4px 15px rgba(255, 255, 255, 0.7),
            0 0 30px var(--glow-pink);
        transform: scale(1);
    }
    50% {
        box-shadow:
            0 25px 50px rgba(255, 182, 193, 0.6),
            inset 0 6px 20px rgba(255, 255, 255, 0.9),
            0 0 40px rgba(255, 105, 180, 0.4);
        transform: scale(1.01);
    }
}

.sprite-emoji {
    font-size: 7rem;
    margin-bottom: 1.5rem;
    animation: spriteFloat 4s ease-in-out infinite;
    line-height: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: auto;
    text-align: center;
    filter: drop-shadow(0 4px 8px var(--shadow-pink));
    transition: all 0.3s ease;
}

.sprite-emoji:hover {
    transform: scale(1.1) rotate(5deg);
    filter: drop-shadow(0 6px 12px var(--glow-pink));
}

/* 🎭 精灵动画效果 */
@keyframes spriteFloat {
    0%, 100% {
        transform: translateY(0px) rotate(0deg);
        filter: drop-shadow(0 4px 8px var(--shadow-pink));
    }
    25% {
        transform: translateY(-12px) rotate(2deg);
        filter: drop-shadow(0 6px 12px var(--shadow-pink));
    }
    50% {
        transform: translateY(-20px) rotate(0deg);
        filter: drop-shadow(0 8px 16px var(--glow-pink));
    }
    75% {
        transform: translateY(-12px) rotate(-2deg);
        filter: drop-shadow(0 6px 12px var(--shadow-pink));
    }
}

@keyframes sparkle {
    0%, 100% {
        opacity: 0.3;
        transform: scale(0.8) rotate(0deg);
    }
    50% {
        opacity: 1;
        transform: scale(1.4) rotate(180deg);
    }
}

@keyframes heartbeat {
    0%, 100% {
        transform: scale(1);
        filter: drop-shadow(0 2px 4px var(--shadow-pink));
    }
    50% {
        transform: scale(1.15);
        filter: drop-shadow(0 4px 8px var(--glow-pink));
    }
}

@keyframes wiggle {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(2deg); }
    75% { transform: rotate(-2deg); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

/* ✨ 装饰性闪光元素 - 马卡龙色彩 */
.decoration {
    position: absolute;
    font-size: 1.5rem;
    animation: sparkle 3s ease-in-out infinite;
    z-index: 2;
}

.decoration:nth-child(1) {
    top: 8%;
    left: 8%;
    animation-delay: 0s;
    color: var(--primary-pink);
}

.decoration:nth-child(2) {
    top: 15%;
    right: 12%;
    animation-delay: 0.7s;
    color: var(--accent-lavender);
}

.decoration:nth-child(3) {
    bottom: 25%;
    left: 15%;
    animation-delay: 1.4s;
    color: var(--accent-mint);
}

.decoration:nth-child(4) {
    bottom: 8%;
    right: 8%;
    animation-delay: 2.1s;
    color: var(--highlight-peach);
}

/* 🎀 精灵名称和状态 - 可爱字体样式 */
.sprite-name {
    font-size: 1.8rem;
    font-weight: 700;
    color: #FF69B4;
    margin-bottom: 0.8rem;
    text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
    position: relative;
    animation: heartbeat 3s ease-in-out infinite;
}

.sprite-name::before {
    content: '💖';
    margin-right: 0.5rem;
    animation: bounce 2s ease-in-out infinite;
}

.sprite-status {
    font-size: 1.2rem;
    color: #8A2BE2;
    font-weight: 600;
    text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.7);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 240, 245, 0.5));
    padding: 0.5rem 1rem;
    border-radius: 20px;
    border: 2px solid rgba(255, 182, 193, 0.4);
    display: inline-block;
    animation: wiggle 4s ease-in-out infinite;
}

/* 💭 回应卡片 - 云朵般柔软 */
.response-card {
    background: linear-gradient(135deg,
        rgba(255, 255, 255, 0.98) 0%,
        var(--background-cream) 50%,
        rgba(248, 240, 255, 0.95) 100%);
    border-radius: 25px;
    padding: 2rem;
    margin-top: 1.5rem;
    box-shadow:
        0 8px 25px var(--shadow-pink),
        inset 0 2px 8px rgba(255, 255, 255, 0.8);
    border: 3px solid rgba(255, 182, 193, 0.4);
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.response-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 215, 0, 0.05) 0%, transparent 70%);
    animation: sparkle 4s ease-in-out infinite;
}

.response-card:hover {
    transform: translateY(-3px);
    box-shadow:
        0 12px 35px var(--shadow-pink),
        inset 0 3px 12px rgba(255, 255, 255, 0.9);
}

.response-card h4 {
    color: #FF69B4 !important;
    margin-bottom: 1.2rem !important;
    font-size: 1.4rem !important;
    position: relative;
    z-index: 1;
    text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.8);
}

.response-card h4::before {
    content: '🌸';
    margin-right: 0.5rem;
}

.response-card p {
    color: var(--text-soft-gray) !important;
    line-height: 1.8 !important;
    font-size: 1.1rem !important;
    position: relative;
    z-index: 1;
    text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.6);
}

/* 🎁 礼物卡片 - 马卡龙糖果盒 */
.gift-card {
    background: linear-gradient(135deg,
        var(--highlight-peach) 0%,
        var(--primary-pink) 30%,
        var(--accent-lavender) 70%,
        rgba(255, 182, 230, 0.9) 100%);
    border-radius: 30px;
    padding: 2rem;
    margin-top: 1.5rem;
    box-shadow:
        0 12px 35px var(--shadow-pink),
        inset 0 3px 12px rgba(255, 255, 255, 0.7),
        0 0 25px var(--glow-pink);
    border: 4px solid rgba(255, 255, 255, 0.8);
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    animation: giftGlow 6s ease-in-out infinite;
}

.gift-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 215, 0, 0.08) 0%, transparent 70%);
    animation: sparkle 5s ease-in-out infinite;
}

.gift-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow:
        0 18px 45px var(--shadow-pink),
        inset 0 4px 16px rgba(255, 255, 255, 0.8),
        0 0 35px var(--glow-pink);
}

@keyframes giftGlow {
    0%, 100% {
        box-shadow:
            0 12px 35px var(--shadow-pink),
            inset 0 3px 12px rgba(255, 255, 255, 0.7),
            0 0 25px var(--glow-pink);
    }
    50% {
        box-shadow:
            0 15px 40px rgba(255, 182, 193, 0.6),
            inset 0 4px 16px rgba(255, 255, 255, 0.9),
            0 0 35px rgba(255, 105, 180, 0.4);
    }
}

.gift-card h4 {
    color: #C2185B !important;
    margin-bottom: 1.5rem !important;
    font-size: 1.5rem !important;
    position: relative;
    z-index: 1;
    text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.9);
    font-weight: 700;
}

.gift-card p {
    color: var(--text-soft-gray) !important;
    line-height: 1.8 !important;
    font-size: 1.2rem !important;
    position: relative;
    z-index: 1;
    text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.7);
    font-weight: 500;
}

/* 🖼️ 历史画廊 - 回忆相册风格 */
.history-gallery {
    margin-top: 3rem;
    padding: 2rem;
    background: linear-gradient(135deg,
        rgba(255, 255, 255, 0.1) 0%,
        rgba(255, 245, 225, 0.2) 100%);
    border-radius: 25px;
    border: 2px solid rgba(255, 182, 193, 0.2);
}

.history-gallery h3 {
    text-align: center;
    color: #FF69B4 !important;
    margin-bottom: 2rem !important;
    font-size: 2rem !important;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
    position: relative;
}

.history-gallery h3::before {
    content: '📸';
    margin-right: 0.5rem;
}

.history-gallery h3::after {
    content: '✨';
    margin-left: 0.5rem;
}

.history-card {
    background: linear-gradient(135deg,
        rgba(255, 255, 255, 0.95) 0%,
        var(--background-cream) 50%,
        rgba(255, 240, 245, 0.9) 100%);
    border-radius: 20px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow:
        0 8px 20px var(--shadow-pink),
        inset 0 2px 8px rgba(255, 255, 255, 0.6);
    border: 3px solid rgba(255, 182, 193, 0.3);
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative;
    overflow: hidden;
}

.history-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transition: left 0.6s ease;
}

.history-card:hover::before {
    left: 100%;
}

.history-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow:
        0 12px 30px var(--shadow-pink),
        inset 0 3px 12px rgba(255, 255, 255, 0.8);
    border-color: rgba(255, 105, 180, 0.5);
}

.timestamp {
    font-size: 1rem;
    color: #C2185B !important;
    text-align: right;
    margin-bottom: 0.8rem;
    font-weight: 600;
    text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.8);
    background: rgba(255, 255, 255, 0.5);
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    display: inline-block;
    float: right;
}

/* 🍭 按钮样式 - 胶囊糖果风格 */
.stButton > button {
    background: linear-gradient(135deg,
        var(--accent-mint) 0%,
        var(--primary-pink) 50%,
        var(--highlight-peach) 100%) !important;
    border: 3px solid rgba(255, 255, 255, 0.8) !important;
    border-radius: 999px !important;  /* 完美胶囊形状 */
    color: var(--text-soft-gray) !important;
    font-weight: 700 !important;
    padding: 0.8rem 2rem !important;
    box-shadow:
        0 6px 20px var(--shadow-pink),
        inset 0 2px 8px rgba(255, 255, 255, 0.6) !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.9) !important;
    font-size: 1.1rem !important;
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    transition: left 0.6s ease;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg,
        var(--primary-pink) 0%,
        var(--highlight-peach) 50%,
        var(--accent-lavender) 100%) !important;
    box-shadow:
        0 8px 25px var(--glow-pink),
        inset 0 3px 12px rgba(255, 255, 255, 0.8) !important;
    transform: translateY(-3px) scale(1.05) !important;
    border-color: rgba(255, 255, 255, 1) !important;
}

/* 🌟 主要提交按钮 - 特别闪亮 */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg,
        var(--primary-pink) 0%,
        var(--highlight-peach) 50%,
        #FF1493 100%) !important;
    border: 4px solid #FF1493 !important;
    box-shadow:
        0 8px 25px var(--glow-pink),
        inset 0 3px 12px rgba(255, 255, 255, 0.7) !important;
    animation: primaryGlow 3s ease-in-out infinite;
}

@keyframes primaryGlow {
    0%, 100% {
        box-shadow:
            0 8px 25px var(--glow-pink),
            inset 0 3px 12px rgba(255, 255, 255, 0.7);
    }
    50% {
        box-shadow:
            0 12px 35px rgba(255, 20, 147, 0.5),
            inset 0 4px 16px rgba(255, 255, 255, 0.9);
    }
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg,
        #FF1493 0%,
        var(--primary-pink) 50%,
        var(--highlight-peach) 100%) !important;
    box-shadow:
        0 12px 35px rgba(255, 20, 147, 0.6),
        inset 0 4px 16px rgba(255, 255, 255, 0.9) !important;
    transform: translateY(-4px) scale(1.08) !important;
}

/* 🎀 次要按钮 - 柔和可爱 */
.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg,
        var(--background-cream) 0%,
        var(--accent-lavender) 50%,
        var(--accent-mint) 100%) !important;
    border: 3px solid var(--accent-lavender) !important;
    color: #C2185B !important;
    box-shadow:
        0 4px 15px rgba(230, 230, 250, 0.4),
        inset 0 2px 8px rgba(255, 255, 255, 0.8) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: linear-gradient(135deg,
        var(--accent-lavender) 0%,
        var(--primary-pink) 50%,
        var(--highlight-peach) 100%) !important;
    border-color: var(--primary-pink) !important;
    box-shadow:
        0 6px 20px var(--shadow-pink),
        inset 0 3px 12px rgba(255, 255, 255, 0.9) !important;
    transform: translateY(-3px) scale(1.05) !important;
}

/* 💭 文本输入区域 - 云朵般柔软 */
.stTextArea > div > div > textarea {
    border: 4px solid transparent !important;
    border-radius: 20px !important;
    background: linear-gradient(
        rgba(255, 255, 255, 0.98),
        var(--background-cream)) padding-box,
        linear-gradient(135deg,
            var(--accent-mint),
            var(--primary-pink),
            var(--accent-lavender)) border-box !important;
    color: var(--text-soft-gray) !important;
    box-shadow:
        inset 0 3px 12px rgba(255, 192, 203, 0.2),
        0 4px 15px var(--shadow-pink) !important;
    font-size: 1.1rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
}

.stTextArea > div > div > textarea:focus {
    background: linear-gradient(
        rgba(255, 255, 255, 1),
        rgba(255, 240, 245, 0.98)) padding-box,
        linear-gradient(135deg,
            var(--primary-pink),
            var(--highlight-peach),
            #FF1493) border-box !important;
    box-shadow:
        0 0 25px var(--glow-pink),
        inset 0 4px 16px rgba(255, 192, 203, 0.3),
        0 8px 25px var(--shadow-pink) !important;
    transform: scale(1.02) !important;
}

.stTextArea > div > div > textarea::placeholder {
    color: rgba(93, 93, 93, 0.6) !important;
    font-style: italic;
}

/* 📝 表单容器 - 梦幻边框 */
.stForm {
    border: 4px solid transparent !important;
    border-radius: 25px !important;
    background: linear-gradient(
        rgba(255, 255, 255, 0.95),
        rgba(255, 255, 255, 0.9)) padding-box,
        linear-gradient(135deg,
            var(--accent-mint),
            var(--primary-pink),
            var(--accent-lavender),
            var(--highlight-peach)) border-box !important;
    padding: 2rem !important;
    box-shadow:
        0 12px 35px var(--shadow-pink),
        inset 0 3px 12px rgba(255, 255, 255, 0.8) !important;
    margin: 1rem 0 !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
}

.stForm:hover {
    transform: translateY(-2px);
    box-shadow:
        0 15px 40px var(--shadow-pink),
        inset 0 4px 16px rgba(255, 255, 255, 0.9) !important;
}

/* 🎨 标题和文本样式优化 */
.stMarkdown h5 {
    color: #FF69B4 !important;
    text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.9) !important;
    margin-bottom: 1.5rem !important;
    font-weight: 700 !important;
    font-size: 1.3rem !important;
}

.stMarkdown h5::before {
    content: '🌈';
    margin-right: 0.5rem;
}

/* 移除Streamlit默认样式 */
div[data-testid="stForm"] {
    border: none !important;
    background: transparent !important;
}

/* 聊天区域标题美化 */
.stMarkdown h3 {
    color: #FF69B4 !important;
    text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.9) !important;
    margin-bottom: 1.5rem !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
    position: relative;
}

/* 标签和帮助文本 */
.stTextArea label {
    color: #C2185B !important;
    font-weight: 700 !important;
    text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.9) !important;
    font-size: 1.1rem !important;
}

.stTextArea .help {
    color: var(--text-soft-gray) !important;
    font-size: 1rem !important;
    font-style: italic;
    text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.7) !important;
}

/* 🚨 警告和提示信息 */
.stAlert {
    border-radius: 20px !important;
    border: 3px solid var(--accent-lavender) !important;
    background: linear-gradient(135deg,
        rgba(255, 240, 245, 0.95) 0%,
        rgba(255, 255, 255, 0.98) 100%) !important;
    box-shadow: 0 6px 20px var(--shadow-pink) !important;
}

/* ⏳ 加载状态美化 */
.stSpinner {
    color: var(--primary-pink) !important;
}

.stSpinner > div {
    border-color: var(--primary-pink) var(--accent-lavender) var(--accent-mint) var(--highlight-peach) !important;
    border-width: 3px !important;
}

/* 📊 列标题 */
.stMarkdown h4 {
    color: #FF69B4 !important;
    text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.9) !important;
    font-weight: 700 !important;
    margin-bottom: 1rem !important;
}

/* ➖ 分隔线美化 */
hr {
    border: none !important;
    height: 3px !important;
    background: linear-gradient(90deg,
        transparent,
        var(--accent-lavender),
        var(--primary-pink),
        var(--accent-mint),
        transparent) !important;
    margin: 3rem 0 !important;
    border-radius: 2px;
}

/* 😊 确保emoji正常显示 */
.sprite-emoji {
    font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif !important;
    font-style: normal !important;
    font-variant: normal !important;
}

/* 🎁 侧边栏美化 - 薰衣草紫主题 */
.stSidebar > div:first-child {
    background: linear-gradient(180deg,
        var(--accent-lavender) 0%,
        rgba(230, 230, 250, 0.8) 50%,
        rgba(191, 252, 198, 0.6) 100%) !important;
    border-right: 4px solid rgba(255, 182, 193, 0.3);
}

/* 聊天气泡样式 - 马卡龙色彩 */
.stChatMessage {
    border-radius: 20px !important;
    padding: 1rem 1.5rem !important;
    margin: 0.5rem 0 !important;
    box-shadow: 0 4px 15px var(--shadow-pink) !important;
    border: 2px solid rgba(255, 255, 255, 0.6) !important;
}

/* 用户消息气泡 - 薄荷绿 */
.stChatMessage[data-testid="user-message"] {
    background: linear-gradient(135deg,
        var(--accent-mint) 0%,
        rgba(191, 252, 198, 0.8) 100%) !important;
    margin-left: 2rem !important;
}

/* AI消息气泡 - 少女粉 */
.stChatMessage[data-testid="assistant-message"] {
    background: linear-gradient(135deg,
        var(--primary-pink) 0%,
        var(--highlight-peach) 100%) !important;
    margin-right: 2rem !important;
}

/* 宝藏盒标题装饰 */
.stMarkdown h3:contains("宝藏")::before {
    content: '🎁 ';
}

/* 📱 响应式设计 - 移动端优化 */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem;
        margin: 1rem 0;
    }

    .main-title::before,
    .main-title::after {
        display: none;
    }

    .sprite-container {
        padding: 1.5rem;
        min-height: 220px;
        margin-bottom: 1.5rem;
    }

    .sprite-emoji {
        font-size: 5rem;
    }

    .response-card, .gift-card {
        padding: 1.5rem;
        margin-top: 1rem;
    }

    .stForm {
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
    }

    .stTextArea > div > div > textarea {
        font-size: 1rem !important;
        padding: 0.8rem !important;
    }

    .stButton > button {
        padding: 0.7rem 1.5rem !important;
        font-size: 1rem !important;
    }

    .history-gallery {
        padding: 1rem;
        margin-top: 2rem;
    }

    .history-card {
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    .stChatMessage {
        margin-left: 0.5rem !important;
        margin-right: 0.5rem !important;
        padding: 0.8rem 1rem !important;
    }
}

/* 🌟 特殊效果 - 鼠标悬停时的魔法光晕 */
.stApp:hover::before {
    animation-duration: 10s;
}

/* 页面加载动画 */
@keyframes pageLoad {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

.stApp > div {
    animation: pageLoad 0.8s ease-out;
}

/* 🎪 最终的魔法触摸 - 整体和谐感 */
* {
    scrollbar-width: thin;
    scrollbar-color: var(--primary-pink) var(--background-cream);
}

*::-webkit-scrollbar {
    width: 8px;
}

*::-webkit-scrollbar-track {
    background: var(--background-cream);
    border-radius: 10px;
}

*::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--primary-pink), var(--accent-lavender));
    border-radius: 10px;
    border: 2px solid var(--background-cream);
}

*::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--highlight-peach), var(--primary-pink));
}
</style>
"""