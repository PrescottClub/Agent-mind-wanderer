"""
会话管理器
负责会话ID管理和状态初始化
"""

import streamlit as st
import uuid
from datetime import datetime
from typing import Optional
from .security import security_manager
from ..utils.validation import input_validator


class SessionManager:
    """会话管理器类"""
    
    def __init__(self):
        self.session_id = self.get_session_id()
        self.initialize_state()
    
    def get_session_id(self) -> str:
        """获取或生成会话ID"""
        # 首先尝试从URL参数获取
        if 'session_id' in st.query_params:
            session_id = st.query_params['session_id']
            if session_id and input_validator.validate_session_id(session_id):
                return session_id

        # 然后尝试从session state获取
        if hasattr(st.session_state, 'session_id') and st.session_state.session_id:
            if input_validator.validate_session_id(st.session_state.session_id):
                return st.session_state.session_id

        # 最后生成新的会话ID
        new_session_id = str(uuid.uuid4())
        st.session_state.session_id = new_session_id
        st.query_params['session_id'] = new_session_id
        return new_session_id
    
    def initialize_state(self):
        """初始化session state中的各种变量"""
        # 基础状态变量
        if 'session_id' not in st.session_state:
            st.session_state.session_id = self.session_id
        
        if 'current_mood' not in st.session_state:
            st.session_state.current_mood = "平静"
        
        if 'current_reaction' not in st.session_state:
            st.session_state.current_reaction = ""
        
        if 'current_gift' not in st.session_state:
            st.session_state.current_gift = {"type": "", "content": ""}
        
        if 'mood_history' not in st.session_state:
            st.session_state.mood_history = []
        
        # API密钥状态
        if 'deepseek_api_key' not in st.session_state:
            st.session_state.deepseek_api_key = ""
        
        # 主动性相关状态
        if 'proactive_greeting_shown' not in st.session_state:
            st.session_state.proactive_greeting_shown = False
        
        # 宝藏盒相关状态
        if 'treasure_count' not in st.session_state:
            st.session_state.treasure_count = 0

        # 聊天消息状态
        if 'messages' not in st.session_state:
            st.session_state.messages = []
    
    def create_new_session(self) -> str:
        """创建新会话"""
        new_session_id = str(uuid.uuid4())
        st.session_state.session_id = new_session_id
        st.query_params['session_id'] = new_session_id
        
        # 重置状态
        st.session_state.current_mood = "平静"
        st.session_state.current_reaction = ""
        st.session_state.current_gift = {"type": "", "content": ""}
        st.session_state.mood_history = []
        st.session_state.proactive_greeting_shown = False
        st.session_state.treasure_count = 0
        st.session_state.messages = []
        
        return new_session_id
    
    def get_current_session_url(self) -> str:
        """获取当前会话的URL"""
        # 动态获取当前URL，避免硬编码
        try:
            import streamlit.web.server.server as server
            port = server.get_current_server_config().port
            return f"http://localhost:{port}/?session_id={self.session_id}"
        except:
            # 如果无法获取端口，使用默认端口
            return f"http://localhost:8501/?session_id={self.session_id}"
    
    def is_api_key_configured(self) -> bool:
        """检查API密钥是否已配置"""
        # 检查加密的API密钥
        encrypted_key = st.session_state.get('encrypted_deepseek_api_key')
        if encrypted_key:
            decrypted_key = security_manager.decrypt_api_key(encrypted_key)
            return bool(decrypted_key and decrypted_key.strip())

        # 兼容旧版本的明文密钥
        old_key = st.session_state.get('deepseek_api_key')
        return bool(old_key and old_key.strip())
    
    def set_api_key(self, api_key: str) -> bool:
        """设置加密的API密钥"""
        if not api_key or not api_key.strip():
            return False

        # 验证API密钥格式
        if not security_manager.validate_api_key_format(api_key.strip()):
            return False

        # 加密并存储API密钥
        encrypted_key = security_manager.encrypt_api_key(api_key.strip())
        if encrypted_key:
            st.session_state.encrypted_deepseek_api_key = encrypted_key
            # 清除旧的明文密钥（如果存在）
            if 'deepseek_api_key' in st.session_state:
                del st.session_state.deepseek_api_key
            return True
        return False

    def get_api_key(self) -> Optional[str]:
        """获取解密的API密钥"""
        encrypted_key = st.session_state.get('encrypted_deepseek_api_key')
        if encrypted_key:
            return security_manager.decrypt_api_key(encrypted_key)

        # 兼容旧版本的明文密钥
        old_key = st.session_state.get('deepseek_api_key')
        if old_key:
            # 迁移到加密存储
            if self.set_api_key(old_key):
                del st.session_state.deepseek_api_key
                return old_key

        return None
