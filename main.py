import pygame

from game import Game
from assets import AssetManager


def main():
    # Создаем менеджер ресурсов
    assets = AssetManager()



    # Проигрывание видеоролика
    assets.play_video()

    # Проигрывание картины
    assets.show_intro_image()

    # Инициализация pygame.display
    pygame.init()

    # Загрузка ресурсов
    assets.load_resources()

    # Воспроизведение фоновой музыки
    assets.play_background_music()

    # Запуск игры
    game = Game(assets)
    game.run()
    game.quit()


if __name__ == "__main__":
    main()
