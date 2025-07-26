"""
Security utilities for API key encryption and sensitive data handling

This module provides encryption/decryption capabilities for sensitive data
like API keys, ensuring they are not stored in plain text in session state.
"""

import base64
import os
from cryptography.fernet import Fernet
from typing import Optional
import streamlit as st
import secrets
import hashlib


class SecurityManager:
    """Handles encryption/decryption of sensitive data"""
    
    def __init__(self):
        self._key = self._get_or_create_key()
        self._cipher = Fernet(self._key)
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        key_env = os.getenv('ENCRYPTION_KEY')
        if key_env:
            try:
                return base64.urlsafe_b64decode(key_env.encode())
            except Exception:
                pass
        
        # Generate new key for session (not persistent across restarts)
        # In production, this should be stored securely
        key = Fernet.generate_key()
        return key
    
    def encrypt_api_key(self, api_key: str) -> str:
        """
        Encrypt API key for storage
        
        Args:
            api_key (str): Plain text API key
            
        Returns:
            str: Encrypted API key as base64 string
        """
        if not api_key:
            return ""
        
        try:
            encrypted_bytes = self._cipher.encrypt(api_key.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
        except Exception as e:
            st.error(f"加密失败: {e}")
            return ""
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """
        Decrypt API key for use
        
        Args:
            encrypted_key (str): Encrypted API key as base64 string
            
        Returns:
            str: Decrypted API key
        """
        if not encrypted_key:
            return ""
        
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_key.encode('utf-8'))
            decrypted_bytes = self._cipher.decrypt(encrypted_bytes)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            st.error(f"解密失败: {e}")
            return ""
    
    def validate_api_key_format(self, api_key: str) -> bool:
        """
        Validate API key format
        
        Args:
            api_key (str): API key to validate
            
        Returns:
            bool: True if format is valid
        """
        if not api_key or len(api_key) < 20:
            return False
        
        # DeepSeek API keys start with 'sk-' and are at least 40 characters
        if api_key.startswith('sk-') and len(api_key) >= 40:
            return True
        
        return False
    
    def generate_secure_session_id(self) -> str:
        """
        Generate a cryptographically secure session ID
        
        Returns:
            str: Secure session ID
        """
        # Generate 32 random bytes and hash them
        random_bytes = secrets.token_bytes(32)
        session_hash = hashlib.sha256(random_bytes).hexdigest()
        return session_hash[:32]  # Use first 32 characters
    
    def sanitize_session_data(self, data: dict) -> dict:
        """
        Sanitize session data to remove sensitive information
        
        Args:
            data (dict): Session data to sanitize
            
        Returns:
            dict: Sanitized session data
        """
        sensitive_keys = [
            'deepseek_api_key', 'encrypted_deepseek_api_key',
            'serpapi_key', 'password', 'token'
        ]
        
        sanitized = {}
        for key, value in data.items():
            if any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value
        
        return sanitized


# Global security manager instance
security_manager = SecurityManager()


def encrypt_sensitive_data(data: str) -> str:
    """Convenience function to encrypt sensitive data"""
    return security_manager.encrypt_api_key(data)


def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Convenience function to decrypt sensitive data"""
    return security_manager.decrypt_api_key(encrypted_data)


def validate_api_key(api_key: str) -> bool:
    """Convenience function to validate API key format"""
    return security_manager.validate_api_key_format(api_key)
