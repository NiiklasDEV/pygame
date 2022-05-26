from cmath import rect
from http.client import MOVED_PERMANENTLY
from math import dist
import pygame
import os
from random import randint, random
from level import Level
from game_data import level_0
from pygame import surface
import pygame.mixer
from settings import Settings

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
    def __init__(self, filename, game):
        super().__init__()
        self.game = game
        self.curhealth = 100
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename))
        self.image = pygame.transform.scale(self.image, Settings.player_size)
        self.anim = []
        self.dead = False
        self.imgindex = 0
        for i in range(4):
            bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"idle_{i}.png"))
            final = pygame.transform.scale(bitmap, (Settings.player_size))
            self.anim.append(final)
        self.image = self.anim[self.imgindex]
        self.rect = self.image.get_rect()
        self.rect.left = 10 #x
        self.rect.top = 800 #y
        self.speed_h = 0
        self.player_y_momentum = 0
        self.speed_v = 0
        self.look_left = False
        self.look_right = True
        self.jumping = False
        self.platform_y = 275
        self.velocity_index = 0
        self.clock_time = pygame.time.get_ticks()
        self.velocity = ([-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5])
        self.velocity_l = ([7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,-0.5,-1,-1.5,-2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5])
        self.animtime = 100

    #Überprüft auf Kollision mit Gegner
    def enemy_collision(self):
        if pygame.sprite.collide_mask(self.player_rect,Enemy.rect):
            Game.damage(50)
            if self.curhealth <= 0:
                self.die()

    def movement(self,rect, movement, tiles):
        collision_type = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += movement[0] 
        hit_list = Game.tile_collision(self,rect,tiles)
        for tile in hit_list:
            #Überprüfung ob rechts läuft
            if movement[0] > 0:
                self.rect = tile.left
                collision_type['right'] = True
                #Überprüfung ob links läuft
            elif movement[0] < 0:
                self.rect = tile.right
                collision_type['left'] = True
        self.rect.y += movement[1]
        hit_list = Game.tile_collision(self,rect,tiles)
        for tile in hit_list:
            #Überprüfung ob mit Boden berührt (Y Achse)
            if movement[1] > 0:
                self.rect = tile.top
                collision_type['bottom'] = True
            elif movement[1] < 0:
                self.rect = tile.bottom
                collision_type['top'] = True
        return rect, collision_type

    def moving(self):
        self.player_y_momentum += 0.2
        self.player_movement = [0,0]
        if Player.moveRight:
            self.player_movement[0] += 2
        if Player.moveLeft:
            self.player_movement[0] -= 2
        self.player_movement[1] += self.player_y_momentum
        if self.player_y_momentum > 3:
            self.player_y_momentum = 3

        self.player_rect, self.collisions = self.movement(self.rect, self.player_movement, Level.terrain_sprites)

    def animation(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.animtime
            self.imgindex += 1
            if self.imgindex >= len(self.anim):
                self.imgindex = 0
            self.image = self.anim[self.imgindex]

    def idle_append(self):
        if self.look_left == True:
            self.anim.clear()
            for i in range(4):
                bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"idle_{i}.png"))
                transformed = pygame.transform.flip(bitmap, True, False)
                final = pygame.transform.scale(transformed, (Settings.player_size))
                self.anim.append(final)
        elif self.look_left == False:
            self.anim.clear()
            for i in range (4):
                bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"idle_{i}.png"))
                final = pygame.transform.scale(bitmap, (Settings.player_size))
                self.anim.append(final)

    def moveRight(self):
        self.look_right = True
        self.look_left = False
        self.anim.clear()
        if self.rect.left < Settings.window_width - 50:
            #self.rect.left = self.rect.left + 5
            self.game.scrolling_offset[0] += 5
        for i in range(2):
            bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"walk_{i}.png"))
            final = pygame.transform.scale(bitmap, (Settings.player_size))
            self.anim.append(final)
        
    def moveLeft(self):
        self.anim.clear()
        self.look_right = False
        self.look_left = True
        if self.rect.left >= 0:
            #self.rect.left = self.rect.left - 5
            self.game.scrolling_offset[0] -= 5
            for i in range(2):
                if self.look_left == True:
                    bitmap = pygame.image.load(os.path.join(Settings.path_image_player, f"walk_{i}.png"))
                    transformed = pygame.transform.flip(bitmap, True, False)
                    final = pygame.transform.scale(transformed, (Settings.player_size))
                    self.anim.append(final)

    #Funktion zum springen eines Sprites
    def jump(self):
        #Legt das springen so fest das er nur auf der angelegten platform_y höhe bleiben kann
        if self.rect.top > self.platform_y: 
            self.rect.top = self.platform_y
            self.jumping = False
            self.velocity_index = 0  
        if self.jumping == True and self.look_left == True:
            self.anim.clear()
            bitmap = pygame.image.load(os.path.join(Settings.path_image_player, "jump.png"))
            transformed = pygame.transform.flip(bitmap, True, False)
            final = pygame.transform.scale(transformed, (Settings.player_size))
            self.anim.append(final)
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1  
        elif self.jumping == True and self.look_right == True:
            self.anim.clear()
            bitmap = pygame.image.load(os.path.join(Settings.path_image_player, "jump.png"))
            final = pygame.transform.scale(bitmap, (Settings.player_size))
            self.anim.append(final)
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1                 

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
        self.rect.move_ip((self.speed_h, self.speed_v))
        self.animation()
        # if self.curhealth <= 0:
        #     Player.respawn(self)

    def draw(self, screen, scrolling_offset):
        #Malen der Spielerpositionen jeweils nach Bewegung
            #screen.blit(self.image ,(self.rect.left + scrolling_offset[0], self.rect.top + scrolling_offset[1]))
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def change_direction_h(self):
        self.speed_h *= -1

    def change_direction_v(self):
        self.speed_v *= -1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image_enemy, filename))
        self.image = pygame.transform.scale(self.image, (Settings.enemy_size))
        self.anim = []
        self.imgindex = 0
        for i in range(4):
            bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, f"idle_{i}.png"))
            final = pygame.transform.scale(bitmap, (Settings.enemy_size))
            self.anim.append(final)
        self.image = self.anim[self.imgindex]
        self.rect = self.image.get_rect()
        self.rect.left = Settings.window_width - 50 #x
        self.rect.top = 450 #y
        self.speed_h = 0
        self.speed_v = 0
        self.look_left = True
        self.look_right = False
        self.jumping = False
        self.platform_y = 450
        self.velocity_index = 0
        self.clock_time = pygame.time.get_ticks()
        self.velocity = ([-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5])
        self.velocity_l = ([7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,-0.5,-1,-1.5,-2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5])
        self.animtime = 150


    def animation(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.animtime
            self.imgindex += 1
            if self.imgindex >= len(self.anim):
                self.imgindex = 0
            self.image = self.anim[self.imgindex]

    def idle_append(self):
        if self.look_left == True:
            self.anim.clear()
            bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, "idle.png"))
            transformed = pygame.transform.flip(bitmap, True, False)
            final = pygame.transform.scale(transformed, (Settings.player_size))
            self.anim.append(final)
        elif self.look_left == False:
            self.anim.clear()
            bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, "idle.png"))
            final = pygame.transform.scale(bitmap, (Settings.enemy_size))
            self.anim.append(final)

    def moveRight(self):
        self.look_right = True
        self.look_left = False
        self.anim.clear()
        self.rect.left = self.rect.left + 1
        for i in range(2):
            if self.look_right == True:
                bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, f"walk_{i}.png"))
                final = pygame.transform.scale(bitmap, (Settings.enemy_size))
                self.anim.append(final)
        
    def moveLeft(self):
        self.look_right = False
        self.look_left = True
        self.anim.clear()
        self.rect.left = self.rect.left - 1
        for i in range(2):
            if self.look_left == True:
                bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, f"walk_{i}.png"))
                transformed = pygame.transform.flip(bitmap, True, False)
                final = pygame.transform.scale(transformed, (Settings.enemy_size))
                self.anim.append(final)

    #Funktion zum springen eines Sprites
    def jump(self):
        if self.rect.top > self.platform_y: 
            self.rect.top = self.platform_y
            self.jumping = False
            self.velocity_index = 0  
        if self.jumping == True and self.look_left == True:
            self.anim.clear()
            bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, "jump.png"))
            transformed = pygame.transform.flip(bitmap, True, False)
            self.anim.append(transformed)
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1  
        elif self.jumping == True and self.look_right == True:
            self.anim.clear()
            bitmap = pygame.image.load(os.path.join(Settings.path_image, "jump.png"))
            self.anim.append(bitmap)
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1                 

    def respawn(self):
        Player.rect.left = 335
        Player.rect.top = 500

    def update(self):
        if self.rect.left <= 0 or self.rect.right >= Settings.window_width:
            self.change_direction_h()
        if self.rect.top <= 0 or self.rect.bottom >= Settings.window_height:
            self.change_direction_v()
        self.rect.move_ip((self.speed_h, self.speed_v))
        self.animation()

    def draw(self, screen):
        screen.blit(self.image,self.rect)

    def change_direction_h(self):
        self.speed_h *= -1

    def change_direction_v(self):
        self.speed_v *= -1

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self.dead = False
        self.pause = False
        self.startmenue = True
        self.points = 0
        self.maxhealth = 1000
        self.health_length = 1000
        self.health_ratio = self.maxhealth / self.health_length
        self.scrolling_offset = [0,0]
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.level = Level(level_0,self.screen,self)
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("background03.png")
        self.player = Player("player.png", self)
        self.enemy = pygame.sprite.Group()
        self.running = True
        self.startbutton = pygame.image.load(os.path.join(Settings.path_image, "start.png"))
        self.startrect = self.startbutton.get_rect()
        self.stopbutton = pygame.image.load(os.path.join(Settings.path_image, "stop.png"))
        self.stoptrect = self.stopbutton.get_rect()
        self.creditssbutton = pygame.image.load(os.path.join(Settings.path_image, "credits.png"))
        self.creditsrect = self.creditssbutton.get_rect()


    #Malt die Punkteanzeige
    def drawpoints(self):
        pointtext = Settings.font.render(f"Points: {self.points}", False, (Settings.white))
        self.screen.blit(pointtext,(300,500))
        pygame.display.flip()
        #Malt die Lebensanzeige
    # def drawlives(self):
    #     pygame.draw.rect(self.screen,Settings.white,(10,10,Player.curhealth/self.health_ratio,25))
    #     pygame.display.flip()
    
    
    def damage(self, amount):
        if self.curhealth > 0:
            self.curhealth -= amount
        if self.curhealth <= 0:
            # Methode Die noch implementieren
            self.curhealth = 0

    def health(self, amount):
        if self.curhealth < self.maxhealth:
            self.curhealth += amount
        if self.curhealth >= self.maxhealth:
            self.curhealth = self.maxhealth

    def tile_collision(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append()
        return hit_list


    def aimove(self):
        for e in self.enemy:
            if e.rect.left <= 0:
                e.look_left = False
                e.look_right = True
            if e.rect.right == Settings.window_width - 50:
                e.look_right = False
                e.look_left = True
            if  e.look_left:
                e.moveLeft()
            if e.look_right:
                e.moveRight()

    def pausescreen(self):
        pause = True
        while pause:
            self.screen.fill(Settings.black)
            pause_text = Settings.font.render("Pause", False, (Settings.white))
            self.screen.blit(pause_text,(Settings.window_width/2 - 50, Settings.window_height/2 - 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
            pygame.display.flip()

    # def deathscreen(self):
    #     self.dead = True
    #     while self.dead:
    #         Game.screen.fill(Settings.black)
    #         pause_text = Settings.font.render("Tot", False, (Settings.white))
    #         Game.screen.blit(pause_text,(Settings.window_width/2 - 50, Settings.window_height/2 - 50))
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 quit()
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_SPACE:
    #                     Player.dead = False
    #                     Player.respawn()

    #         pygame.display.flip()

    # #Funktion zum zurücksetzen des Punktestandes und der Leben
    # def die(self):
    #     Player.curhealth = 100
    #     self.points = 0
    #     deathscreen

    def startmenu(self):
        self.startmenue = True
        while self.startmenue:
            self.screen.fill(Settings.black)
            pause_text = Settings.font.render("Galaxy Jump", False, (Settings.white))
            self.screen.blit(pause_text,(Settings.window_width/2 - 50, Settings.window_height/2 - 200))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.flip()
            
    def run(self):
        while self.running:
            if self.dead:
                self.deathscreen()
            if self.pause == True:
                self.pausescreen()
            #self.startmenu()
            self.clock.tick(60)                     
            self.watch_for_events()
            self.update()
            self.draw()
            self.player.jump()
            self.aimove()
            self.level.run()
        pygame.quit()       


    def keybindings(self):
        control = pygame.key.get_pressed()
        if control[pygame.K_d]:
            self.player.moving()
        if control[pygame.K_a]:
            self.player.moving()
        if control[pygame.K_SPACE]:
            self.player.jumping = True
        if control[pygame.K_ESCAPE]:
            self.pausescreen()
        if control[pygame.K_x]:
            self.enemy.add(Enemy("idle.png"))
 
    
    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                self.player.idle_append()


    def update(self):
        self.player.update()
        self.enemy.update()
        self.keybindings()
        

    def draw(self):
        #self.background.draw(self.screen)
        self.player.draw(self.screen, self.scrolling_offset)
        self.enemy.draw(self.screen)
        #self.drawlives()
        # self.startbutton.draw(self.screen)
        # self.screen.blit(self.startbutton)
        # self.screen.blit(self.stopbutton,(200,200))
        pygame.display.flip()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "350, 350"

    game = Game()
    game.run()

