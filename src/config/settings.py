"""
心绪精灵应用设置
环境变量、AI配置等设置
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional


class Settings:
    """应用设置类，管理所有配置"""

    def __init__(self):
        self.load_environment()

    def load_environment(self):
        """加载环境变量"""
        env_path = Path(__file__).parent.parent.parent / '.env'
        env_loaded = False

        try:
            load_dotenv(dotenv_path=env_path)
            env_loaded = True
        except Exception as e:
            # 如果遇到任何问题，尝试手动读取并设置环境变量
            try:
                with open(env_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig 会自动处理BOM
                    for line in f:
                        line = line.strip()
                        if line and '=' in line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
                env_loaded = True
            except Exception as e2:
                print(f"Warning: Could not load .env file: {e2}")
                pass

        # 设置默认配置（不包含API密钥，确保安全性）
        if not os.getenv('DEEPSEEK_MODEL'):
            os.environ['DEEPSEEK_MODEL'] = 'deepseek-chat'  # V3模型，速度快，适合日常对话
        if not os.getenv('DEEPSEEK_API_BASE'):
            os.environ['DEEPSEEK_API_BASE'] = 'https://api.deepseek.com'
        if not os.getenv('MAX_TOKENS'):
            os.environ['MAX_TOKENS'] = '512'  # 优化速度的token设置
        if not os.getenv('TEMPERATURE'):
            os.environ['TEMPERATURE'] = '0.5'  # 优化速度的温度设置

    @property
    def deepseek_api_key(self) -> Optional[str]:
        """获取DeepSeek API密钥"""
        return os.getenv('DEEPSEEK_API_KEY')

    @property
    def deepseek_model(self) -> str:
        """获取DeepSeek模型名称"""
        return os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

    @property
    def deepseek_api_base(self) -> str:
        """获取DeepSeek API基础URL"""
        return os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com')

    @property
    def serp_api_key(self) -> Optional[str]:
        """获取SerpApi密钥"""
        return os.getenv('SERPAPI_API_KEY')

    @property
    def search_enabled(self) -> bool:
        """是否启用搜索功能"""
        return self.serp_api_key is not None

    @property
    def debug_mode(self) -> bool:
        """是否开启调试模式"""
        return os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    @property
    def max_tokens(self) -> int:
        """AI模型最大token数"""
        return int(os.getenv('MAX_TOKENS', '512'))  # 优化速度的token设置

    @property
    def temperature(self) -> float:
        """AI模型温度参数"""
        return float(os.getenv('TEMPERATURE', '0.5'))  # 优化速度的温度设置


# 全局设置实例
settings = Settings()