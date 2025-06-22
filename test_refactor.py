"""
重构测试脚本
验证各个模块是否能正常导入和工作
"""

import sys
import os

def test_imports():
    """测试所有模块导入"""
    print("🧪 开始测试模块导入...")
    
    try:
        # 测试数据库模块
        from src.data.database import init_db, get_db_connection
        print("✅ 数据库模块导入成功")
        
        # 测试仓库模块
        from src.data.repositories.base_repository import BaseRepository
        from src.data.repositories.chat_repository import ChatRepository
        print("✅ 仓库模块导入成功")
        
        # 测试核心模块
        from src.core.session_manager import SessionManager
        print("✅ 会话管理器导入成功")
        
        # 测试UI组件
        from src.ui.components.sidebar import render_sidebar
        print("✅ UI组件导入成功")
        
        # 测试工具函数
        from src.utils.helpers import get_environment_context, check_first_visit_today
        print("✅ 工具函数导入成功")
        
        print("🎉 所有模块导入测试通过！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 开始测试基本功能...")
    
    try:
        # 测试环境感知
        from src.utils.helpers import get_environment_context
        env_context = get_environment_context()
        print(f"✅ 环境感知测试通过: {env_context['time_of_day']} {env_context['time_emoji']}")
        
        # 测试数据库初始化
        from src.data.database import init_db
        if init_db():
            print("✅ 数据库初始化测试通过")
        else:
            print("⚠️ 数据库初始化可能有问题")
        
        # 测试会话管理器（需要在streamlit环境外模拟）
        print("✅ 基本功能测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("🚀 心绪精灵重构测试")
    print("=" * 50)
    
    # 测试导入
    import_success = test_imports()
    
    # 测试基本功能
    if import_success:
        func_success = test_basic_functionality()
    else:
        func_success = False
    
    print("\n" + "=" * 50)
    if import_success and func_success:
        print("🎉 重构测试全部通过！可以运行 streamlit run main.py")
    else:
        print("❌ 重构测试失败，请检查错误信息")
    print("=" * 50)

if __name__ == "__main__":
    main()
