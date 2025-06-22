# 📁 心绪精灵 v5.1 项目结构

## 🏗️ 目录结构

```
心绪精灵/
├── main.py                    # 🚀 应用主入口文件
├── README.md                  # 📖 项目说明文档
├── requirements.txt           # 📦 Python依赖包列表
├── mind_sprite.db            # 💾 SQLite数据库文件（自动生成）
└── src/                      # 📂 源代码目录
    ├── __init__.py           # 🐍 Python包初始化文件
    ├── config/               # ⚙️ 配置模块
    │   ├── __init__.py
    │   ├── constants.py      # 📋 常量定义
    │   └── settings.py       # 🔧 应用设置
    ├── core/                 # 🧠 核心功能模块
    │   ├── __init__.py
    │   ├── ai_engine.py      # 🤖 AI引擎（DeepSeek集成）
    │   └── session_manager.py # 📝 会话管理器
    ├── data/                 # 💾 数据层模块
    │   ├── __init__.py
    │   ├── database.py       # 🗄️ 数据库连接管理
    │   ├── models.py         # 📊 数据模型定义
    │   └── repositories/     # 📚 数据仓库模式
    │       ├── __init__.py
    │       ├── base_repository.py     # 🏗️ 基础仓库类
    │       ├── chat_repository.py     # 💬 聊天记录仓库
    │       ├── memory_repository.py   # 🧠 记忆仓库
    │       ├── treasure_repository.py # 🎁 宝藏仓库
    │       └── intimacy_repository.py # 💖 亲密度仓库
    ├── models/               # 📋 数据模型
    │   ├── __init__.py
    │   ├── chat.py          # 💬 聊天模型
    │   ├── memory.py        # 🧠 记忆模型
    │   ├── treasure.py      # 🎁 宝藏模型
    │   └── intimacy.py      # 💖 亲密度模型
    ├── services/            # 🔧 业务服务层
    │   ├── __init__.py
    │   ├── chat_service.py  # 💬 聊天服务
    │   ├── memory_service.py # 🧠 记忆服务
    │   ├── treasure_service.py # 🎁 宝藏服务
    │   └── intimacy_service.py # 💖 亲密度服务
    ├── ui/                  # 🎨 用户界面模块
    │   ├── __init__.py
    │   ├── components/      # 🧩 UI组件
    │   │   ├── __init__.py
    │   │   └── sidebar.py   # 📋 侧边栏组件
    │   └── styles/          # 🎨 样式文件
    │       ├── __init__.py
    │       └── custom_css.py # 🍰 甜美马卡龙CSS样式
    └── utils/               # 🛠️ 工具函数
        ├── __init__.py
        ├── helpers.py       # 🔧 辅助函数
        └── validators.py    # ✅ 验证函数
```

## 🚀 启动方式

```bash
streamlit run main.py
```

## 📝 核心文件说明

### 🎯 主入口文件
- **main.py**: 应用的唯一启动入口，整合所有模块

### 🧠 核心模块
- **ai_engine.py**: DeepSeek AI集成，处理情感分析和对话生成
- **session_manager.py**: 会话状态管理，URL参数持久化

### 💾 数据层
- **database.py**: SQLite数据库连接和初始化
- **repositories/**: 数据访问层，实现Repository模式
- **models/**: 数据模型定义，对应数据库表结构

### 🎨 UI层
- **custom_css.py**: 甜美马卡龙风格的完整CSS样式
- **sidebar.py**: 侧边栏组件，包含配置和状态显示

### ⚙️ 配置
- **settings.py**: 应用配置管理（已移除硬编码API密钥）
- **constants.py**: 常量定义，包含提示模板等

## 🔒 安全特性

- ✅ 无硬编码API密钥
- ✅ 用户输入的API密钥仅存储在浏览器会话中
- ✅ 数据库文件本地存储，保护隐私
- ✅ 会话级别的状态管理

## 🎨 设计特色

- 🍰 甜美马卡龙风格UI
- 🌈 动态色彩情绪映射
- ✨ 18种精美动画效果
- 📱 完美的响应式设计
- 💖 治愈系视觉体验

## 📊 技术特点

- 🏗️ 模块化架构，易于维护和扩展
- 🔄 Repository模式，数据访问层抽象
- 🎯 单一职责原则，每个模块功能明确
- 🧪 易于测试的代码结构
- 📈 可扩展的设计模式
