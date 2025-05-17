import pygame
import sys
from pygame.math import Vector2

# 初始化
pygame.init()
pygame.mixer.init()

# 游戏常量
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
GRAVITY = 0.6
PLAYER_SPEED = 5
JUMP_FORCE = -13
TILE_SIZE = 64

# 颜色定义
SKY_BLUE = (135, 206, 235)

class Camera:
    def __init__(self, width, height):
        self.offset = Vector2(0, 0)
        self.width = width
        self.height = height

    def update(self, target):
        # 修正1：添加垂直居中限制
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        x = min(0, x)  # 左边界
        x = max(-(self.width - SCREEN_WIDTH), x)  # 右边界
        y = -target.rect.centery + SCREEN_HEIGHT // 2
        y = min(0, y)  # 下边界
        y = max(-(self.height - SCREEN_HEIGHT), y)  # 上边界
        self.offset.update(x, y)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # 修正2：添加默认图像防止资源缺失
        self.image = pygame.Surface((32, 64))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft=pos)
        
        # 运动属性
        self.direction = Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.6
        self.jump_speed = -13
        self.on_ground = False
        self.facing_right = True
        self.invincible = False

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0  # 修正3：重置水平移动
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False

        # 修正4：添加跳跃状态检查
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.on_ground = False

    def update(self):
        self.get_input()
        # 暂时移除动画相关代码

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((139, 69, 19))  # 修正5：添加默认颜色
        self.rect = self.image.get_rect(topleft=pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((128, 0, 0))  # 修正6：添加默认颜色
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = Vector2(-1, 0)
        self.speed = 2

    def update(self):
        self.rect.x += self.direction.x * self.speed

class Level:
    def __init__(self, level_data):
        self.display_surface = pygame.display.get_surface()
        self.setup_level(level_data)
        self.camera = Camera(3000, SCREEN_HEIGHT)
        self.game_over = False

    def setup_level(self, layout):
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == 'X':
                    block = Block((x,y), TILE_SIZE)
                    self.blocks.add(block)
                elif cell == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                elif cell == 'E':
                    enemy = Enemy((x,y))
                    self.enemies.add(enemy)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        # 修正7：使用更精确的碰撞检测
        for sprite in self.blocks.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.blocks.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

        # 修正8：优化地面状态判断
        player.on_ground = any(
            sprite.rect.collidepoint(player.rect.midbottom) 
            for sprite in self.blocks
        )

    def enemy_collision(self):
        player = self.player.sprite
        for enemy in self.enemies:
            # 修正9：添加完整的碰撞检测逻辑
            if enemy.rect.colliderect(player.rect):
                if player.rect.bottom <= enemy.rect.top + 10:
                    enemy.kill()
                    player.direction.y = JUMP_FORCE * 0.5
                else:
                    self.game_over = True

    def run(self):
        if not self.game_over:
            self.player.update()
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.enemy_collision()
            self.camera.update(self.player.sprite)

            # 绘制场景
            self.display_surface.fill(SKY_BLUE)
            
            for sprite in self.blocks:
                offset_pos = sprite.rect.topleft + self.camera.offset
                self.display_surface.blit(sprite.image, offset_pos)
            
            for enemy in self.enemies:
                offset_pos = enemy.rect.topleft + self.camera.offset
                self.display_surface.blit(enemy.image, offset_pos)
            
            player_offset = self.player.sprite.rect.topleft + self.camera.offset
            self.display_surface.blit(self.player.sprite.image, player_offset)
        else:
            # 显示游戏结束文字
            font = pygame.font.Font(None, 74)
            text = font.render('GAME OVER', True, (255, 0, 0))
            self.display_surface.blit(text, (SCREEN_WIDTH//2-140, SCREEN_HEIGHT//2-40))

# 修正10：优化关卡布局数据
level_map = [
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X                                          X',
    'X                                          X',
    'X                          XXX             X',
    'X                   E      XXX             X',
    'X          P               XXX         E   X',
    'X       XXXX           XXXXXXX             X',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

# 游戏主循环
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
level = Level(level_map)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(SKY_BLUE)
    level.run()
    pygame.display.update()
    clock.tick(60)