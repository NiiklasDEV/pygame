import pygame
import os
from random import randint, random

class Settings(object):
    window_height = 600
    window_width = 700
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    player_size = (25,25)
    size1 = randint(25,75)
    size2 = randint(25,75)
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)
    enemy_size = (size1,size2)
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 32)
    title = "Projekt Pygame"

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


class Player(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.player_size)
        self.rect = self.image.get_rect()
        self.rect.left = randint(5, Settings.window_width - self.rect.width)
        self.rect.top = randint(5, Settings.window_height - self.rect.height - 100)
        self.speed_h = 0
        self.speed_v = 0

    #Geplant für die Bewegund des Spieler Sprites
    def movement(self,x,y):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_UP:    
                    Player.control(steps,0)
                if event.type == pygame.K_DOWN:
                    Player.control(-steps,0)
                if event.type == pygame.K_RIGHT:
                    self.movex += x
                if event.type == pygame.K_LEFT:
                    self.movex -= x



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


class enemys(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.enemy_size)
        self.rect = self.image.get_rect()
        self.rect.left = randint(1,650)
        self.rect.top = 1
        self.speed_h = 0
        self.speed_v = randint(1,3)

    def update(self):
        if self.rect.left <= 0 or self.rect.right >= Settings.window_width:
            self.change_direction_h()
        self.rect.move_ip((self.speed_h, self.speed_v))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def change_direction_h(self):
        self.speed_h *= -1

    

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("background03.png")
        self.player = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.running = True
        self.points = 0


    def die(self):
        for enemy in self.enemy:
            if enemy.rect.top <= 0 or enemy.rect.bottom >= Settings.window_height:
                self.enemy.remove(enemy)
                self.points += 1
                print(self.points)

    def spawnplayer(self,num):
        for i in range(num):
            self.player.add(Player("player.png"))

    def spawnenemy(self,num):
        for count in range(num):
            self.enemy.add(enemys("enemy.png"))


    def draw_points(self):
        X = 400
        Y = 400
        text = Settings.font.render("test", True, Settings.green, Settings.blue)
        display_surface = pygame.display.set_mode((X, Y))
        textRect = text.get_rect()
        while True:
            display_surface.fill(Settings.white)
            display_surface.blit(text, textRect)

    def collide(self):
        for player in self.player:
            for enemy in self.enemy:
                self.radius = 25
                if pygame.sprite.collide_circle(player,enemy): 
                    self.enemy.remove(enemy)

    
    

    def run(self):
        self.spawnplayer(1)
        self.spawnenemy(7)
        while self.running:
            self.clock.tick(60)                         # Auf 1/60 Sekunde takten
            self.watch_for_events()
            self.update()
            self.update2()
            self.draw()
            self.collide()
            self.die()
            #self.draw_points()
        pygame.quit()       

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        # Taste unten?
                if event.key == pygame.K_ESCAPE:    # ESC gedrückt?
                    self.running = False
            elif event.type == pygame.QUIT:         # Fenster ge-x-t?
                self.running = False

    def update(self):
        self.player.update()
    
    def update2(self):
        self.enemy.update()

    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        pygame.display.flip()



if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    game = Game()
    game.run()