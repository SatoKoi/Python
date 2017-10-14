# coding=utf-8
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_LSHIFT:
        ship.moving_speed_low = True
    if event.key == pygame.K_z:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_LSHIFT:
        ship.moving_speed_low = False
    if event.key == pygame.K_z:
        ship.shot_continue = False


def check_events(ai_settings, stats, screen, sbd, ship, aliens, bullets, play_button):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        # 游戏关闭
        if event.type == pygame.QUIT:
            sys.exit()

        # 键盘键按下
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        # 键盘键松开
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        # 鼠标键点击
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, screen, sbd, ship, aliens, bullets, play_button, mouse_x, mouse_y)


def update_screen(ai_settings, stats, screen, sbd, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""

    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制外星人
    aliens.draw(screen)

    # 绘制飞船
    ship.blitme()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 显示得分
    sbd.show_score()

    # 让绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, stats, screen, sbd, ship, bullets, aliens):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    check_bullet_alien_collisions(ai_settings, stats, screen, sbd, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_rows(ai_settings, ship_height, alien_height):
    """获取外星人行数"""
    # 将屏幕高度减去第一行外星人的上边距（外星人高度）、飞船的高度以及最初外星人群与飞船的距离（外星人高度的两倍）
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))               # 可容纳的外星人函数
    return number_rows


def get_number_alien_x(ai_settings, alien_width):
    """计算每行最多可容纳多少行外星人"""
    # 将屏幕宽度减去两倍外星人的宽度得到可允许的水平空间
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width                                              # 外接矩形宽
    alien.x = alien_width + 2 * alien_width * alien_number                      # 计算外星人当前水平位置
    alien.rect.x = alien.x                                                      # 外星人水平位置
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number       # 外星人竖直位置
    aliens.add(alien)                                                           # 向外星人编组加入该外星人


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)

    # 一行能容纳的外星人数
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    # 能容纳的外星人行数
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(ai_settings, stats, screen, sbd, ship, aliens, bullets):
    """检查外星人是否触碰到屏幕左右边缘, 更新每个外星人位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):                    # 接受两个实参,一个精灵,一个编组
        ship_hit(ai_settings, stats, screen, sbd, ship, aliens, bullets)

    # 检测外星人和屏幕底端的碰撞
    check_aliens_bottom(ai_settings, stats, screen, sbd, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达屏幕边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人一起向下移动"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.alien_direction *= -1                                           # 改变方向标记


def check_bullet_alien_collisions(ai_settings, stats, screen, sbd, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 确保每个被消灭的外星人都能记成分数
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sbd.prep_score()
            check_high_score(stats, sbd)
            sbd.prep_high_score()

    # 若现有的外星人为0
    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        stats.level += 1
        sbd.prep_level()
        ai_settings.increase_speed()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, stats, screen, sbd, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ship_lefts > ai_settings.ship_limit:
        # 飞船数减一
        stats.ship_lefts -= 1
        sbd.prep_ships()
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人并放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.3)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)              # 显示光标
        ai_settings.initialize_dynamic_settings()


def check_aliens_bottom(ai_settings, stats, screen, sbd, ship, aliens, bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sbd, ship, aliens, bullets)


def check_play_button(ai_settings, stats, screen, sbd, ship, aliens, bullets, play_button, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)         # 检查鼠标单击位置是否在play_button.rect这个矩形内
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)                         # 隐藏光标
        stats.reset_stats()                                     # 重置游戏统计信息
        stats.game_active = True                                # 设置活动状态为True
        aliens.empty()                                          # 清空外星人列表
        bullets.empty()                                         # 清空子弹列表
        create_fleet(ai_settings, screen, ship, aliens)         # 创建新的外星人群
        ship.center_ship()                                      # 让飞船居中

        # 此时重新绘制计分板
        sbd.prep_score()
        sbd.prep_level()
        sbd.prep_ships()
        update_screen(ai_settings, stats, screen, sbd, ship, aliens, bullets, play_button)


def check_high_score(stats, sbd):
    """检测是否产生最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sbd.prep_high_score()

