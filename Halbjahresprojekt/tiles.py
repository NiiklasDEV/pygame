import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, size,x,y, surface):
        super().__init__()
        #self.image = pygame.Surface((size,size))
        self.image = pygame.transform.scale(surface,(size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

    def updatee(self,shift):
        self.rect.x + shift

    def draw(self, scrolling, screen):
        screen.blit(self.image ,(self.rect.left - scrolling[0], self.rect.top - scrolling[1]))

class StaticTile(Tile):
    def __init__(self, size, x, y,surface):
        super().__init__(size, x, y)
        self.image = surface
