"""
增强的搜索服务模块
实现本地心理健康资源搜索功能，包含错误处理、缓存机制和性能优化
"""

import os
import re
import time
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import streamlit as st
from functools import lru_cache


class SearchServiceError(Exception):
    """自定义搜索服务异常"""
    pass


class EnhancedSearchService:
    """增强的本地心理健康资源搜索服务"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化搜索服务
        
        Args:
            api_key (str, optional): SerpApi API密钥
        """
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"
        self.request_timeout = 10.0
        self.max_retries = 3
        self.retry_delay = 1.0
        
        # 速率限制
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 最小请求间隔1秒
        
        # 缓存设置
        self.cache_duration = timedelta(hours=24)
        self._search_cache = {}
        
        # 性能指标
        self._total_requests = 0
        self._cache_hits = 0
        self._cache_misses = 0
    
    def _rate_limit_check(self):
        """实施速率限制"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get_cache_key(self, query: str, location: str) -> str:
        """生成缓存键"""
        return f"{query}_{location}".lower().replace(" ", "_")
    
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """检查缓存条目是否仍然有效"""
        if 'timestamp' not in cache_entry:
            return False
        
        cache_time = datetime.fromisoformat(cache_entry['timestamp'])
        return datetime.now() - cache_time < self.cache_duration
    
    @lru_cache(maxsize=100)
    def _cached_search_request(self, query: str, location: str) -> Dict:
        """缓存的搜索请求以避免重复API调用"""
        cache_key = self._get_cache_key(query, location)
        
        # 检查内存缓存
        if cache_key in self._search_cache:
            cache_entry = self._search_cache[cache_key]
            if self._is_cache_valid(cache_entry):
                self._cache_hits += 1
                return cache_entry['results']
        
        # 执行实际搜索
        self._cache_misses += 1
        results = self._perform_search_request(query, location)
        
        # 缓存结果
        self._search_cache[cache_key] = {
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
        return results
    
    def _perform_search_request(self, query: str, location: str) -> Dict:
        """执行实际的搜索请求，包含重试机制"""
        if not self.api_key:
            raise SearchServiceError("SerpApi密钥未配置")
        
        search_params = {
            "q": f"{query} {location} 心理健康 心理咨询",
            "location": location,
            "hl": "zh-cn",
            "gl": "cn",
            "api_key": self.api_key,
            "num": 10
        }
        
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                self._rate_limit_check()
                
                response = requests.get(
                    self.base_url,
                    params=search_params,
                    timeout=self.request_timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._process_search_results(data)
                elif response.status_code == 429:
                    # 速率限制，等待更长时间
                    wait_time = self.retry_delay * (2 ** attempt)
                    time.sleep(wait_time)
                    continue
                else:
                    raise SearchServiceError(f"API返回状态码 {response.status_code}")
                    
            except requests.RequestException as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
        
        # 所有重试都失败了
        raise SearchServiceError(f"搜索失败，重试{self.max_retries}次后仍然失败: {last_exception}")
    
    def _process_search_results(self, data: Dict) -> Dict:
        """处理和格式化搜索结果"""
        results = {
            "success": True,
            "resources": [],
            "total_found": 0,
            "search_time": datetime.now().isoformat()
        }
        
        if "organic_results" in data:
            for result in data["organic_results"][:5]:  # 限制为前5个结果
                resource = {
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "source": "SerpApi"
                }
                results["resources"].append(resource)
            
            results["total_found"] = len(data["organic_results"])
        
        return results
    
    def search_local_resources(self, user_input: str, location: str = "北京") -> Dict:
        """
        搜索本地心理健康资源
        
        Args:
            user_input (str): 用户输入
            location (str): 搜索位置
            
        Returns:
            Dict: 搜索结果
        """
        try:
            self._total_requests += 1
            
            # 从用户输入中提取搜索意图
            search_query = self._extract_search_query(user_input)
            
            # 执行缓存搜索
            results = self._cached_search_request(search_query, location)
            results["location"] = location
            results["query"] = search_query
            
            return results
            
        except SearchServiceError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "搜索服务暂时不可用，请稍后再试",
                "location": location
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"未知错误: {str(e)}",
                "message": "搜索时发生未知错误",
                "location": location
            }
    
    def _extract_search_query(self, user_input: str) -> str:
        """从用户输入中提取相关搜索词"""
        # 心理健康相关关键词
        mental_health_keywords = [
            "心理咨询", "心理医生", "心理治疗", "心理健康",
            "抑郁", "焦虑", "压力", "情绪", "心理问题"
        ]
        
        # 在用户输入中查找相关关键词
        found_keywords = [kw for kw in mental_health_keywords if kw in user_input]
        
        if found_keywords:
            return " ".join(found_keywords[:2])  # 使用前2个关键词
        else:
            return "心理咨询 心理健康"  # 默认搜索词
    
    def get_stats(self) -> Dict:
        """获取搜索服务统计信息"""
        hit_rate = (self._cache_hits / self._total_requests) * 100 if self._total_requests > 0 else 0
        
        return {
            'total_requests': self._total_requests,
            'cache_hits': self._cache_hits,
            'cache_misses': self._cache_misses,
            'hit_rate_percent': round(hit_rate, 2),
            'cache_size': len(self._search_cache)
        }
    
    def clear_cache(self):
        """清除搜索缓存"""
        self._search_cache.clear()
        self._cached_search_request.cache_clear()


class SearchTriggerDetector:
    """搜索触发检测器"""
    
    @staticmethod
    def detect_search_intent(user_input: str) -> Dict:
        """检测用户输入是否需要搜索功能"""
        
        # 表示需要搜索的模式
        search_patterns = {
            "local_mental_health": [
                r"附近.*心理", r"本地.*心理", r"这里.*心理咨询",
                r"推荐.*心理医生", r"哪里.*心理治疗", r"找.*心理咨询师",
                r"心理医院", r"心理诊所", r"心理健康中心"
            ],
            "crisis_resources": [
                r"紧急.*帮助", r"危机.*干预", r"自杀.*热线",
                r"心理急救", r"24小时.*心理"
            ]
        }
        
        for intent_type, patterns in search_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    return {
                        "intent": intent_type,
                        "confidence": 0.8,
                        "trigger_pattern": pattern
                    }
        
        return {"intent": "none", "confidence": 0.0}


# 全局搜索服务实例
_search_service = None


def get_search_service() -> EnhancedSearchService:
    """获取全局搜索服务实例"""
    global _search_service
    
    if _search_service is None:
        api_key = os.getenv('SERPAPI_API_KEY')
        _search_service = EnhancedSearchService(api_key)
    
    return _search_service
