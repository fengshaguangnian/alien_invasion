#coding:utf-8 # 由于中文注释可能会导致报错，所以需要在文件开头加一行魔法注释#coding：utf-8

import pygame

from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    '''显示得分信息的类'''
    def __init__(self,ai_settings,screen,stats):
        '''初始化显示得分信息的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #显示得分信息时显示的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)
        #font.Font的的第一个参数必须是文件的全路径，而font.SysFont的第一个参数组合只需要写名字，如果不写则是默认字体
        # self.font = pygame.font.Font('C:\Windows\Fonts\simkai.ttf',48)

        #准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        '''将得分转化为渲染的图像'''
        #函数round()通常让小数精确到小数点后多少位，其中小数位数是由第二个实参指定的。然而，如果将第二个实参指定为负数，
        #  round()将圆整到最近的10、 100、 1000等整数倍。 处的代码让Python将stats.score的值圆整到最近的10的整数倍，
        # 并将结果存储到rounded_score中。
        rounded_score = int(round(self.stats.score,-1))
        #此处使用了一个字符串格式设置指令，它让Python将数值转换为字符串时在其中插入逗号，例：输出1,000,000而不是1000000。
        score_str = "{}:{:,}".format("Score",rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_colors)

        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        '''将最高得分转换为渲染的图像'''
        high_score = int(round(self.stats.high_score,-1))
        high_score_str = "{}:{:,}".format("High Score",high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_colors)

        #把最高得分放在屏幕顶部的正中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        '''在屏幕显示飞船等级、当前得分和最高得分'''
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        #绘制飞船
        self.ships.draw(self.screen)

    def prep_level(self):
        '''将等级转换为渲染的图像'''
        self.level_image = self.font.render(("Lv:" + str(self.stats.level)),True,self.text_color,
                                            self.ai_settings.bg_colors)

        #将等级放在得分下面
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        '''显示还剩下多少艘飞船'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
