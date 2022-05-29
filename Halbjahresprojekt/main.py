from cmath import rect
from http.client import MOVED_PERMANENTLY
from importlib.resources import path
from math import dist
from tkinter import Canvas
from numpy import tile
import pygame
import os
from random import randint, random
from level import Level
from game_data import level_0
from pygame import K_ESCAPE, surface
import pygame.mixer
from settings import Settings

class Background(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image,(0,0))
        
    def update(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, filename, game):
        super().__init__()
        self.game = game
        self.curhealth = 100
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename))
        self.image = pygame.transform.scale(self.image, Settings.player_size)
        self.anim = []
        self.dead = False
        self.imgindex = 0
        self.points = 0
        for i in range(2):
            bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"idle_{i}.png"))
            final = pygame.transform.scale(bitmap, (Settings.player_size))
            self.anim.append(final)
        self.image = self.anim[self.imgindex]
        self.rect = self.image.get_rect()
        self.rect.left = 10 #x
        self.rect.top = 270 #y
        self.origin_rect = self.rect.copy()
        self.speed_h = 0
        self.player_y_momentum = 0
        self.speed_v = 0
        self.look_left = False
        self.look_right = True
        self.jumping = False
        self.platform_y = 280
        self.velocity_index = 0
        self.clock_time = pygame.time.get_ticks()
        self.velocity = ([-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10])
        self.velocity_l = ([7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,-0.5,-1,-1.5,-2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5,-8,-8.5,-9,-9.5,-10])
        self.animtime = 175

    #Überprüft auf Kollision mit Gegner
    def enemy_collision(self):
        if pygame.sprite.collide_mask(self.player_rect,Enemy.rect):
            self.game.damage(50)
            print(self.curhealth)
            if self.curhealth <= 0:
                self.die()

    def player_shoot(self):
        return Bullet(self.rect.x + 40, self.rect.y + 30)

    def die(self):
        self.dead = True
        Game.deathscreen(game)
        for enemy in self.game.enemy:
            self.game.enemy.remove(enemy)


    def obstacle_collision(self):
        if pygame.sprite.spritecollide(self,self.game.level.obstacle_sprites, False):
            self.game.damage(100)
            if self.curhealth <= 0:
                self.die()

    def movement(self,rect, movement, tiles):
        collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += movement[0] 
        hit_list = Game.tile_collision(self,rect,tiles)
        for tile in hit_list:
            #Überprüfung ob rechts läuft
            if movement[0] > 0:
                self.rect.right = tile.rect.left
                collision_type['right'] = True
                #Überprüfung ob links läuft 
            if movement[0] < 0:
                self.rect.left= tile.rect.right
                collision_type['left'] = True
        self.rect.y += movement[1]
        hit_list = Game.tile_collision(self,rect,tiles)
        for tile in hit_list:
            #Überprüfung ob mit Boden berührt (Y Achse)
            if movement[1] < 0:
                collision_type['bottom'] = True
                self.rect.top = tile.rect.bottom
            if movement[1] > 0:
                collision_type['top'] = True
                self.rect.bottom = tile.rect.top
            if collision_type['bottom']:
                self.player_y_momentum = 0
        return rect, collision_type

    def moving(self, direction):
        self.player_movement = [0,0]
        if direction == "right":
            for i in range(2):
                self.anim.clear()
                self.look_left = True
                if self.look_right == True:
                    bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"walk_{i}.png"))
                    final = pygame.transform.scale(bitmap, (Settings.player_size))
                    self.anim.append(final)
            self.idle_append()
            self.player_movement[0] += 2
        elif direction == "left":
            self.look_right = False
            self.look_left = True
            self.player_movement[0] -= 2
            for i in range(2):
                self.anim.clear()
                if self.look_left == True:
                    bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"walk_{i}.png"))
                    transformed = pygame.transform.flip(bitmap, True, False)
                    final = pygame.transform.scale(transformed, (Settings.player_size))
                    self.anim.append(final)
            self.idle_append()
        else:
            self.player_movement[0] = 0
        if direction == "jump":
            self.jumping = True
        self.player_movement[1] += self.player_y_momentum
        self.player_y_momentum += 0.2
        if self.player_y_momentum > 3:
            self.player_y_momentum = 3
        self.player_rect, self.collisions = self.movement(self.rect, self.player_movement, self.game.level.terrain_sprites)

    def animation(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.animtime
            self.imgindex += 1
            if self.imgindex >= len(self.anim):
                self.imgindex = 0
            self.image = self.anim[self.imgindex]

    def idle_append(self):
        if self.look_left:
            for i in range(2):
                bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"idle_{i}.png"))
                transformed = pygame.transform.flip(bitmap, True, False)
                final = pygame.transform.scale(transformed, (Settings.player_size))
                self.anim.append(final)
        if self.look_left == False:
            for i in range (2):
                bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"idle_{i}.png"))
                final = pygame.transform.scale(bitmap, (Settings.player_size))
                self.anim.append(final)

    #Funktion zum springen eines Sprites
    def jump(self):
        #Legt das springen so fest das er nur auf der angelegten platform_y höhe bleiben kann
        if self.rect.top > self.platform_y: 
            self.rect.top = self.platform_y
            self.jumping = False
            self.velocity_index = 0  
        # elif self.jumping == True and self.look_right == True:
        #     self.anim.clear()
        #     bitmap = pygame.image.load(os.path.join(Settings.path_image_player, "jump.png"))
        #     final = pygame.transform.scale(bitmap, (Settings.player_size))
        #     self.anim.append(final)
        #     self.rect.top += self.velocity[self.velocity_index]
        #     self.velocity_index += 1
        #     if self.velocity_index >= len(self.velocity) -1:
        #         self.velocity_index = len(self.velocity) - 1                  

    def respawn(self):
        self.player.dead = False
        self.player.curhealth = 100
        self.points = 0
        self.player.rect.left = 10
        self.player.rect.top = 270

    def update(self):
        if self.rect.left <= 0 or self.rect.right >= Settings.window_width:
            self.change_direction_h()
        if self.rect.top <= 0 or self.rect.bottom >= Settings.window_height:
            self.change_direction_v()
        self.animation()
        self.obstacle_collision()
        # if self.curhealth <= 0:
        #     Player.respawn(self)

    def draw(self, screen):
        #Malen der Spielerpositionen jeweils nach Bewegung
        #self.rect.x, self.rect.y = self.rect.x + scrolling_offset[0], self.rect.y + scrolling_offset[1]
        screen.blit(self.image, self.rect)

    def change_direction_h(self):
        self.speed_h *= -1

    def change_direction_v(self):
        self.speed_v *= -1
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image_player, "bullet.png"))
        self.rect = self.image.get_rect(center = (pos_x,pos_y))

    def update(self):
        self.rect.x += 2

        if self.rect.x > Settings.window_width:
            self.kill()
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.curhealth = 50
        self.image = pygame.image.load(os.path.join(Settings.path_image_enemy, filename))
        self.image = pygame.transform.scale(self.image, Settings.enemy_size)
        self.anim = []
        self.dead = False
        self.imgindex = 0
        self.points = 0
        bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, "idle.png"))
        final = pygame.transform.scale(bitmap, (Settings.enemy_size))
        self.anim.append(final)
        self.image = self.anim[self.imgindex]
        self.rect = self.image.get_rect()
        self.rect.left = randint(50,Settings.window_width) #x
        self.rect.top = 270 #y
        self.speed_h = 0
        self.enemy_y_momentum = 0
        self.speed_v = 0
        self.look_left = False
        self.look_right = True
        self.jumping = False
        self.enemy_movement = [0,0]
        self.platform_y = 280
        self.velocity_index = 0
        self.clock_time = pygame.time.get_ticks()
        self.velocity = ([-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10])
        self.velocity_l = ([7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,-0.5,-1,-1.5,-2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5,-8,-8.5,-9,-9.5,-10])
        self.animtime = 175

    
    def movement(self,rect, movement, tiles):
        collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += movement[0] 
        hit_list = Game.tile_collision(self,rect,tiles)
        for tile in hit_list:
            #Überprüfung ob rechts läuft
            if self.enemy_movement[0] > 0:
                self.rect.right = tile.rect.left
                collision_type['right'] = True
                #Überprüfung ob links läuft 
            if self.enemy_movement[0] < 0:
                self.rect.left= tile.rect.right
                collision_type['left'] = True
        self.rect.y += movement[1]
        hit_list = Game.tile_collision(self,rect,tiles)
        for tile in hit_list:
            #Überprüfung ob mit Boden berührt (Y Achse)
            if self.enemy_movement[1] < 0:
                collision_type['bottom'] = True
                self.rect.top = tile.rect.bottom
            if self.enemy_movement[1] > 0:
                collision_type['top'] = True
                self.rect.bottom = tile.rect.top
            if collision_type['bottom']:
                self.enemy_y_momentum = 0
        return rect, collision_type

    def moving(self, direction):
        self.enemy_movement = [0,0]
        if direction == "right":
            for i in range(2):
                self.look_left = True
                if self.look_right == True:
                    bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, f"walk_{i}.png"))
                    final = pygame.transform.scale(bitmap, (Settings.enemy_size))
                    self.anim.append(final)
            self.idle_append()
            #Dont run out the Window
            if self.rect > Settings.window_width:
                self.enemy_movement[0] += 2
        if direction == "left":
            self.look_right = False
            self.look_left = True
            #Dont run out the Window
            if self.rect > Settings.window_width:
                self.enemy_movement[0] -= 2
            for i in range(2):
                if self.look_left == True:
                    bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, f"walk_{i}.png"))
                    transformed = pygame.transform.flip(bitmap, True, False)
                    final = pygame.transform.scale(transformed, (Settings.enemy_size))
                    self.anim.append(final)
            self.idle_append()
        if direction == "jump":
            self.jumping = True
        self.enemy_movement[1] += self.enemy_y_momentum
        self.enemy_y_momentum += 0.2
        if self.enemy_y_momentum > 3:
            self.enemy_y_momentum = 3

        self.enemy_rect, self.collisions = self.movement(self.rect, self.enemy_movement, self.game.level.terrain_sprites)

    def animation(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.animtime
            self.imgindex += 1
            if self.imgindex >= len(self.anim):
                self.imgindex = 0
            self.image = self.anim[self.imgindex]

    def idle_append(self):
        if self.look_left:
            for i in range(2):
                bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, f"idle_{i}.png"))
                transformed = pygame.transform.flip(bitmap, True, False)
                final = pygame.transform.scale(transformed, (Settings.enemy_size))
                self.anim.append(final)
        if self.look_left == False:
            for i in range (2):
                bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, f"idle_{i}.png"))
                final = pygame.transform.scale(bitmap, (Settings.enemy_size))
                self.anim.append(final)

    #Funktion zum springen eines Sprites
    def jump(self):
        #Legt das springen so fest das er nur auf der angelegten platform_y höhe bleiben kann
        if self.rect.top > self.platform_y: 
            self.rect.top = self.platform_y
            self.jumping = False
            self.velocity_index = 0  
        # elif self.jumping == True and self.look_right == True:
        #     self.anim.clear()
        #     bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, "jump.png"))
        #     final = pygame.transform.scale(bitmap, (Settings.enemy_size))
        #     self.anim.append(final)
        #     self.rect.top += self.velocity[self.velocity_index]
        #     self.velocity_index += 1
        #     if self.velocity_index >= len(self.velocity) -1:
        #         self.velocity_index = len(self.velocity) - 1                  

    # def respawn(self):
    #     self.curhealth = 100
    #     Game.points = 0
    #     Game.deathscreen(self)
    #     self.rect.left = 335
    #     self.rect.top = 500

    def update(self):
        if self.rect.left <= 0 or self.rect.right >= Settings.window_width:
            self.change_direction_h()
        if self.rect.top <= 0 or self.rect.bottom >= Settings.window_height:
            self.change_direction_v()
        self.animation()
        # if self.curhealth <= 0:
        #     enemy.respawn(self)

    def draw(self, screen):
        #Malen der Spielerpositionen jeweils nach Bewegung
        #self.rect.x, self.rect.y = self.rect.x + scrolling_offset[0], self.rect.y + scrolling_offset[1]
        screen.blit(self.image, self.rect)

    def change_direction_h(self):
        self.speed_h *= -1

    def change_direction_v(self):
        self.speed_v *= -1

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self.click = False
        self.dead = False
        self.pause = False
        self.startmenue = True
        self.maxhealth = 1000
        self.health_length = 1000
        self.health_ratio = self.maxhealth / self.health_length
        self.scrolling_offset = [0,0]
        self.scrolling_origin = [0,0]
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.level = Level(level_0,self.screen,self)
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.player = Player("player.png", self)
        self.enemy = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.startbutton = pygame.image.load(os.path.join(Settings.path_image, "start.png"))
        self.startrect = self.startbutton.get_rect()
        self.stopbutton = pygame.image.load(os.path.join(Settings.path_image, "stop.png"))
        self.stoptrect = self.stopbutton.get_rect()
        self.creditssbutton = pygame.image.load(os.path.join(Settings.path_image, "credits.png"))
        self.creditsrect = self.creditssbutton.get_rect()

    def calc_scroll(self):
        self.scrolling_origin[0] += (self.player.rect.x - self.scrolling_origin[0] - ( Settings.player_size[0] // 2)) / 10
        # self.scrolling_origin[1] += (self.player.rect.y - self.scrolling_origin[1]) / 10
        self.scrolling_offset = self.scrolling_origin.copy()
        self.scrolling_offset[0] = int(self.scrolling_offset[0])
        # self.scrolling_offset[1] = int(self.scrolling_offset[1])
    
        #Malt die Punkteanzeige
    def drawpoints(self):
        pointtext = Settings.font.render(f"Points: {self.player.points}", False, (Settings.white))
        self.screen.blit(pointtext,(Settings.window_width - 175,5))
        pygame.display.flip()
        #Malt die Lebensanzeige
    def drawlives(self):
        pygame.draw.rect(self.screen,Settings.white,(10,10,self.player.curhealth/self.health_ratio,25))
        pygame.display.flip()

    def bullet_collision(self):
        for tiles in self.level.terrain_sprites:
            for bullet in self.bullets:
                get_hit = pygame.sprite.collide_mask(bullet,tiles)
                if get_hit:
                    self.bullets.remove(bullet)
        for enemy in self.enemy:
            for bullet in self.bullets:
                #Killen der Bullets bei Aufprall auf Terrain Sprites
                get_hit = pygame.sprite.collide_mask(enemy, bullet)
                if get_hit:
                    self.bullets.remove(bullet)
                    self.enemy.remove(enemy)
                    self.player.points += 3

    #Überprüft auf Kollision mit Gegner
    def enemy_collision(self):
        for enemy in self.enemy:
            get_hit = pygame.sprite.spritecollideany(self.player,self.enemy)
            if get_hit:
                self.damage(15)
                self.enemy.remove(enemy)

    def enemy_damage(self, amount):
        if self.enemy.curhealth > 0:
            self.enemy.curhealth -= amount
        if self.enemy.curhealth <= 0:
            # Methode Die noch implementieren
            self.enemy.curhealth = 0


    def damage(self, amount):
        if self.player.curhealth > 0:
            self.player.curhealth -= amount
        if self.player.curhealth <= 0:
            # Methode Die noch implementieren
            self.player.curhealth = 0
            self.player.die()

    def health(self, amount):
        if self.curhealth < self.maxhealth:
            self.curhealth += amount
        if self.curhealth >= self.maxhealth:
            self.curhealth = self.maxhealth

    def tile_collision(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list


    def aimove(self):
        for e in self.enemy:
            if e.enemy_movement[0] > 0:
                e.look_right = True
                e.look_left = False
            if e.enemy_movement[0] < 0:
                e.look_left = True
                e.look_right = False
            if e.rect.right == Settings.window_width - 50:
                e.look_right = False
                e.look_left = True
            if  e.look_left:
                e.enemy_movement[0] -= 2
            if e.look_right:
                e.enemy_movement[0] += 2

    def pausescreen(self):
        pause = True
        while pause:
            self.screen.fill(Settings.black)
            pause_text = Settings.font.render("Pause", False, (Settings.white))
            self.screen.blit(pause_text,(Settings.window_width/2 - 50, Settings.window_height/2 - 50))
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.player.look_right = False
                    if event.key == pygame.K_a:
                        self.player.look_left = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
            pygame.display.flip()

    def deathscreen(self):
        while self.player.dead:
            self.screen.fill(Settings.black)
            pause_text = Settings.font.render("Oh no, you died!", False, (Settings.white))
            respawn_text = Settings.font.render("Press Space to Respawn or Escape to ragequit.", False, (Settings.white))
            self.screen.blit(respawn_text, (Settings.window_width/2 - 275, Settings.window_height/2 - 20))
            self.screen.blit(pause_text,(Settings.window_width/2 - 50, Settings.window_height/2 - 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Player.respawn(self)

            pygame.display.flip()

    # #Funktion zum zurücksetzen des Punktestandes und der Leben
    # def die(self):
    #     Player.curhealth = 100
    #     self.points = 0
    #     deathscreen

    def startmenu(self):
        while self.startmenue:
            self.mX, self.mY = pygame.mouse.get_pos()
            self.background = Background("background03.png")
            self.background.draw(self.screen)
            #self.screen.fill(Settings.black)
            pause_text = Settings.font.render("Galaxy Jump", False, (Settings.white))
            button1text = Settings.font.render("Start", False, (Settings.black))
            button2text = Settings.font.render("Exit", False, (Settings.black))
            self.screen.blit(pause_text,(Settings.window_width/2 - 60, Settings.window_height/2 - 100))
            button1 = pygame.Rect(Settings.window_width / 2 - 75,150,200,50)
            button2 = pygame.Rect(Settings.window_width / 2 - 75,225,200,50)


            if button1.collidepoint((self.mX,self.mY)):
                if self.click:
                    self.run()
            if button2.collidepoint((self.mX,self.mY)):
                if self.click:
                    pygame.quit()

            pygame.draw.rect(self.screen, Settings.white, button1)
            pygame.draw.rect(self.screen, Settings.white, button2)
            self.screen.blit(button1text, (Settings.window_width / 2 - 15, 150))
            self.screen.blit(button2text, (Settings.window_width / 2 - 10, 225))

            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
            pygame.display.flip()
            
    def run(self):
        self.running = True
        while self.running:
            if self.dead:
                self.deathscreen()
            if self.pause:
                self.pausescreen()
            #self.startmenu()
            self.clock.tick(60)                     
            self.watch_for_events()
            self.calc_scroll()
            self.enemy_collision()
            self.bullet_collision()
            self.update()
            self.level.run(self.scrolling_offset)
            self.draw()
            self.drawpoints()
            self.player.jump()
            self.aimove()
            self.player.moving("")
        pygame.quit()       


    def keybindings(self):
        control = pygame.key.get_pressed()
        if control[pygame.K_d]:
            self.player.moving("right")
        if control[pygame.K_a]:
            self.player.moving("left")
        if control[pygame.K_SPACE]:
            self.player.player_y_momentum = - 3
        if control[pygame.K_ESCAPE]:
            self.pausescreen()
        if control[pygame.K_x]:
            self.enemy.add(Enemy("idle.png"))
            
 
    
    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                self.player.idle_append()
                self.player.player_movement = [0,0]
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.bullets.add(self.player.player_shoot())


    def update(self):
        self.player.update()
        self.bullets.update()
        self.enemy.update()
        self.keybindings()
        

    def draw(self):
        self.player.draw(self.screen)
        self.bullets.draw(self.screen)
        self.enemy.draw(self.screen)
        self.drawlives()
        # self.startbutton.draw(self.screen)
        #self.screen.blit(self.stopbutton,(200,200))
        pygame.display.flip()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "350, 350"

    game = Game()
    game.startmenu()

