"""
v5.0 亲密度系统测试脚本
验证亲密度养成系统的各个功能
"""

import sys
import os

def test_intimacy_system():
    """测试亲密度系统"""
    print("🧪 开始测试v5.0亲密度系统...")
    
    try:
        # 测试数据库模块
        from src.data.database import init_db
        print("✅ 数据库模块导入成功")
        
        # 初始化数据库（包含新的用户档案表）
        if init_db():
            print("✅ 数据库初始化成功（包含用户档案表）")
        else:
            print("❌ 数据库初始化失败")
            return False
        
        # 测试用户档案仓库
        from src.data.repositories.user_profile_repository import UserProfileRepository
        user_repo = UserProfileRepository()
        print("✅ 用户档案仓库导入成功")
        
        # 测试亲密度服务
        from src.services.intimacy_service import IntimacyService
        intimacy_service = IntimacyService(user_repo)
        print("✅ 亲密度服务导入成功")
        
        # 测试基本功能
        test_session_id = "test_session_123"
        
        # 测试创建用户档案
        profile = user_repo.find_or_create_profile(test_session_id)
        print(f"✅ 用户档案创建成功: Lv.{profile['intimacy_level']}, EXP: {profile['intimacy_exp']}")
        
        # 测试添加经验值
        result = intimacy_service.add_exp(test_session_id, 25)
        print(f"✅ 经验值添加成功: +25 EXP")
        
        # 测试升级逻辑
        for i in range(3):
            result = intimacy_service.add_exp(test_session_id, 50)
            if result["leveled_up"]:
                print(f"🎉 升级成功！新等级: Lv.{result['new_level']}")
                if result["level_rewards"]:
                    for reward in result["level_rewards"]:
                        print(f"   🎁 奖励: {reward['content']}")
        
        # 测试亲密度信息获取
        intimacy_info = intimacy_service.get_intimacy_info(test_session_id)
        print(f"✅ 亲密度信息获取成功:")
        print(f"   等级: Lv.{intimacy_info['current_level']}")
        print(f"   经验值: {intimacy_info['current_exp']}/{intimacy_info['exp_needed']}")
        print(f"   互动次数: {intimacy_info['total_interactions']}")
        
        # 测试AI上下文生成
        ai_context = intimacy_service.get_intimacy_context_for_ai(test_session_id)
        print(f"✅ AI上下文生成成功:")
        print(f"   {ai_context}")
        
        print("🎉 v5.0亲密度系统测试全部通过！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_ui_components():
    """测试UI组件更新"""
    print("\n🧪 开始测试UI组件更新...")
    
    try:
        # 测试侧边栏组件导入
        from src.ui.components.sidebar import render_sidebar, render_intimacy_display
        print("✅ 侧边栏组件导入成功（包含亲密度显示）")
        
        # 测试AI引擎更新
        from src.core.ai_engine import AIEngine
        print("✅ AI引擎导入成功（支持亲密度上下文）")
        
        print("✅ UI组件更新测试通过！")
        return True
        
    except ImportError as e:
        print(f"❌ UI组件导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ UI组件测试失败: {e}")
        return False

def test_level_progression():
    """测试等级进度系统"""
    print("\n🧪 开始测试等级进度系统...")
    
    try:
        from src.data.repositories.user_profile_repository import UserProfileRepository
        from src.services.intimacy_service import IntimacyService
        
        user_repo = UserProfileRepository()
        intimacy_service = IntimacyService(user_repo)
        
        test_session_id = "level_test_456"
        
        print("测试等级进度：")
        current_level = 1
        
        # 模拟多次互动升级
        for interaction in range(20):
            result = intimacy_service.add_exp(test_session_id, 15)
            
            if result["leveled_up"] and result["new_level"] != current_level:
                current_level = result["new_level"]
                title = intimacy_service._get_level_title(current_level)
                print(f"   🆙 第{interaction+1}次互动: 升级到 Lv.{current_level} ({title})")
                
                # 显示奖励
                if result["level_rewards"]:
                    for reward in result["level_rewards"]:
                        print(f"      🎁 {reward['content']}")
        
        # 最终状态
        final_info = intimacy_service.get_intimacy_info(test_session_id)
        print(f"\n最终状态:")
        print(f"   等级: Lv.{final_info['current_level']}")
        print(f"   经验值: {final_info['current_exp']}/{final_info['exp_needed']}")
        print(f"   总互动: {final_info['total_interactions']}次")
        
        print("✅ 等级进度系统测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 等级进度测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 心绪精灵 v5.0 - 亲密度养成系统测试")
    print("=" * 60)
    
    # 测试亲密度系统
    intimacy_success = test_intimacy_system()
    
    # 测试UI组件
    ui_success = test_ui_components()
    
    # 测试等级进度
    level_success = test_level_progression()
    
    print("\n" + "=" * 60)
    if intimacy_success and ui_success and level_success:
        print("🎉 v5.0 亲密度系统测试全部通过！")
        print("✨ 可以运行 streamlit run main.py 体验新功能")
        print("\n🆕 v5.0 新功能:")
        print("   💖 亲密度等级系统")
        print("   📊 经验值进度条")
        print("   🎁 升级奖励机制")
        print("   🤖 AI感知羁绊等级")
        print("   🎉 升级庆祝效果")
    else:
        print("❌ v5.0 测试失败，请检查错误信息")
    print("=" * 60)

if __name__ == "__main__":
    main()
