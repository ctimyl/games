import pygame
from assets import AssetManager
from settings import Settings, Colours
from sprites import Player, Mob, Bullet, Explosion


class Game:
    def __init__(self, assets):
        self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
        pygame.display.set_caption("Shmup!")
        self.clock = pygame.time.Clock()
        self.assets = assets
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()  # Группа для взрывов
        self.player = Player(self.assets.player_img)
        self.all_sprites.add(self.player)
        for i in range(8):
            m = Mob(self.assets.mobs_img)
            self.all_sprites.add(m)
            self.mobs.add(m)
        self.running = True
        self.font = pygame.font.Font(None, 74)
        self.score = 0
        self.game_over = False  # Флаг для окончания игры

    def run(self):
        while self.running:
            self.clock.tick(Settings.FPS)
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()


    def display_score(self):
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {self.score}", True, Colours.WHITE)
        self.screen.blit(score_text, (10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot(self.all_sprites, self.bullets, self.assets.bullet_img)

    def update(self):
        self.all_sprites.update()

        # Проверка столкновений между пулями и врагами
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            self.score += 1
            explosion = Explosion(hit.rect.center, self.assets.explosion_images)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            # self.assets.explosion_sound.play()
            m = Mob(self.assets.mobs_img)
            self.all_sprites.add(m)
            self.mobs.add(m)

        # Проверка победы
        if self.score >= 25:
            self.game_over = True

    def draw(self):
        self.screen.blit(self.assets.bg_img, (0, 0))  # Устанавливаем фоновое изображение
        if not self.game_over:
            self.all_sprites.draw(self.screen)
            self.display_score()
        else:
            self.display_victory_screen()
        pygame.display.flip()

    def display_victory_screen(self):
        # Отображение изображения победы
        self.screen.blit(self.assets.victory_image, (0, 0))

        # Отображение текста победы
        text = self.font.render("ПОБЕДА!", True, Colours.RED)
        text_rect = text.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)

        score_font = pygame.font.SysFont(None, 40)
        score_text = score_font.render(f"Спасибо, ты спас галактику!", True, Colours.WHITE)
        score_rect = score_text.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 50))
        self.screen.blit(score_text, score_rect)

    def quit(self):
        pygame.mixer.music.stop()
        pygame.quit()
        print("Game Over")

    def show_intro_image(self):
        # Инициализация Pygame
        pygame.init()

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