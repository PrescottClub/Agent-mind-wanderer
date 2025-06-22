"""
用户档案仓库类
负责亲密度养成系统的数据管理
"""

from datetime import datetime
from typing import Optional, Dict, Tuple
from .base_repository import BaseRepository


class UserProfileRepository(BaseRepository):
    """用户档案仓库类 - v5.0 亲密度养成系统"""
    
    def get_profile(self, session_id: str) -> Optional[Dict]:
        """获取用户档案信息"""
        query = '''
            SELECT intimacy_level, intimacy_exp, total_interactions, created_at, updated_at
            FROM user_profiles
            WHERE session_id = ?
        '''
        params = (session_id,)
        results = self.execute_query(query, params)
        
        if results and results[0]:
            level, exp, total_interactions, created_at, updated_at = results[0]
            return {
                "intimacy_level": level,
                "intimacy_exp": exp,
                "total_interactions": total_interactions,
                "created_at": created_at,
                "updated_at": updated_at
            }
        return None
    
    def update_profile(self, session_id: str, level: int, exp: int, total_interactions: int = None) -> bool:
        """更新用户档案信息"""
        if total_interactions is not None:
            query = '''
                UPDATE user_profiles 
                SET intimacy_level = ?, intimacy_exp = ?, total_interactions = ?, updated_at = ?
                WHERE session_id = ?
            '''
            params = (level, exp, total_interactions, datetime.now(), session_id)
        else:
            query = '''
                UPDATE user_profiles 
                SET intimacy_level = ?, intimacy_exp = ?, updated_at = ?
                WHERE session_id = ?
            '''
            params = (level, exp, datetime.now(), session_id)
        
        return self.execute_update(query, params)
    
    def find_or_create_profile(self, session_id: str) -> Dict:
        """查找或创建用户档案"""
        # 先尝试获取现有档案
        profile = self.get_profile(session_id)
        
        if profile:
            return profile
        
        # 如果不存在，创建新档案
        query = '''
            INSERT INTO user_profiles (session_id, intimacy_level, intimacy_exp, total_interactions, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        params = (session_id, 1, 0, 0, datetime.now(), datetime.now())
        
        if self.execute_insert(query, params):
            # 返回新创建的档案
            return {
                "intimacy_level": 1,
                "intimacy_exp": 0,
                "total_interactions": 0,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        else:
            # 创建失败，返回默认值
            return {
                "intimacy_level": 1,
                "intimacy_exp": 0,
                "total_interactions": 0,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
    
    def increment_interactions(self, session_id: str) -> bool:
        """增加互动次数"""
        query = '''
            UPDATE user_profiles 
            SET total_interactions = total_interactions + 1, updated_at = ?
            WHERE session_id = ?
        '''
        params = (datetime.now(), session_id)
        return self.execute_update(query, params)
    
    def get_level_stats(self, session_id: str) -> Dict:
        """获取等级统计信息"""
        profile = self.get_profile(session_id)
        if not profile:
            profile = self.find_or_create_profile(session_id)
        
        current_level = profile["intimacy_level"]
        current_exp = profile["intimacy_exp"]
        
        # 计算升级所需经验值 (等级 * 50)
        exp_needed = current_level * 50
        
        # 计算经验值进度百分比
        exp_progress = min(current_exp / exp_needed, 1.0) if exp_needed > 0 else 0.0
        
        return {
            "current_level": current_level,
            "current_exp": current_exp,
            "exp_needed": exp_needed,
            "exp_progress": exp_progress,
            "total_interactions": profile["total_interactions"]
        }
    
    def get_all_profiles_count(self) -> int:
        """获取总用户数（用于统计）"""
        query = 'SELECT COUNT(*) FROM user_profiles'
        results = self.execute_query(query)
        
        if results and results[0]:
            return results[0][0]
        return 0
    
    def get_top_levels(self, limit: int = 10) -> list:
        """获取等级排行榜（可选功能）"""
        query = '''
            SELECT session_id, intimacy_level, intimacy_exp, total_interactions
            FROM user_profiles
            ORDER BY intimacy_level DESC, intimacy_exp DESC
            LIMIT ?
        '''
        params = (limit,)
        results = self.execute_query(query, params)
        
        if results:
            return [
                {
                    "session_id": session_id[:8] + "...",  # 隐私保护，只显示前8位
                    "level": level,
                    "exp": exp,
                    "interactions": interactions
                }
                for session_id, level, exp, interactions in results
            ]
        return []
