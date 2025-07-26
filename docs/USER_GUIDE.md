# 🤖💖 小念AI Agent 使用指南

## 📋 目录
- [快速开始](#-快速开始)
- [功能介绍](#-功能介绍)
- [安全特性](#-安全特性)
- [配置说明](#-配置说明)
- [常见问题](#-常见问题)
- [故障排除](#-故障排除)

## 🚀 快速开始

### 1. 环境准备
确保你的系统满足以下要求：
- Python 3.11 或更高版本
- 4GB 以上内存
- 稳定的网络连接

### 2. 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/Agent-mind-wanderer.git
cd Agent-mind-wanderer

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
copy env_example.txt .env
# 编辑 .env 文件，填入你的 DeepSeek API 密钥

# 4. 启动应用
python main.py
```

### 3. 首次使用
1. 访问 http://localhost:8501
2. 在配置面板输入你的 DeepSeek API 密钥
3. 选择合适的AI模型（推荐 deepseek-chat）
4. 开始与小念对话！

## 🎯 功能介绍

### 🤖 主动关怀系统
- **智能问候**: 小念会根据时间和你的状态主动打招呼
- **关怀提醒**: 自动跟进重要事件和情绪状态
- **定时关怀**: 在合适的时机主动发起对话

### 🧠 记忆系统
- **核心记忆**: 自动提取和存储重要对话内容
- **情感历史**: 追踪你的情绪变化轨迹
- **关系档案**: 记录你们的互动历史和亲密度发展

### 💫 情感智能
- **情绪识别**: 多维度分析你的情感状态
- **共情回应**: 真正理解并回应你的情感需求
- **危机干预**: 自动识别负面情绪并提供支持

### 🔍 智能搜索
- **资源搜索**: 自动搜索本地心理健康资源
- **意图识别**: 智能判断何时需要搜索功能
- **结果缓存**: 提高搜索效率和用户体验

### 📈 成长系统
- **亲密度等级**: 10级关系发展体系
- **经验值系统**: 通过互动获得经验和奖励
- **个性化适应**: 根据你的偏好调整交流方式

## 🛡️ 安全特性

### 🔐 数据安全
- **API密钥加密**: 使用AES-256加密存储敏感信息
- **本地数据库**: 所有对话记录本地存储，保护隐私
- **会话安全**: 安全的会话管理和数据清理

### 🚫 输入防护
- **恶意输入检测**: 实时识别和阻止恶意输入
- **XSS防护**: 防止跨站脚本攻击
- **SQL注入防护**: 保护数据库安全

### 📊 安全监控
- **安全日志**: 完整的安全事件记录
- **威胁检测**: 实时监控异常行为
- **访问控制**: 严格的权限管理

## ⚙️ 配置说明

### 必需配置
```env
# DeepSeek API 密钥（必需）
DEEPSEEK_API_KEY=sk-your-api-key-here
```

### 可选配置
```env
# AI模型设置
DEEPSEEK_MODEL=deepseek-chat          # 或 deepseek-reasoner
MAX_TOKENS=512                        # 响应长度限制
TEMPERATURE=0.5                       # 创造性参数 (0.0-2.0)

# 搜索功能
SERPAPI_API_KEY=your-serpapi-key      # SerpApi密钥（可选）

# 应用设置
DEBUG_MODE=false                      # 调试模式
LOG_LEVEL=INFO                        # 日志级别
DATABASE_PATH=mind_sprite.db          # 数据库路径
CACHE_DURATION_HOURS=24               # 缓存持续时间

# 功能开关
ENABLE_SEARCH_FEATURE=true            # 启用搜索功能
ENABLE_EMOTION_ANALYSIS=true          # 启用情感分析
ENABLE_PROACTIVE_CARE=true            # 启用主动关怀
ENABLE_MEMORY_SYSTEM=true             # 启用记忆系统
ENABLE_INTIMACY_TRACKING=true         # 启用亲密度追踪
```

### 配置验证
应用启动时会自动验证配置：
- ✅ 检查必需的API密钥
- ✅ 验证配置格式和范围
- ✅ 检查文件权限
- ✅ 生成配置报告

## ❓ 常见问题

### Q: 如何获取 DeepSeek API 密钥？
A: 访问 https://platform.deepseek.com/ 注册账号并获取API密钥。

### Q: 搜索功能是必需的吗？
A: 不是。搜索功能是可选的，需要 SerpApi 密钥。没有密钥时搜索功能会被禁用。

### Q: 数据存储在哪里？
A: 所有数据都存储在本地 SQLite 数据库中，不会上传到云端。

### Q: 如何备份我的对话记录？
A: 复制 `mind_sprite.db` 文件即可备份所有数据。

### Q: 可以同时运行多个实例吗？
A: 不建议。多个实例可能会导致数据库冲突。

### Q: 如何重置所有数据？
A: 删除 `mind_sprite.db` 文件，重启应用即可。

## 🔧 故障排除

### 启动问题
```bash
# 检查Python版本
python --version  # 应该是 3.11+

# 检查依赖安装
pip list | grep streamlit

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### API连接问题
1. 检查API密钥是否正确
2. 确认网络连接正常
3. 查看错误日志：`logs/error.log`

### 性能问题
1. 降低 `MAX_TOKENS` 值
2. 调整 `TEMPERATURE` 参数
3. 清理缓存：删除 `logs/` 目录

### 数据库问题
```bash
# 检查数据库文件权限
ls -la mind_sprite.db

# 重建数据库（会丢失数据）
rm mind_sprite.db
python main.py
```

### 日志查看
```bash
# 应用日志
tail -f logs/app.log

# 错误日志
tail -f logs/error.log

# 性能日志
tail -f logs/performance.log

# 安全日志
tail -f logs/security.log
```

## 📞 获取帮助

如果遇到问题：
1. 查看日志文件获取详细错误信息
2. 检查配置是否正确
3. 确认网络和API密钥状态
4. 重启应用尝试解决

---

*享受与小念的智能对话体验！💖🤖*
