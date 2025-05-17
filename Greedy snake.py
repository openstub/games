import pygame
import random
import time

# 初始化Pygame
pygame.init()

# 游戏窗口设置
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇小游戏")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 蛇和食物初始化
snake_pos = [[100, 100], [90, 100], [80, 100]]
snake_speed = [10, 0]
food_pos = [random.randrange(1, (WIDTH//10)) * 10, 
            random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True

# 游戏主循环
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_speed[1] == 0:
                snake_speed = [0, -10]
            elif event.key == pygame.K_DOWN and snake_speed[1] == 0:
                snake_speed = [0, 10]
            elif event.key == pygame.K_LEFT and snake_speed[0] == 0:
                snake_speed = [-10, 0]
            elif event.key == pygame.K_RIGHT and snake_speed[0] == 0:
                snake_speed = [10, 0]

    # 移动蛇身
    snake_pos.insert(0, [snake_pos[0][0] + snake_speed[0], 
                        snake_pos[0][1] + snake_speed[1]])

    # 吃食物检测
    if snake_pos[0][0] == food_pos[0] and snake_pos[0][1] == food_pos[1]:
        food_spawn = False
    else:
        snake_pos.pop()

    # 生成新食物
    if not food_spawn:
        food_pos = [random.randrange(1, (WIDTH//10)) * 10, 
                   random.randrange(1, (HEIGHT//10)) * 10]
        food_spawn = True

    # 绘制游戏界面
    screen.fill(BLACK)
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, WHITE, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # 碰撞检测
    if (snake_pos[0][0] < 0 or snake_pos[0][0] > WIDTH-10 or
        snake_pos[0][1] < 0 or snake_pos[0][1] > HEIGHT-10):
        running = False
    for block in snake_pos[1:]:
        if snake_pos[0][0] == block[0] and snake_pos[0][1] == block[1]:
            running = False

    # 更新显示
    pygame.display.flip()
    time.sleep(0.1)

pygame.quit()