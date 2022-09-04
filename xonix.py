import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class EnemyIn(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyIn, self).__init__()
        self.surf = pygame.Surface((10, 10))
        # self.surf.fill((255, 255, 255))
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(5, SCREEN_WIDTH - 5),
                random.randint(5, SCREEN_HEIGHT - 5),
            )
        )
        pygame.draw.circle(self.surf, (255, 255, 255), (5, 5), 5)
        pygame.draw.circle(self.surf, (0, 0, 0), (5, 5), 3)
        self.v_dir = random.choice((-1, 1))
        self.h_dir = random.choice((-1, 1))
        self.speed = 10

    def update(self):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.h_dir *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.v_dir *= -1
        self.rect.move_ip(self.speed*self.h_dir, self.speed*self.v_dir)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
ENEMY_NUMBER = 2
for item in range(ENEMY_NUMBER):
    new_enemy = EnemyIn()
    enemies.add(new_enemy)
    all_sprites.add(new_enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    screen.fill((0, 0, 0))

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
