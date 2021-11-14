from math import dist
from typing import Text
import pygame
import os
from random import randint, random

from pygame import surface

class Settings(object):
    window_height = 600
    window_width = 700
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    player_size = (25,25)
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 30)
    size1 = 35
    size2 = 35
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)
    enemy_size = (size1,size2)
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
        self.frame = 0
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.player_size)
        self.rect = self.image.get_rect()
        self.rect.left = 335
        self.rect.top = 500
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


class enemys(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.enemy_size)
        self.image2 = pygame.transform.scale2x(self.image)
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
       # self.x = 355
        #self.y = 500
        self.points = 0
        self.lives = 3
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("background03.png")
        self.player = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.running = True

    #def drawplayer(self):
      #  Game.screen.blit(Player.image, (self.x, self.y))

    def drawpoints(self):
        pointtext = Settings.font.render(f"Points: {self.points}", False, (Settings.white))
        self.screen.blit(pointtext,(15,15))

        pygame.display.flip()
    #----------------- Bewegung überarbeiten grüne Teile sind markiert
   # def handle_keys(self):
    #    dist = 5
     #   for event in pygame.event.get():
      #      if event.type == pygame.KEYDOWN:  
       #         if event.type == pygame.K_UP:    
        #            self.y -= dist
         #       if event.type == pygame.K_DOWN:
          #          self.y += dist
           #     if event.type == pygame.K_RIGHT:
            #        self.x += dist
             #   if event.type == pygame.K_LEFT:
              #      self.x -= dist

    def drawlives(self):
        livetext = Settings.font.render(f"Lives: {self.lives}", False, (Settings.white))
        self.screen.blit(livetext,(14,50))

        pygame.display.flip()

    def die(self):
        for enemy in self.enemy:
            if enemy.rect.top <= 0 or enemy.rect.bottom >= Settings.window_height:
                self.enemy.remove(enemy)
                self.points += 1
                print(self.points)
                self.spawnenemy(1)

    def spawnplayer(self,num):
        for i in range(num):
            self.player.add(Player("player.png"))

    def spawnenemy(self,num):
        for count in range(num):
            self.enemy.add(enemys("enemy.png"))


    #Überarbeitung nötig
    def gameover(self):
        for enemy in self.enemy:
            self.enemy.remove(enemy)
        #vorher bevor man spawnt wieder Spieler auf Position setzen (ergänzung nötig)
        self.spawnenemy(7)
        self.lives = 3
        self.points = 0
        


    def collide(self):
        for player in self.player:
            for enemy in self.enemy:
                if pygame.sprite.collide_mask(player,enemy): 
                    self.enemy.remove(enemy)
                    if self.lives > 0:
                        self.lives -= 1
                    else:
                        self.gameover()


    def run(self):
        self.spawnplayer(1)
        self.spawnenemy(10)
        while self.running:
            self.clock.tick(60)                         # Auf 1/60 Sekunde takten
            self.watch_for_events()
            #self.handle_keys()
            #self.drawplayer()
            self.update()
            self.update2()
            self.draw()
            self.drawpoints()
            self.drawlives()
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