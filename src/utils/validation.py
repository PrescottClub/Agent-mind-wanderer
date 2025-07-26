"""
Input validation and sanitization utilities

This module provides comprehensive input validation and sanitization
to prevent XSS attacks, SQL injection, and other security vulnerabilities.
"""

import re
import html
from typing import Optional, Dict, Any, List
import bleach
import uuid


class InputValidator:
    """Handles input validation and sanitization"""
    
    # Maximum lengths for different input types
    MAX_MESSAGE_LENGTH = 2000
    MAX_SESSION_ID_LENGTH = 100
    MAX_USERNAME_LENGTH = 50
    
    # Allowed HTML tags for rich text (none for security)
    ALLOWED_TAGS = []
    ALLOWED_ATTRIBUTES = {}
    
    # Dangerous patterns to detect
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',                # JavaScript URLs
        r'on\w+\s*=',                 # Event handlers
        r'data:text/html',            # Data URLs
        r'vbscript:',                 # VBScript URLs
        r'<iframe[^>]*>.*?</iframe>', # Iframe tags
        r'<object[^>]*>.*?</object>', # Object tags
        r'<embed[^>]*>.*?</embed>',   # Embed tags
    ]
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)',
        r'(--|#|/\*|\*/)',
        r'(\bOR\b.*=.*\bOR\b)',
        r'(\bAND\b.*=.*\bAND\b)',
        r'(\'.*\bOR\b.*\')',
        r'(\".*\bOR\b.*\")',
    ]
    
    @classmethod
    def sanitize_user_input(cls, text: str) -> str:
        """
        Sanitize user input text
        
        Args:
            text (str): Raw user input
            
        Returns:
            str: Sanitized text safe for processing
        """
        if not text:
            return ""
        
        # Remove HTML tags and entities
        text = bleach.clean(
            text, 
            tags=cls.ALLOWED_TAGS, 
            attributes=cls.ALLOWED_ATTRIBUTES,
            strip=True
        )
        
        # Escape HTML entities
        text = html.escape(text)
        
        # Remove dangerous patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Check for SQL injection patterns
        for pattern in cls.SQL_INJECTION_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove null bytes and control characters
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        
        return text
    
    @classmethod
    def validate_message_input(cls, message: str) -> Dict[str, Any]:
        """
        Validate chat message input
        
        Args:
            message (str): User message to validate
            
        Returns:
            Dict containing validation results
        """
        result = {
            'valid': True,
            'sanitized_message': '',
            'errors': [],
            'warnings': []
        }
        
        if not message or not message.strip():
            result['valid'] = False
            result['errors'].append('消息不能为空')
            return result
        
        if len(message) > cls.MAX_MESSAGE_LENGTH:
            result['valid'] = False
            result['errors'].append(f'消息长度不能超过{cls.MAX_MESSAGE_LENGTH}字符')
            return result
        
        # Sanitize the message
        original_length = len(message)
        result['sanitized_message'] = cls.sanitize_user_input(message)
        sanitized_length = len(result['sanitized_message'])
        
        # Check if sanitization removed too much content
        if sanitized_length < original_length * 0.3:
            result['valid'] = False
            result['errors'].append('消息包含过多不安全内容')
            return result
        
        # Warning if content was significantly modified
        if sanitized_length < original_length * 0.8:
            result['warnings'].append('消息内容已被清理以确保安全')
        
        return result
    
    @classmethod
    def validate_session_id(cls, session_id: str) -> bool:
        """
        Validate session ID format
        
        Args:
            session_id (str): Session ID to validate
            
        Returns:
            bool: True if valid UUID format
        """
        if not session_id:
            return False
        
        if len(session_id) > cls.MAX_SESSION_ID_LENGTH:
            return False
        
        # Try to parse as UUID
        try:
            uuid.UUID(session_id)
            return True
        except ValueError:
            # Also accept simple alphanumeric session IDs
            if re.match(r'^[a-zA-Z0-9_-]{8,64}$', session_id):
                return True
            return False
    
    @classmethod
    def validate_username(cls, username: str) -> Dict[str, Any]:
        """
        Validate username input
        
        Args:
            username (str): Username to validate
            
        Returns:
            Dict containing validation results
        """
        result = {
            'valid': True,
            'sanitized_username': '',
            'errors': []
        }
        
        if not username or not username.strip():
            result['valid'] = False
            result['errors'].append('用户名不能为空')
            return result
        
        if len(username) > cls.MAX_USERNAME_LENGTH:
            result['valid'] = False
            result['errors'].append(f'用户名长度不能超过{cls.MAX_USERNAME_LENGTH}字符')
            return result
        
        # Username should only contain safe characters
        if not re.match(r'^[a-zA-Z0-9\u4e00-\u9fff_-]+$', username):
            result['valid'] = False
            result['errors'].append('用户名只能包含字母、数字、中文、下划线和连字符')
            return result
        
        result['sanitized_username'] = cls.sanitize_user_input(username)
        return result
    
    @classmethod
    def detect_potential_threats(cls, text: str) -> List[str]:
        """
        Detect potential security threats in text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            List[str]: List of detected threat types
        """
        threats = []
        
        # Check for XSS patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                threats.append('XSS_ATTEMPT')
                break
        
        # Check for SQL injection patterns
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                threats.append('SQL_INJECTION_ATTEMPT')
                break
        
        # Check for excessive special characters
        special_char_ratio = len(re.findall(r'[^\w\s\u4e00-\u9fff]', text)) / max(len(text), 1)
        if special_char_ratio > 0.3:
            threats.append('SUSPICIOUS_CONTENT')
        
        return threats


# Global validator instance
input_validator = InputValidator()


def sanitize_input(text: str) -> str:
    """Convenience function to sanitize input"""
    return input_validator.sanitize_user_input(text)


def validate_message(message: str) -> Dict[str, Any]:
    """Convenience function to validate message"""
    return input_validator.validate_message_input(message)


def validate_session(session_id: str) -> bool:
    """Convenience function to validate session ID"""
    return input_validator.validate_session_id(session_id)
