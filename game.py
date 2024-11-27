import pygame
from assets import AssetManager
from settings import Settings, Colours
from sprites import Player, Mob


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
        pygame.display.set_caption("Shmup!")

        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(self.assets.player_img)
        self.all_sprites.add(self.player)
        for i in range(8):
            m = Mob(self.assets.mobs_img)
            self.all_sprites.add(m)
            self.mobs.add(m)
        self.running = True
        self.font = pygame.font.Font(None, 74)
        self.score = 0

    def run(self):
        while self.running:
            self.clock.tick(Settings.FPS)
            self.handle_events()
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
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            self.score += 1
            m = Mob(self.assets.mobs_img)
            self.all_sprites.add(m)
            self.mobs.add(m)
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
        if hits:
            self.running = False

    def draw(self):
        self.screen.fill(Colours.BLACK)
        self.all_sprites.draw(self.screen)
        self.display_score()
        pygame.display.flip()

    def quit(self):
        self.display_game_over()
        pygame.time.wait(4000)
        pygame.quit()
        print("Game Over")

    def display_game_over(self):
        self.screen.fill(Colours.BLACK)
        text = self.font.render("Game Over", True, Colours.RED)
        text_rect = text.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2))
        self.screen.blit(text, text_rect)
        score_font = pygame.font.SysFont(None, 40)
        score_text = score_font.render(f"Score: {self.score}", True, Colours.WHITE)
        score_rect = score_text.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 50))
        self.screen.blit(score_text, score_rect)
        pygame.display.flip()


