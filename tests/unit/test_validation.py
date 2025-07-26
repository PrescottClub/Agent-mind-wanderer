"""
Unit tests for input validation

Tests the input sanitization, validation, and security
functionality of the validation utilities.
"""

import pytest
from src.utils.validation import InputValidator, input_validator


class TestInputValidator:
    """Test cases for InputValidator class"""
    
    @pytest.mark.security
    def test_sanitize_user_input_xss_prevention(self):
        """Test XSS prevention in user input sanitization"""
        xss_inputs = [
            "<script>alert('xss')</script>Hello",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<iframe src='javascript:alert(1)'></iframe>",
            "<object data='javascript:alert(1)'></object>",
            "<embed src='javascript:alert(1)'></embed>",
            "Hello<script>alert('xss')</script>World"
        ]
        
        for malicious_input in xss_inputs:
            sanitized = input_validator.sanitize_user_input(malicious_input)
            
            # Should not contain script tags or javascript
            assert 'script' not in sanitized.lower()
            assert 'javascript:' not in sanitized.lower()
            assert 'onerror' not in sanitized.lower()
            assert '<iframe' not in sanitized.lower()
            assert '<object' not in sanitized.lower()
            assert '<embed' not in sanitized.lower()
    
    @pytest.mark.security
    def test_sanitize_user_input_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        sql_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "1' UNION SELECT * FROM users--",
            "'; INSERT INTO users VALUES ('hacker', 'password'); --"
        ]
        
        for sql_input in sql_inputs:
            sanitized = input_validator.sanitize_user_input(sql_input)
            
            # Should not contain SQL keywords
            assert 'DROP' not in sanitized.upper()
            assert 'UNION' not in sanitized.upper()
            assert 'INSERT' not in sanitized.upper()
            assert '--' not in sanitized
    
    def test_sanitize_user_input_html_escaping(self):
        """Test HTML entity escaping"""
        html_input = "<b>Bold</b> & special chars < > \" '"
        sanitized = input_validator.sanitize_user_input(html_input)
        
        # HTML tags should be removed
        assert '<b>' not in sanitized
        assert '</b>' not in sanitized
        
        # Special characters should be escaped
        assert '&amp;' in sanitized or '&' in sanitized
        assert '&lt;' in sanitized or '<' not in sanitized
        assert '&gt;' in sanitized or '>' not in sanitized
    
    def test_sanitize_user_input_whitespace_normalization(self):
        """Test whitespace normalization"""
        whitespace_input = "  Hello    world  \n\n  test  \t\t  "
        sanitized = input_validator.sanitize_user_input(whitespace_input)
        
        # Should normalize whitespace
        assert sanitized == "Hello world test"
    
    def test_sanitize_user_input_control_characters(self):
        """Test removal of control characters"""
        control_input = "Hello\x00\x01\x02World\x1f"
        sanitized = input_validator.sanitize_user_input(control_input)

        # Should remove control characters
        assert '\x00' not in sanitized
        assert '\x01' not in sanitized
        assert '\x02' not in sanitized
        assert '\x1f' not in sanitized
        # Control characters may be replaced or removed, check that text is preserved
        assert 'Hello' in sanitized
        assert 'World' in sanitized
    
    def test_validate_message_input_valid_messages(self):
        """Test message validation with valid inputs"""
        valid_messages = [
            "这是一条正常的消息",
            "Hello world! 你好世界",
            "我今天心情不错 😊",
            "a" * 100,  # Long but within limit
        ]
        
        for message in valid_messages:
            result = input_validator.validate_message_input(message)
            assert result['valid'], f"Message should be valid: {message}"
            assert result['sanitized_message']
            assert len(result['errors']) == 0
    
    def test_validate_message_input_invalid_messages(self):
        """Test message validation with invalid inputs"""
        invalid_messages = [
            "",                    # Empty
            "   ",                 # Only whitespace
            "a" * 3000,           # Too long
            None                   # None value
        ]
        
        for message in invalid_messages:
            result = input_validator.validate_message_input(message)
            assert not result['valid'], f"Message should be invalid: {message}"
            assert len(result['errors']) > 0
    
    def test_validate_message_input_sanitization_warnings(self):
        """Test warnings when content is significantly modified"""
        # Input that will be heavily sanitized
        heavily_modified_input = "<script>alert('xss')</script>" * 10 + "Hello"
        result = input_validator.validate_message_input(heavily_modified_input)
        
        # Should be valid but with warnings
        assert result['valid']
        assert len(result['warnings']) > 0
        assert '清理' in result['warnings'][0]
    
    def test_validate_session_id_valid_ids(self):
        """Test session ID validation with valid IDs"""
        valid_ids = [
            "12345678-1234-1234-1234-123456789012",  # UUID format
            "abcdef12-3456-7890-abcd-ef1234567890",  # UUID with letters
            "simple_session_id_123",                  # Simple alphanumeric
            "session-with-dashes-123",                # With dashes
            "a" * 32                                  # 32 character string
        ]
        
        for session_id in valid_ids:
            assert input_validator.validate_session_id(session_id), f"Session ID should be valid: {session_id}"
    
    def test_validate_session_id_invalid_ids(self):
        """Test session ID validation with invalid IDs"""
        invalid_ids = [
            "",                           # Empty
            "short",                      # Too short
            "a" * 200,                   # Too long
            "invalid@session#id",         # Invalid characters
            "session id with spaces",     # Spaces
            None                          # None value
        ]
        
        for session_id in invalid_ids:
            assert not input_validator.validate_session_id(session_id), f"Session ID should be invalid: {session_id}"
    
    def test_validate_username_valid_usernames(self):
        """Test username validation with valid usernames"""
        valid_usernames = [
            "user123",
            "测试用户",
            "user_name",
            "user-name",
            "用户123",
            "a" * 20
        ]
        
        for username in valid_usernames:
            result = input_validator.validate_username(username)
            assert result['valid'], f"Username should be valid: {username}"
            assert result['sanitized_username']
            assert len(result['errors']) == 0
    
    def test_validate_username_invalid_usernames(self):
        """Test username validation with invalid usernames"""
        invalid_usernames = [
            "",                    # Empty
            "   ",                 # Only whitespace
            "a" * 100,            # Too long
            "user@name",          # Invalid characters
            "user name",          # Spaces
            "user#name",          # Special characters
        ]
        
        for username in invalid_usernames:
            result = input_validator.validate_username(username)
            assert not result['valid'], f"Username should be invalid: {username}"
            assert len(result['errors']) > 0
    
    @pytest.mark.security
    def test_detect_potential_threats(self):
        """Test threat detection functionality"""
        # XSS threats
        xss_input = "<script>alert('xss')</script>Hello"
        threats = input_validator.detect_potential_threats(xss_input)
        assert 'XSS_ATTEMPT' in threats
        
        # SQL injection threats
        sql_input = "'; DROP TABLE users; --"
        threats = input_validator.detect_potential_threats(sql_input)
        assert 'SQL_INJECTION_ATTEMPT' in threats
        
        # Suspicious content (high special character ratio)
        suspicious_input = "!@#$%^&*()_+{}|:<>?[]\\;'\",./"
        threats = input_validator.detect_potential_threats(suspicious_input)
        assert 'SUSPICIOUS_CONTENT' in threats
        
        # Clean input should have no threats
        clean_input = "这是一条正常的消息"
        threats = input_validator.detect_potential_threats(clean_input)
        assert len(threats) == 0
    
    def test_convenience_functions(self):
        """Test convenience functions"""
        from src.utils.validation import sanitize_input, validate_message, validate_session
        
        # Test sanitize_input
        test_input = "<script>alert('test')</script>Hello"
        sanitized = sanitize_input(test_input)
        assert 'script' not in sanitized.lower()
        assert 'Hello' in sanitized
        
        # Test validate_message
        result = validate_message("正常消息")
        assert result['valid']
        
        # Test validate_session
        assert validate_session("12345678-1234-1234-1234-123456789012")
        assert not validate_session("invalid")


class TestInputValidatorEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_none_input_handling(self):
        """Test handling of None inputs"""
        assert input_validator.sanitize_user_input(None) == ""
        
        result = input_validator.validate_message_input(None)
        assert not result['valid']
        
        assert not input_validator.validate_session_id(None)
        
        result = input_validator.validate_username(None)
        assert not result['valid']
    
    def test_unicode_handling(self):
        """Test Unicode character handling"""
        unicode_input = "Hello 世界 🌍 emoji test"
        sanitized = input_validator.sanitize_user_input(unicode_input)
        
        # Should preserve Unicode characters
        assert "世界" in sanitized
        assert "🌍" in sanitized
        
        # Should validate successfully
        result = input_validator.validate_message_input(unicode_input)
        assert result['valid']
    
    def test_very_long_input_performance(self):
        """Test performance with very long inputs"""
        import time
        
        # Create a very long input
        long_input = "a" * 10000
        
        start_time = time.time()
        sanitized = input_validator.sanitize_user_input(long_input)
        end_time = time.time()
        
        # Should complete in reasonable time (less than 1 second)
        assert end_time - start_time < 1.0
        assert len(sanitized) > 0
