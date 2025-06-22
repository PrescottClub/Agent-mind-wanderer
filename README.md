# 思绪漫游者 ✨ (Mind Wanderer)

一个基于LangChain和Streamlit的诗意思绪延展应用。

## 项目理念

这不是一个普通的问答机器人，而是一个"思绪放大器"或"诗意生成器"。用户输入零散、模糊的念头，应用会返回一段充满想象力、诗意或哲理的文字，对这个念头进行延展和升华。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

1. 复制 `.env.example` 文件并重命名为 `.env`
2. 在 `.env` 文件中填入您的 DeepSeek API 配置：

```
DEEPSEEK_API_KEY=your_actual_api_key_here
DEEPSEEK_MODEL=deepseek-reasoner
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
```

### 3. 运行应用

```bash
streamlit run app.py
```

## 技术栈

- **Python** - 主要编程语言
- **Streamlit** - Web界面框架
- **LangChain** - AI链式调用框架
- **DeepSeek API** - AI模型服务

## 使用体验

在输入框中分享任何脑海中一闪而过的念头，比如：
- 雨后的柏油路气味
- 一只飞过窗台的蓝色蝴蝶
- 一个忘记了内容的梦

点击"开始漫游"，让AI为您的思绪注入诗意和哲理。

## 特色功能

- 🎨 **沉浸式界面** - 隐藏默认UI元素，专注于思绪交流
- ⚡ **打字机效果** - 逐字显示AI响应，增强体验感
- 🌟 **诗意Prompt** - 精心设计的提示词，确保输出富有想象力
- 🔒 **安全配置** - 环境变量管理API密钥

## 注意事项

- 确保您有有效的 DeepSeek API 密钥
- 应用需要网络连接来访问AI服务
- 建议在安静的环境中使用，以获得最佳的冥想体验
