#coding:utf-8 # 由于中文注释可能会导致报错，所以需要在文件开头加一行魔法注释#coding：utf-8
import time

import pygame

from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,ai_settings,screen):
        #初始化飞船并设置其初始位置
        super(Ship,self).__init__()

        self.screen = screen

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        #也可以在settings类中设置宽高及X,Y坐标，然后用 pygame.Rect(X,Y,W,H)来设置其大小
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        #在飞船的属性center和center_y中存储小数值,center代表着飞船的中心的X坐标，center_y代表着飞船中心的Y坐标
        self.center = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

    def update(self):
        #根据移动标志调整飞船的位置,并限制飞船的移动范围
        if self.moving_right and self.rect.right < self.screen_rect.right:
            '''这里之所以不直接用self.rect.centerx,是因为rect只能储存值的整数部分，这在加减的过程中，使用rect作为
            参数，对结果的影响很大。如果rect作为最后的形参只保留整数那没有问题，但是一旦作为参与过程中的参数，
            则大大影响结果。如0.5+0.6，实际为1.1，取整数为1。用上述方法将会变成0+0.6，取整数为0。差之太多。
            '''
            self.center += self.ai_settings.ship_speed_factor
            # print("execute ship update: ",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        elif self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor

        elif self.moving_up and self.rect.top > self.screen_rect.top:
            self.center_y -= self.ai_settings.ship_speed_factor

        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_y += self.ai_settings.ship_speed_factor

        #根据self.center和self.center_y更新rect对象
        self.rect.centerx = self.center
        self.rect.centery = self.center_y

    def blitme(self):
        #在指定位置绘制飞船
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        # 让飞船在屏幕居中
        self.center = self.screen_rect.centerx
        #也要控制飞船的Y轴位置，原文默认飞船是不移动Y轴的，但是我们新增了这项功能,图片像素为60*48
        self.center_y = self.screen_rect.bottom - 24





'''
#下边的这段代码，可以获取图片的像素和格式，需要先pip Pillow模块
from PIL import Image

image1 = Image.open('images/ship.bmp')
print(image1.size,image1.format)
'''