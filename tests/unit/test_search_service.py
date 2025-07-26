"""
Unit tests for enhanced search service

Tests the search functionality including caching, error handling,
and API integration.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import requests
from datetime import datetime, timedelta
from src.services.enhanced_search_service import (
    EnhancedSearchService,
    SearchServiceError,
    SearchTriggerDetector
)


class TestEnhancedSearchService:
    """Test cases for EnhancedSearchService class"""
    
    @pytest.fixture
    def search_service(self):
        """Create search service instance for testing"""
        return EnhancedSearchService("test_api_key")
    
    @pytest.fixture
    def mock_successful_response(self):
        """Mock successful API response"""
        return {
            "organic_results": [
                {
                    "title": "测试心理咨询中心",
                    "link": "https://test-clinic.com",
                    "snippet": "专业的心理咨询服务"
                },
                {
                    "title": "北京心理健康医院",
                    "link": "https://test-hospital.com",
                    "snippet": "提供全面的心理健康服务"
                }
            ]
        }
    
    def test_initialization(self):
        """Test service initialization"""
        service = EnhancedSearchService("test_key")
        
        assert service.api_key == "test_key"
        assert service.max_retries == 3
        assert service.request_timeout == 10.0
        assert service._total_requests == 0
        assert service._cache_hits == 0
        assert service._cache_misses == 0
    
    def test_cache_key_generation(self, search_service):
        """Test cache key generation"""
        cache_key = search_service._get_cache_key("心理咨询", "北京")
        
        assert cache_key == "心理咨询_北京"
        assert isinstance(cache_key, str)
    
    def test_cache_validity_check(self, search_service):
        """Test cache validity checking"""
        # Valid cache entry
        valid_entry = {
            'timestamp': datetime.now().isoformat(),
            'results': {'test': 'data'}
        }
        assert search_service._is_cache_valid(valid_entry)
        
        # Expired cache entry
        expired_entry = {
            'timestamp': (datetime.now() - timedelta(days=2)).isoformat(),
            'results': {'test': 'data'}
        }
        assert not search_service._is_cache_valid(expired_entry)
        
        # Invalid cache entry (missing timestamp)
        invalid_entry = {'results': {'test': 'data'}}
        assert not search_service._is_cache_valid(invalid_entry)
    
    def test_extract_search_query(self, search_service):
        """Test search query extraction from user input"""
        # Test with mental health keywords
        input1 = "我需要心理咨询帮助"
        query1 = search_service._extract_search_query(input1)
        assert "心理咨询" in query1
        
        # Test with multiple keywords
        input2 = "我有抑郁和焦虑问题"
        query2 = search_service._extract_search_query(input2)
        assert "抑郁" in query2 or "焦虑" in query2
        
        # Test with no keywords
        input3 = "今天天气很好"
        query3 = search_service._extract_search_query(input3)
        assert query3 == "心理咨询 心理健康"  # Default
    
    @patch('requests.get')
    def test_successful_search_request(self, mock_get, search_service, mock_successful_response):
        """Test successful search request"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_successful_response
        mock_get.return_value = mock_response
        
        result = search_service._perform_search_request("心理咨询", "北京")
        
        assert result["success"]
        assert len(result["resources"]) == 2
        assert result["resources"][0]["title"] == "测试心理咨询中心"
        assert result["total_found"] == 2
    
    @patch('requests.get')
    def test_api_error_handling(self, mock_get, search_service):
        """Test API error handling"""
        # Mock API error
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        with pytest.raises(SearchServiceError):
            search_service._perform_search_request("心理咨询", "北京")
    
    @patch('requests.get')
    def test_rate_limiting_handling(self, mock_get, search_service):
        """Test rate limiting handling"""
        # Mock rate limit response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response
        
        with pytest.raises(SearchServiceError):
            search_service._perform_search_request("心理咨询", "北京")
        
        # Should have made multiple attempts
        assert mock_get.call_count == search_service.max_retries
    
    @patch('requests.get')
    def test_request_timeout_handling(self, mock_get, search_service):
        """Test request timeout handling"""
        # Mock timeout
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        with pytest.raises(SearchServiceError):
            search_service._perform_search_request("心理咨询", "北京")
    
    def test_search_result_processing(self, search_service, mock_successful_response):
        """Test search result processing"""
        processed = search_service._process_search_results(mock_successful_response)
        
        assert processed["success"]
        assert len(processed["resources"]) == 2
        assert processed["total_found"] == 2
        assert "search_time" in processed
        
        # Check resource structure
        resource = processed["resources"][0]
        assert "title" in resource
        assert "link" in resource
        assert "snippet" in resource
        assert "source" in resource
        assert resource["source"] == "SerpApi"
    
    def test_search_result_processing_empty(self, search_service):
        """Test processing empty search results"""
        empty_response = {}
        processed = search_service._process_search_results(empty_response)
        
        assert processed["success"]
        assert len(processed["resources"]) == 0
        assert processed["total_found"] == 0
    
    @patch.object(EnhancedSearchService, '_perform_search_request')
    def test_caching_mechanism(self, mock_perform_search, search_service):
        """Test caching mechanism"""
        # Mock search result
        mock_result = {
            "success": True,
            "resources": [{"title": "Test", "link": "test.com", "snippet": "test"}],
            "total_found": 1
        }
        mock_perform_search.return_value = mock_result
        
        # First search - should call API
        result1 = search_service.search_local_resources("心理咨询", "北京")
        assert result1["success"]
        assert mock_perform_search.call_count == 1
        
        # Second search with same parameters - should use cache
        result2 = search_service.search_local_resources("心理咨询", "北京")
        assert result2["success"]
        # Should still be 1 because of caching
        assert mock_perform_search.call_count == 1
    
    def test_search_without_api_key(self):
        """Test search without API key"""
        service = EnhancedSearchService(None)
        
        result = service.search_local_resources("心理咨询", "北京")
        
        assert not result["success"]
        assert "error" in result
        assert "SerpApi密钥未配置" in result["error"]
    
    def test_get_stats(self, search_service):
        """Test statistics retrieval"""
        # Simulate some requests
        search_service._total_requests = 10
        search_service._cache_hits = 7
        search_service._cache_misses = 3
        
        stats = search_service.get_stats()
        
        assert stats["total_requests"] == 10
        assert stats["cache_hits"] == 7
        assert stats["cache_misses"] == 3
        assert stats["hit_rate_percent"] == 70.0
    
    def test_clear_cache(self, search_service):
        """Test cache clearing"""
        # Add some cache entries
        search_service._search_cache["test_key"] = {"test": "data"}
        
        search_service.clear_cache()
        
        assert len(search_service._search_cache) == 0


