# coding=utf-8
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像,并设置其rect属性
        self.image = pygame.image.load('alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """更新外星人位置"""
        if self.ai_settings.alien_direction == 1:
            self.x += self.ai_settings.alien_speed_factor
            self.rect.x = self.x

        else:
            self.x -= self.ai_settings.alien_speed_factor
            self.rect.x = self.x

    def check_edge(self):
        """检测外星人是否碰撞到屏幕边缘"""
        screen_rect = self.screen.get_rect()
        # 若外星人右边超过屏幕右界限
        if self.rect.right >= screen_rect.right:
            return True

        # 若外星人左边超过屏幕左界限
        if self.rect.left <= screen_rect.left:
            return True

        # True表示产生了一个碰撞
