"""
数据库管理模块
负责SQLite数据库的连接、初始化和基础操作
"""

import sqlite3
import os
from datetime import datetime
import streamlit as st


def get_db_connection():
    """获取数据库连接对象"""
    try:
        conn = sqlite3.connect('mind_sprite.db')
        return conn
    except Exception as e:
        st.error(f"数据库连接失败: {e}")
        return None


def init_db():
    """初始化SQLite数据库和表结构"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()

        # 创建聊天历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建核心记忆表 - 实现深度共情的关键
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS core_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                memory_type TEXT NOT NULL,  -- 'insight', 'event', 'person', 'preference'
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_history(session_id)
            )
        ''')

        # 创建宝藏盒表 - 精灵的宝藏小盒功能
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treasure_box (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                gift_type TEXT NOT NULL,
                gift_content TEXT NOT NULL,
                collected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_favorite BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (session_id) REFERENCES chat_history(session_id)
            )
        ''')

        # 创建AI缓存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_hash TEXT NOT NULL,
                model TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 【v5.0新增】创建用户档案表 - 亲密度养成系统
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL UNIQUE,
                intimacy_level INTEGER NOT NULL DEFAULT 1,
                intimacy_exp INTEGER NOT NULL DEFAULT 0,
                total_interactions INTEGER NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建索引以提高查询性能
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_session_timestamp
            ON chat_history(session_id, timestamp)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_core_memories_session_type
            ON core_memories(session_id, memory_type, timestamp)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_treasure_box_session
            ON treasure_box(session_id, collected_at)
        ''')

        # 【v5.0新增】为用户档案表创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_profiles_session
            ON user_profiles(session_id)
        ''')

        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        st.error(f"数据库初始化失败: {e}")
        return False
