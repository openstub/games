import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),   # I型-青色
    (255, 165, 0),   # L型-橙色
    (0, 0, 255),     # J型-蓝色
    (255, 255, 0),   # O型-黄色
    (0, 255, 0),     # S型-绿色
    (255, 0, 255),   # T型-紫色
    (255, 0, 0)      # Z型-红色
]

# 定义方块形状（7种基本形状）
SHAPES = [
    [[1, 1, 1, 1]],                 # I
    [[1, 0], [1, 0], [1, 1]],       # L
    [[0, 1], [0, 1], [1, 1]],       # J
    [[1, 1], [1, 1]],               # O
    [[0, 1, 1], [1, 1, 0]],         # S
    [[1, 1, 1], [0, 1, 0]],         # T
    [[1, 1, 0], [0, 1, 1]]          # Z
]

# 游戏窗口设置
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 初始化游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("俄罗斯方块")

# 游戏网格（记录每个格子的颜色）
grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# 当前下落中的方块
current_shape = None
current_color = None
current_x = GRID_WIDTH // 2
current_y = 0

# 分数
score = 0

def new_shape():
    """生成新方块"""
    global current_shape, current_color, current_x, current_y
    idx = random.randint(0, len(SHAPES)-1)
    current_shape = SHAPES[idx]
    current_color = COLORS[idx]
    current_x = GRID_WIDTH // 2 - len(current_shape[0])//2
    current_y = 0
    if check_collision(current_shape, current_x, current_y):
        game_over()

def check_collision(shape, x, y):
    """检测碰撞（边界、其他方块）"""
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                grid_x = x + col
                grid_y = y + row
                if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                    return True
                if grid_y >=0 and grid[grid_y][grid_x] != BLACK:
                    return True
    return False

def rotate_shape(shape):
    """修复：正确逆时针旋转90度"""
    return [[shape[y][x] for y in range(len(shape))] for x in reversed(range(len(shape[0])))]

def clear_lines():
    """修复：从下往上消除满行"""
    global grid, score
    lines_cleared = 0
    row = GRID_HEIGHT - 1  # 从底部开始检查
    while row >= 0:
        if all(cell != BLACK for cell in grid[row]):
            # 删除当前行并添加新行到顶部
            del grid[row]
            grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
            lines_cleared += 1
            # 删除后不减少row，继续检查同一位置的新行
        else:
            row -= 1
    score += lines_cleared * 100


def draw_block(x, y, color):
    """绘制单个方块"""
    pygame.draw.rect(screen, color, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE-1, BLOCK_SIZE-1))

def game_over():
    """游戏结束"""
    global running
    print("Game Over! Score:", score)
    running = False

# 游戏主循环
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 500  # 下落间隔（毫秒）
running = True
new_shape()

while running:
    screen.fill(BLACK)
    delta_time = clock.get_rawtime()
    fall_time += delta_time

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(current_shape, current_x-1, current_y):
                    current_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(current_shape, current_x+1, current_y):
                    current_x += 1
            elif event.key == pygame.K_DOWN:
                if not check_collision(current_shape, current_x, current_y+1):
                    current_y += 1
            elif event.key == pygame.K_UP:
                rotated = rotate_shape(current_shape)
                if not check_collision(rotated, current_x, current_y):
                    current_shape = rotated

    # 自动下落
    if fall_time >= fall_speed:
        if not check_collision(current_shape, current_x, current_y+1):
            current_y += 1
            fall_time = 0
        else:
            # 固定当前方块到网格
            for row in range(len(current_shape)):
                for col in range(len(current_shape[row])):
                    if current_shape[row][col]:
                        grid_y = current_y + row
                        grid_x = current_x + col
                        if grid_y >= 0:
                            grid[grid_y][grid_x] = current_color
            clear_lines()
            new_shape()

    # 绘制网格
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            draw_block(x, y, grid[y][x])

    # 绘制当前方块
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col]:
                draw_block(current_x + col, current_y + row, current_color)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()