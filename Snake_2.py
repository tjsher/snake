# -*- coding: utf-8 -*-
import pygame
import sys
import random
import easygui

# 以25为单位长度
# 屏幕长宽定义
SCREEN_X = 600
SCREEN_Y = 600

class Snake(object):
    # 初始化各种需要的属性
    def __init__(self):
        self.dirction = pygame.K_RIGHT#开始时默认向右
        self.body = []
        for x in range(5):#身体初始时有五个单位长度
            self.addnode()

    #在前端（蛇头）增加单位长度（块）
    def addnode(self):
        left, top = (0, 0)#声明两个变量
        if self.body:#获取头部位置
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, 25, 25)
        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0, node)

    # 删除最后一个块
    def delnode(self):
        self.body.pop()

    # 死亡判断
    def isdead(self):
        # 撞墙
        if self.body[0].x not in range(SCREEN_X):
            return True
        #等效于 for self.body[0].x in range(SCREEN_X):
        #           if self.body[0].x: return True
        if self.body[0].y not in range(SCREEN_Y):
            return True
        # 撞自己
        if self.body[0] in self.body[1:]:
            return True
        return False

    # 移动
    def move(self):
        self.addnode()
        self.delnode()

    # 改变方向时的判定
    #本来就往左或者右时输入的左右操作是无效的，上下同理
    def changedirection(self, mark):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if mark in LR + UD:
            if (mark in LR) and (self.dirction in LR):
                return
            if (mark in UD) and (self.dirction in UD):
                return
            self.dirction = mark

class Food:
    def __init__(self):
        self.rect = pygame.Rect(-25, 0, 25, 25)

    def remove(self):#设定特殊值以确认是否存在食物
        self.rect.x = -25

    def set(self):
        if self.rect.x == -25:
            allpos = []
            #25—SCREEN_X-25 食物在范围内
            for pos in range(25, SCREEN_X - 25, 25):
                                   #第三个参数：每次加25
                allpos.append(pos)
            self.rect.left = random.choice(allpos)#从allpos中获取随机一个值
            self.rect.top = random.choice(allpos)



def show_text(screen, pos, text, color, font_bold=False, font_size=30, font_italic=False):
    # 获取系统字体，并设置文字大小
    cur_font = pygame.font.SysFont("宋体", font_size)
    # 设置是否加粗属性
    cur_font.set_bold(font_bold)
    # 设置是否斜体属性
    cur_font.set_italic(font_italic)
    # 设置文字内容
    text_fmt = cur_font.render(text, 1, color)
    # 绘制文字
    screen.blit(text_fmt, pos)


def main():
    my_time = easygui.integerbox("what is snake's speed?")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('JIN_SNAKE')
    clock = pygame.time.Clock()
    scores = 0
    isdead = False
    Play_again=False

    # 蛇/食物
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#退出游戏操作
                sys.exit()
            if event.type == pygame.KEYDOWN:#按下键盘的操作
                snake.changedirection(event.key)
            if Play_again:
                return main()



        screen.fill((0, 49, 79))

        # 画蛇身 / 每一步+1分
        if not isdead:
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen, (252, 157, 154), rect, 0)

        # 显示死亡,并输入是否重新开始游戏
        isdead = snake.isdead()
        if isdead:
            Dead_Message= easygui.buttonbox("you are dead, do you want to play again?",choices=['yes','no'])
            if Dead_Message=='yes': Play_again =True
            else :Play_again =False


        # 当食物rect与蛇头重合,蛇头增加一个单位，移除食物
        if food.rect == snake.body[0]:
            scores += 1# 吃到+1分
            food.remove()
            snake.addnode()

        # 食物投递
        food.set()
        pygame.draw.rect(screen, (29, 191, 151), food.rect, 0)

        # 显示分数文字
        show_text(screen, (50, 500), 'Scores: ' + str(scores), (223, 223, 223))
        pygame.display.flip()
        clock.tick(my_time)


if __name__ == '__main__':
    main()