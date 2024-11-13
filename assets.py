import pygame
import os
from settings import Colours


class AssetManager:
    def __init__(self):
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        self.player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()
        self.player_img.set_colorkey(Colours.BLACK)  # Установим цвет прозрачности для игрока
        self.mobs_img = pygame.image.load(os.path.join(img_folder, 'bomb.png')).convert()
        self.mobs_img.set_colorkey(Colours.BLACK)  # Установим цвет прозрачности для врагов
        self.bullet_img = pygame.Surface((10, 20))
        self.bullet_img.fill(Colours.YELLOW)
        self.bullet_img.set_colorkey(Colours.BLACK)  # Установим цвет прозрачности для пуль
