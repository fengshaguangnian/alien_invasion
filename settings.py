#coding:utf-8 # 由于中文注释可能会导致报错，所以需要在文件开头加一行魔法注释#coding：utf-8

class Settings():
    '''存储《外星人入侵》的所有设置的类'''

    def __init__(self):
        #初始化游戏的静态设置
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colors = (0, 251, 240)
        #飞船设置
        #飞船的移动速度
        #飞船的生命数限制
        self.ship_limit = 3

        #子弹设置
        #子弹数限制
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        #外星人设置，水平移动速度及下落移动速度
        self.fleet_drop_speed = 10
        #以某种速度提升游戏难度
        self.speedup_scale = 1.1
        #外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''初始化随游戏进程而变化的速度'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #fleet_direction为1时表示向右移动，为-1时表示向左移动.将方向设置为1或者-1，这个设想值得以借鉴，使得计算较方便。
        self.fleet_direction = 1

        #计分
        self.alien_points = 50

    def increase_speed(self):
        '''提高速度设置和外星人点数'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

