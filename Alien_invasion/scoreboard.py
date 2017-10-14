# coding=utf-8
import pygame.font


class Scoreboard(object):
    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # 显示得分时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分对象
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)                # 千位加逗号
        # 创建分数图像
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分渲染为图像"""
        rounded_score = int(round(self.stats.high_score, -1))
        score_str = "{:,}".format(rounded_score)
        # 创建最高分数图像
        self.high_score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将最高分放在屏幕中间最上方
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = self.screen_rect.center
        self.high_score_rect.top = 20

    def prep_level(self):
        """将关卡等级渲染为图像"""
        # 创建等级数图像
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # 将等级放在屏幕左上方
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.left = self.screen_rect.left + 20
        self.level_image_rect.top = 20

    def prep_ships(self):
        """显示剩余船只"""
        # 创建飞船图像
        self.ship_image = self.font.render(str(self.stats.ship_lefts), True, self.text_color, self.ai_settings.bg_color)

        # 将飞船数放在左下方
        self.ship_image_rect = self.ship_image.get_rect()
        self.ship_image_rect.left = self.screen_rect.left + 20
        self.ship_image_rect.bottom = self.screen_rect.bottom

    def show_score(self):
        """显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.screen.blit(self.ship_image, self.ship_image_rect)




