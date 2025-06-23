"""
本地心理健康资源搜索功能测试脚本
"""

import os
from src.services.search_service import LocalMentalHealthSearchService, SearchTriggerDetector


def test_search_trigger_detection():
    """测试搜索意图检测"""
    print("🔍 测试搜索意图检测...")
    
    test_cases = [
        "我想找附近的心理咨询师",
        "北京有好的心理医生推荐吗？",
        "今天心情不太好",  # 不应触发搜索
        "找个心理诊所看看",
        "推荐个靠谱的咨询师",
        "我很开心今天"  # 不应触发搜索
    ]
    
    for text in test_cases:
        intent = SearchTriggerDetector.detect_search_intent(text)
        trigger = intent["intent"] == "local_mental_health"
        print(f"  输入: '{text}'")
        print(f"  触发搜索: {'✅' if trigger else '❌'}")
        if trigger:
            print(f"  匹配关键词: {intent['matched_keywords']}")
        print()


def test_location_extraction():
    """测试位置提取"""
    print("📍 测试位置提取...")
    
    # 创建搜索服务实例（不需要API密钥测试位置提取）
    search_service = LocalMentalHealthSearchService()
    
    test_cases = [
        "我想找北京的心理咨询师",
        "上海有好的心理医生吗？",
        "广州心理诊所推荐",
        "找附近的心理咨询师",  # 无明确位置
        "深圳市心理健康中心在哪",
        "朝阳区有心理医生吗"
    ]
    
    for text in test_cases:
        location = search_service.extract_location(text)
        print(f"  输入: '{text}'")
        print(f"  提取位置: '{location}'")
        print()


def test_search_query_generation():
    """测试搜索查询生成"""
    print("🔎 测试搜索查询生成...")
    
    search_service = LocalMentalHealthSearchService()
    
    test_cases = [
        ("我想找北京的心理咨询师", "北京"),
        ("上海有治疗抑郁症的医院吗", "上海"),
        ("广州心理诊所推荐", "广州"),
        ("找个好的心理医生", "当地")
    ]
    
    for user_input, location in test_cases:
        query = search_service.generate_search_query(user_input, location)
        print(f"  用户输入: '{user_input}'")
        print(f"  位置: '{location}'")
        print(f"  生成查询: '{query}'")
        print()


def test_real_search():
    """测试真实搜索（需要API密钥）"""
    print("🌐 测试真实搜索功能...")
    
    api_key = os.getenv('SERPAPI_API_KEY')
    if not api_key:
        print("  ⚠️ 未配置SERPAPI_API_KEY，跳过真实搜索测试")
        print("  💡 如需测试，请在.env文件中配置SERPAPI_API_KEY")
        return
    
    search_service = LocalMentalHealthSearchService(api_key)
    
    if search_service.search_wrapper:
        print("  ✅ SerpApi连接成功")
        
        # 测试一个简单的搜索
        test_query = "北京心理咨询师推荐"
        print(f"  🔍 测试搜索: '{test_query}'")
        
        try:
            result = search_service.search_local_resources(test_query)
            if result["success"]:
                print("  ✅ 搜索成功")
                print(f"  📍 搜索位置: {result['location']}")
                print(f"  🔎 搜索查询: {result['query']}")
                print(f"  📄 结果长度: {len(result['results'][0]['content'])}字符")
            else:
                print(f"  ❌ 搜索失败: {result['message']}")
        except Exception as e:
            print(f"  ❌ 搜索异常: {e}")
    else:
        print("  ❌ SerpApi初始化失败")


def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 心绪精灵 - 本地搜索功能测试")
    print("=" * 50)
    print()
    
    # 运行所有测试
    test_search_trigger_detection()
    print("-" * 30)
    test_location_extraction()
    print("-" * 30)
    test_search_query_generation()
    print("-" * 30)
    test_real_search()
    
    print("=" * 50)
    print("✅ 测试完成！")
    print()
    print("💡 使用提示：")
    print("  1. 在聊天中说 '我想找附近的心理咨询师' 即可触发搜索")
    print("  2. 可以指定城市如 '北京有好的心理医生吗？'")
    print("  3. 配置SERPAPI_API_KEY后可获得真实搜索结果")


if __name__ == "__main__":
    main() 