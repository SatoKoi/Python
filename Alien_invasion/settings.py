# coding=utf-8
class Settings(object):
    def __init__(self):
        # 游戏窗口为1200*800像素
        self.screen_width = 1200
        self.screen_height = 800

        # 背景颜色为灰色
        self.bg_color = (230, 230, 230)

        # 飞船速度设置
        self.ship_speed_factor = 1.6            # 平时速度
        self.ship_speed_low = 0.8               # 低速速度
        self.ship_life = 3                      # 一开始玩家拥有的飞船数
        self.ship_limit = 1                     # 飞船数少于该标准,游戏失败

        # 子弹设置
        self.bullet_width = 3                   # 子弹宽
        self.bullet_height = 15                 # 子弹高度
        self.bullet_color = (230, 60, 60)       # 子弹颜色
        self.bullet_speed_factor = 1.8          # 子弹速度
        self.bullets_allowed = 5                # 最大子弹数量

        # 外星人设置
        self.alien_speed_factor = 1             # 外星人速度
        self.alien_drop_speed = 10              # 外星人下降速度
        self.alien_direction = 1                # 设置为1,默认表示向右移动; -1, 向左移动
        self.alien_points = 1.5                 # 外星人初始分值

        # 关卡设置
        self.speedup_scale = 1.1                # 加快速度
        self.points_scale = 50                  # 分数增加
        self.initialize_dynamic_settings()      # 初始化

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_direction = 1
        self.alien_points = 50                  # 外星人初始分

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points += self.points_scale

