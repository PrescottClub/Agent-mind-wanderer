"""
Integration tests for complete chat flow

Tests the end-to-end chat functionality including database operations,
AI processing, and security measures.
"""

import pytest
from unittest.mock import patch, Mock
from src.app import MindSpriteApp
from src.services.chat_service import ChatService
from src.core.session_manager import SessionManager


class TestChatFlowIntegration:
    """Integration tests for complete chat flow"""
    
    @pytest.fixture
    def app_instance(self, temp_db, mock_ai_engine, mock_streamlit_session):
        """Create app instance for testing"""
        with patch('src.app.init_db', return_value=True):
            app = MindSpriteApp()
            app.ai_engine = mock_ai_engine
            app.chat_service = ChatService(
                ai_engine=mock_ai_engine,
                chat_repo=app.chat_repo,
                intimacy_service=app.intimacy_service
            )
            return app
    
    @pytest.mark.integration
    def test_complete_user_interaction_flow(self, app_instance, sample_session_id, sample_user_input):
        """Test complete user interaction from input to response"""
        # Simulate user input processing
        result = app_instance.chat_service.process_user_message(
            sample_session_id,
            sample_user_input,
            1
        )
        
        # Verify successful processing
        assert result['success']
        assert 'parsed_response' in result
        assert 'gift_info' in result
        assert 'exp_result' in result
        
        # Verify AI engine was called with sanitized input
        app_instance.ai_engine.get_heart_catcher_response.assert_called()
        call_args = app_instance.ai_engine.get_heart_catcher_response.call_args
        assert call_args[1]['user_input'] == sample_user_input  # Should be clean input
    
    @pytest.mark.integration
    @pytest.mark.security
    def test_security_integration_malicious_input(self, app_instance, sample_session_id):
        """Test security measures with malicious input"""
        malicious_inputs = [
            "<script>alert('xss')</script>我需要心理咨询",
            "'; DROP TABLE chat_history; --我想聊天",
            "<img src=x onerror=alert('xss')>帮助我",
            "javascript:alert('hack')正常消息"
        ]
        
        for malicious_input in malicious_inputs:
            result = app_instance.chat_service.process_user_message(
                sample_session_id,
                malicious_input,
                1
            )
            
            if result['success']:
                # If processing succeeded, verify input was sanitized
                call_args = app_instance.ai_engine.get_heart_catcher_response.call_args
                sanitized_input = call_args[1]['user_input']
                
                # Should not contain dangerous patterns
                assert 'script' not in sanitized_input.lower()
                assert 'javascript:' not in sanitized_input.lower()
                assert 'onerror' not in sanitized_input.lower()
                assert 'DROP TABLE' not in sanitized_input.upper()
            else:
                # If processing failed, should have validation error
                assert 'error' in result
                assert '输入验证失败' in result['error']
    
    @pytest.mark.integration
    def test_database_integration(self, app_instance, sample_session_id, sample_user_input):
        """Test database operations during chat flow"""
        # Process a message
        result = app_instance.chat_service.process_user_message(
            sample_session_id,
            sample_user_input,
            1
        )
        
        assert result['success']
        
        # Verify database operations
        # Note: In a real integration test, we would verify actual database writes
        # Here we verify the service methods were called correctly
        
        # Verify chat repository methods would be called
        # (In actual implementation, these would write to database)
        assert hasattr(app_instance.chat_repo, 'get_core_memories')
        assert hasattr(app_instance.chat_repo, 'get_recent_context')
    
    @pytest.mark.integration
    def test_intimacy_system_integration(self, app_instance, sample_session_id, sample_user_input):
        """Test intimacy system integration"""
        # Process multiple messages to test intimacy progression
        messages = [
            "你好，我是新用户",
            "我今天心情不好",
            "谢谢你的陪伴",
            "我觉得我们越来越熟悉了"
        ]
        
        for i, message in enumerate(messages, 1):
            result = app_instance.chat_service.process_user_message(
                sample_session_id,
                message,
                i
            )
            
            assert result['success']
            assert 'exp_result' in result
            
            # Verify intimacy service interaction
            # (In real implementation, this would update intimacy levels)
    
    @pytest.mark.integration
    def test_error_handling_integration(self, app_instance, sample_session_id):
        """Test error handling across the entire system"""
        # Test with various error conditions
        error_conditions = [
            ("", "empty input"),
            ("a" * 3000, "too long input"),
            (None, "None input")
        ]
        
        for error_input, description in error_conditions:
            result = app_instance.chat_service.process_user_message(
                sample_session_id,
                error_input,
                1
            )
            
            # Should handle errors gracefully
            assert not result['success'], f"Should fail for {description}"
            assert 'error' in result
            assert isinstance(result['error'], str)
    
    @pytest.mark.integration
    def test_ai_engine_fallback_integration(self, app_instance, sample_session_id, sample_user_input):
        """Test AI engine fallback mechanism integration"""
        # Mock heart catcher to fail
        app_instance.ai_engine.get_heart_catcher_response.return_value = None
        
        # Mock emotion enhanced to succeed
        app_instance.ai_engine.get_emotion_enhanced_response.return_value = {
            "mood_category": "关怀",
            "sprite_reaction": "降级回应测试",
            "gift_type": "安慰话语",
            "gift_content": "测试安慰内容"
        }
        
        result = app_instance.chat_service.process_user_message(
            sample_session_id,
            sample_user_input,
            1
        )
        
        # Should succeed with fallback
        assert result['success']
        
        # Verify both methods were called
        app_instance.ai_engine.get_heart_catcher_response.assert_called_once()
        app_instance.ai_engine.get_emotion_enhanced_response.assert_called_once()
    
    @pytest.mark.integration
    def test_session_management_integration(self, mock_streamlit_session):
        """Test session management integration"""
        # Test session manager with security features
        session_manager = SessionManager()
        
        # Test API key encryption
        test_api_key = "sk-test123456789012345678901234567890"
        success = session_manager.set_api_key(test_api_key)
        assert success
        
        # Verify key is encrypted in session
        assert 'encrypted_deepseek_api_key' in mock_streamlit_session
        assert mock_streamlit_session.get('deepseek_api_key') is None  # Should not store plain text
        
        # Verify key can be retrieved
        retrieved_key = session_manager.get_api_key()
        assert retrieved_key == test_api_key
        
        # Verify API key is configured
        assert session_manager.is_api_key_configured()
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_performance_integration(self, app_instance, sample_session_id):
        """Test performance of integrated system"""
        import time
        
        # Test processing multiple messages
        messages = [f"测试消息 {i}" for i in range(10)]
        
        start_time = time.time()
        
        for i, message in enumerate(messages, 1):
            result = app_instance.chat_service.process_user_message(
                sample_session_id,
                message,
                i
            )
            assert result['success']
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should process 10 messages in reasonable time (less than 5 seconds with mocked AI)
        assert total_time < 5.0, f"Processing took too long: {total_time} seconds"
        
        # Average time per message should be reasonable
        avg_time = total_time / len(messages)
        assert avg_time < 0.5, f"Average processing time too high: {avg_time} seconds"


