# coding=utf-8
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('ship.bmp')              # 返回一个表示飞船的surface
        self.rect = self.image.get_rect()                       # 获取一个飞船surface属性的外接矩形
        self.screen_rect = self.screen.get_rect()               # 获取屏幕的外接矩形

        # 将每艘新飞船放在屏幕中央底部
        self.rect.centerx = self.screen_rect.centerx            # 飞船中心的x坐标居中 值为600
        self.rect.bottom = self.screen_rect.bottom              # 飞船下边缘的y坐标 值为800

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)                  # 水平坐标
        self.bottom = float(self.rect.bottom)                   # 纵向坐标

        # 移动标志,飞船默认不移动为False
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_speed_low = False
        self.shot_continue = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            if self.moving_speed_low:
                self.center += self.ai_settings.ship_speed_low
            else:
                self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > self.screen_rect.left:
            if self.moving_speed_low:
                self.center -= self.ai_settings.ship_speed_low
            else:
                self.center -= self.ai_settings.ship_speed_factor

        if self.moving_up and self.rect.top > self.screen_rect.top:
            if self.moving_speed_low:
                self.bottom -= self.ai_settings.ship_speed_low
            else:
                self.bottom -= self.ai_settings.ship_speed_factor

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            if self.moving_speed_low:
                self.bottom += self.ai_settings.ship_speed_low
            else:
                self.bottom += self.ai_settings.ship_speed_factor

        # 更新rect属性
        self.rect.centerx = self.center             # rect属性只能获取整数部分
        self.rect.bottom = self.bottom

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom