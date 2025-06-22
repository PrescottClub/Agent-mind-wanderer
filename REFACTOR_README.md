# 心绪精灵 - 重构文档 📋

## 🎯 重构目标

将原有的2800多行单体文件`app.py`重构为清晰、可维护的模块化架构，提升代码质量和可扩展性。

## 📁 新架构目录结构

```
mind-sprite/
├── src/
│   ├── core/                    # 核心业务逻辑层
│   │   ├── __init__.py
│   │   ├── ai_engine.py         # AI引擎 - DeepSeek模型封装
│   │   └── session_manager.py   # 会话管理器
│   ├── data/                    # 数据访问层
│   │   ├── __init__.py
│   │   ├── database.py          # 数据库连接和初始化
│   │   └── repositories/        # 数据仓库模式
│   │       ├── __init__.py
│   │       ├── base_repository.py    # 基础仓库类
│   │       └── chat_repository.py    # 聊天记录仓库
│   ├── ui/                      # 用户界面层
│   │   ├── __init__.py
│   │   └── components/          # UI组件
│   │       ├── __init__.py
│   │       └── sidebar.py       # 侧边栏组件
│   └── utils/                   # 工具函数层
│       ├── __init__.py
│       └── helpers.py           # 辅助函数
├── main.py                      # 新的主入口文件
├── app.py                       # 原有文件（保留作为参考）
├── requirements.txt             # 依赖配置
└── test_refactor.py            # 重构测试脚本
```

## 🔧 核心模块说明

### 1. 数据访问层 (`src/data/`)

**`database.py`**
- `init_db()`: 初始化所有数据库表
- `get_db_connection()`: 获取数据库连接

**`repositories/chat_repository.py`**
- `ChatRepository`: 封装所有数据库操作
  - `add_message()`: 添加聊天消息
  - `get_history()`: 获取聊天历史
  - `get_core_memories()`: 获取核心记忆
  - `add_treasure()`: 添加宝藏
  - 缓存管理方法

### 2. 核心业务逻辑层 (`src/core/`)

**`ai_engine.py`**
- `AIEngine`: AI引擎类
  - `get_response()`: 核心方法，获取AI回应
  - 支持思考过程可视化
  - 集成环境感知和记忆系统

**`session_manager.py`**
- `SessionManager`: 会话管理器
  - `get_session_id()`: 会话ID管理
  - `initialize_state()`: 状态初始化
  - API密钥管理

### 3. 用户界面层 (`src/ui/`)

**`components/sidebar.py`**
- `render_sidebar()`: 渲染侧边栏
- 包含API密钥输入、会话管理等功能
- 保持原有的美化样式

### 4. 工具函数层 (`src/utils/`)

**`helpers.py`**
- `get_environment_context()`: 环境感知
- `check_first_visit_today()`: 主动性检查
- `generate_proactive_greeting()`: 生成问候语
- `parse_ai_response()`: 解析AI回应
- `extract_gift_from_response()`: 提取礼物信息

## 🚀 使用方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行测试
```bash
python test_refactor.py
```

### 3. 启动应用
```bash
streamlit run main.py
```

## ✨ 重构优势

### 1. **模块化设计**
- 单一职责原则：每个模块专注特定功能
- 低耦合高内聚：模块间依赖清晰
- 易于测试和维护

### 2. **数据访问层分离**
- Repository模式：统一数据访问接口
- 基础仓库类：提供通用数据库操作
- 易于扩展新的数据源

### 3. **业务逻辑封装**
- AI引擎独立：便于切换不同模型
- 会话管理集中：状态管理更清晰
- 环境感知模块化：便于功能扩展

### 4. **UI组件化**
- 侧边栏组件独立：便于复用和修改
- 样式与逻辑分离：提升可维护性

## 🔄 迁移状态

### ✅ 已完成的模块
- [x] 数据库初始化和连接管理
- [x] 聊天记录仓库（包含核心记忆、宝藏盒）
- [x] AI引擎核心功能
- [x] 会话管理器
- [x] 侧边栏UI组件
- [x] 环境感知和主动性功能
- [x] 主入口文件重构

### 🚧 待完成的功能
- [ ] 心情调色盘可视化
- [ ] 完整的宝藏盒UI展示
- [ ] 秘密彩蛋功能
- [ ] 更多UI组件的模块化
- [ ] 错误处理和日志系统

## 🎯 下一步计划

1. **Phase 2**: 完善UI组件模块化
2. **Phase 3**: 添加配置管理系统
3. **Phase 4**: 实现插件化架构
4. **Phase 5**: 添加测试覆盖和CI/CD

## 📝 注意事项

1. **兼容性**: 新架构完全兼容原有数据库结构
2. **API密钥**: 仍需在侧边栏输入DeepSeek API密钥
3. **会话持久化**: 支持URL参数的会话管理
4. **原文件保留**: `app.py`保留作为参考，可随时回退

## 🤝 贡献指南

1. 遵循模块化设计原则
2. 保持代码风格一致
3. 添加适当的文档和注释
4. 运行测试确保功能正常

---

**重构完成时间**: 2025-06-22  
**重构版本**: v4.0 - 模块化架构版  
**测试状态**: ✅ 全部通过
