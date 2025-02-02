import pygame
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

from settings import Settings, Colours


class AssetManager:
    def __init__(self):
        game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(game_folder, 'img')
        self.sound_folder = os.path.join(game_folder, 'sound')
        self.video_folder = os.path.join(game_folder, 'videos')
        self.music_folder = os.path.join(game_folder, 'music')  # Папка с музыкой

        # Путь к видеоролику
        self.video_path = os.path.join(self.video_folder, 'intro.mp4')

        # Путь к фоновой музыке
        self.music_path = os.path.join(self.music_folder, 'background_music.mp3')

        self.intro_image_path = os.path.join(self.img_folder, 'intro_image.jpeg')

    def load_resources(self):
        # Загрузка спрайтов
        self.player_img = pygame.image.load(os.path.join(self.img_folder, 'p1_jump.png')).convert()
        self.player_img.set_colorkey((0, 0, 0))  # Цвет прозрачности для игрока

        self.mobs_img = pygame.image.load(os.path.join(self.img_folder, 'alien.png')).convert()
        self.mobs_img.set_colorkey((0, 0, 0))  # Цвет прозрачности для врагов

        self.bullet_img = pygame.image.load(os.path.join(self.img_folder, 'fire01.png')).convert()
        self.bullet_img.set_colorkey((0, 0, 0))  # Цвет прозрачности для пуль

        self.bg_img = pygame.image.load(os.path.join(self.img_folder, 'moon-1.jpg')).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (Settings.WIDTH, Settings.HEIGHT))

        # Загрузка спрайтов взрыва
        explosion_folder = os.path.join(self.img_folder, 'explosion')
        self.explosion_images = []
        for img_name in sorted(os.listdir(explosion_folder)):
            img_path = os.path.join(explosion_folder, img_name)
            img = pygame.image.load(img_path).convert()
            img.set_colorkey((0, 0, 0))
            img = pygame.transform.scale(img, (80, 80))  # Масштабируем спрайты до нужного размера
            self.explosion_images.append(img)

        # Загрузка изображения победы
        self.victory_image = pygame.image.load(os.path.join(self.img_folder, 'victory.jpg')).convert()
        self.victory_image = pygame.transform.scale(self.victory_image, (Settings.WIDTH, Settings.HEIGHT))

        # Загрузка звуков
        self.explosion_sound = pygame.mixer.Sound(os.path.join(self.sound_folder, 'explosion.mp3'))
        self.explosion_sound.set_volume(0.5)  # Настройка громкости взрыва

        self.shoot_sound = pygame.mixer.Sound(os.path.join(self.sound_folder, 'shoot.ogg'))
        self.shoot_sound.set_volume(0.3)  # Настройка громкости выстрела

    def play_background_music(self):
        # Загрузка и проигрывание фоновой музыки
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(0.3)  # Установка громкости музыки
        pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение

    def play_video(self):
        # Загрузка видео
        clip = VideoFileClip(self.video_path)
        game_width, game_height = Settings.WIDTH, Settings.HEIGHT
        clip = clip.resized(width=game_width)

        audio_clip = clip.audio

        # Инициализация Pygame
        pygame.init()
        pygame.mixer.init()

        # Сохраняем аудио во временный файл
        audio_clip.write_audiofile("temp_audio.wav", codec="pcm_s16le")  # Используем PCM для лучшей совместимости
        pygame.mixer.music.load("temp_audio.wav")  # Загружаем аудио в pygame
        pygame.mixer.music.play()  # Начинаем проигрывание аудио
        pygame.mixer.music.set_volume(1)

        screen = pygame.display.set_mode((clip.size))  # Размер экрана соответствует размеру видео
        clock = pygame.time.Clock()

        # Проигрывание видео кадр за кадром
        for frame in clip.iter_frames(fps=clip.fps):
            # Преобразование кадра в поверхность Pygame
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            # Отображение кадра на экране
            screen.blit(frame_surface, (0, 0))
            pygame.display.flip()

            # Обработка событий (например, закрытие окна)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clip.close()
                    pygame.quit()
                    return

            # Ограничение FPS
            clock.tick(clip.fps)

        # Закрытие видео после завершения
        clip.close()
        if audio_clip is not None:
            pygame.mixer.music.stop()
            os.remove("temp_audio.wav")

            # Возобновляем фоновую музыку
        self.play_background_music()

    def show_intro_image(self):
        # Инициализация Pygame
        pygame.init()

        screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))  # Инициализируем экран
        clock = pygame.time.Clock()

        # Загрузка изображения
        intro_image = pygame.image.load(self.intro_image_path).convert()
        intro_image = pygame.transform.scale(intro_image, (Settings.WIDTH, Settings.HEIGHT))

        # Создание экрана
        screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
        clock = pygame.time.Clock()

        # Рендеринг текста
        font = pygame.font.Font(None, 74)
        text = font.render("Спаси галактику!", True, Colours.YELLOW)
        text_rect = text.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 100))

        # Отображение изображения и текста
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    running = False

            screen.blit(intro_image, (0, 0))  # Отображаем изображение
            screen.blit(text, text_rect)  # Отображаем текст
            pygame.display.flip()
            clock.tick(60)
