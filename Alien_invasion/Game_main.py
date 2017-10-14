# coding=utf-8
import game_functions as gf
import pygame
from button import Button
from settings import Settings
from ship import Ship
from scoreboard import Scoreboard
from game_stats import Gamestats


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()                                       # 初始化背景设置
    ai_settings = Settings()                            # 设置类
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))       # 创建显示窗口,传入元组为游戏窗口尺寸
    pygame.display.set_caption("Alien invasion")        # 标题为外星人入侵
    play_button = Button(ai_settings, screen, "Play")   # 创建Play按钮

    ship = Ship(ai_settings, screen)                    # 创建一艘飞船
    aliens = pygame.sprite.Group()                      # 创建一个用于存储外星人群的编组
    bullets = pygame.sprite.Group()                     # 创建一个用于存储子弹的编组
    stats = Gamestats(ai_settings)                      # 开始
    sbd = Scoreboard(ai_settings, screen, stats)        # 创建计数板
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, stats, screen, sbd, ship, aliens, bullets, play_button)     # 键盘鼠标响应检测
        if stats.game_active:
            ship.update()                                                                        # 更新飞船位置
            gf.update_aliens(ai_settings, stats, screen, sbd, ship, aliens, bullets)             # 更新外星人
            gf.update_bullets(ai_settings, stats, screen, sbd, ship, bullets, aliens)            # 更新子弹位置
        gf.update_screen(ai_settings, stats, screen, sbd, ship, aliens, bullets, play_button)    # 更新屏幕

run_game()
