"""
主动关怀调度服务
实现Agent的主动关怀和跟进功能，让小念能够记住重要事件并主动关心用户
"""

from datetime import datetime, timedelta
import re
from typing import List, Dict, Optional, Tuple
from src.data.database import get_db_connection


class CareType:
    """关怀类型枚举"""
    EMOTION_FOLLOWUP = "emotion_followup"  # 情绪跟进
    EVENT_FOLLOWUP = "event_followup"      # 事件跟进
    REGULAR_CARE = "regular_care"          # 定期关怀


class CareSchedulerService:
    """主动关怀调度服务"""
    
    def __init__(self):
        # 情绪关键词检测
        self.emotion_keywords = {
            'negative_immediate': {  # 需要1-2天跟进的负面情绪
                'keywords': ['紧张', '焦虑', '担心', '害怕', '不安', '恐慌', '压力大', '压力太大', '撑不下去', '要崩溃'],
                'followup_days': 1
            },
            'negative_extended': {  # 需要3-5天跟进的负面情绪
                'keywords': ['抑郁', '低落', '难过', '失望', '沮丧', '孤独', '疲惫', '无聊', '没意思', '没劲', '心累'],
                'followup_days': 3
            },
            'conflict': {  # 人际冲突，1天跟进
                'keywords': ['吵架', '争执', '矛盾', '冲突', '分手', '闹翻', '生气', '愤怒', '讨厌'],
                'followup_days': 1
            }
        }
        
        # 重要事件关键词检测
        self.event_keywords = {
            'exam_interview': {  # 考试/面试类
                'keywords': ['考试', '面试', '答辩', '比赛', '演讲', '汇报'],
                'followup_days': 2
            },
            'health': {  # 健康相关
                'keywords': ['看病', '检查', '手术', '体检', '治疗'],
                'followup_days': 3
            },
            'work_study': {  # 工作学习相关  
                'keywords': ['上班', '入职', '辞职', '开学', '毕业', '实习'],
                'followup_days': 7
            },
            'relationship': {  # 感情相关
                'keywords': ['表白', '约会', '见家长', '求婚', '结婚'],
                'followup_days': 2
            },
            'travel': {  # 出行相关
                'keywords': ['旅行', '出差', '搬家', '出国'],
                'followup_days': 5
            }
        }
        
        # 关怀消息模板
        self.care_templates = {
            CareType.EMOTION_FOLLOWUP: [
                "小念一直记挂着你呢~ {trigger_summary}，现在感觉怎么样？💙",
                "这几天过得还好吗？小念记得你之前{trigger_summary}，心情好一些了吗？🌸",
                "小念想起你之前说{trigger_summary}，现在情况改善了吗？小念一直在这里陪着你哦💕"
            ],
            CareType.EVENT_FOLLOWUP: [
                "小念记得你{trigger_summary}，结果怎么样呀？无论如何，小念都为你骄傲！✨",
                "之前你提到要{trigger_summary}，进展如何？小念很关心你呢~💫",
                "想起你说的{trigger_summary}，现在情况怎样？小念一直在默默为你加油哦！🌟"
            ],
            CareType.REGULAR_CARE: [
                "小念好想你呀~最近过得怎么样？有什么开心的事情要分享吗？💕",
                "好久不见了呢！小念一直在想你，最近有什么新鲜事吗？🌸",
                "小念在这里等你好久啦~快来和小念聊聊最近的生活吧！✨"
            ]
        }
    
    def detect_care_opportunities(self, user_input: str, session_id: str) -> List[Dict]:
        """
        检测用户输入中的关怀机会
        
        Args:
            user_input: 用户输入内容
            session_id: 会话ID
            
        Returns:
            关怀任务列表
        """
        care_tasks = []
        
        # 检测情绪关怀机会
        emotion_tasks = self._detect_emotion_care(user_input, session_id)
        care_tasks.extend(emotion_tasks)
        
        # 检测事件关怀机会
        event_tasks = self._detect_event_care(user_input, session_id)
        care_tasks.extend(event_tasks)
        
        return care_tasks
    
    def _detect_emotion_care(self, user_input: str, session_id: str) -> List[Dict]:
        """检测情绪关怀机会"""
        care_tasks = []
        
        for emotion_type, config in self.emotion_keywords.items():
            for keyword in config['keywords']:
                if keyword in user_input:
                    # 创建关怀任务
                    scheduled_time = datetime.now() + timedelta(days=config['followup_days'])
                    trigger_summary = self._extract_trigger_summary(user_input, keyword)
                    
                    care_task = {
                        'session_id': session_id,
                        'care_type': CareType.EMOTION_FOLLOWUP,
                        'trigger_content': user_input,
                        'care_message': self._generate_care_message(
                            CareType.EMOTION_FOLLOWUP, 
                            trigger_summary
                        ),
                        'scheduled_time': scheduled_time,
                        'priority': 'high' if emotion_type == 'negative_immediate' else 'medium'
                    }
                    care_tasks.append(care_task)
                    break  # 每种情绪类型只创建一个任务
        
        return care_tasks
    
    def _detect_event_care(self, user_input: str, session_id: str) -> List[Dict]:
        """检测事件关怀机会"""
        care_tasks = []
        
        # 检测未来时态的重要事件
        future_patterns = [
            r'明天.*?([^，。！？]*)',
            r'后天.*?([^，。！？]*)',
            r'下周.*?([^，。！？]*)',
            r'准备.*?([^，。！？]*)',
            r'要去.*?([^，。！？]*)',
            r'计划.*?([^，。！？]*)'
        ]
        
        for event_type, config in self.event_keywords.items():
            for keyword in config['keywords']:
                if keyword in user_input:
                    # 检查是否为未来事件
                    is_future_event = False
                    for pattern in future_patterns:
                        if re.search(pattern, user_input) and keyword in user_input:
                            is_future_event = True
                            break
                    
                    if is_future_event or any(word in user_input for word in ['明天', '后天', '下周', '准备', '要去']):
                        scheduled_time = datetime.now() + timedelta(days=config['followup_days'])
                        trigger_summary = self._extract_trigger_summary(user_input, keyword)
                        
                        care_task = {
                            'session_id': session_id,
                            'care_type': CareType.EVENT_FOLLOWUP,
                            'trigger_content': user_input,
                            'care_message': self._generate_care_message(
                                CareType.EVENT_FOLLOWUP,
                                trigger_summary
                            ),
                            'scheduled_time': scheduled_time,
                            'priority': 'medium'
                        }
                        care_tasks.append(care_task)
                        break
        
        return care_tasks
    
    def _extract_trigger_summary(self, user_input: str, keyword: str) -> str:
        """提取触发关怀的事件摘要"""
        # 简单的事件摘要提取逻辑
        sentences = re.split(r'[。！？\n]', user_input)
        for sentence in sentences:
            if keyword in sentence:
                # 清理句子，保留核心信息
                summary = sentence.strip()
                if len(summary) > 30:
                    summary = summary[:30] + "..."
                return summary
        return f"提到了{keyword}"
    
    def _generate_care_message(self, care_type: str, trigger_summary: str) -> str:
        """生成关怀消息"""
        import random
        templates = self.care_templates.get(care_type, [])
        if not templates:
            return f"小念记得你之前{trigger_summary}，现在怎么样了？💕"
        
        template = random.choice(templates)
        return template.format(trigger_summary=trigger_summary)
    
    def schedule_care_task(self, care_task: Dict) -> bool:
        """将关怀任务保存到数据库"""
        try:
            conn = get_db_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO scheduled_care 
                (session_id, care_type, trigger_content, care_message, scheduled_time, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                care_task['session_id'],
                care_task['care_type'],
                care_task['trigger_content'],
                care_task['care_message'],
                care_task['scheduled_time'].isoformat(),
                care_task['priority']
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"保存关怀任务失败: {e}")
            return False
    
    def get_pending_care_tasks(self, session_id: str) -> List[Dict]:
        """获取待执行的关怀任务"""
        try:
            conn = get_db_connection()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, care_type, trigger_content, care_message, scheduled_time, priority
                FROM scheduled_care
                WHERE session_id = ? 
                  AND status = 'pending'
                  AND scheduled_time <= ?
                ORDER BY priority DESC, scheduled_time ASC
            ''', (session_id, datetime.now().isoformat()))
            
            tasks = []
            for row in cursor.fetchall():
                tasks.append({
                    'id': row[0],
                    'care_type': row[1],
                    'trigger_content': row[2],
                    'care_message': row[3],
                    'scheduled_time': row[4],
                    'priority': row[5]
                })
            
            conn.close()
            return tasks
            
        except Exception as e:
            print(f"获取关怀任务失败: {e}")
            return []
    
    def mark_care_task_completed(self, task_id: int) -> bool:
        """标记关怀任务为已完成"""
        try:
            conn = get_db_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE scheduled_care 
                SET status = 'completed', executed_at = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), task_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"更新关怀任务状态失败: {e}")
            return False
    
    def cleanup_old_tasks(self, days_old: int = 30) -> bool:
        """清理过期的关怀任务"""
        try:
            conn = get_db_connection()
            if not conn:
                return False
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM scheduled_care
                WHERE created_at < ? AND status IN ('completed', 'cancelled')
            ''', (cutoff_date.isoformat(),))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"清理关怀任务失败: {e}")
            return False
    
    def should_create_regular_care(self, session_id: str) -> bool:
        """判断是否应该创建定期关怀任务"""
        try:
            conn = get_db_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # 检查最近是否有定期关怀任务
            cursor.execute('''
                SELECT COUNT(*) FROM scheduled_care
                WHERE session_id = ? 
                  AND care_type = 'regular_care'
                  AND created_at > ?
            ''', (session_id, (datetime.now() - timedelta(days=7)).isoformat()))
            
            recent_regular_care = cursor.fetchone()[0]
            
            # 检查用户活跃度
            cursor.execute('''
                SELECT COUNT(*) FROM chat_history
                WHERE session_id = ?
                  AND timestamp > ?
            ''', (session_id, (datetime.now() - timedelta(days=14)).isoformat()))
            
            recent_interactions = cursor.fetchone()[0]
            
            conn.close()
            
            # 如果最近没有定期关怀且用户不太活跃，则创建定期关怀
            return recent_regular_care == 0 and recent_interactions < 10
            
        except Exception as e:
            print(f"检查定期关怀条件失败: {e}")
            return False
    
    def create_regular_care_task(self, session_id: str) -> Optional[Dict]:
        """创建定期关怀任务"""
        if not self.should_create_regular_care(session_id):
            return None
        
        scheduled_time = datetime.now() + timedelta(days=7)  # 7天后关怀
        care_message = self._generate_care_message(CareType.REGULAR_CARE, "")
        
        care_task = {
            'session_id': session_id,
            'care_type': CareType.REGULAR_CARE,
            'trigger_content': "系统生成的定期关怀",
            'care_message': care_message,
            'scheduled_time': scheduled_time,
            'priority': 'low'
        }
        
        if self.schedule_care_task(care_task):
            return care_task
        
        return None 