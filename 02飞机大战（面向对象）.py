import pygame
from pygame import QUIT, K_a, K_LEFT, K_d, K_RIGHT, K_w, K_s, K_SPACE, K_DOWN, K_UP
import time
import random


#   创建玩家飞机类
class PlayerPlane(object):
    def __init__(self, screen):  # 初始化属性
        #   再创建一个玩家图片
        self.player = pygame.image.load("./picture/hero1.png")

        #   飞机的初始坐标
        self.x = 480 / 2 - 100 / 2
        self.y = 500
        #   飞机的速度
        self.speed = 5

        self.screen = screen

        # 装子弹的列表
        self.bullets = []

    def key_control(self):  # 创建一个方法
        # 让飞机动起来，连续监听按键行为
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            # print("上")
            self.y -= self.speed
            if self.y < 0:  # 防止飞机出屏幕
                self.y = 0
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            # print("左")
            self.x -= self.speed
            if self.x < 0:  # 防止飞机出屏幕
                self.x = 0
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            # print("下")
            self.y += self.speed
            if self.y > 700 - 124:  # 防止飞机出屏幕
                self.y = 700 - 124
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            # print("右")
            self.x += self.speed
            if self.x > 380:  # 防止飞机出屏幕
                self.x = 380
        if key_pressed[K_SPACE]:
            # print("空格")
            # 按下空格发射子弹
            bullet = Bullet(self.screen, self.x, self.y)
            # 把子弹放到列表里
            self.bullets.append(bullet)

    def display(self):  # 创建一个显示方法
        #   飞机图片放到窗口里
        self.screen.blit(self.player, (self.x, self.y))
        #   遍历所有子弹
        for bullet in self.bullets:
            # 让子弹飞
            bullet.auto_move()
            bullet.display()


# 飞机要发射子弹，子弹不属于飞机，创建一个子弹类
class Bullet(object):
    def __init__(self, screen, x, y):  # 初始化
        self.x = x + 39
        self.y = y - 22
        # 子弹图片
        self.image = pygame.image.load("./picture/bullet.png")
        # 窗口
        self.screen = screen
        # 定义子弹速度
        self.speed = 5

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def auto_move(self):
        self.y -= self.speed


# 创建一个敌机类
class EnemyPlane(object):
    def __init__(self, screen):
        self.enemy = pygame.image.load("./picture/enemy0.png")
        self.x = 0
        self.y = 0
        self.speed = 1.5
        self.screen = screen

        self.direction = 'right'

        self.bullets = []

    def enemy_move(self):
        if self.direction == 'right':
            self.x += self.speed
            if self.x >= 480 - 51:
                self.direction = 'left'
        elif self.direction == 'left':
            self.x -= self.speed
            if self.x <= 0:
                self.direction = 'right'

    def auto_fire(self):
        random_number = random.randint(1, 40)
        if random_number == 8:
            bullet = EnemyBullet(self.screen, self.x, self.y)
            self.bullets.append(bullet)

    # time.sleep(0.01)

    def display(self):
        self.screen.blit(self.enemy, (self.x, self.y))
        for bullet in self.bullets:
            bullet.auto_move()
            bullet.display()


# 敌机子弹
class EnemyBullet(object):
    def __init__(self, screen, x, y):  # 初始化
        self.x = x + 52 / 2 - 8 / 2
        self.y = y + 39
        # 子弹图片
        self.image = pygame.image.load("./picture/bullet1.png")
        # 窗口
        self.screen = screen
        # 定义子弹速度
        self.speed = 10

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def auto_move(self):
        self.y += self.speed


# 添加游戏bgm
class GameSound(object):
    def __init__(self):
        pygame.mixer.init()  # 音乐模块初始化
        pygame.mixer.music.load("./picture/bg2.ogg")  # 载入声音
        pygame.mixer.music.set_volume(0.5)  # 设置声音大小

    def Play_BGM(self):
        pygame.mixer.music.play(-1)  # 开始播放音乐 -1让背景音乐循环播放


def main():
    sound = GameSound()
    sound.Play_BGM()

    # 1、创建一个窗口
    screen = pygame.display.set_mode((480, 700), 0, 32)  # 像素，设置模式
    # 2、拿一个图片当背景
    background = pygame.image.load("./picture/background.png")  # 加载图片位置， .为当前目录

    player = PlayerPlane(screen)
    enemy1 = EnemyPlane(screen)

    while True:  # 让显示窗口陷入死循环，保证窗口一直显示

        # 3、将图片贴到背景中
        screen.blit(background, (0, 0))  # 两个参数， 第一个是图片，第二个是坐标，以左上为原点

        # 获取事件，防止程序进入卡死状态
        # pygame.event.get()
        # 列表，用循环来判断事件
        for event in pygame.event.get():
            # 判断事件类型
            if event.type == QUIT:  # 程序退出
                pygame.quit()
                # 退出python程序
                exit()

        # 执行飞机的按键监听
        player.key_control()
        # 显示飞机
        player.display()

        enemy1.display()
        enemy1.enemy_move()
        enemy1.auto_fire()

        # 4、显示窗口中的内容
        pygame.display.update()
        time.sleep(0.01)  # 让循环停留0.01秒，防止执行过快，同时也防止cpu消耗


if __name__ == '__main__':
    main()
