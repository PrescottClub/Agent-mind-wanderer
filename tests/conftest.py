"""
Pytest configuration and shared fixtures

This module provides common test fixtures and configuration
for the Mind Sprite AI Agent test suite.
"""

import pytest
import tempfile
import os
import sqlite3
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import streamlit as st

# Add src to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.core.ai_engine import AIEngine
from src.core.session_manager import SessionManager
from src.core.security import SecurityManager
from src.data.database import init_db
from src.services.emotional_companion_service import EmotionalCompanionService
from src.services.chat_service import ChatService
from src.data.repositories.chat_repository import ChatRepository
from src.services.intimacy_service import IntimacyService


@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    # Patch the database connection to use temp database
    original_db_path = 'mind_sprite.db'
    
    def mock_get_connection():
        return sqlite3.connect(db_path)
    
    with patch('src.data.database.get_db_connection', side_effect=mock_get_connection):
        # Initialize the temporary database
        init_db()
        yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def mock_streamlit_session():
    """Mock Streamlit session state"""
    mock_session = {}
    with patch.object(st, 'session_state', mock_session):
        yield mock_session


@pytest.fixture
def mock_ai_engine():
    """Mock AI engine for testing"""
    engine = Mock(spec=AIEngine)
    
    # Mock standard response
    engine.get_enhanced_response.return_value = {
        "mood_category": "温暖",
        "memory_association": "测试记忆联想",
        "sprite_reaction": "测试回应内容",
        "emotional_resonance": "测试情感共鸣",
        "gift_type": "元气咒语",
        "gift_content": "✨ 测试礼物内容 ✨"
    }
    
    # Mock heart catcher response
    engine.get_heart_catcher_response.return_value = {
        "mood_category": "温暖",
        "sprite_reaction": "心灵捕手测试回应",
        "gift_type": "温暖拥抱",
        "gift_content": "🤗 测试拥抱"
    }
    
    # Mock emotion enhanced response
    engine.get_emotion_enhanced_response.return_value = {
        "mood_category": "关怀",
        "sprite_reaction": "情感增强测试回应",
        "gift_type": "安慰话语",
        "gift_content": "💝 测试安慰"
    }
    
    # Mock care opportunities
    engine.process_care_opportunities.return_value = []
    
    return engine


@pytest.fixture
def sample_session_id():
    """Sample session ID for testing"""
    return "12345678-1234-1234-1234-123456789012"


@pytest.fixture
def sample_user_input():
    """Sample user input for testing"""
    return "我今天心情不太好，感觉很累"


@pytest.fixture
def sample_malicious_input():
    """Sample malicious input for security testing"""
    return "<script>alert('xss')</script>我想要心理咨询"


@pytest.fixture
def emotional_companion_service():
    """Emotional companion service instance"""
    return EmotionalCompanionService()


@pytest.fixture
def security_manager():
    """Security manager instance"""
    return SecurityManager()


@pytest.fixture
def session_manager(mock_streamlit_session):
    """Session manager instance with mocked Streamlit"""
    return SessionManager()


@pytest.fixture
def chat_repository(temp_db):
    """Chat repository with temporary database"""
    return ChatRepository()


@pytest.fixture
def intimacy_service(temp_db):
    """Intimacy service with temporary database"""
    from src.data.repositories.user_profile_repository import UserProfileRepository
    user_profile_repo = UserProfileRepository()
    return IntimacyService(user_profile_repo)


@pytest.fixture
def chat_service(mock_ai_engine, chat_repository, intimacy_service):
    """Chat service with mocked dependencies"""
    return ChatService(
        ai_engine=mock_ai_engine,
        chat_repo=chat_repository,
        intimacy_service=intimacy_service
    )


@pytest.fixture
def sample_chat_history():
    """Sample chat history for testing"""
    return [
        ("user", "你好"),
        ("assistant", "你好！我是小念，很高兴见到你~"),
        ("user", "我今天心情不好"),
        ("assistant", "听起来你今天遇到了一些困难，小念在这里陪伴你~")
    ]


@pytest.fixture
def sample_core_memories():
    """Sample core memories for testing"""
    return [
        ("insight", "用户喜欢在晚上聊天", "2024-01-01 20:00:00"),
        ("preference", "用户偏好温暖的回应风格", "2024-01-02 19:30:00"),
        ("event", "用户提到工作压力大", "2024-01-03 21:15:00")
    ]


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "security: mark test as security related"
    )
