from pickle import TRUE
import time
from math import dist
from turtle import st
from typing import Text
import pygame
import os
from random import randint, random

from pygame import surface
from pygame.constants import GL_MULTISAMPLEBUFFERS

class Settings(object):
    window_height = 800
    window_width = 800
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    player_size = (35,35)
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 30)
    asteroid_sizes = { "0": (25,25), "1": (50,50), "2": (65,65)}
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)
    title = "Asteroid Clone"

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
        self.rect.left = Settings.window_height/2
        self.rect.top = Settings.window_width/2
        self.speed_h = 0
        self.speed_v = 0       

    #Rotierung des Sprites
    #def rotate(self):
     #   pygame.transform.rotate(Player.image.get_rect(), 22.5)

    #Respawnpunkt nach Tot setzen
    #def respawn(self):
        #Player.rect.left = Settings.window_height/2
        #Player.rect.top = Settings.window_width/2

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
 
class Asteroids(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.asteroid_sizes[str(randint(0,2))])
        self.big_image = pygame.transform.scale(self.image, Settings.asteroid_sizes[str(2)])
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

class fat_Asteroids(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.asteroid_sizes[str(2)])
        self.rect = self.image.get_rect()
        self.rect.left = randint(1,650)
        self.rect.top = randint(1,650)
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
        self.points = 0
        self.lives = 3
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("background03.png")
        self.player = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.running = True

    #Malt die Punkteanzeige
    def drawpoints(self):
        pointtext = Settings.font.render(f"Points: {self.points}", False, (Settings.white))
        self.screen.blit(pointtext,(15,15))

        pygame.display.flip()

        #Malt die Lebensanzeige
    def drawlives(self):
        livetext = Settings.font.render(f"Lives: {self.lives}", False, (Settings.white))
        self.screen.blit(livetext,(14,50))

        pygame.display.flip()

    #Löscht die Gegner wenn sie unten ankommen und lässt automatisch einen neuen Spawnen
    def die(self):
        for enemy in self.enemy:
            if enemy.rect.top <= 0 or enemy.rect.bottom >= Settings.window_height:
                self.enemy.remove(enemy)
                self.points += 1
                self.spawnenemy(1)

    def spawnplayer(self,num):
        for i in range(num):
            self.player.add(Player("Player.png"))

    def spawnenemy(self,num):
        for count in range(num):
            self.Asteroids = []
            self.Asteroids.append(Asteroids("enemy.png"))
            self.enemy.add(self.Asteroids)

    def spawn_fat_enemy(self,num):
        for count in range(num):
            self.fat_Asteroids = []
            self.fat_Asteroids.append(fat_Asteroids("enemy.png"))
            self.enemy.add(self.fat_Asteroids)
            

    #Wird ausgeführt wenn der Spieler bzw. das Raumschiff einen Asteroiden berührt und setzt damit die Punkte und Leben zurück.
    def gameover(self):
        for enemy in self.enemy:
            self.enemy.remove(enemy)
        #Player.respawn(self)
        self.spawnenemy(7)
        self.lives = 3
        self.points = 0
        

    #Führt eine Kollisionsprüfung mit "Mask" durch + den Abzug der leben bei Kollision
    def collide(self):
        for player in self.player:
            for enemy in self.enemy:
                if pygame.sprite.collide_mask(player,enemy): 
                    self.enemy.remove(enemy)
                    self.gameover()
                    #if self.lives > 0:
                    #    self.lives -= 1
                    #else:
                    #    self.gameover()

    
    def run(self):
        start_time = time.time()
        self.spawnplayer(1)
        self.spawnenemy(10)
        while self.running:
            #Für die Berechnung der 3 Sekunden + spawnen des "fat_enemys" pro 3 Sekunden + Abfrage ob mehr als 5 exestieren.
            stop = time.time() - start_time
            while stop / 3 == True and self.fat_Asteroids > 5:
                self.spawn_fat_enemy(1)
                print(stop)
            self.clock.tick(60)                        
            self.watch_for_events()
            self.update()
            self.update2()
            self.draw()
            self.drawpoints()
            self.drawlives()
            self.collide()
            self.die()
        pygame.quit()       



    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    screen.blit(pygame.trasnform.rotate())
                if event.key == pygame.K_LEFT:
                    Player.speed_v -= 1
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
    player = Player()

