import pygame
from pygame import QUIT, K_a, K_LEFT, K_d, K_RIGHT, K_w, K_s, K_SPACE, K_DOWN, K_UP
import time
import random


#   创建玩家飞机类
class PlayerPlane(pygame.sprite.Sprite):
    def __init__(self, screen):  # 初始化属性
        # 初始化精灵
        pygame.sprite.Sprite.__init__(self)
        #   再创建一个玩家图片
        self.player = pygame.image.load("./picture/hero1.png")

        # 根据image获取矩形对象
        self.rect = self.player.get_rect()  # 直接获取上一行载入的矩形图片 宽 高
        self.rect.topleft = [480 / 2 - 100 / 2, 500]  # 确定矩形位置

        # #   飞机的初始坐标
        # self.x = 480 / 2 - 100 / 2
        # self.y = 500

        #   飞机的速度
        self.speed = 5

        self.screen = screen

        # 装子弹的列表
        # self.bullets = []
        self.bullets = pygame.sprite.Group()  # 用Group装精灵

    def key_control(self):  # 创建一个方法
        # 让飞机动起来，连续监听按键行为
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            # print("上")
            self.rect.top -= self.speed
            if self.rect.top < 0:  # 防止飞机出屏幕
                self.rect.top = 0
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            # print("左")
            self.rect.left -= self.speed
            if self.rect.left < 0:  # 防止飞机出屏幕
                self.rect.left = 0
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            # print("下")
            self.rect.bottom += self.speed
            if self.rect.top > 700 - 124:  # 防止飞机出屏幕
                self.rect.top = 700 - 124
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            # print("右")
            self.rect.right += self.speed
            if self.rect.left > 380:  # 防止飞机出屏幕
                self.rect.left = 380
        if key_pressed[K_SPACE]:
            # print("空格")
            # 按下空格发射子弹
            # random_num = random.randint(1, 30)
            # if random_num == 8:
            bullet = Bullet(self.screen, self.rect.left, self.rect.top)

            # 把子弹放到列表里
            self.bullets.add(bullet)

    def update(self):
        self.key_control()
        self.display()

    def display(self):  # 创建一个显示方法
        #   飞机图片放到窗口里
        self.screen.blit(self.player, self.rect)

        # 更新子弹坐标
        self.bullets.update()
        # 把所有子弹添加到屏幕
        self.bullets.draw(self.screen)


# 飞机要发射子弹，子弹不属于飞机，创建一个子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):  # 初始化
        pygame.sprite.Sprite.__init__(self)

        # 子弹图片
        self.image = pygame.image.load("./picture/bullet.png")

        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 39, y - 22]

        # 窗口
        self.screen = screen
        # 定义子弹速度
        self.speed = 5

    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        # 如果子弹超出屏幕 销毁子弹
        if self.rect.top < -22:
            self.kill()


# 创建一个敌机类
class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.enemy = pygame.image.load("./picture/enemy0.png")
        self.rect = self.enemy.get_rect()
        self.rect.topleft = [0, 0]

        self.speed = 1
        self.screen = screen

        self.direction = 'right'

        self.bullets = pygame.sprite.Group()

    def enemy_move(self):
        if self.direction == 'right':
            self.rect.right += self.speed
            if self.rect.right >= 480 - 51:
                self.direction = 'left'
        elif self.direction == 'left':
            self.rect.right -= self.speed
            if self.rect.right <= 0:
                self.direction = 'right'

    def auto_fire(self):
        random_number = random.randint(1, 40)
        if random_number == 8:
            bullet = EnemyBullet(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(bullet)

    # time.sleep(0.01)

    def display(self):
        self.screen.blit(self.enemy, self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 把所有子弹添加到屏幕
        self.bullets.draw(self.screen)

    def update(self):
        self.enemy_move()
        self.auto_fire()
        self.display()


# 敌机子弹
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):  # 初始化
        pygame.sprite.Sprite.__init__(self)

        # 子弹图片
        self.image = pygame.image.load("./picture/bullet1.png")

        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 52 / 2 - 8 / 2, y + 39]

        # 窗口
        self.screen = screen
        # 定义子弹速度
        self.speed = 5

    def update(self):
        self.rect.top += self.speed
        if self.rect.top > 700:
            self.kill()


# 添加游戏bgm
class GameSound(object):
    def __init__(self):
        pygame.mixer.init()  # 音乐模块初始化
        pygame.mixer.music.load("./picture/bg2.ogg")  # 载入声音
        pygame.mixer.music.set_volume(0.5)  # 设置声音大小

    def Play_BGM(self):
        pygame.mixer.music.play(-1)  # 开始播放音乐 -1让背景音乐循环播放


class Bomb(object):
    # 初始化碰撞
    def __init__(self, screen, type):
        self.screen = screen
        if type == "enemy":
            # 加载爆炸资源
            # 用列表推导式载入几张连续的图片
            self.mImage = [pygame.image.load
                           ("./picture/enemy0_down" + str(v) + ".png") for v in range(1, 5)]
        else:
            self.mImage = [pygame.image.load
                           ("./picture/hero_blowup_n" + str(v) + ".png") for v in range(1, 5)]
        # 设置当前爆炸播放索引
        self.mIndex = 0
        # 爆炸的坐标位置 从这播放爆炸
        self.mPos = [0, 0]
        # 可见否
        self.mVisible = False

    def action(self, rect):
        # 触发爆炸方法draw
        # 爆炸坐标
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        # 开启爆炸
        self.mVisible = True


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
