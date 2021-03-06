import pygame
from pygame import QUIT, K_a, K_LEFT, K_d, K_RIGHT, K_w, K_s, K_SPACE, K_DOWN, K_UP
import time


def main():
    # 1、创建一个窗口
    screen = pygame.display.set_mode((480, 700), 0, 32)  # 像素，设置模式
    # 2、拿一个图片当背景
    background = pygame.image.load("./picture/background.png")  # 加载图片位置， .为当前目录
    #   再创建一个玩家图片
    player = pygame.image.load("./picture/hero1.png")

    #   飞机的初始坐标
    x = 480 / 2 - 100 / 2
    y = 500
    #   飞机的速度
    speed = 5

    while True:  # 让显示窗口陷入死循环，保证窗口一直显示

        # 3、将图片贴到背景中
        screen.blit(background, (0, 0))  # 两个参数， 第一个是图片，第二个是坐标，以左上为原点
        #   飞机图片放到窗口里
        screen.blit(player, (x, y))

        # 获取事件，防止程序进入卡死状态
        # pygame.event.get()
        # 列表，用循环来判断事件
        for event in pygame.event.get():
            # 判断事件类型
            if event.type == QUIT:  # 程序退出
                pygame.quit()
                # 退出python程序
                exit()
        # 让飞机动起来，连续监听按键行为
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            print("上")
            y -= speed
        elif key_pressed[K_a] or key_pressed[K_LEFT]:
            print("左")
            x -= speed
        elif key_pressed[K_s] or key_pressed[K_DOWN]:
            print("下")
            y += speed
        elif key_pressed[K_d] or key_pressed[K_RIGHT]:
            print("右")
            x += speed
        elif key_pressed[K_SPACE]:
            print("空格")

        # 4、显示窗口中的内容
        pygame.display.update()
        time.sleep(0.01)  # 让循环停留0.01秒，防止执行过快，同时也防止cpu消耗


if __name__ == '__main__':
    main()
