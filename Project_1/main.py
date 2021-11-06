import pygame
import os
from random import randint

class Settings(object):
    window_height = 600
    window_width = 700
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    pacman_size = (25,25)
    Ghosts_size = (25,25)
    title = "Pacman Pygame"

class Background(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass


class Pacman(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.pacman_size)
        self.rect = self.image.get_rect()
        self.rect.left = randint(5, Settings.window_width - self.rect.width)
        self.rect.top = randint(5, Settings.window_height - self.rect.height - 100)
        self.speed_h = 0
        self.speed_v = 0

    def update(self):
        if self.rect.left <= 0 or self.rect.right >= Settings.window_width:
            self.change_direction_h()
        if self.rect.top <= 0 or self.rect.bottom >= Settings.window_height:
            self.change_direction_v()
        self.rect.move_ip((self.speed_h, self.speed_v))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def change_direction_h(self):
        self.speed_h *= -1

    def change_direction_v(self):
        self.speed_v *= -1


class Ghosts(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.Ghosts_size)
        self.rect = self.image.get_rect()
        self.rect.left = 1
        self.rect.top = 1
        self.speed_h = randint(1,3)
        self.speed_v = randint(1,3)

    def update(self):
        if self.rect.left <= 0 or self.rect.right >= Settings.window_width:
            self.change_direction_h()
        if self.rect.top <= 0 or self.rect.bottom >= Settings.window_height:
            self.change_direction_v()
        self.rect.move_ip((self.speed_h, self.speed_v))


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def change_direction_h(self):
        self.speed_h *= -1

    def change_direction_v(self):
        self.speed_v *= -1

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("background03.png")
        self.pacmans = pygame.sprite.Group()
        self.Ghosts = pygame.sprite.Group()
        self.running = True


    def spawnpacmans(self,num):
        for i in range(num):
            self.pacmans.add(Pacman("pacman.png"))

    def spawnghosts(self,num):
        for count in range(num):
            self.Ghosts.add(Ghosts("geister.png"))


    def collide(self):
        for pacman in self.pacmans:
            for ghosts in self.Ghosts:
                self.radius = 25
                if pygame.sprite.collide_circle(pacman,ghosts): 
                    self.Ghosts.remove(ghosts)
                    self.spawnghosts(1)


    

    def run(self):
        self.spawnpacmans(5)
        self.spawnghosts(10)
        while self.running:
            self.clock.tick(60)                         # Auf 1/60 Sekunde takten
            self.watch_for_events()
            self.update()
            self.update2()
            self.draw()
            self.collide()
        pygame.quit()       

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        # Taste unten?
                if event.key == pygame.K_ESCAPE:    # ESC gedrückt?
                    self.running = False
            elif event.type == pygame.QUIT:         # Fenster ge-x-t?
                self.running = False

    def update(self):
        self.pacmans.update()
    
    def update2(self):
        self.Ghosts.update()

    def draw(self):
        self.background.draw(self.screen)
        self.pacmans.draw(self.screen)
        self.Ghosts.draw(self.screen)
        pygame.display.flip()



if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    game = Game()
    game.run()