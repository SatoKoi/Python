# coding=utf-8


class Gamestats(object):
    """跟踪统计游戏的信息"""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False                                 # 游戏处于非活动状态
        self.score = 0
        self.high_score = 0                                      # 记录玩家最高分
        self.level = 1

    def reset_stats(self):
        """初始化在游戏中可能变化的统计信息"""
        self.ship_lefts = self.ai_settings.ship_life             # 飞船数重置
        self.score = 0                                           # 分数置零
        self.level = 1                                           # 关卡重置
