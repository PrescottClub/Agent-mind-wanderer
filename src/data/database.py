"""
数据库管理模块
负责SQLite数据库的连接、初始化和基础操作
"""

import sqlite3
import os
from datetime import datetime
import streamlit as st
from .connection_pool import get_connection_pool


def get_db_connection():
    """获取数据库连接对象（使用连接池）"""
    return get_connection_pool().get_connection()


def get_db_connection_direct():
    """获取直接数据库连接（不使用连接池，仅用于初始化）"""
    try:
        conn = sqlite3.connect('mind_sprite.db')
        return conn
    except Exception as e:
        st.error(f"数据库连接失败: {e}")
        return None


def init_db():
    """初始化SQLite数据库和表结构"""
    try:
        # Use direct connection for initialization to avoid pool issues
        conn = get_db_connection_direct()
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

        # 【v5.1新增】创建主动关怀调度表 - Agent主动关怀系统
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_care (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                care_type TEXT NOT NULL,  -- 'emotion_followup', 'event_followup', 'regular_care'
                trigger_content TEXT NOT NULL,  -- 触发关怀的原始用户内容
                care_message TEXT NOT NULL,  -- 关怀消息内容
                scheduled_time DATETIME NOT NULL,  -- 预定关怀时间
                status TEXT NOT NULL DEFAULT 'pending',  -- 'pending', 'completed', 'cancelled'
                priority TEXT NOT NULL DEFAULT 'medium',  -- 'high', 'medium', 'low'
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                executed_at DATETIME NULL,
                FOREIGN KEY (session_id) REFERENCES chat_history(session_id)
            )
        ''')

        # 【v5.2新增】创建情感分析表 - 深度情感理解系统
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotion_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message_id INTEGER NOT NULL,  -- 关联的聊天记录ID
                primary_emotion TEXT NOT NULL,  -- 主要情绪类型
                emotion_intensity REAL NOT NULL,  -- 情绪强度 0.0-10.0
                emotion_valence REAL NOT NULL,  -- 情感效价 -1.0(负面)到1.0(正面)
                emotion_arousal REAL NOT NULL,  -- 情感唤醒度 0.0(平静)到1.0(激动)
                secondary_emotions TEXT,  -- 次要情绪(JSON格式)
                confidence_score REAL NOT NULL,  -- 分析置信度 0.0-1.0
                trigger_keywords TEXT,  -- 触发关键词(JSON格式)
                empathy_strategy TEXT NOT NULL,  -- 共情策略类型
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_history(session_id),
                FOREIGN KEY (message_id) REFERENCES chat_history(id)
            )
        ''')

        # 【v5.2新增】创建情感趋势表 - 情感变化轨迹追踪
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotion_trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                time_period TEXT NOT NULL,  -- 'hourly', 'daily', 'weekly'
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                avg_intensity REAL NOT NULL,  -- 平均情绪强度
                avg_valence REAL NOT NULL,  -- 平均情感效价
                dominant_emotion TEXT NOT NULL,  -- 主导情绪
                emotion_volatility REAL NOT NULL,  -- 情绪波动性 0.0-1.0
                trend_direction TEXT NOT NULL,  -- 'improving', 'stable', 'declining'
                insights TEXT,  -- 情感洞察(JSON格式)
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_history(session_id)
            )
        ''')

        # 【v5.2新增】创建共情回应表 - 深度共情历史记录
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empathy_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                analysis_id INTEGER NOT NULL,  -- 关联的情感分析ID
                empathy_type TEXT NOT NULL,  -- 'comfort', 'solution', 'companion', 'celebration'
                response_tone TEXT NOT NULL,  -- 'gentle', 'encouraging', 'supportive', 'joyful'
                key_phrases TEXT NOT NULL,  -- 核心共情短语(JSON格式)
                effectiveness_score REAL,  -- 效果评分(用户反馈) 0.0-5.0
                user_feedback TEXT,  -- 用户反馈内容
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_history(session_id),
                FOREIGN KEY (analysis_id) REFERENCES emotion_analysis(id)
            )
        ''')

        # 创建搜索缓存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cache_key TEXT UNIQUE NOT NULL,
                query TEXT NOT NULL,
                location TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME NOT NULL
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

        # 【v5.1新增】为关怀调度表创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_scheduled_care_session_time
            ON scheduled_care(session_id, scheduled_time, status)
        ''')

        # 【v5.2新增】为情感分析表创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_emotion_analysis_session_time
            ON emotion_analysis(session_id, created_at)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_emotion_analysis_emotion
            ON emotion_analysis(primary_emotion, emotion_intensity)
        ''')

        # 【v5.2新增】为情感趋势表创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_emotion_trends_session_period
            ON emotion_trends(session_id, time_period, start_time)
        ''')

        # 【v5.2新增】为共情回应表创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_empathy_responses_session_type
            ON empathy_responses(session_id, empathy_type, created_at)
        ''')

        # 为搜索缓存表创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_search_cache_key_expires
            ON search_cache(cache_key, expires_at)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_search_cache_location_expires
            ON search_cache(location, expires_at)
        ''')

        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        st.error(f"数据库初始化失败: {e}")
        return False
