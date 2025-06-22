# 心绪精灵 ✨ (Mind Sprite)

<div align="center">

![心绪精灵](https://img.shields.io/badge/心绪精灵-Mind%20Sprite-FF69B4)
![Version](https://img.shields.io/badge/version-2.0-FF1493)
![Python](https://img.shields.io/badge/python-3.8+-3776AB)
![License](https://img.shields.io/badge/license-MIT-green)

🧚‍♀️ **一个具备持久化记忆的治愈系AI情感陪伴应用，让可爱的小念陪伴你的每一种心情** 🧚‍♀️

[在线体验](#快速开始) · [功能特色](#功能特色) · [技术架构](#技术架构) · [部署指南](#部署指南)

</div>

---

## 🌟 项目简介

心绪精灵是一只住在网页里的可爱小精灵，名叫**小念(Xiao Nian)**。她拥有粉色的小翅膀和会发光的眼睛，总是充满爱心和温暖。当你感到开心、难过、平静、兴奋或困惑时，她会用超级可爱的语气回应你，并送给你一份专属的心灵礼物。

**2.0版本升级特性：**
- 🔄 **Agent化架构** - 模块化设计，更易维护扩展
- 💾 **持久化记忆** - SQLite数据库存储，会话历史永不丢失
- 🧠 **DeepSeek Reasoner** - 采用最新的R1推理模型，情感识别更精准
- 🔗 **会话持久化** - URL参数保持会话状态，刷新页面不丢失对话

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
- **持久化记忆** - SQLite数据库存储所有对话，建立长期情感连接

### 🎁 心灵礼物系统
- **🎭 元气咒语** - 充满正能量的魔法咒语，帮助获得内心力量
- **🌸 三行情诗** - 温柔浪漫的小诗，表达美好情感
- **🌙 梦境碎片** - 如梦如幻的场景描述，带来深度治愈感
- **🎨 心情壁纸** - 根据当前心情设计的唯美壁纸场景

### 🎨 沉浸式体验
- **响应式设计** - 完美适配手机、平板、电脑等所有设备
- **梦幻UI界面** - 渐变背景、浮动动画、可爱装饰元素
- **实时互动** - 快捷心情按钮，一键表达当前感受
- **会话持续性** - 通过URL参数保持会话状态，刷新不丢失

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
DEBUG_MODE=false
MAX_TOKENS=4096
```

### 4️⃣ 启动应用

**方式一：使用主应用 (推荐)**
```bash
streamlit run app.py
```

**方式二：使用模块化版本**
```bash
cd src
streamlit run main.py
```

🎉 打开浏览器访问 `http://localhost:8501`，开始和小念的治愈之旅！

---

## 💻 技术架构

### 核心技术栈
- **🐍 Python 3.8+** - 主要编程语言
- **⚡ Streamlit** - 现代化Web界面框架
- **🔗 LangChain** - AI应用开发框架
- **🧠 DeepSeek R1 (Reasoner)** - 最新推理模型，强大的情感分析能力
- **💾 SQLite** - 轻量级数据库，持久化存储对话历史
- **🎨 CSS3** - 自定义样式和动画效果

### 项目结构
```
Agent-mind-wanderer/
├── app.py                      # 主应用程序（单文件版本）
├── requirements.txt            # 项目依赖
├── README.md                  # 项目文档
├── .env                       # 环境变量配置
├── .gitignore                # Git忽略文件
├── mind_sprite.db            # SQLite数据库文件
└── src/                      # 模块化架构源码
    ├── main.py               # 模块化应用入口
    ├── config/               # 配置模块
    │   ├── settings.py       # 环境变量与配置管理
    │   ├── constants.py      # 常量定义
    │   └── prompts.py        # AI提示词模板
    ├── core/                 # 核心功能
    │   └── ai_engine.py      # AI引擎，封装LangChain与DeepSeek
    ├── models/               # 数据模型
    │   └── emotion.py        # 情绪结果与心情记录模型
    ├── ui/                   # 用户界面
    │   ├── components/       # UI组件
    │   │   ├── sprite_display.py    # 精灵显示组件
    │   │   └── gift_display.py     # 礼物显示组件
    │   └── styles/           # 样式文件
    │       └── custom_css.py # 自定义CSS样式
    └── utils/                # 工具函数（预留）
```

### 核心功能模块
- **🎭 AI Engine** - 基于DeepSeek R1的情感分析引擎
- **💾 数据库层** - SQLite持久化存储聊天历史
- **🎨 UI组件系统** - 模块化的界面组件
- **⚙️ 配置管理** - 环境变量与应用设置统一管理
- **🧠 推理模型** - DeepSeek Reasoner提供强大的思维链推理能力

---

## 🎯 使用指南

### 基础交互
1. **💭 自由表达** - 在文本框中输入任何想说的话
2. **🎭 快捷按钮** - 点击预设的心情按钮快速互动
3. **🎁 收集礼物** - 每次对话都会收到专属的心灵礼物
4. **🔗 会话持续** - 通过URL中的session_id保持对话连续性

### 高级功能
- **持久化记忆** - 所有对话都保存在本地数据库中
- **会话恢复** - 刷新页面或关闭浏览器后可以继续之前的对话
- **情绪趋势** - 通过历史记录观察情绪变化模式
- **思维链查看** - 在调试模式下查看AI的推理过程

---

## 🔧 部署指南

### 本地开发
```bash
# 启动主应用
streamlit run app.py --server.port 8501

# 启动模块化版本
cd src
streamlit run main.py --server.port 8501

# 调试模式（.env文件中设置DEBUG_MODE=true）
streamlit run app.py --logger.level debug
```

### 数据库管理
```bash
# 查看数据库内容（需要安装sqlite3）
sqlite3 mind_sprite.db

# 清空历史记录（谨慎操作）
sqlite3 mind_sprite.db "DELETE FROM chat_history;"
```

### 云端部署

#### Streamlit Cloud
1. Fork 这个项目到你的 GitHub
2. 登录 [Streamlit Cloud](https://streamlit.io/cloud)
3. 连接 GitHub 仓库并部署
4. 在Secrets中配置环境变量

#### Docker 部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
VOLUME ["/app/data"]
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

---

## 🎨 界面预览

### 主界面
- **🧚‍♀️ 精灵展示区** - 小念的动态表情和状态显示
- **💬 聊天互动区** - 温馨的对话交流界面
- **🎁 礼物展示区** - 精美的心灵礼物呈现
- **📚 心绪回响画廊** - 持久化的美好回忆展示

### 设计特色
- **梦幻渐变背景** - 粉色系温暖色调
- **浮动动画效果** - 轻盈灵动的视觉体验
- **响应式布局** - 完美适配各种设备尺寸
- **可爱装饰元素** - 星星、花朵、爱心等20+装饰

---

## 📊 2.0版本新特性

### Agent化架构
- **模块分离** - 配置、核心逻辑、UI、数据模型完全分离
- **易于扩展** - 新功能可以独立开发和测试
- **代码复用** - 组件化设计，提高开发效率

### 持久化系统
- **SQLite集成** - 轻量级数据库，无需额外配置
- **会话管理** - 通过UUID管理不同用户会话
- **历史查询** - 支持按时间、会话ID查询历史记录

### AI能力升级
- **DeepSeek R1** - 最新推理模型，具备强大的思维链能力
- **错误恢复** - 完善的容错机制，AI响应更稳定
- **调试支持** - 可选的思维过程展示，便于开发调试

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
2. 遵循模块化架构设计
3. 编写清晰的代码注释
4. 确保代码通过测试
5. 提交时使用规范的commit信息

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 💝 致谢

感谢以下开源项目和服务：
- [Streamlit](https://streamlit.io/) - 强大的Python Web应用框架
- [LangChain](https://www.langchain.com/) - 优秀的AI应用开发框架
- [DeepSeek](https://www.deepseek.com/) - 提供先进的AI推理能力
- 所有为这个项目贡献想法和代码的开发者们

---

<div align="center">

**让心绪精灵小念陪伴你的每一天 ✨**

如果这个项目对你有帮助，请给它一个⭐️

</div>
