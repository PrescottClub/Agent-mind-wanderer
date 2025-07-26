"""
Unit tests for chat service

Tests the chat service functionality including message processing,
validation, and AI response handling.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.chat_service import ChatService


class TestChatService:
    """Test cases for ChatService class"""
    
    def test_process_user_message_valid_input(self, chat_service, sample_session_id, sample_user_input):
        """Test processing valid user message"""
        result = chat_service.process_user_message(
            sample_session_id,
            sample_user_input,
            1
        )
        
        assert result['success']
        assert 'parsed_response' in result
        assert 'response_data' in result
        assert 'full_response' in result
        assert 'gift_info' in result
        assert 'exp_result' in result
        assert 'care_tasks' in result
    
    def test_process_user_message_invalid_session_id(self, chat_service, sample_user_input):
        """Test processing message with invalid session ID"""
        invalid_session_ids = [
            "",
            "short",  # Too short (less than 8 chars)
            None,
            "session with spaces",  # Contains spaces
            "session@with#special$chars"  # Contains invalid characters
        ]

        for invalid_id in invalid_session_ids:
            result = chat_service.process_user_message(
                invalid_id,
                sample_user_input,
                1
            )

            assert not result['success']
            assert 'error' in result
            assert '无效的会话ID' in result['error']
    
    @pytest.mark.security
    def test_process_user_message_malicious_input(self, chat_service, sample_session_id, sample_malicious_input):
        """Test processing malicious user input"""
        result = chat_service.process_user_message(
            sample_session_id,
            sample_malicious_input,
            1
        )
        
        # Should either succeed with sanitized input or fail with validation error
        if result['success']:
            # If successful, the input should have been sanitized
            # The AI engine should have received clean input
            chat_service.ai_engine.get_heart_catcher_response.assert_called()
            call_args = chat_service.ai_engine.get_heart_catcher_response.call_args
            sanitized_input = call_args[1]['user_input']
            
            # Sanitized input should not contain script tags
            assert 'script' not in sanitized_input.lower()
        else:
            # If failed, should have validation error
            assert 'error' in result
            assert '输入验证失败' in result['error']
    
    def test_process_user_message_empty_input(self, chat_service, sample_session_id):
        """Test processing empty user input"""
        empty_inputs = ["", "   ", "\n\t  "]
        
        for empty_input in empty_inputs:
            result = chat_service.process_user_message(
                sample_session_id,
                empty_input,
                1
            )
            
            assert not result['success']
            assert 'error' in result
            assert '输入验证失败' in result['error']
    
    def test_process_user_message_too_long_input(self, chat_service, sample_session_id):
        """Test processing overly long user input"""
        long_input = "a" * 3000  # Exceeds MAX_MESSAGE_LENGTH
        
        result = chat_service.process_user_message(
            sample_session_id,
            long_input,
            1
        )
        
        assert not result['success']
        assert 'error' in result
        assert '消息长度不能超过' in result['error']
    
    def test_stream_ai_response_success(self, chat_service, sample_session_id, sample_user_input):
        """Test streaming AI response successfully"""
        # Mock the AI engine to return a proper response
        mock_response = {
            "mood_category": "温暖",
            "sprite_reaction": "测试回应。这是第二句。",
            "gift_type": "元气咒语",
            "gift_content": "测试礼物"
        }
        chat_service.ai_engine.get_heart_catcher_response.return_value = mock_response

        # Collect streamed content
        streamed_content = list(chat_service.stream_ai_response(
            sample_session_id,
            sample_user_input,
            1
        ))

        # Should have content
        assert len(streamed_content) > 0

        # Should contain the response text
        full_content = "".join(streamed_content)
        assert "测试回应" in full_content
    
    def test_stream_ai_response_error_handling(self, chat_service, sample_session_id, sample_user_input):
        """Test streaming AI response with error"""
        # Mock the AI engine to raise an exception
        chat_service.ai_engine.get_heart_catcher_response.side_effect = Exception("AI Error")
        chat_service.ai_engine.get_emotion_enhanced_response.side_effect = Exception("AI Error")

        # Collect streamed content
        streamed_content = list(chat_service.stream_ai_response(
            sample_session_id,
            sample_user_input,
            1
        ))

        # Should have error message
        assert len(streamed_content) > 0
        full_content = "".join(streamed_content)
        assert "技术问题" in full_content or "陪伴你" in full_content
    
    def test_ai_engine_fallback_mechanism(self, chat_service, sample_session_id, sample_user_input):
        """Test AI engine fallback mechanism"""
        # Mock heart catcher to fail, emotion enhanced to succeed
        chat_service.ai_engine.get_heart_catcher_response.return_value = None
        chat_service.ai_engine.get_emotion_enhanced_response.return_value = {
            "mood_category": "关怀",
            "sprite_reaction": "降级回应",
            "gift_type": "安慰话语",
            "gift_content": "测试安慰"
        }
        
        result = chat_service.process_user_message(
            sample_session_id,
            sample_user_input,
            1
        )
        
        assert result['success']
        
        # Should have called both methods
        chat_service.ai_engine.get_heart_catcher_response.assert_called_once()
        chat_service.ai_engine.get_emotion_enhanced_response.assert_called_once()
    
    def test_care_opportunities_processing(self, chat_service, sample_session_id, sample_user_input):
        """Test care opportunities processing"""
        # Mock care opportunities
        mock_care_tasks = [
            {
                'care_type': 'EMOTION_FOLLOWUP',
                'scheduled_time': '2024-01-02 10:00:00',
                'care_message': '测试关怀消息'
            }
        ]
        chat_service.ai_engine.process_care_opportunities.return_value = mock_care_tasks
        
        result = chat_service.process_user_message(
            sample_session_id,
            sample_user_input,
            1
        )
        
        assert result['success']
        assert result['care_tasks'] == mock_care_tasks
        chat_service.ai_engine.process_care_opportunities.assert_called_once()
    
    def test_care_opportunities_error_handling(self, chat_service, sample_session_id, sample_user_input):
        """Test care opportunities error handling"""
        # Mock care opportunities to raise exception
        chat_service.ai_engine.process_care_opportunities.side_effect = Exception("Care error")
        
        result = chat_service.process_user_message(
            sample_session_id,
            sample_user_input,
            1
        )
        
        # Should still succeed but with empty care tasks
        assert result['success']
        assert result['care_tasks'] == []
    
    @patch('src.services.chat_service.st')
    def test_display_ai_response_success(self, mock_st, chat_service):
        """Test displaying AI response successfully"""
        mock_result = {
            'success': True,
            'response_data': {
                'sprite_reaction': '测试回应',
                'memory_association': '测试记忆'
            },
            'parsed_response': {
                'sprite_reaction': '测试回应',
                'memory_association': '测试记忆',
                'emotional_resonance': '测试情感共鸣',
                'is_emergency': False
            },
            'gift_info': {
                'type': '元气咒语',
                'content': '测试礼物'
            },
            'exp_result': {
                'gained_exp': 10,
                'exp_gained': 10,
                'level_up': False,
                'leveled_up': False,
                'current_level': 1,
                'new_level': 1,
                'current_exp': 50,
                'exp_to_next': 100,
                'level_rewards': []
            },
            'care_tasks': []
        }

        # Should not raise any exceptions
        chat_service.display_ai_response(mock_result)
    
    @patch('src.services.chat_service.st')
    def test_display_ai_response_error(self, mock_st, chat_service):
        """Test displaying AI response with error"""
        mock_result = {
            'success': False,
            'error': '测试错误消息'
        }
        
        chat_service.display_ai_response(mock_result)
        
        # Should call st.error
        mock_st.error.assert_called_once_with('测试错误消息')


class TestChatServiceIntegration:
    """Integration tests for chat service"""
    
    @pytest.mark.integration
    def test_complete_chat_flow(self, chat_service, sample_session_id, sample_user_input):
        """Test complete chat processing flow"""
        # Process message
        result = chat_service.process_user_message(
            sample_session_id,
            sample_user_input,
            1
        )
        
        # Verify all components were called
        assert result['success']
        
        # Verify AI engine was called
        chat_service.ai_engine.get_heart_catcher_response.assert_called()
        
        # Verify intimacy service was used (through exp_result)
        assert 'exp_result' in result
        
        # Verify response structure
        assert 'parsed_response' in result
        assert 'response_data' in result
        assert 'full_response' in result
        assert 'gift_info' in result
    
    @pytest.mark.integration
    def test_chat_service_with_real_validation(self, mock_ai_engine, chat_repository, intimacy_service):
        """Test chat service with real validation (not mocked)"""
        # Create chat service with real validation
        chat_service = ChatService(
            ai_engine=mock_ai_engine,
            chat_repo=chat_repository,
            intimacy_service=intimacy_service
        )
        
        # Test with malicious input
        malicious_input = "<script>alert('xss')</script>我需要帮助"
        result = chat_service.process_user_message(
            "12345678-1234-1234-1234-123456789012",
            malicious_input,
            1
        )
        
        # Should succeed with sanitized input
        assert result['success']
        
        # Verify AI engine received sanitized input
        call_args = mock_ai_engine.get_heart_catcher_response.call_args
        sanitized_input = call_args[1]['user_input']
        assert 'script' not in sanitized_input.lower()
        assert '我需要帮助' in sanitized_input
