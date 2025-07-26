"""
Unit tests for security utilities

Tests the encryption, decryption, and validation functionality
of the security manager.
"""

import pytest
from unittest.mock import patch, Mock
from src.core.security import SecurityManager, security_manager


class TestSecurityManager:
    """Test cases for SecurityManager class"""
    
    def test_api_key_encryption_decryption(self, security_manager):
        """Test API key encryption and decryption"""
        test_key = "sk-test123456789012345678901234567890abcdef"
        
        # Test encryption
        encrypted = security_manager.encrypt_api_key(test_key)
        assert encrypted != test_key
        assert len(encrypted) > 0
        assert isinstance(encrypted, str)
        
        # Test decryption
        decrypted = security_manager.decrypt_api_key(encrypted)
        assert decrypted == test_key
    
    def test_api_key_validation_valid_keys(self, security_manager):
        """Test API key format validation with valid keys"""
        valid_keys = [
            "sk-test123456789012345678901234567890abcdef",  # 43 chars total
            "sk-abcdefghijklmnopqrstuvwxyz1234567890abcdef",  # 47 chars total
            "sk-" + "a" * 40  # 43 chars total
        ]
        
        for key in valid_keys:
            assert security_manager.validate_api_key_format(key), f"Key should be valid: {key}"
    
    def test_api_key_validation_invalid_keys(self, security_manager):
        """Test API key format validation with invalid keys"""
        invalid_keys = [
            "",                           # Empty
            "invalid",                    # No sk- prefix
            "sk-short",                   # Too short
            "sk-",                        # Just prefix
            "not-sk-prefix123456789012345678901234567890",  # Wrong prefix
            None                          # None value
        ]
        
        for key in invalid_keys:
            assert not security_manager.validate_api_key_format(key), f"Key should be invalid: {key}"
    
    def test_empty_key_handling(self, security_manager):
        """Test handling of empty API keys"""
        # Test empty string encryption
        encrypted = security_manager.encrypt_api_key("")
        assert encrypted == ""
        
        # Test empty string decryption
        decrypted = security_manager.decrypt_api_key("")
        assert decrypted == ""
        
        # Test None handling
        encrypted_none = security_manager.encrypt_api_key(None)
        assert encrypted_none == ""
    
    def test_encryption_error_handling(self, security_manager):
        """Test encryption error handling"""
        # Test with invalid input types
        with patch.object(security_manager._cipher, 'encrypt', side_effect=Exception("Encryption error")):
            result = security_manager.encrypt_api_key("test-key")
            assert result == ""
    
    def test_decryption_error_handling(self, security_manager):
        """Test decryption error handling"""
        # Test with invalid encrypted data
        invalid_encrypted = "invalid-base64-data"
        result = security_manager.decrypt_api_key(invalid_encrypted)
        assert result == ""
        
        # Test with corrupted data
        with patch.object(security_manager._cipher, 'decrypt', side_effect=Exception("Decryption error")):
            result = security_manager.decrypt_api_key("dGVzdA==")  # Valid base64 but will fail decryption
            assert result == ""
    
    def test_secure_session_id_generation(self, security_manager):
        """Test secure session ID generation"""
        session_id = security_manager.generate_secure_session_id()
        
        assert isinstance(session_id, str)
        assert len(session_id) == 32
        assert session_id.isalnum()  # Should be alphanumeric
        
        # Test uniqueness
        session_id2 = security_manager.generate_secure_session_id()
        assert session_id != session_id2
    
    def test_session_data_sanitization(self, security_manager):
        """Test session data sanitization"""
        sensitive_data = {
            'deepseek_api_key': 'sk-secret123',
            'encrypted_deepseek_api_key': 'encrypted_secret',
            'serpapi_key': 'serp_secret',
            'password': 'user_password',
            'token': 'auth_token',
            'normal_data': 'public_info',
            'user_name': 'test_user'
        }
        
        sanitized = security_manager.sanitize_session_data(sensitive_data)
        
        # Check sensitive data is redacted
        assert sanitized['deepseek_api_key'] == '[REDACTED]'
        assert sanitized['encrypted_deepseek_api_key'] == '[REDACTED]'
        assert sanitized['serpapi_key'] == '[REDACTED]'
        assert sanitized['password'] == '[REDACTED]'
        assert sanitized['token'] == '[REDACTED]'
        
        # Check normal data is preserved
        assert sanitized['normal_data'] == 'public_info'
        assert sanitized['user_name'] == 'test_user'
    
    @pytest.mark.security
    def test_encryption_strength(self, security_manager):
        """Test encryption strength and randomness"""
        test_key = "sk-test123456789012345678901234567890"
        
        # Encrypt the same key multiple times
        encrypted1 = security_manager.encrypt_api_key(test_key)
        encrypted2 = security_manager.encrypt_api_key(test_key)
        
        # Results should be different due to random IV/nonce
        assert encrypted1 != encrypted2
        
        # But both should decrypt to the same value
        decrypted1 = security_manager.decrypt_api_key(encrypted1)
        decrypted2 = security_manager.decrypt_api_key(encrypted2)
        
        assert decrypted1 == test_key
        assert decrypted2 == test_key
    
    def test_convenience_functions(self):
        """Test convenience functions"""
        from src.core.security import encrypt_sensitive_data, decrypt_sensitive_data, validate_api_key
        
        test_data = "sensitive_information"
        
        # Test encryption/decryption convenience functions
        encrypted = encrypt_sensitive_data(test_data)
        decrypted = decrypt_sensitive_data(encrypted)
        assert decrypted == test_data
        
        # Test validation convenience function
        assert validate_api_key("sk-test123456789012345678901234567890abcdef")
        assert not validate_api_key("invalid-key")


class TestSecurityIntegration:
    """Integration tests for security functionality"""
    
    @pytest.mark.integration
    def test_security_manager_singleton(self):
        """Test that security manager works as expected"""
        from src.core.security import security_manager as sm1
        from src.core.security import security_manager as sm2
        
        # Should be the same instance
        assert sm1 is sm2
        
        # Should work consistently
        test_key = "sk-test123456789012345678901234567890"
        encrypted1 = sm1.encrypt_api_key(test_key)
        decrypted2 = sm2.decrypt_api_key(encrypted1)
        
        assert decrypted2 == test_key
