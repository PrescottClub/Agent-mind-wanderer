# 🔧 Mind Sprite AI Agent 技术指南

## 📋 目录
- [架构概览](#-架构概览)
- [核心模块](#-核心模块)
- [安全系统](#-安全系统)
- [数据库设计](#-数据库设计)
- [API集成](#-api集成)
- [测试框架](#-测试框架)
- [性能优化](#-性能优化)

## 🏗️ 架构概览

### 系统架构图
```
Mind Sprite AI Agent
├── 🎨 UI层 (Streamlit)
│   ├── 聊天界面
│   ├── 配置面板
│   └── 状态显示
├── 🤖 服务层
│   ├── ChatService (聊天服务)
│   ├── EmotionalCompanionService (情感伴侣)
│   ├── IntimacyService (亲密度管理)
│   ├── EnhancedSearchService (搜索服务)
│   └── CareSchedulerService (关怀调度)
├── 🧠 核心层
│   ├── AIEngine (AI引擎)
│   ├── SessionManager (会话管理)
│   └── EmotionAnalyzer (情感分析)
├── 🗄️ 数据层
│   ├── ChatRepository (聊天记录)
│   ├── UserProfileRepository (用户档案)
│   ├── CoreMemoryRepository (核心记忆)
│   └── SearchCacheRepository (搜索缓存)
├── 🛡️ 安全层
│   ├── SecurityManager (安全管理)
│   ├── InputValidator (输入验证)
│   └── EncryptionService (加密服务)
└── ⚙️ 基础设施层
    ├── Database (SQLite)
    ├── Logging (结构化日志)
    └── Configuration (配置管理)
```

### 设计原则
- **模块化**: 清晰的模块分离和职责划分
- **可扩展**: 插件化架构支持功能扩展
- **安全性**: 多层安全防护机制
- **性能**: 缓存和优化策略
- **可测试**: 完整的单元测试覆盖

## 🔧 核心模块

### 1. AI引擎 (AIEngine)
```python
class AIEngine:
    """AI引擎核心类"""
    
    def __init__(self, api_key: str, serp_api_key: str = None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.search_service = EnhancedSearchService(serp_api_key)
    
    def get_heart_catcher_response(self, **kwargs) -> Dict:
        """获取心灵捕手回应"""
        
    def get_emotion_enhanced_response(self, **kwargs) -> Dict:
        """获取情感增强回应"""
```

**特性**:
- 双模式AI回应（心灵捕手 + 情感增强）
- 智能回退机制
- 搜索功能集成
- 错误处理和重试

### 2. 聊天服务 (ChatService)
```python
class ChatService:
    """聊天服务核心类"""
    
    def process_user_message(self, session_id: str, user_input: str, 
                           interaction_count: int) -> Dict:
        """处理用户消息的完整流程"""
        
    def display_ai_response(self, result: Dict):
        """显示AI回应（UI渲染）"""
```

**功能**:
- 输入验证和清理
- AI引擎调用
- 记忆系统集成
- 亲密度管理
- 关怀任务处理

### 3. 情感伴侣服务 (EmotionalCompanionService)
```python
class EmotionalCompanionService:
    """情感陪伴服务"""
    
    def analyze_user_emotional_state(self, user_input: str, 
                                   session_history: List) -> EmotionalState:
        """分析用户情感状态"""
        
    def generate_companion_response(self, emotional_state: EmotionalState, 
                                  intimacy_level: IntimacyLevel) -> str:
        """生成陪伴回应"""
```

**特性**:
- 多维情感分析
- 动态人格调整
- 亲密度感知
- 个性化回应生成

### 4. 搜索服务 (EnhancedSearchService)
```python
class EnhancedSearchService:
    """增强搜索服务"""
    
    def search_local_resources(self, user_input: str, 
                             location: str = "北京") -> Dict:
        """搜索本地心理健康资源"""
        
    def _cached_search_request(self, query: str, location: str) -> Dict:
        """缓存的搜索请求"""
```

**特性**:
- 智能缓存机制
- 速率限制
- 错误处理和重试
- 搜索意图检测

## 🛡️ 安全系统

### 1. 安全管理器 (SecurityManager)
```python
class SecurityManager:
    """安全管理器"""
    
    def encrypt_api_key(self, api_key: str) -> str:
        """加密API密钥"""
        
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """解密API密钥"""
        
    def sanitize_session_data(self, data: Dict) -> Dict:
        """清理会话数据"""
```

**安全特性**:
- AES-256加密
- 安全的密钥管理
- 会话数据清理
- 威胁检测

### 2. 输入验证器 (InputValidator)
```python
class InputValidator:
    """输入验证器"""
    
    @classmethod
    def sanitize_user_input(cls, user_input: str) -> str:
        """清理用户输入"""
        
    @classmethod
    def validate_message_input(cls, message: str) -> Dict[str, Any]:
        """验证消息输入"""
        
    @classmethod
    def detect_potential_threats(cls, text: str) -> List[str]:
        """检测潜在威胁"""
```

**防护机制**:
- XSS防护
- SQL注入防护
- 恶意输入检测
- HTML标签清理

## 🗄️ 数据库设计

### 核心表结构

#### 1. 聊天历史表 (chat_history)
```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    emotion_score REAL,
    intimacy_level INTEGER
);
```

#### 2. 核心记忆表 (core_memories)
```sql
CREATE TABLE core_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    memory_content TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    importance_score REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. 用户档案表 (user_profiles)
```sql
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    current_intimacy_level INTEGER DEFAULT 1,
    total_interactions INTEGER DEFAULT 0,
    total_exp INTEGER DEFAULT 0,
    personality_traits TEXT,
    preferences TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. 搜索缓存表 (search_cache)
```sql
CREATE TABLE search_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key TEXT UNIQUE NOT NULL,
    query TEXT NOT NULL,
    location TEXT NOT NULL,
    results TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL
);
```

### 索引优化
```sql
-- 性能优化索引
CREATE INDEX idx_session_timestamp ON chat_history(session_id, timestamp);
CREATE INDEX idx_core_memories_session_type ON core_memories(session_id, memory_type);
CREATE INDEX idx_search_cache_key_expires ON search_cache(cache_key, expires_at);
```

## 🔌 API集成

### DeepSeek API
```python
# 配置
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 调用示例
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    max_tokens=512,
    temperature=0.5
)
```

### SerpApi 集成
```python
# 搜索请求
search_params = {
    "q": f"{query} {location} 心理健康",
    "location": location,
    "hl": "zh-cn",
    "gl": "cn",
    "api_key": self.api_key,
    "num": 10
}

response = requests.get(
    "https://serpapi.com/search",
    params=search_params,
    timeout=self.request_timeout
)
```

## 🧪 测试框架

### 测试结构
```
tests/
├── unit/                    # 单元测试
│   ├── test_chat_service.py
│   ├── test_security.py
│   ├── test_validation.py
│   └── test_search_service.py
├── integration/             # 集成测试
│   └── test_chat_flow.py
├── fixtures/                # 测试数据
│   └── test_data.py
└── conftest.py             # 测试配置
```

### 测试覆盖
- **单元测试**: 59个测试用例
- **覆盖率**: 核心功能100%覆盖
- **Mock策略**: 外部API和数据库Mock
- **安全测试**: 专门的安全测试套件

### 运行测试
```bash
# 运行所有单元测试
pytest tests/unit/ -v

# 运行特定测试
pytest tests/unit/test_security.py -v

# 生成覆盖率报告
pytest --cov=src tests/unit/
```

## ⚡ 性能优化

### 1. 缓存策略
- **搜索缓存**: 24小时有效期
- **LRU缓存**: 函数级缓存
- **数据库连接池**: 复用连接

### 2. 数据库优化
- **索引优化**: 关键查询字段建索引
- **查询优化**: 避免N+1查询
- **连接管理**: 连接池管理

### 3. 内存管理
- **对象复用**: 避免重复创建
- **垃圾回收**: 及时清理无用对象
- **内存监控**: 监控内存使用情况

### 4. 网络优化
- **请求重试**: 智能重试机制
- **超时控制**: 合理的超时设置
- **速率限制**: 防止API滥用

## 📊 监控和日志

### 日志系统
```python
# 结构化日志
{
    "timestamp": "2025-01-26T10:30:00Z",
    "level": "INFO",
    "logger": "mind_sprite.chat",
    "message": "User interaction completed",
    "session_id": "abc123",
    "performance": {
        "duration_ms": 1500,
        "operation": "process_message"
    }
}
```

### 监控指标
- **响应时间**: API调用和处理时间
- **错误率**: 各类错误的发生频率
- **缓存命中率**: 缓存效果监控
- **用户活跃度**: 交互频率和模式

### 性能监控
```python
@monitor_performance("chat_processing")
def process_user_message(self, session_id: str, user_input: str) -> Dict:
    # 自动记录性能指标
    pass
```

---

*这份技术指南为开发者提供了深入理解和扩展 Mind Sprite AI Agent 的完整信息。*
