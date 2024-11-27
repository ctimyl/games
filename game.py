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

    def run(self):
        while self.running:
            self.clock.tick(Settings.FPS)
            self.handle_events()
            self.update()
            self.draw()

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
            m = Mob(self.assets.mobs_img)
            self.all_sprites.add(m)
            self.mobs.add(m)
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
        if hits:
            self.running = False

    def draw(self):
        self.screen.fill(Colours.BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        print("GAME OVER")
