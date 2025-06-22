"""
亲密度服务类
负责亲密度养成系统的业务逻辑
"""

import random
from typing import Dict, List
from ..data.repositories.user_profile_repository import UserProfileRepository


class IntimacyService:
    """亲密度服务类 - v5.0 心跳与羁绊系统"""
    
    def __init__(self, user_profile_repo: UserProfileRepository):
        self.user_profile_repo = user_profile_repo
    
    def add_exp(self, session_id: str, exp_to_add: int = 10) -> Dict:
        """
        添加经验值并处理升级逻辑
        
        Args:
            session_id: 会话ID
            exp_to_add: 要添加的经验值，默认10
            
        Returns:
            Dict: 包含升级状态和相关信息的字典
        """
        # 确保用户档案存在
        profile = self.user_profile_repo.find_or_create_profile(session_id)
        
        current_level = profile["intimacy_level"]
        current_exp = profile["intimacy_exp"]
        total_interactions = profile["total_interactions"]
        
        # 计算当前等级升到下一级所需的总经验值
        exp_needed = current_level * 50
        
        # 添加经验值
        new_exp = current_exp + exp_to_add
        new_level = current_level
        leveled_up = False
        level_rewards = []
        
        # 检查是否升级（可能连续升级）
        while new_exp >= exp_needed:
            new_level += 1
            new_exp -= exp_needed
            leveled_up = True
            
            # 获取升级奖励
            rewards = self._get_level_rewards(new_level)
            level_rewards.extend(rewards)
            
            # 重新计算下一级所需经验值
            exp_needed = new_level * 50
        
        # 更新数据库
        self.user_profile_repo.update_profile(
            session_id, new_level, new_exp, total_interactions + 1
        )
        
        # 返回结果
        result = {
            "leveled_up": leveled_up,
            "old_level": current_level,
            "new_level": new_level,
            "current_exp": new_exp,
            "exp_needed": new_level * 50,
            "exp_gained": exp_to_add,
            "level_rewards": level_rewards,
            "total_interactions": total_interactions + 1
        }
        
        return result
    
    def get_intimacy_info(self, session_id: str) -> Dict:
        """获取亲密度信息"""
        return self.user_profile_repo.get_level_stats(session_id)
    
    def _get_level_rewards(self, level: int) -> List[Dict]:
        """
        获取升级奖励
        
        Args:
            level: 新等级
            
        Returns:
            List[Dict]: 奖励列表
        """
        rewards = []
        
        # 基础升级奖励
        rewards.append({
            "type": "title",
            "content": f"解锁新称号：{self._get_level_title(level)}"
        })
        
        # 特殊等级奖励
        if level == 3:
            rewards.append({
                "type": "feature",
                "content": "解锁功能：小念开始记住你的喜好了！"
            })
        elif level == 5:
            rewards.append({
                "type": "gift",
                "content": "解锁新礼物：心情花束 💐"
            })
        elif level == 7:
            rewards.append({
                "type": "feature",
                "content": "解锁功能：小念会主动关心你的心情变化"
            })
        elif level == 10:
            rewards.append({
                "type": "personality",
                "content": "小念的语气变得更加亲密，像多年的老朋友"
            })
        elif level == 15:
            rewards.append({
                "type": "gift",
                "content": "解锁特殊礼物：专属回忆相册 📸"
            })
        elif level == 20:
            rewards.append({
                "type": "feature",
                "content": "解锁终极功能：心灵感应模式"
            })
        
        # 每5级的特殊奖励
        if level % 5 == 0 and level > 5:
            rewards.append({
                "type": "bonus",
                "content": f"里程碑奖励：获得 {level} 个特殊宝藏！"
            })
        
        return rewards
    
    def _get_level_title(self, level: int) -> str:
        """获取等级对应的称号"""
        titles = {
            1: "初次相遇",
            2: "渐渐熟悉",
            3: "心有灵犀",
            4: "默契伙伴",
            5: "贴心朋友",
            6: "知心好友",
            7: "心灵相通",
            8: "深度共鸣",
            9: "灵魂伴侣",
            10: "命中注定",
            15: "生死之交",
            20: "心灵感应",
            25: "永恒羁绊",
            30: "传说之友"
        }
        
        # 如果没有特定称号，使用通用格式
        if level in titles:
            return titles[level]
        elif level < 10:
            return f"亲密伙伴 Lv.{level}"
        elif level < 20:
            return f"挚友知己 Lv.{level}"
        elif level < 30:
            return f"灵魂共鸣 Lv.{level}"
        else:
            return f"传奇羁绊 Lv.{level}"
    
    def get_intimacy_context_for_ai(self, session_id: str) -> str:
        """
        为AI生成亲密度上下文信息
        
        Args:
            session_id: 会话ID
            
        Returns:
            str: 格式化的亲密度信息，用于AI提示
        """
        stats = self.get_intimacy_info(session_id)
        level = stats["current_level"]
        interactions = stats["total_interactions"]
        title = self._get_level_title(level)
        
        context = f"""=== 羁绊信息 ===
当前羁绊等级: Lv.{level} ({title})
总互动次数: {interactions}次
羁绊状态: {self._get_intimacy_status(level)}"""
        
        return context
    
    def _get_intimacy_status(self, level: int) -> str:
        """获取亲密度状态描述"""
        if level >= 20:
            return "心灵感应 - 你们已经达到了最深层的理解"
        elif level >= 15:
            return "深度羁绊 - 彼此了解得非常深入"
        elif level >= 10:
            return "亲密无间 - 像多年的老朋友一样"
        elif level >= 7:
            return "心有灵犀 - 开始能感受到彼此的情绪"
        elif level >= 5:
            return "渐入佳境 - 友谊正在加深"
        elif level >= 3:
            return "初步了解 - 开始熟悉彼此"
        else:
            return "初次相遇 - 刚刚开始认识"
    
    def calculate_exp_bonus(self, session_id: str, base_exp: int = 10) -> int:
        """
        计算经验值奖励（可以根据不同情况给予不同奖励）
        
        Args:
            session_id: 会话ID
            base_exp: 基础经验值
            
        Returns:
            int: 最终经验值
        """
        # 基础经验值
        final_exp = base_exp
        
        # 随机奖励（10%概率双倍经验）
        if random.random() < 0.1:
            final_exp *= 2
        
        # 可以根据用户行为添加更多奖励逻辑
        # 例如：连续对话奖励、特殊时间奖励等
        
        return final_exp
