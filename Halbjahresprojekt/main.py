from math import dist
from typing import Text
import pygame
import os
from random import randint, random

from pygame import surface
from pygame.constants import GL_MULTISAMPLEBUFFERS

class Settings(object):
    window_height = 800
    window_width = 1600
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    player_size = (50,75)
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 30)
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)
    title = "Galaxy Jump"

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
    def __init__(self, filename):
        super().__init__()
        self.frame = 0
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.player_size)
        self.rect = self.image.get_rect()
        self.rect.left = 335 #x
        self.rect.top = 500 #y
        self.speed_h = 0
        self.speed_v = 0
        self.jumping = False
        self.platform_y = 500
        self.velocity_index = 0
        self.velocity = ([-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5])

    def moveRight(self):
        if self.rect.left < Settings.window_width - 50:
            self.rect.left = self.rect.left + 5
    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left = self.rect.left - 5 
    def jump(self):
        self.rect.top += self.velocity[self.velocity_index]
        self.velocity_index += 1
        if self.velocity_index >= len(self.velocity) -1:
            self.velocity_index = len(self.velocity) - 1
        if self.rect.top > self.platform_y:
            self.rect.top = self.platform_y
            self.jumping = False
            self.velocity_index = 0



    def respawn(self):
        Player.rect.left = 335
        Player.rect.top = 500

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
        self.points = 0
        self.lives = 3
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("background03.png")
        self.player = Player("player.png")
        self.enemy = pygame.sprite.Group()
        self.running = True

    #Malt die Punkteanzeige
    def drawpoints(self):
        pointtext = Settings.font.render(f"Points: {self.points}", False, (Settings.white))
        self.screen.blit(pointtext,(300,500))

        pygame.display.flip()

        #Malt die Lebensanzeige
    def drawlives(self):
        livetext = Settings.font.render(f"Lives: {self.lives}", False, (Settings.white))
        self.screen.blit(livetext,(14,50))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)                     
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()       


    def keybindings(self):
        control = pygame.key.get_pressed()
        if control[pygame.K_d]:
            self.player.moveRight()
        if control[pygame.K_a]:
            self.player.moveLeft()
        if control[pygame.K_SPACE]:
            self.player.jumping = True
            self.player.jump()
 

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.update()
        self.keybindings()

    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "50, 50"

    game = Game()
    game.run()

