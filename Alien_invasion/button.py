# coding=utf-8
import pygame.font                                  # 将文本渲染到屏幕上


class Button(object):
    def __init__(self, ai_settings, screen, msg):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (255, 0, 0)             # 设置亮绿色
        self.text_color = (255, 255, 255)           # 设置灰白色
        self.font = pygame.font.SysFont(None, 48)   # 指定字体渲染文本,None使用默认字体,48指定字体字号

        # 创建按钮的rect对象,并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg渲染为图像,并使其在按钮上居中"""
        # 布尔实参指定反锯齿功能,text_color指定文本颜色,button_color指定按钮颜色
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