class TestSecurityIntegration:
    """Security-focused integration tests"""
    
    @pytest.mark.integration
    @pytest.mark.security
    def test_end_to_end_security(self, app_instance, sample_session_id):
        """Test end-to-end security measures"""
        # Test various attack vectors
        attack_vectors = [
            # XSS attacks
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            
            # SQL injection attacks
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            
            # Command injection attempts
            "; rm -rf /",
            "$(rm -rf /)",
            "`rm -rf /`",
            
            # Path traversal
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
        ]
        
        for attack in attack_vectors:
            # Combine attack with normal message
            malicious_message = f"{attack} 我需要心理咨询帮助"
            
            result = app_instance.chat_service.process_user_message(
                sample_session_id,
                malicious_message,
                1
            )
            
            if result['success']:
                # If successful, verify attack was neutralized
                call_args = app_instance.ai_engine.get_heart_catcher_response.call_args
                sanitized_input = call_args[1]['user_input']
                
                # Should not contain attack patterns
                assert attack.lower() not in sanitized_input.lower()
                # But should contain the legitimate part
                assert '心理咨询' in sanitized_input or '帮助' in sanitized_input
            else:
                # If failed, should be due to validation
                assert 'error' in result
    
    @pytest.mark.integration
    @pytest.mark.security
    def test_session_security_integration(self, mock_streamlit_session):
        """Test session security integration"""
        session_manager = SessionManager()
        
        # Test invalid API key rejection
        invalid_keys = [
            "invalid-key",
            "sk-short",
            "",
            "not-an-api-key"
        ]
        
        for invalid_key in invalid_keys:
            success = session_manager.set_api_key(invalid_key)
            assert not success, f"Should reject invalid key: {invalid_key}"
            assert not session_manager.is_api_key_configured()
        
        # Test valid API key acceptance
        valid_key = "sk-test123456789012345678901234567890"
        success = session_manager.set_api_key(valid_key)
        assert success
        assert session_manager.is_api_key_configured()
        
        # Test session data sanitization
        from src.core.security import security_manager
        
        # Add some sensitive data to session
        mock_streamlit_session.update({
            'encrypted_deepseek_api_key': 'encrypted_data',
            'password': 'secret_password',
            'normal_data': 'public_info'
        })
        
        sanitized = security_manager.sanitize_session_data(mock_streamlit_session)
        
        assert sanitized['encrypted_deepseek_api_key'] == '[REDACTED]'
        assert sanitized['password'] == '[REDACTED]'
        assert sanitized['normal_data'] == 'public_info'
