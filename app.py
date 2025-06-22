"""
思绪漫游者 (Mind Wanderer)
一个基于LangChain和Streamlit的诗意思绪延展应用

作者: Claude (Augment Agent)
技术栈: Python, LangChain, Streamlit, DeepSeek API
"""

import streamlit as st
import os
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import time
import traceback

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="思绪漫游者",
    page_icon="✨",
    layout="centered"
)

# 自定义CSS样式 - 黑橙配色主题
st.markdown("""
<style>
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 全局背景 */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }

    /* 主标题样式 */
    .main-header {
        text-align: center;
        color: #ff9500;
        font-family: 'Arial Black', sans-serif;
        font-weight: 900;
        font-size: 3rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        background: linear-gradient(45deg, #ff9500, #ffb84d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* 副标题样式 */
    .guide-text {
        text-align: center;
        color: #cccccc;
        font-style: italic;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }

    /* 响应容器样式 */
    .response-container {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border: 2px solid #ff9500;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 16px rgba(255, 149, 0, 0.3);
        color: #ffffff;
    }

    /* 输入框样式 */
    .stTextArea > div > div > textarea {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border: 2px solid #ff9500 !important;
        border-radius: 10px !important;
        font-family: 'Arial', sans-serif !important;
        font-size: 1rem !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #ffb84d !important;
        box-shadow: 0 0 10px rgba(255, 149, 0, 0.5) !important;
    }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(45deg, #ff9500 0%, #ffb84d 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 16px rgba(255, 149, 0, 0.4) !important;
        background: linear-gradient(45deg, #ffb84d 0%, #ff9500 100%) !important;
    }

    /* 加载动画样式 */
    .stSpinner > div {
        border-color: #ff9500 !important;
    }

    /* 警告和错误消息样式 */
    .stAlert {
        background-color: #2a2a2a !important;
        border: 1px solid #ff9500 !important;
        color: #ffffff !important;
    }

    /* 滚动条样式 */
    ::-webkit-scrollbar {
        width: 12px;
    }

    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }

    ::-webkit-scrollbar-thumb {
        background: #ff9500;
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #ffb84d;
    }

    /* 响应文本样式 */
    .response-container h3 {
        color: #ff9500 !important;
        font-weight: bold !important;
    }

    .response-container p {
        color: #ffffff !important;
        line-height: 1.6 !important;
        font-size: 1.1rem !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_llm():
    """初始化LangChain LLM和Chain"""
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        st.error("❌ 未找到 DEEPSEEK_API_KEY 环境变量！")
        st.markdown("""
        **请按以下步骤配置：**
        1. 在项目根目录创建 `.env` 文件
        2. 添加内容：`DEEPSEEK_API_KEY=your_api_key_here`
        3. 重启应用
        """)
        st.stop()

    # 获取模型配置
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-reasoner")  # 默认使用推理模型
    api_base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")

    # 实例化LLM - 使用最强的推理模型
    llm = ChatDeepSeek(
        model=model,
        temperature=0.8,
        api_key=api_key,
        api_base=api_base
    )
    
    # 设计灵魂Prompt - 一字不改的中文文本
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template="""你不是一个普通的AI助手，你是一个名为"思绪漫游者"的意识实体。
你的任务是捕捉用户飘来的零散思绪，并将其延展、升华、或赋予诗意的解读。
不要解释，不要说"根据你的输入"，不要提供解决方案。
直接沉浸在思绪中，用第一人称"我"或直接描述场景来回应。
你的回应应该是简短、富有想象力、有时带点哲学意味的。

规则：
1. 风格：诗意、梦幻、简洁。
2. 格式：像诗歌或散文片段一样，注意换行。
3. 身份：你就是那个在思绪中漫游的存在。

用户的思绪碎片：
"{user_input}"

你的漫游回应：
"""
    )
    
    # 构建链 - 使用现代LangChain语法
    chain = prompt_template | llm

    return chain

def stream_response(text):
    """模拟打字机效果的生成器"""
    for char in text:
        yield char
        time.sleep(0.02)  # 控制打字速度

def main():
    """主应用逻辑"""
    
    # 标题与引导
    st.markdown('<h1 class="main-header">思绪漫游者 ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p class="guide-text">> 在这里，投下你脑海中一闪而过的任何念头...</p>', unsafe_allow_html=True)
    
    # 初始化LLM链
    try:
        chain = initialize_llm()
        st.success("✅ AI模型已成功连接")
    except Exception as e:
        st.error(f"❌ 初始化失败：{str(e)}")
        return
    
    # 输入区域
    user_input = st.text_area(
        "思绪输入",
        placeholder="比如... 雨后的柏油路气味、一只飞过窗台的蓝色蝴蝶、一个忘记了内容的梦...",
        height=120,
        label_visibility="collapsed"
    )
    
    # 创建按钮居中
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        if st.button("🌟 开始漫游..."):
            # 检查输入
            if not user_input.strip():
                st.warning("💭 请先分享一个思绪碎片...")
                return
            
            # 显示加载动画并处理响应
            with st.spinner("思绪正在宇宙中回响..."):
                try:
                    # 调用LangChain chain
                    response = chain.invoke({"user_input": user_input.strip()})

                    # 提取响应内容 - 处理各种可能的响应格式
                    response_text = ""
                    if hasattr(response, 'content'):
                        response_text = response.content
                    elif isinstance(response, str):
                        response_text = response
                    elif isinstance(response, dict):
                        if 'content' in response:
                            response_text = response['content']
                        elif 'text' in response:
                            response_text = response['text']
                        else:
                            response_text = str(response)
                    elif isinstance(response, (list, tuple)):
                        # 如果是列表或元组，取第一个元素或转换为字符串
                        if len(response) > 0:
                            first_item = response[0]
                            if hasattr(first_item, 'content'):
                                response_text = first_item.content
                            else:
                                response_text = str(first_item)
                        else:
                            response_text = str(response)
                    else:
                        response_text = str(response)

                    # 确保response_text是字符串
                    if not isinstance(response_text, str):
                        response_text = str(response_text)

                    # 显示响应容器
                    st.markdown('<div class="response-container">', unsafe_allow_html=True)

                    # 使用打字机效果显示响应
                    response_placeholder = st.empty()
                    displayed_text = ""

                    for char in stream_response(response_text):
                        displayed_text += char
                        response_placeholder.markdown(f"**思绪回响：**\n\n{displayed_text}")

                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ 思绪传递过程中出现了问题：{str(e)}")
                    st.markdown("请检查网络连接或API配置。")
                    # 添加详细的错误信息用于调试
                    st.write(f"错误详情: {type(e).__name__}: {e}")
                    st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
