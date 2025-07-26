"""
基础仓库类
提供通用的数据库操作方法
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple, Any
import streamlit as st
from ..database import get_db_connection


class BaseRepository:
    """基础仓库类，提供通用的数据库操作方法"""
    
    def __init__(self):
        self.db_name = 'mind_sprite.db'
    
    def get_connection(self) -> Optional[sqlite3.Connection]:
        """获取数据库连接"""
        return get_db_connection()
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[List[Tuple]]:
        """执行查询并返回结果"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results

        except Exception as e:
            st.error(f"查询执行失败: {e}")
            return None
    
    def execute_insert(self, query: str, params: tuple = ()) -> bool:
        """执行插入操作"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True

        except Exception as e:
            st.error(f"插入操作失败: {e}")
            return False
    
    def execute_update(self, query: str, params: tuple = ()) -> bool:
        """执行更新操作"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True

        except Exception as e:
            st.error(f"更新操作失败: {e}")
            return False
    
    def execute_delete(self, query: str, params: tuple = ()) -> bool:
        """执行删除操作"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True

        except Exception as e:
            st.error(f"删除操作失败: {e}")
            return False