class TestSearchTriggerDetector:
    """Test cases for SearchTriggerDetector class"""
    
    def test_detect_local_mental_health_intent(self):
        """Test detection of local mental health search intent"""
        test_inputs = [
            "附近有心理咨询师吗",
            "本地心理医生推荐",
            "这里哪里有心理治疗",
            "找心理咨询师",
            "心理医院在哪里"
        ]
        
        for input_text in test_inputs:
            result = SearchTriggerDetector.detect_search_intent(input_text)
            assert result["intent"] == "local_mental_health"
            assert result["confidence"] > 0.5
    
    def test_detect_crisis_resources_intent(self):
        """Test detection of crisis resources search intent"""
        test_inputs = [
            "紧急心理帮助",
            "危机干预热线",
            "自杀预防热线",
            "24小时心理急救"
        ]
        
        for input_text in test_inputs:
            result = SearchTriggerDetector.detect_search_intent(input_text)
            assert result["intent"] == "crisis_resources"
            assert result["confidence"] > 0.5
    
    def test_no_search_intent(self):
        """Test when no search intent is detected"""
        test_inputs = [
            "我今天心情不好",
            "谢谢你的帮助",
            "天气真好",
            "我想聊天"
        ]
        
        for input_text in test_inputs:
            result = SearchTriggerDetector.detect_search_intent(input_text)
            assert result["intent"] == "none"
            assert result["confidence"] == 0.0


class TestSearchServiceIntegration:
    """Integration tests for search service"""
    
    @pytest.mark.integration
    @patch('requests.get')
    def test_complete_search_flow(self, mock_get):
        """Test complete search flow from input to result"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "organic_results": [
                {
                    "title": "北京心理咨询中心",
                    "link": "https://beijing-clinic.com",
                    "snippet": "专业心理咨询服务"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        service = EnhancedSearchService("test_key")
        
        # Test search
        result = service.search_local_resources("我需要心理咨询帮助", "北京")
        
        assert result["success"]
        assert result["location"] == "北京"
        assert "query" in result
        assert len(result["resources"]) == 1
        assert result["resources"][0]["title"] == "北京心理咨询中心"
    
    @pytest.mark.integration
    def test_error_recovery(self):
        """Test error recovery and graceful degradation"""
        service = EnhancedSearchService(None)  # No API key
        
        result = service.search_local_resources("心理咨询", "北京")
        
        # Should fail gracefully
        assert not result["success"]
        assert "message" in result
        assert result["location"] == "北京"
