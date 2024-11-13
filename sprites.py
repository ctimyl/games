import pygame
import random
from settings import Settings

class Player(pygame.sprite.Sprite):
    def __init__(self, player_img):
        super().__init__()
        self.image = player_img
        self.image.set_colorkey((0, 0, 0))  # Установите черный цвет как прозрачный
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
        self.image.set_colorkey((0, 0, 0))  # Установите черный цвет как прозрачный
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
