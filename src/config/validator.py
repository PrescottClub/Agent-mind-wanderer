"""
Configuration validation utilities

Validates application configuration on startup to ensure all required
settings are present and properly formatted.
"""

import os
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ValidationLevel(Enum):
    """Validation severity levels"""
    ERROR = "error"      # Critical - app cannot start
    WARNING = "warning"  # Important - app may have issues
    INFO = "info"        # Informational - best practices


@dataclass
class ValidationResult:
    """Result of configuration validation"""
    level: ValidationLevel
    field: str
    message: str
    current_value: Any = None
    suggested_value: Any = None


class ConfigValidator:
    """Configuration validation service"""
    
    def __init__(self):
        self.validation_rules = self._define_validation_rules()
    
    def _define_validation_rules(self) -> Dict:
        """Define validation rules for configuration fields"""
        return {
            'DEEPSEEK_API_KEY': {
                'required': True,
                'pattern': r'^sk-[a-zA-Z0-9]{32,}$',
                'description': 'DeepSeek API key must start with sk- and be at least 32 characters'
            },
            'DEEPSEEK_MODEL': {
                'required': False,
                'allowed_values': ['deepseek-chat', 'deepseek-reasoner'],
                'default': 'deepseek-chat',
                'description': 'Must be a valid DeepSeek model name'
            },
            'DEEPSEEK_API_BASE': {
                'required': False,
                'pattern': r'^https?://[^\s/$.?#].[^\s]*$',
                'default': 'https://api.deepseek.com',
                'description': 'Must be a valid HTTPS URL'
            },
            'SERPAPI_API_KEY': {
                'required': False,
                'pattern': r'^[a-f0-9]{64}$',
                'description': 'SerpApi key should be 64 character hex string'
            },
            'MAX_TOKENS': {
                'required': False,
                'type': int,
                'min_value': 100,
                'max_value': 4000,
                'default': 512,
                'description': 'Token limit must be between 100 and 4000'
            },
            'TEMPERATURE': {
                'required': False,
                'type': float,
                'min_value': 0.0,
                'max_value': 2.0,
                'default': 0.5,
                'description': 'Temperature must be between 0.0 and 2.0'
            },
            'DEBUG_MODE': {
                'required': False,
                'allowed_values': ['true', 'false'],
                'default': 'false',
                'description': 'Must be true or false'
            },
            'LOG_LEVEL': {
                'required': False,
                'allowed_values': ['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                'default': 'INFO',
                'description': 'Must be a valid log level'
            },
            'DATABASE_PATH': {
                'required': False,
                'default': 'mind_sprite.db',
                'description': 'Path to SQLite database file'
            },
            'CACHE_DURATION_HOURS': {
                'required': False,
                'type': int,
                'min_value': 1,
                'max_value': 168,  # 1 week
                'default': 24,
                'description': 'Cache duration must be between 1 and 168 hours'
            }
        }
    
    def validate_configuration(self) -> List[ValidationResult]:
        """
        Validate current configuration
        
        Returns:
            List[ValidationResult]: List of validation issues found
        """
        results = []
        
        for field, rules in self.validation_rules.items():
            current_value = os.getenv(field)
            
            # Check required fields
            if rules.get('required', False) and not current_value:
                results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    field=field,
                    message=f"Required configuration field '{field}' is missing",
                    current_value=current_value,
                    suggested_value=rules.get('default', 'Please provide a value')
                ))
                continue
            
            # Skip validation if field is not set and not required
            if not current_value:
                if 'default' in rules:
                    results.append(ValidationResult(
                        level=ValidationLevel.INFO,
                        field=field,
                        message=f"Using default value for '{field}'",
                        current_value=current_value,
                        suggested_value=rules['default']
                    ))
                continue
            
            # Type validation
            if 'type' in rules:
                try:
                    if rules['type'] == int:
                        typed_value = int(current_value)
                    elif rules['type'] == float:
                        typed_value = float(current_value)
                    else:
                        typed_value = current_value
                except (ValueError, TypeError):
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        field=field,
                        message=f"'{field}' must be of type {rules['type'].__name__}",
                        current_value=current_value,
                        suggested_value=rules.get('default')
                    ))
                    continue
            else:
                typed_value = current_value
            
            # Pattern validation
            if 'pattern' in rules:
                if not re.match(rules['pattern'], current_value):
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        field=field,
                        message=f"'{field}' format is invalid. {rules.get('description', '')}",
                        current_value=current_value,
                        suggested_value=rules.get('default')
                    ))
                    continue
            
            # Allowed values validation
            if 'allowed_values' in rules:
                if current_value not in rules['allowed_values']:
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        field=field,
                        message=f"'{field}' must be one of: {', '.join(rules['allowed_values'])}",
                        current_value=current_value,
                        suggested_value=rules['allowed_values'][0]
                    ))
                    continue
            
            # Range validation
            if 'min_value' in rules or 'max_value' in rules:
                if 'type' in rules and rules['type'] in (int, float):
                    min_val = rules.get('min_value')
                    max_val = rules.get('max_value')
                    
                    if min_val is not None and typed_value < min_val:
                        results.append(ValidationResult(
                            level=ValidationLevel.ERROR,
                            field=field,
                            message=f"'{field}' must be at least {min_val}",
                            current_value=current_value,
                            suggested_value=str(min_val)
                        ))
                        continue
                    
                    if max_val is not None and typed_value > max_val:
                        results.append(ValidationResult(
                            level=ValidationLevel.ERROR,
                            field=field,
                            message=f"'{field}' must be at most {max_val}",
                            current_value=current_value,
                            suggested_value=str(max_val)
                        ))
                        continue
        
        return results
    
    def validate_file_permissions(self) -> List[ValidationResult]:
        """Validate file system permissions"""
        results = []
        
        # Check database directory permissions
        db_path = os.getenv('DATABASE_PATH', 'mind_sprite.db')
        db_dir = os.path.dirname(os.path.abspath(db_path))
        
        if not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
            except PermissionError:
                results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    field='DATABASE_PATH',
                    message=f"Cannot create database directory: {db_dir}",
                    current_value=db_path
                ))
        
        if not os.access(db_dir, os.W_OK):
            results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                field='DATABASE_PATH',
                message=f"No write permission for database directory: {db_dir}",
                current_value=db_path
            ))
        
        # Check logs directory permissions
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            try:
                os.makedirs(logs_dir, exist_ok=True)
            except PermissionError:
                results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    field='LOG_DIRECTORY',
                    message=f"Cannot create logs directory: {logs_dir}",
                    current_value=logs_dir
                ))
        
        return results
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration"""
        summary = {}
        
        for field, rules in self.validation_rules.items():
            current_value = os.getenv(field)
            
            summary[field] = {
                'value': current_value or rules.get('default', 'Not set'),
                'is_set': current_value is not None,
                'is_required': rules.get('required', False),
                'description': rules.get('description', 'No description available')
            }
        
        return summary
    
    def generate_env_template(self) -> str:
        """Generate a template .env file with all configuration options"""
        template_lines = [
            "# Mind Sprite AI Agent Configuration",
            "# Copy this file to .env and fill in your values",
            "",
        ]
        
        for field, rules in self.validation_rules.items():
            # Add description as comment
            if 'description' in rules:
                template_lines.append(f"# {rules['description']}")
            
            # Add required/optional indicator
            if rules.get('required', False):
                template_lines.append(f"# REQUIRED")
            else:
                template_lines.append(f"# OPTIONAL (default: {rules.get('default', 'none')})")
            
            # Add the field with example or default value
            example_value = rules.get('default', 'your_value_here')
            if field.endswith('_KEY'):
                example_value = 'your_api_key_here'
            
            template_lines.append(f"{field}={example_value}")
            template_lines.append("")
        
        return "\n".join(template_lines)


def validate_startup_config() -> bool:
    """
    Validate configuration on startup
    
    Returns:
        bool: True if configuration is valid for startup, False otherwise
    """
    validator = ConfigValidator()
    results = validator.validate_configuration()
    results.extend(validator.validate_file_permissions())
    
    has_errors = False
    
    for result in results:
        if result.level == ValidationLevel.ERROR:
            print(f"❌ ERROR: {result.message}")
            if result.current_value is not None:
                print(f"   Current value: {result.current_value}")
            if result.suggested_value is not None:
                print(f"   Suggested value: {result.suggested_value}")
            has_errors = True
        elif result.level == ValidationLevel.WARNING:
            print(f"⚠️  WARNING: {result.message}")
        elif result.level == ValidationLevel.INFO:
            print(f"ℹ️  INFO: {result.message}")
    
    if has_errors:
        print("\n❌ Configuration validation failed. Please fix the errors above.")
        return False
    else:
        print("✅ Configuration validation passed.")
        return True


def print_config_summary():
    """Print a summary of current configuration"""
    validator = ConfigValidator()
    summary = validator.get_configuration_summary()
    
    print("\n📋 Configuration Summary:")
    print("=" * 50)
    
    for field, info in summary.items():
        status = "✅ SET" if info['is_set'] else "❌ NOT SET"
        required = "REQUIRED" if info['is_required'] else "OPTIONAL"
        
        print(f"{field}: {status} ({required})")
        print(f"  Value: {info['value']}")
        print(f"  Description: {info['description']}")
        print()


if __name__ == "__main__":
    # Run validation when script is executed directly
    validate_startup_config()
    print_config_summary()
