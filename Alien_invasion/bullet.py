# coding=utf-8
import pygame
from pygame.sprite import Sprite    # 通过使用精灵，可将游戏中相关的元素编组


class Bullet(Sprite):
    """对一个飞船发射子弹管理的类"""
    def __init__(self, ai_settings, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen

        # 在(0, 0)处创建一个表示子弹的矩形，再设置正确的位置
        # (0, 0)表示矩形左上角x, y的位置,在提供宽和高
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                  ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx                       # 矩形中心置于飞船中心
        self.rect.top = ship.rect.top                               # 矩形高置于飞船高

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color                       # 子弹颜色
        self.speed_factor = ai_settings.bullet_speed_factor         # 子弹速度

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor

        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)




