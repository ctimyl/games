import pygame
import random
from settings import Settings, Colours

class Player(pygame.sprite.Sprite):
    def __init__(self, player_img):
        super().__init__()
        self.image = player_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.WIDTH / 2
        self.rect.bottom = Settings.HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > Settings.WIDTH:
            self.rect.right = Settings.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, all_sprites, bullets, bullet_img):
        bullet = Bullet(self.rect.centerx, self.rect.top, bullet_img)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self, mob_img):
        super().__init__()
        self.image = mob_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(Settings.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > Settings.HEIGHT + 10 or self.rect.left < -25 or self.rect.right > Settings.WIDTH + 20:
            self.rect.x = random.randrange(Settings.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img):
        super().__init__()
        self.image = bullet_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, explosion_images):
        super().__init__()
        self.explosion_images = explosion_images
        self.image = explosion_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30  # Увеличили скорость анимации (было 50)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(random.choice([Colours.RED, Colours.YELLOW, Colours.GREEN]))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = random.uniform(-5, 5)
        self.speedy = random.uniform(-10, -5)
        self.lifetime = random.randint(20, 50)  # Время жизни частицы

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

# Добавление частиц при взрыве
def create_particles(center, all_sprites):
    for _ in range(20):  # Создаем 20 частиц
        particle = Particle(*center)
        all_sprites.add(particle)