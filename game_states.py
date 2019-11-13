#coding:utf-8 # 由于中文注释可能会导致报错，所以需要在文件开头加一行魔法注释#coding：utf-8

class GameStates():
    '''跟踪游戏的统计信息'''
    def __init__(self,ai_settings):
        '''初始化游戏的统计信息'''
        self.aisettings = ai_settings
        #在类的一个函数中调用另一个函数，需要在之前加self，不然不合法
        self.reset_states()

        #游戏刚启动时处于非活动状态
        self.game_active = False
        #在任何情况下都不重置最高得分
        self.high_score = 0

    # 不要在__init__()之外初始化统计信息，不然重启游戏，这个值也会保持在上一次游戏终结时的值
    # 在这个游戏运行期间，我们只创建一个GameStats实例，但每当玩家开始新游戏时，需要重置一些统计信息。
    # 为此，我们在方法reset_stats()中初始化大部分统计信息，而不是在__init__()中直接初始化它们。
    # 我们在__init__()中调用这个方法，这样创建GameStats实例时将妥善地设置这些统计信息
    # 同时在玩家开始新游戏时也能调用reset_stats()。
    def reset_states(self):
        '''初始化游戏运行期间可能变化的统计信息'''
        #飞船的生命数、得分
        self.ships_left = self.aisettings.ship_limit
        self.score = 0
        self.level = 1
