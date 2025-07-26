"""
搜索结果缓存仓库
用于缓存搜索结果以提高性能和减少API调用
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from .base_repository import BaseRepository


class SearchCacheRepository(BaseRepository):
    """搜索结果缓存仓库"""
    
    def save_search_result(self, query: str, location: str, results: Dict) -> bool:
        """
        保存搜索结果到缓存
        
        Args:
            query (str): 搜索查询
            location (str): 搜索位置
            results (Dict): 搜索结果
            
        Returns:
            bool: 是否保存成功
        """
        cache_key = f"{query}_{location}".lower().replace(" ", "_")
        
        query_sql = '''
            INSERT OR REPLACE INTO search_cache 
            (cache_key, query, location, results, created_at, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        expires_at = datetime.now() + timedelta(hours=24)
        
        params = (
            cache_key,
            query,
            location,
            json.dumps(results, ensure_ascii=False),
            datetime.now().isoformat(),
            expires_at.isoformat()
        )
        
        return self.execute_insert(query_sql, params)
    
    def get_cached_result(self, query: str, location: str) -> Optional[Dict]:
        """
        获取缓存的搜索结果（如果有效）
        
        Args:
            query (str): 搜索查询
            location (str): 搜索位置
            
        Returns:
            Optional[Dict]: 缓存的搜索结果，如果不存在或已过期则返回None
        """
        cache_key = f"{query}_{location}".lower().replace(" ", "_")
        
        query_sql = '''
            SELECT results, expires_at FROM search_cache 
            WHERE cache_key = ? AND expires_at > ?
        '''
        
        results = self.execute_query(query_sql, (cache_key, datetime.now().isoformat()))
        
        if results:
            try:
                return json.loads(results[0][0])
            except json.JSONDecodeError:
                # 如果JSON解析失败，删除损坏的缓存条目
                self.delete_cache_entry(cache_key)
                return None
        
        return None
    
    def delete_cache_entry(self, cache_key: str) -> bool:
        """
        删除特定的缓存条目
        
        Args:
            cache_key (str): 缓存键
            
        Returns:
            bool: 是否删除成功
        """
        query = 'DELETE FROM search_cache WHERE cache_key = ?'
        return self.execute_delete(query, (cache_key,))
    
    def cleanup_expired_cache(self) -> int:
        """
        清理过期的缓存条目
        
        Returns:
            int: 删除的条目数量
        """
        # 首先获取过期条目的数量
        count_query = 'SELECT COUNT(*) FROM search_cache WHERE expires_at <= ?'
        count_results = self.execute_query(count_query, (datetime.now().isoformat(),))
        expired_count = count_results[0][0] if count_results else 0
        
        # 删除过期条目
        delete_query = 'DELETE FROM search_cache WHERE expires_at <= ?'
        success = self.execute_delete(delete_query, (datetime.now().isoformat(),))
        
        return expired_count if success else 0
    
    def get_cache_stats(self) -> Dict:
        """
        获取缓存统计信息
        
        Returns:
            Dict: 缓存统计信息
        """
        stats = {
            'total_entries': 0,
            'expired_entries': 0,
            'valid_entries': 0,
            'cache_size_mb': 0.0
        }
        
        # 总条目数
        total_query = 'SELECT COUNT(*) FROM search_cache'
        total_results = self.execute_query(total_query)
        if total_results:
            stats['total_entries'] = total_results[0][0]
        
        # 过期条目数
        expired_query = 'SELECT COUNT(*) FROM search_cache WHERE expires_at <= ?'
        expired_results = self.execute_query(expired_query, (datetime.now().isoformat(),))
        if expired_results:
            stats['expired_entries'] = expired_results[0][0]
        
        # 有效条目数
        stats['valid_entries'] = stats['total_entries'] - stats['expired_entries']
        
        # 缓存大小估算（基于结果字段的长度）
        size_query = 'SELECT SUM(LENGTH(results)) FROM search_cache WHERE expires_at > ?'
        size_results = self.execute_query(size_query, (datetime.now().isoformat(),))
        if size_results and size_results[0][0]:
            stats['cache_size_mb'] = round(size_results[0][0] / (1024 * 1024), 2)
        
        return stats
    
    def get_recent_searches(self, limit: int = 10) -> List[Dict]:
        """
        获取最近的搜索记录
        
        Args:
            limit (int): 返回的记录数量限制
            
        Returns:
            List[Dict]: 最近的搜索记录
        """
        query = '''
            SELECT query, location, created_at, expires_at 
            FROM search_cache 
            WHERE expires_at > ?
            ORDER BY created_at DESC 
            LIMIT ?
        '''
        
        results = self.execute_query(query, (datetime.now().isoformat(), limit))
        
        if results:
            return [
                {
                    'query': row[0],
                    'location': row[1],
                    'created_at': row[2],
                    'expires_at': row[3]
                }
                for row in results
            ]
        
        return []
    
    def clear_all_cache(self) -> bool:
        """
        清除所有缓存条目
        
        Returns:
            bool: 是否清除成功
        """
        query = 'DELETE FROM search_cache'
        return self.execute_delete(query)
    
    def get_cache_by_location(self, location: str) -> List[Dict]:
        """
        获取特定位置的所有有效缓存
        
        Args:
            location (str): 搜索位置
            
        Returns:
            List[Dict]: 该位置的缓存记录
        """
        query = '''
            SELECT query, results, created_at 
            FROM search_cache 
            WHERE location = ? AND expires_at > ?
            ORDER BY created_at DESC
        '''
        
        results = self.execute_query(query, (location, datetime.now().isoformat()))
        
        if results:
            cache_entries = []
            for row in results:
                try:
                    parsed_results = json.loads(row[1])
                    cache_entries.append({
                        'query': row[0],
                        'results': parsed_results,
                        'created_at': row[2]
                    })
                except json.JSONDecodeError:
                    # 跳过损坏的条目
                    continue
            
            return cache_entries
        
        return []
    
    def update_cache_expiry(self, cache_key: str, new_expiry: datetime) -> bool:
        """
        更新缓存条目的过期时间
        
        Args:
            cache_key (str): 缓存键
            new_expiry (datetime): 新的过期时间
            
        Returns:
            bool: 是否更新成功
        """
        query = 'UPDATE search_cache SET expires_at = ? WHERE cache_key = ?'
        return self.execute_update(query, (new_expiry.isoformat(), cache_key))
