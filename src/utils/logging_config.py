"""
Logging configuration for Mind Sprite AI Agent

Provides structured logging with different levels for development and production,
including performance monitoring, error tracking, and user interaction logging.
"""

import logging
import logging.handlers
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'performance_data'):
            log_entry['performance'] = record.performance_data
        if hasattr(record, 'error_data'):
            log_entry['error'] = record.error_data
        
        return json.dumps(log_entry, ensure_ascii=False)


class MindSpriteLogger:
    """Centralized logging manager for Mind Sprite AI Agent"""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize logging configuration
        
        Args:
            log_dir (str): Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self._setup_loggers()
    
    def _setup_loggers(self):
        """Set up different loggers for different purposes"""
        
        # Main application logger
        self.app_logger = self._create_logger(
            'mind_sprite.app',
            self.log_dir / 'app.log',
            logging.INFO
        )
        
        # Performance logger
        self.performance_logger = self._create_logger(
            'mind_sprite.performance',
            self.log_dir / 'performance.log',
            logging.INFO
        )
        
        # Error logger
        self.error_logger = self._create_logger(
            'mind_sprite.error',
            self.log_dir / 'error.log',
            logging.ERROR
        )
        
        # User interaction logger (for analytics)
        self.interaction_logger = self._create_logger(
            'mind_sprite.interaction',
            self.log_dir / 'interactions.log',
            logging.INFO
        )
        
        # Security logger
        self.security_logger = self._create_logger(
            'mind_sprite.security',
            self.log_dir / 'security.log',
            logging.WARNING
        )
    
    def _create_logger(self, name: str, log_file: Path, level: int) -> logging.Logger:
        """Create a configured logger"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)
        
        # Console handler for development
        if os.getenv('DEBUG_MODE', 'false').lower() == 'true':
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            logger.addHandler(console_handler)
        
        return logger
    
    def log_user_interaction(self, session_id: str, user_input: str, 
                           ai_response: str, processing_time: float):
        """Log user interaction for analytics"""
        self.interaction_logger.info(
            "User interaction completed",
            extra={
                'session_id': session_id,
                'interaction_data': {
                    'user_input_length': len(user_input),
                    'ai_response_length': len(ai_response),
                    'processing_time_ms': processing_time * 1000
                }
            }
        )
    
    def log_performance_metric(self, operation: str, duration: float, 
                             metadata: Optional[Dict] = None):
        """Log performance metrics"""
        self.performance_logger.info(
            f"Performance metric: {operation}",
            extra={
                'performance_data': {
                    'operation': operation,
                    'duration_ms': duration * 1000,
                    'metadata': metadata or {}
                }
            }
        )
    
    def log_error(self, error: Exception, context: Optional[Dict] = None,
                  session_id: Optional[str] = None):
        """Log error with context"""
        self.error_logger.error(
            f"Error occurred: {str(error)}",
            extra={
                'session_id': session_id,
                'error_data': {
                    'error_type': type(error).__name__,
                    'error_message': str(error),
                    'context': context or {}
                }
            },
            exc_info=True
        )
    
    def log_security_event(self, event_type: str, details: Dict, 
                          session_id: Optional[str] = None):
        """Log security-related events"""
        self.security_logger.warning(
            f"Security event: {event_type}",
            extra={
                'session_id': session_id,
                'security_data': {
                    'event_type': event_type,
                    'details': details,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
        )


# Global logger instance
mind_sprite_logger = MindSpriteLogger()


# Convenience functions
def log_interaction(session_id: str, user_input: str, ai_response: str, processing_time: float):
    """Log user interaction"""
    mind_sprite_logger.log_user_interaction(session_id, user_input, ai_response, processing_time)


def log_performance(operation: str, duration: float, metadata: Dict = None):
    """Log performance metric"""
    mind_sprite_logger.log_performance_metric(operation, duration, metadata)


def log_error(error: Exception, context: Dict = None, session_id: str = None):
    """Log error with context"""
    mind_sprite_logger.log_error(error, context, session_id)


def log_security_event(event_type: str, details: Dict, session_id: str = None):
    """Log security event"""
    mind_sprite_logger.log_security_event(event_type, details, session_id)


def get_logger(name: str) -> logging.Logger:
    """Get logger by name"""
    return logging.getLogger(f'mind_sprite.{name}')


# Performance monitoring decorator
def monitor_performance(operation_name: str):
    """Decorator to monitor function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                log_performance(operation_name, duration, {
                    'function': func.__name__,
                    'success': True
                })
                return result
            except Exception as e:
                duration = time.time() - start_time
                log_performance(operation_name, duration, {
                    'function': func.__name__,
                    'success': False,
                    'error': str(e)
                })
                raise
        return wrapper
    return decorator
