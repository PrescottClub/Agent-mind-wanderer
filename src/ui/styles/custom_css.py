"""
自定义CSS样式
包含所有Streamlit应用的样式定义
"""

CUSTOM_CSS = """
<style>
/* 隐藏Streamlit默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* 全局字体和背景 - 可爱粉色渐变 */
.stApp {
    background: linear-gradient(135deg, #FFB6C1 0%, #FFC0CB 25%, #FFCCCB 50%, #FFB3E6 75%, #FFE4E6 100%);
    background-attachment: fixed;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    color: #8B4A78;
    animation: colorShift 10s ease-in-out infinite;
}

@keyframes colorShift {
    0%, 100% { 
        background: linear-gradient(135deg, #FFB6C1 0%, #FFC0CB 25%, #FFCCCB 50%, #FFB3E6 75%, #FFE4E6 100%);
    }
    50% { 
        background: linear-gradient(135deg, #FFE4E6 0%, #FFB3E6 25%, #FFCCCB 50%, #FFC0CB 75%, #FFB6C1 100%);
    }
}

* {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #8B4A78 !important;
}

/* Streamlit组件文字颜色修复 - 可爱粉色系 */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #8B4A78 !important;
}

.stTextArea label, .stButton label {
    color: #C2185B !important;
    font-weight: 600 !important;
}

/* 主标题样式 - 超可爱粉色 */
.main-title {
    text-align: center;
    background: linear-gradient(45deg, #FF69B4, #FFB3E6, #FFC0CB);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(255,105,180,0.3);
    animation: titleShimmer 3s ease-in-out infinite;
}

@keyframes titleShimmer {
    0%, 100% { 
        background: linear-gradient(45deg, #FF69B4, #FFB3E6, #FFC0CB);
        -webkit-background-clip: text;
        background-clip: text;
    }
    50% { 
        background: linear-gradient(45deg, #FFC0CB, #FF69B4, #FFB3E6);
        -webkit-background-clip: text;
        background-clip: text;
    }
}

.subtitle {
    text-align: center;
    color: #C2185B !important;
    font-size: 1.2rem;
    margin-bottom: 2rem;
    font-weight: 500;
    text-shadow: 1px 1px 2px rgba(255,105,180,0.2);
}

/* 精灵展示区样式 - 超可爱粉色泡泡 */
.sprite-container {
    background: linear-gradient(135deg, #FFB3E6 0%, #FFC0CB 25%, #FFE4E6 50%, #FFCCCB 75%, #FFB6C1 100%);
    border-radius: 35px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 15px 35px rgba(255, 105, 180, 0.4), inset 0 2px 10px rgba(255, 255, 255, 0.6);
    border: 4px solid rgba(255, 255, 255, 0.8);
    margin-bottom: 1rem;
    min-height: 250px;
    position: relative;
    overflow: hidden;
    animation: containerGlow 4s ease-in-out infinite;
}

@keyframes containerGlow {
    0%, 100% { 
        box-shadow: 0 15px 35px rgba(255, 105, 180, 0.4), inset 0 2px 10px rgba(255, 255, 255, 0.6);
    }
    50% { 
        box-shadow: 0 20px 40px rgba(255, 105, 180, 0.6), inset 0 3px 15px rgba(255, 255, 255, 0.8);
    }
}

.sprite-emoji {
    font-size: 6rem;
    margin-bottom: 1rem;
    animation: float 3s ease-in-out infinite;
    line-height: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: auto;
    text-align: center;
}

/* 添加超可爱的粉色泡泡背景装饰 */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
        radial-gradient(circle at 20% 80%, rgba(255, 105, 180, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 80% 20%, rgba(255, 192, 203, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 40% 40%, rgba(255, 182, 230, 0.1) 0%, transparent 35%),
        radial-gradient(circle at 70% 70%, rgba(255, 204, 204, 0.12) 0%, transparent 50%),
        radial-gradient(circle at 10% 30%, rgba(255, 179, 230, 0.08) 0%, transparent 30%);
    pointer-events: none;
    z-index: -1;
    animation: backgroundFloat 15s ease-in-out infinite;
}

@keyframes backgroundFloat {
    0%, 100% {
        background-position: 0% 0%, 100% 100%, 50% 50%, 25% 25%, 75% 75%;
    }
    33% {
        background-position: 33% 67%, 67% 33%, 80% 20%, 90% 10%, 10% 90%;
    }
    66% {
        background-position: 67% 33%, 33% 67%, 20% 80%, 70% 30%, 40% 60%;
    }
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    25% { transform: translateY(-8px) rotate(1deg); }
    50% { transform: translateY(-15px) rotate(0deg); }
    75% { transform: translateY(-8px) rotate(-1deg); }
}

@keyframes sparkle {
    0%, 100% { opacity: 0; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
}

@keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

@keyframes wiggle {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(1deg); }
    75% { transform: rotate(-1deg); }
}

/* 装饰性闪光元素 */
.decoration {
    position: absolute;
    animation: sparkle 2s ease-in-out infinite;
}

.decoration:nth-child(1) {
    top: 10%;
    left: 10%;
    animation-delay: 0s;
}

.decoration:nth-child(2) {
    top: 20%;
    right: 15%;
    animation-delay: 0.5s;
}

.decoration:nth-child(3) {
    bottom: 30%;
    left: 20%;
    animation-delay: 1s;
}

.decoration:nth-child(4) {
    bottom: 10%;
    right: 10%;
    animation-delay: 1.5s;
}

/* 精灵名称和状态样式 */
.sprite-name {
    font-size: 1.5rem;
    font-weight: 600;
    color: #FF69B4;
    margin-bottom: 0.5rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.sprite-status {
    font-size: 1rem;
    color: #8A2BE2;
    font-weight: 500;
}

/* 回应卡片样式 */
.response-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,240,255,0.9) 100%);
    border-radius: 20px;
    padding: 1.5rem;
    margin-top: 1rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border: 2px solid rgba(255,182,193,0.3);
}

.response-card h4 {
    color: #FF69B4 !important;
    margin-bottom: 1rem !important;
    font-size: 1.2rem !important;
}

.response-card p {
    color: #8B4A78 !important;
    line-height: 1.6 !important;
    font-size: 1rem !important;
}

/* 礼物卡片样式 - 可爱粉色渐变 */
.gift-card {
    background: linear-gradient(135deg, rgba(255,182,193,0.9) 0%, rgba(255,192,203,0.85) 50%, rgba(255,182,230,0.8) 100%);
    border-radius: 25px;
    padding: 1.5rem;
    margin-top: 1rem;
    box-shadow: 0 8px 25px rgba(255,105,180,0.3);
    border: 3px solid rgba(255,192,203,0.7);
    position: relative;
    overflow: hidden;
}

.gift-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,215,0,0.1) 0%, transparent 70%);
    animation: sparkle 3s ease-in-out infinite;
}

.gift-card h4 {
    color: #C2185B !important;
    margin-bottom: 1rem !important;
    font-size: 1.3rem !important;
    position: relative;
    z-index: 1;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
}

.gift-card p {
    color: #8B4A78 !important;
    line-height: 1.7 !important;
    font-size: 1.1rem !important;
    position: relative;
    z-index: 1;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.6);
}

/* 历史画廊样式 */
.history-gallery {
    margin-top: 2rem;
    padding: 1rem;
}

.history-gallery h3 {
    text-align: center;
    color: #FF69B4 !important;
    margin-bottom: 1.5rem !important;
    font-size: 1.8rem !important;
}

.history-card {
    background: linear-gradient(135deg, rgba(255,182,193,0.85) 0%, rgba(255,192,203,0.75) 50%, rgba(255,240,245,0.9) 100%);
    border-radius: 20px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 5px 15px rgba(255,105,180,0.25);
    border-left: 5px solid #FF69B4;
    border: 2px solid rgba(255,105,180,0.3);
    transition: all 0.3s ease;
}

.history-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(255,105,180,0.4);
    border-color: rgba(255,105,180,0.5);
}

.timestamp {
    font-size: 0.9rem;
    color: #C2185B !important;
    text-align: right;
    margin-bottom: 0.5rem;
    font-weight: 500;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
}

/* 按钮样式 - 超可爱粉色 */
.stButton > button {
    background: linear-gradient(135deg, #FFB3E6 0%, #FFC0CB 50%, #FFE4E6 100%) !important;
    border: 2px solid #FF69B4 !important;
    border-radius: 25px !important;
    color: #8B4A78 !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 15px rgba(255,105,180,0.3) !important;
    transition: all 0.3s ease !important;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #FF69B4 0%, #FFB3E6 50%, #FFC0CB 100%) !important;
    box-shadow: 0 6px 20px rgba(255,105,180,0.5) !important;
    transform: translateY(-2px) !important;
}

/* 特别处理主要提交按钮 */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #FF69B4 0%, #FFB3E6 50%, #FFC0CB 100%) !important;
    border: 3px solid #FF1493 !important;
    box-shadow: 0 6px 20px rgba(255,105,180,0.4) !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #FF1493 0%, #FF69B4 50%, #FFB3E6 100%) !important;
    box-shadow: 0 8px 25px rgba(255,105,180,0.6) !important;
    transform: translateY(-3px) !important;
}

/* 快速表达心情按钮 */
.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #FFE4E6 0%, #FFC0CB 50%, #FFB3E6 100%) !important;
    border: 2px solid #FFB3E6 !important;
    color: #C2185B !important;
    box-shadow: 0 3px 10px rgba(255,192,203,0.3) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: linear-gradient(135deg, #FFC0CB 0%, #FFB3E6 50%, #FF69B4 100%) !important;
    border-color: #FF69B4 !important;
    box-shadow: 0 5px 15px rgba(255,105,180,0.4) !important;
    transform: translateY(-2px) !important;
}

.stTextArea > div > div > textarea {
    border: 3px solid transparent !important;
    border-radius: 15px !important;
    background: linear-gradient(rgba(255,255,255,0.98), rgba(255,240,245,0.95)) padding-box, 
                linear-gradient(135deg, #FFE4E6, #FFC0CB, #FFB3E6) border-box !important;
    color: #8B4A78 !important;
    box-shadow: inset 0 2px 8px rgba(255,192,203,0.15) !important;
}

.stTextArea > div > div > textarea:focus {
    background: linear-gradient(rgba(255,255,255,1), rgba(255,240,245,0.98)) padding-box, 
                linear-gradient(135deg, #FF69B4, #FFB3E6, #FFC0CB) border-box !important;
    box-shadow: 0 0 20px rgba(255,105,180,0.3), inset 0 3px 10px rgba(255,192,203,0.2) !important;
}

/* 修复表单容器的样式 - 渐变边框 */
.stForm {
    border: 3px solid transparent !important;
    border-radius: 20px !important;
    background: linear-gradient(white, white) padding-box, 
                linear-gradient(135deg, #FFB3E6, #FFC0CB, #FFE4E6, #FFCCCB) border-box !important;
    padding: 1.5rem !important;
    box-shadow: 0 8px 25px rgba(255,105,180,0.2) !important;
}

/* 修复快速心情按钮区域 */
.stMarkdown h5 {
    color: #FF69B4 !important;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
    margin-bottom: 1rem !important;
}

/* 移除Streamlit默认的黑色边框 */
div[data-testid="stForm"] {
    border: none !important;
    background: transparent !important;
}

/* 修复聊天区域的标题 */
.stMarkdown h3 {
    color: #FF69B4 !important;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
    margin-bottom: 1rem !important;
}

/* 修复标签和说明文字颜色 */
.stTextArea label {
    color: #C2185B !important;
    font-weight: 600 !important;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
}

.stTextArea .help {
    color: #8B4A78 !important;
    font-size: 0.9rem !important;
}

/* 修复警告信息样式 */
.stAlert {
    border-radius: 15px !important;
    border: 2px solid #FFB3E6 !important;
    background: linear-gradient(135deg, rgba(255,240,245,0.9) 0%, rgba(255,255,255,0.95) 100%) !important;
}

/* 修复加载状态的颜色 */
.stSpinner {
    color: #FF69B4 !important;
}

.stSpinner > div {
    border-color: #FF69B4 #FFB3E6 #FFC0CB #FFE4E6 !important;
}

/* 修复列标题颜色 */
.stMarkdown h4 {
    color: #FF69B4 !important;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
}

/* 修复分隔线颜色 */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, #FFB3E6, #FFC0CB, #FFB3E6, transparent) !important;
    margin: 2rem 0 !important;
}

/* 确保表情emoji正常显示 */
.sprite-emoji {
    font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif !important;
    font-style: normal !important;
    font-variant: normal !important;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .main-title {
        font-size: 2rem;
    }
    
    .sprite-container {
        padding: 1rem;
        min-height: 200px;
    }
    
    .sprite-emoji {
        font-size: 4.5rem;
    }
    
    .response-card, .gift-card {
        padding: 1rem;
    }
    
    .stForm {
        padding: 1rem !important;
    }
}
</style>
""" 