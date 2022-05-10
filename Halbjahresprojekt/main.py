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
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename))
        self.image = pygame.transform.scale(self.image, Settings.player_size)
        self.anim = []
        self.imgindex = 0
        for i in range(4):
            bitmap = pygame.image.load(os.path.join(Settings.path_image_hotdog, f"idle_{i}.png"))
            final = pygame.transform.scale(bitmap, (Settings.player_size))
            self.anim.append(final)
        self.image = self.anim[self.imgindex]
        self.rect = self.image.get_rect()
        self.rect.left = 335 #x
        self.rect.top = 550 #y
        self.speed_h = 0
        self.speed_v = 0
        self.look_left = False
        self.look_right = True
        self.jumping = False
        self.platform_y = 550
        self.velocity_index = 0
        self.clock_time = pygame.time.get_ticks()
        self.velocity = ([-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5])
        self.velocity_l = ([7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,-0.5,-1,-1.5,-2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5])
        self.animtime = 100
        #Animation Area
        ###    

    def animation(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.animtime
            self.imgindex += 1
            # print(self.imgindex)
            # print(self.anim)
            if self.imgindex >= len(self.anim):
                self.imgindex = 0
                #print(self.imgindex)
            self.image = self.anim[self.imgindex]

    def idle_append(self):
        if self.look_left == True:
            self.anim.clear()
            for i in range(4):
                bitmap = pygame.image.load(os.path.join(Settings.path_image_hotdog, f"idle_{i}.png"))
                transformed = pygame.transform.flip(bitmap, True, False)
                final = pygame.transform.scale(transformed, (Settings.player_size))
                self.anim.append(final)
        elif self.look_left == False:
            self.anim.clear()
            for i in range (4):
                bitmap = pygame.image.load(os.path.join(Settings.path_image_hotdog, f"idle_{i}.png"))
                final = pygame.transform.scale(bitmap, (Settings.player_size))
                self.anim.append(final)

    def moveRight(self):
        self.look_right = True
        self.look_left = False
        self.anim.clear()
        if self.rect.left < Settings.window_width - 50:
            self.rect.left = self.rect.left + 5
        for i in range(2):
            bitmap = pygame.image.load(os.path.join(Settings.path_image_hotdog, f"walk_{i}.png"))
            final = pygame.transform.scale(bitmap, (Settings.player_size))
            self.anim.append(final)
        
    def moveLeft(self):
        self.anim.clear()
        self.look_right = False
        self.look_left = True
        if self.rect.left >= 0:
            self.rect.left = self.rect.left - 5
            for i in range(2):
                if self.look_left == True:
                    bitmap = pygame.image.load(os.path.join(Settings.path_image_hotdog, f"walk_{i}.png"))
                    transformed = pygame.transform.flip(bitmap, True, False)
                    final = pygame.transform.scale(transformed, (Settings.player_size))
                    self.anim.append(final)

    #Funktion zum springen eines Sprites
    def jump(self):
        if self.rect.top > self.platform_y: 
            self.rect.top = self.platform_y
            self.jumping = False
            self.velocity_index = 0  
        if self.jumping == True and self.look_left == True:
            self.anim.clear()
            bitmap = pygame.image.load(os.path.join(Settings.path_image_hotdog, "jump.png"))
            transformed = pygame.transform.flip(bitmap, True, False)
            final = pygame.transform.scale(transformed, (Settings.player_size))
            self.anim.append(final)
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1  
        elif self.jumping == True and self.look_right == True:
            self.anim.clear()
            bitmap = pygame.image.load(os.path.join(Settings.path_image_hotdog, "jump.png"))
            final = pygame.transform.scale(bitmap, (Settings.player_size))
            self.anim.append(final)
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
        #Animation Area
        ###    

    def animation(self):
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.animtime
            self.imgindex += 1
            print(self.imgindex)
            #print(self.anim)
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
        self.rect.left = self.rect.left + 3
        for i in range(2):
            if self.look_right == True:
                bitmap = pygame.image.load(os.path.join(Settings.path_image_enemy, f"walk_{i}.png"))
                final = pygame.transform.scale(bitmap, (Settings.enemy_size))
                self.anim.append(final)
        
    def moveLeft(self):
        self.look_right = False
        self.look_left = True
        self.anim.clear()
        self.rect.left = self.rect.left - 3
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
        self.pause = False
        self.startmenue = True
        self.points = 0
        self.lives = 3
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.level = Level(level_0,self.screen)
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("background03.png")
        self.player = Player("player.png")
        self.enemy = pygame.sprite.Group()
        self.running = True
        self.startbutton = pygame.image.load(os.path.join(Settings.path_image, "start.png"))
        self.startrect = self.startbutton.get_rect()
        self.stopbutton = pygame.image.load(os.path.join(Settings.path_image, "stop.png"))
        self.stoptrect = self.stopbutton.get_rect()
        self.creditssbutton = pygame.image.load(os.path.join(Settings.path_image, "credits.png"))
        self.creditsrect = self.creditssbutton.get_rect()

    #Malt die Punkteanzeige
    #def drawpoints(self):
    #    pointtext = Settings.font.render(f"Points: {self.points}", False, (Settings.white))
    #    self.screen.blit(pointtext,(300,500))
    #    pygame.display.flip()
        #Malt die Lebensanzeige
    #def drawlives(self):
    #    livetext = Settings.font.render(f"Lives: {self.lives}", False, (Settings.white))
    #    self.screen.blit(livetext,(14,50))
    #    pygame.display.flip()

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
            self.player.moveRight()
        if control[pygame.K_a]:
            self.player.moveLeft()
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
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        # self.startbutton.draw(self.screen)
        # self.screen.blit(self.startbutton)
        # self.screen.blit(self.stopbutton,(200,200))
        pygame.display.flip()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "50, 50"

    game = Game()
    game.run()
    game.level.run()

