#!/usr/bin/env python3
"""
测试模型配置的脚本
验证DeepSeek V3模型配置是否正确
"""

import os
import sys
sys.path.append('.')

from src.config.settings import settings
from src.core.ai_engine import AIEngine


def test_model_configuration():
    """测试模型配置"""
    print("🧪 测试DeepSeek模型配置...")
    print("=" * 50)
    
    # 显示当前配置
    print(f"📱 当前模型: {settings.deepseek_model}")
    print(f"🌐 API基础URL: {settings.deepseek_api_base}")
    print(f"📊 最大Token数: {settings.max_tokens}")
    print(f"🌡️ 温度参数: {settings.temperature}")
    print(f"🔍 调试模式: {settings.debug_mode}")
    print()
    
    # 验证模型类型
    if settings.deepseek_model == "deepseek-chat":
        print("✅ 正在使用DeepSeek V3模型 (快速)")
        print("   - 适合日常对话和情感陪伴")
        print("   - 响应速度快")
        print("   - 推荐用于心绪精灵应用")
    elif settings.deepseek_model == "deepseek-reasoner":
        print("⚠️ 正在使用DeepSeek R1模型 (推理)")
        print("   - 适合复杂推理任务")
        print("   - 响应速度较慢")
        print("   - 建议切换到V3以提升速度")
    else:
        print(f"❓ 未知模型: {settings.deepseek_model}")
    print()
    
    # 性能建议
    print("🚀 性能优化建议:")
    if settings.max_tokens > 512:
        print(f"   ⚠️ Token数({settings.max_tokens})较高，建议设置为512以下")
    else:
        print(f"   ✅ Token数({settings.max_tokens})已优化")
    
    if settings.temperature > 0.5:
        print(f"   ⚠️ 温度({settings.temperature})较高，建议设置为0.5以下")
    else:
        print(f"   ✅ 温度({settings.temperature})已优化")
    print()
    
    # 测试API密钥配置
    api_key = settings.deepseek_api_key
    if api_key:
        print("🔑 API密钥状态: ✅ 已配置")
        print(f"   密钥前缀: {api_key[:10]}...")
        
        # 尝试初始化AI引擎
        try:
            ai_engine = AIEngine(api_key)
            if ai_engine.llm:
                print("🤖 AI引擎初始化: ✅ 成功")
                print("   模型已准备就绪")
            else:
                print("🤖 AI引擎初始化: ❌ 失败")
        except Exception as e:
            print(f"🤖 AI引擎初始化: ❌ 错误 - {e}")
    else:
        print("🔑 API密钥状态: ❌ 未配置")
        print("   请在.env文件中设置DEEPSEEK_API_KEY")
    print()
    
    # 配置建议
    print("💡 推荐配置:")
    print("   DEEPSEEK_MODEL=deepseek-chat")
    print("   MAX_TOKENS=512")
    print("   TEMPERATURE=0.5")
    print("   这样配置可以获得最佳的速度和质量平衡")


def show_model_comparison():
    """显示模型对比"""
    print("\n📊 DeepSeek模型对比:")
    print("=" * 50)
    
    print("🚀 DeepSeek V3 (deepseek-chat)")
    print("   ✅ 响应速度: 快")
    print("   ✅ 适用场景: 日常对话、情感陪伴、创意写作")
    print("   ✅ 推荐指数: ⭐⭐⭐⭐⭐")
    print("   💰 成本: 较低")
    print()
    
    print("🧠 DeepSeek R1 (deepseek-reasoner)")
    print("   ⚠️ 响应速度: 慢 (需要推理时间)")
    print("   ✅ 适用场景: 复杂推理、数学问题、逻辑分析")
    print("   ⚠️ 推荐指数: ⭐⭐⭐ (仅特殊需求)")
    print("   💰 成本: 较高")
    print()
    
    print("🎯 对于心绪精灵应用，强烈推荐使用V3模型！")


if __name__ == "__main__":
    test_model_configuration()
    show_model_comparison()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！如需修改配置，请编辑.env文件或使用应用内的配置面板")
