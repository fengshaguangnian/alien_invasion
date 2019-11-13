#coding:utf-8 # 由于中文注释可能会导致报错，所以需要在文件开头加一行魔法注释#coding：utf-8

import sys

import pygame
# 如果对引入sprite模块有疑问，转至https://www.bbsmax.com/A/amd0EAqWzg/

import game_functions as gf

from pygame.sprite import Group

from settings import Settings

from game_states import GameStates

from button import Button

from ship import Ship

from alien import Alien

from scoreboard import Scoreboard

def run_game():
    '''初始化游戏并创建一个屏幕对象'''
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    #创建button按钮
    play_button = Button(ai_settings,screen,'Play')

    #创建一个用于统计游戏信息的实例，并创建计分板
    stats = GameStates(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    #创建一艘飞船，一个子弹编组和一个外星人编组
    ship = Ship(ai_settings,screen)
    alien = Alien(ai_settings,screen)
    #创建一个用于存储子弹的编组,如果在循环内部创建这样的编组，游戏运行时将创建数千个子弹编组，导致游戏慢得像
    # 蜗牛。如果游戏停滞不前，请仔细查看主while循环中发生的情况。
    bullets = Group()
    aliens = Group()

    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #开始游戏的主循环
    while True:

        #响应按键和鼠标事件
        # gf.check_events(ship)
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            #更新移动飞船位置
            ship.update()
            #这若没有这行代码，子弹不会显示.对编组Group调用update()方法，
            # 编程将会自动对组内的每一个sprite调用update()方法。
            #详细请看https://www.jianshu.com/p/126ef3e4e36e，bullet的方法名称和sprite的方法update必须一致，不然不起作用
            #被放到了update_bullets(bullets)中,可以让主程序alien_invasion更加简洁
            # bullets.update()
            #更新子弹的位置，并删除已消失的子弹
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)

            gf.update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets)

        #每次循环时都重绘屏幕
        #gf.update_screen(ai_settings,screen,ship)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()
###


