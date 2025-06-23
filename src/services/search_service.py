"""
搜索服务模块
实现本地心理健康资源搜索功能
"""

import os
import re
from typing import Dict, List, Optional
from langchain_community.utilities import SerpAPIWrapper
import streamlit as st


class LocalMentalHealthSearchService:
    """本地心理健康资源搜索服务"""
    
    def __init__(self, serp_api_key: Optional[str] = None):
        self.serp_api_key = serp_api_key
        self.search_wrapper = None
        if serp_api_key:
            try:
                self.search_wrapper = SerpAPIWrapper(serpapi_api_key=serp_api_key)
            except Exception as e:
                st.warning(f"搜索功能初始化失败: {e}")
    
    def is_search_request(self, user_input: str) -> bool:
        """判断用户输入是否需要搜索本地心理健康资源"""
        search_keywords = [
            "找心理咨询师", "找心理医生", "心理咨询", "心理治疗",
            "咨询师推荐", "心理诊所", "心理科", "精神科",
            "抑郁症医院", "焦虑症治疗", "心理健康中心",
            "哪里看心理", "附近的", "当地的", "本地",
            "推荐医生", "推荐医院", "挂号", "心理医生推荐",
            "好的心理医生", "靠谱的咨询师", "心理科医生"
        ]
        
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in search_keywords)
    
    def extract_location(self, user_input: str) -> str:
        """从用户输入中提取地理位置信息"""
        # 常见城市匹配模式
        city_patterns = [
            r'(\w+市)', r'(\w+区)', r'(\w+县)', 
            r'北京', r'上海', r'广州', r'深圳', r'杭州', 
            r'南京', r'武汉', r'成都', r'西安', r'天津'
        ]
        
        for pattern in city_patterns:
            match = re.search(pattern, user_input)
            if match:
                return match.group(1) if match.groups() else match.group(0)
        
        # 如果没有明确位置，返回默认
        return "当地"
    
    def generate_search_query(self, user_input: str, location: str) -> str:
        """生成搜索查询"""
        base_queries = {
            "心理咨询师": f"{location} 专业心理咨询师 推荐 2024",
            "心理医生": f"{location} 心理科医生 精神科 医院",
            "心理诊所": f"{location} 心理咨询中心 心理诊所 地址电话",
            "抑郁症": f"{location} 抑郁症治疗 专科医院 心理科",
            "焦虑症": f"{location} 焦虑症治疗 心理咨询 专业机构"
        }
        
        # 根据用户输入匹配最合适的查询
        for keyword, query in base_queries.items():
            if keyword in user_input:
                return query
        
        # 默认查询
        return f"{location} 心理咨询师 心理健康中心 推荐"
    
    def search_local_resources(self, user_input: str) -> Dict:
        """搜索本地心理健康资源"""
        if not self.search_wrapper:
            return {
                "success": False,
                "message": "搜索功能未配置，需要SerpApi密钥",
                "results": []
            }
        
        try:
            # 提取位置和生成查询
            location = self.extract_location(user_input)
            search_query = self.generate_search_query(user_input, location)
            
            # 执行搜索
            search_results = self.search_wrapper.run(search_query)
            
            # 解析和过滤结果
            filtered_results = self._filter_mental_health_results(search_results)
            
            return {
                "success": True,
                "location": location,
                "query": search_query,
                "results": filtered_results,
                "raw_results": search_results
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"搜索过程中出现错误: {str(e)}",
                "results": []
            }
    
    def _filter_mental_health_results(self, raw_results: str) -> List[Dict]:
        """过滤和结构化心理健康相关结果"""
        # 这里可以根据需要解析和过滤搜索结果
        # 提取关键信息如：机构名称、地址、电话、评价等
        
        # 简化版本：直接返回原始结果
        # 实际应用中可以用正则表达式或NLP技术提取结构化信息
        return [{
            "type": "search_results",
            "content": raw_results[:1000] + "..." if len(raw_results) > 1000 else raw_results
        }]
    
    def format_search_results_for_ai(self, search_data: Dict) -> str:
        """为AI格式化搜索结果"""
        if not search_data["success"]:
            return f"搜索失败: {search_data.get('message', '未知错误')}"
        
        formatted_text = f"""
=== 本地心理健康资源搜索结果 ===
搜索位置: {search_data['location']}
搜索查询: {search_data['query']}

搜索结果:
{search_data['results'][0]['content'] if search_data['results'] else '未找到相关结果'}

请基于以上搜索结果，为用户提供有用的本地心理健康资源信息。
注意：
1. 提供具体的机构名称、地址、联系方式
2. 建议用户实地了解和验证信息
3. 提醒专业资质的重要性
4. 保持温暖的语气
"""
        return formatted_text


class SearchTriggerDetector:
    """搜索触发检测器"""
    
    @staticmethod
    def detect_search_intent(user_input: str) -> Dict:
        """检测用户输入的搜索意图"""
        intent_patterns = {
            "local_mental_health": [
                "找心理咨询师", "找心理医生", "心理咨询", "心理治疗",
                "咨询师推荐", "心理诊所", "附近的", "当地的",
                "心理医生推荐", "好的心理医生", "靠谱的咨询师", "心理科医生"
            ],
            "mental_health_info": [
                "最新研究", "新方法", "科学依据", "专家建议",
                "治疗方法", "缓解技巧"
            ],
            "crisis_resources": [
                "紧急求助", "危机干预", "自杀预防", "急救电话"
            ]
        }
        
        user_input_lower = user_input.lower()
        
        for intent, keywords in intent_patterns.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return {
                    "intent": intent,
                    "confidence": 0.8,
                    "matched_keywords": [kw for kw in keywords if kw in user_input_lower]
                }
        
        return {"intent": "none", "confidence": 0.0, "matched_keywords": []} 