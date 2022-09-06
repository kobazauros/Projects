import pygame


class Line(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((200, 200))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.line(self.image, (255, 255, 0), (0, 0), (200, 200), 5)
        self.rect = self.image.get_rect(topleft=(50, 50))


class Rectt(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, 50, 50))
        self.rect = self.image.get_rect(topleft=(25, 100))


pygame.init()
screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

running = True
l = Line()
m = Rectt()
group = pygame.sprite.Group([l, m])

while running:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    m.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3
    m.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 3
    m.rect.clamp_ip(screen.get_rect())
    hit = pygame.sprite.collide_mask(m, l)

    screen.fill((0, 0, 0))
    group.draw(screen)
    if hit:
        pygame.draw.rect(screen, (255, 0, 0), m.rect, 5)
    pygame.display.flip()

pygame.quit()
