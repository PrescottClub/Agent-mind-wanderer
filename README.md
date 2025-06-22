# 心绪精灵 ✨ (Mind Sprite)

<div align="center">

![心绪精灵](https://img.shields.io/badge/心绪精灵-Mind%20Sprite-FF69B4)
![Version](https://img.shields.io/badge/version-1.0.0-FF1493)
![Python](https://img.shields.io/badge/python-3.8+-3776AB)
![License](https://img.shields.io/badge/license-MIT-green)

🧚‍♀️ **一个治愈系的AI情感陪伴应用，让可爱的小念陪伴你的每一种心情** 🧚‍♀️

[在线体验](#快速开始) · [功能特色](#功能特色) · [技术架构](#技术架构) · [部署指南](#部署指南)

</div>

---

## 🌟 项目简介

心绪精灵是一只住在网页里的可爱小精灵，名叫**小念(Xiao Nian)**。她拥有粉色的小翅膀和会发光的眼睛，总是充满爱心和温暖。当你感到开心、难过、平静、兴奋或困惑时，她会用超级可爱的语气回应你，并送给你一份专属的心灵礼物。

### ✨ 设计理念

- 🎯 **情感陪伴** - 不仅是AI助手，更是贴心的情感伙伴
- 🎨 **治愈美学** - 梦幻粉色系UI，带来视觉上的温暖慰藉  
- 🧚‍♀️ **可爱互动** - 萌萌的小念会用颜文字和你对话
- 🎁 **心灵礼物** - 每次互动都能收到独特的治愈小礼物

---

## 🎯 功能特色

### 🧚‍♀️ 智能情感陪伴
- **多维情绪识别** - 精准识别9种情绪状态（开心/难过/平静/兴奋/困惑/温暖/疲惫/期待/感动）
- **个性化回应** - 小念会根据你的具体情况给出贴心回应
- **情绪记忆** - 记录你的心情变化，形成专属的心绪画廊

### 🎁 心灵礼物系统
- **🎭 元气咒语** - 充满正能量的魔法咒语，帮助获得内心力量
- **🌸 三行情诗** - 温柔浪漫的小诗，表达美好情感
- **🌙 梦境碎片** - 如梦如幻的场景描述，带来深度治愈感
- **🎨 心情壁纸** - 根据当前心情设计的唯美壁纸场景

### 🎨 沉浸式体验
- **响应式设计** - 完美适配手机、平板、电脑等所有设备
- **梦幻UI界面** - 渐变背景、浮动动画、可爱装饰元素
- **实时互动** - 快捷心情按钮，一键表达当前感受
- **心绪画廊** - 记录与小念的每一次温暖对话

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 有效的 DeepSeek API 密钥

### 1️⃣ 克隆项目
```bash
git clone https://github.com/yourusername/Agent-mind-wanderer.git
cd Agent-mind-wanderer
```

### 2️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

### 3️⃣ 配置环境变量
创建 `.env` 文件：
```env
DEEPSEEK_API_KEY=your_actual_api_key_here
DEEPSEEK_MODEL=deepseek-reasoner
DEEPSEEK_API_BASE=https://api.deepseek.com
```

### 4️⃣ 启动应用
```bash
streamlit run app.py
```

🎉 打开浏览器访问 `http://localhost:8501`，开始和小念的治愈之旅！

---

## 💻 技术架构

### 核心技术栈
- **🐍 Python** - 主要编程语言
- **⚡ Streamlit** - 现代化Web界面框架
- **🔗 LangChain** - AI应用开发框架
- **🧠 DeepSeek API** - 智能推理模型服务
- **🎨 CSS3** - 自定义样式和动画效果

### 项目结构
```
Agent-mind-wanderer/
├── app.py              # 主应用程序
├── requirements.txt    # 项目依赖
├── README.md          # 项目文档
├── .env               # 环境变量配置
├── .gitignore         # Git忽略文件
└── .cursor/           # 开发工具配置
```

### 核心功能模块
- **🎭 情绪分析引擎** - 基于先进NLP模型的情感识别
- **🎨 UI渲染系统** - 响应式布局和动画效果
- **💾 会话管理** - 智能的对话历史记录
- **🎁 礼物生成器** - 个性化内容创作系统

---

## 🎯 使用指南

### 基础交互
1. **💭 自由表达** - 在文本框中输入任何想说的话
2. **🎭 快捷按钮** - 点击预设的心情按钮快速互动
3. **🎁 收集礼物** - 每次对话都会收到专属的心灵礼物
4. **📚 回顾历史** - 在心绪画廊中重温温暖时光

### 高级功能
- **情绪趋势分析** - 观察自己的情绪变化模式
- **个性化定制** - 小念会学习你的喜好特点
- **治愈时刻** - 在特殊时刻收到额外的惊喜

---

## 🔧 部署指南

### 本地开发
```bash
# 启动开发服务器
streamlit run app.py --server.port 8501

# 调试模式
streamlit run app.py --logger.level debug
```

### 云端部署

#### Streamlit Cloud
1. Fork 这个项目到你的 GitHub
2. 登录 [Streamlit Cloud](https://streamlit.io/cloud)
3. 连接 GitHub 仓库并部署

#### Docker 部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 🎨 界面预览

### 主界面
- **🧚‍♀️ 精灵展示区** - 小念的动态表情和状态显示
- **💬 聊天互动区** - 温馨的对话交流界面
- **🎁 礼物展示区** - 精美的心灵礼物呈现
- **📚 心绪画廊** - 美好回忆的时光隧道

### 设计特色
- **梦幻渐变背景** - 粉色系温暖色调
- **浮动动画效果** - 轻盈灵动的视觉体验
- **响应式布局** - 完美适配各种设备尺寸
- **可爱装饰元素** - 星星、花朵、爱心等20+装饰

---

## 🤝 参与贡献

我们欢迎所有形式的贡献！

### 贡献方式
- 🐛 **报告Bug** - 提交Issue描述问题
- 💡 **功能建议** - 分享你的创意想法
- 🔧 **代码贡献** - 提交Pull Request
- 📖 **文档改进** - 完善项目文档

### 开发规范
1. Fork 项目并创建功能分支
2. 编写清晰的代码注释
3. 确保代码通过测试
4. 提交时使用规范的commit信息

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 💝 致谢

感谢以下技术和服务的支持：
- [Streamlit](https://streamlit.io/) - 快速构建Web应用
- [LangChain](https://python.langchain.com/) - AI应用开发框架
- [DeepSeek](https://www.deepseek.com/) - 智能AI模型服务

---

## 📞 联系我们

- 📧 **Email**: [your-email@example.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/Agent-mind-wanderer/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/Agent-mind-wanderer/discussions)

---

<div align="center">

**愿小念能成为你心灵路上的温暖陪伴 ✨**

Made with 💖 by [Your Name] | Powered by AI & Love

</div>
