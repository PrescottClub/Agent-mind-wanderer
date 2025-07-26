"""
聊天记录仓库类
负责聊天历史、核心记忆、宝藏盒等数据的管理
"""

from datetime import datetime
from typing import Optional, List, Tuple
import json
from .base_repository import BaseRepository


class ChatRepository(BaseRepository):
    """聊天记录仓库类"""
    
    def add_message(self, session_id: str, role: str, content: str) -> Optional[int]:
        """添加聊天消息，返回消息ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO chat_history (session_id, role, content, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (session_id, role, content, datetime.now()))

                message_id = cursor.lastrowid
                conn.commit()
                return message_id

        except Exception as e:
            print(f"添加消息失败: {e}")
            return None
    
    def get_history(self, session_id: str, limit: int = 20) -> List[Tuple[str, str, str]]:
        """获取聊天历史"""
        query = '''
            SELECT role, content, timestamp FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        params = (session_id, limit)
        results = self.execute_query(query, params)
        
        if results:
            # 返回按时间正序排列的历史记录
            return [(role, content, timestamp) for role, content, timestamp in reversed(results)]
        return []

    def get_history_paginated(self, session_id: str, limit: int = 20, offset: int = 0) -> List[Tuple[str, str, str]]:
        """获取分页聊天历史"""
        query = '''
            SELECT role, content, timestamp FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        '''
        results = self.execute_query(query, (session_id, limit, offset))
        if results:
            # 返回按时间正序排列的历史记录
            return [(role, content, timestamp) for role, content, timestamp in reversed(results)]
        return []

    def get_message_count(self, session_id: str) -> int:
        """获取会话的消息总数"""
        query = 'SELECT COUNT(*) FROM chat_history WHERE session_id = ?'
        results = self.execute_query(query, (session_id,))
        return results[0][0] if results else 0

    def get_recent_context(self, session_id: str, context_turns: int = 6) -> List[Tuple[str, str]]:
        """获取最近的对话上下文用于AI"""
        query = '''
            SELECT role, content FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        params = (session_id, context_turns * 2)  # 乘以2因为每轮有用户和助手两条消息
        results = self.execute_query(query, params)
        
        if results:
            # 按时间正序排列
            return [(role, content) for role, content in reversed(results)]
        return []
    
    def get_last_message_timestamp(self, session_id: str) -> Optional[str]:
        """获取最后一条消息的时间戳"""
        query = '''
            SELECT timestamp FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        '''
        params = (session_id,)
        results = self.execute_query(query, params)
        
        if results and results[0]:
            return results[0][0]
        return None
    
    def add_core_memory(self, session_id: str, memory_type: str, content: str) -> bool:
        """添加核心记忆"""
        query = '''
            INSERT INTO core_memories (session_id, memory_type, content, timestamp)
            VALUES (?, ?, ?, ?)
        '''
        params = (session_id, memory_type, content, datetime.now())
        return self.execute_insert(query, params)
    
    def get_core_memories(self, session_id: str, limit: int = 5) -> List[Tuple[str, str, str]]:
        """获取核心记忆"""
        query = '''
            SELECT memory_type, content, timestamp FROM core_memories
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        params = (session_id, limit)
        results = self.execute_query(query, params)
        
        if results:
            return [(memory_type, content, timestamp) for memory_type, content, timestamp in results]
        return []
    
    def add_treasure(self, session_id: str, gift_type: str, gift_content: str, is_favorite: bool = False) -> bool:
        """添加宝藏"""
        query = '''
            INSERT INTO treasure_box (session_id, gift_type, gift_content, collected_at, is_favorite)
            VALUES (?, ?, ?, ?, ?)
        '''
        params = (session_id, gift_type, gift_content, datetime.now(), is_favorite)
        return self.execute_insert(query, params)
    
    def get_treasures(self, session_id: str, limit: int = 10) -> List[Tuple[str, str, str, bool]]:
        """获取宝藏列表"""
        query = '''
            SELECT gift_type, gift_content, collected_at, is_favorite FROM treasure_box
            WHERE session_id = ?
            ORDER BY collected_at DESC
            LIMIT ?
        '''
        params = (session_id, limit)
        results = self.execute_query(query, params)
        
        if results:
            return [(gift_type, gift_content, collected_at, is_favorite) for gift_type, gift_content, collected_at, is_favorite in results]
        return []
    
    def save_cached_response(self, input_hash: str, model_name: str, response: dict) -> bool:
        """保存AI响应到缓存"""
        query = '''
            INSERT OR REPLACE INTO ai_cache (input_hash, model, response)
            VALUES (?, ?, ?)
        '''
        params = (input_hash, model_name, json.dumps(response, ensure_ascii=False))
        return self.execute_insert(query, params)
    
    def get_cached_response(self, input_hash: str, model_name: str) -> Optional[dict]:
        """获取缓存的AI响应"""
        query = '''
            SELECT response FROM ai_cache
            WHERE input_hash = ? AND model = ?
            AND created_at > datetime('now', '-1 hour')
        '''
        params = (input_hash, model_name)
        results = self.execute_query(query, params)
        
        if results and results[0]:
            try:
                return json.loads(results[0][0])
            except json.JSONDecodeError:
                return None
        return None
