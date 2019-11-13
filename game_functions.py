#coding:utf-8 # 由于中文注释可能会导致报错，所以需要在文件开头加一行魔法注释#coding：utf-8

import sys

import pygame

from time import sleep

from bullet import Bullet

from alien import Alien

def check_keydown_events(event,ai_settings,screen,sb,ship,bullets,stats,aliens):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        #向右移动飞船
        # ship.rect.centerx += 1
        ship.moving_right = True
        # print('KEYDOWN execute')
    elif event.key == pygame.K_LEFT:
        #向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        #向上移动飞船
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        #向下移动飞船
        ship.moving_down = True
    elif event.key == pygame.K_SPACE and stats.game_active:
        #这样可以保证在游戏结束时，按空格键将不能继续发射子弹
        fire_bullet(ai_settings,screen,ship,bullets)
    #游戏运行之后，按q键可以退出
    elif event.key == pygame.K_q:
        sys.exit()
    #游戏需要开始时，按p键可以开始游戏
    elif event.key == pygame.K_p:
        check_game_start(ai_settings,screen,stats,sb,ship,aliens,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
    '''限制出现在屏幕范围内的子弹数量,如果还没有达到限制，就可以再发射子弹'''
    if len(bullets) < ai_settings.bullets_allowed:
        #创建一颗子弹，并使其加入到编组bullets中
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
        #print('KEYUP execute')
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        #退出
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,sb,ship,bullets,stats,aliens)

        #下面的这段代码是用来制止用户在按一下右方向键后，飞船一直移动的问题，可以屏蔽后试一下效果
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x , mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    #用户单击Play按钮开始新游戏
    #知识点：rect.collidepoint
    # 一种是矩形区域的碰撞检测，API是：rect.collidepoint(position)返回True时代表position左边在rect的范围内
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    #当鼠标左键点击了play按钮区域并且游戏处于不活跃状态，点击按钮才能触发相应功能
    if button_clicked and not stats.game_active:
        game_reset(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_game_start(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''用户开始新游戏，当用户按下p键时调用，开始新游戏，和play按钮功能类似'''
    if not stats.game_active:
        game_reset(ai_settings,screen,stats,sb,ship,aliens,bullets)

def game_reset(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''游戏重新开始时，重置游戏信息'''
    #重置游戏的速度设置
    ai_settings.initialize_dynamic_settings()
    #隐藏光标
    pygame.mouse.set_visible(False)
    #重置游戏统计信息
    stats.reset_states()
    stats.game_active = True

    #重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    #清空外星人和子弹列表
    aliens.empty()
    bullets.empty()

    #创建一群新的外星人，并将飞船重置在屏幕底部中央
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_colors)

    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #单个飞船
    ship.blitme()
    # aliens.blitme()
    #多个外星人绘制
    aliens.draw(screen)
    #显示得分
    sb.show_score()


    #如果游戏处于非活跃状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''更新子弹的位置，并删除已消失的子弹'''
    #更新子弹的位置，用于主程序中alien_invasion中才有意义
    bullets.update()

    #删除已消失的子弹
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #用于检测当前剩余子弹的数量，但是循环打印该信息会大大降低运行速度
    #print(len(bullets))
    #检查是否有子弹击中了外星人
    #如果是这样，就删除相应的子弹和外星人
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #方法sprite.groupcollide()将每颗子弹的rect同每个外星人的rect进行比较，并返回一个字典，其中包含发生了碰撞的子弹和
    # 外星人。在这个字典中，每个键都是一颗子弹，而相应的值都是被击中的外星人
    #新增的这行代码遍历编组bullets中的每颗子弹，再遍历编组aliens中的每个外星人。每当
    #有子弹和外星人的rect重叠时， groupcollide()就在它返回的字典中添加一个键值对。两个实参
    # True告诉Pygame删除发生碰撞的子弹和外星人。（要模拟能够穿行到屏幕顶端的高能子弹——消
    # 灭它击中的每个外星人，可将第一个布尔实参设置为False，并让第二个布尔实参为True。这样
    # 被击中的外星人将消失，但所有的子弹都始终有效，直到抵达屏幕顶端后消失。）
    '''响应子弹和外星人的碰撞'''
    #删除碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    if collisions:
        #collisions是字典，子弹是键，.values()是取其键值
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        #删除当前的子弹并新建一批外星人
        # 使用方法empty()删除编组中余下的所有精灵，从而删除现有的所有子弹
        #如果整群外星人都被消灭，就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()

        #提升等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings,screen,ship,aliens)

def get_number_aliens_x(ai_settings,alien_width):
    '''外星人间距为外星人宽度,计算每行可容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_row(ai_settings,ship_height,alien_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    '''创建一个外星人并放在当前行'''
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + alien_width * 2 * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + 50
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    '''创建外星人群'''
    #创建一个外星人，并计算每行可容纳的外星人数量
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_row(ai_settings,ship.rect.height,alien.rect.height)

    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建一个外星人并将其加入当前行
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    '''有外星人到达边缘时采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    '''将整群外星人下移，并改变它们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0 :
        #将ships_left减1
        stats.ships_left -= 1

        #更新记分牌
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船重置在屏幕底部中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        #暂停,sleep() 函数推迟调用线程的运行，可通过参数secs指秒数，表示进程挂起的时间。
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets):
    '''检查是否有外星人达到屏幕底部'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 和飞船与外星人相撞同样处理
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
            break

def check_high_score(stats,sb):
    '''检查是否诞生了新的最高得分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        loadfile_high_score(stats)
        sb.prep_high_score()

def loadfile_high_score(stats):
    '''将最高得分写入文件中'''
    path = 'images/high_score_loadfile.txt'
    #这里用（path，“w+”），因为可以读写，并且对以前的文件进行清空，如果不清空的话要用r+
    with open(path,"w+") as file:
        file.write(str(stats.high_score))

def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
    '''检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #检测外星人和飞船之间的碰撞
    #方法spritecollideany()接受两个实参：一个精灵和一个编组。它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生了
    # 碰撞的成员后就停止遍历编组。在这里，它遍历编组aliens，并返回它找到的第一个与飞船发生了碰撞的外星人。
    # 如果没有发生碰撞， spritecollideany()将返回None
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets)

