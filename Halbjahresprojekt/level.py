import pygame
from support import import_csv_layout
from settings import tile_size
from tiles import Tile

class Level():
    def __init__(self,level_data,surface):
        self.display_surface = surface

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")
    
    def create_tile_group(self,layout,type):
        self.sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        sprite = Tile(tile_size,x,y)
                        self.sprite_group.add(sprite)


        return self.sprite_group

    def run(self):
        self.terrain_sprites.draw(self.display_surface)
        #Updaten das es rechts moved + 1
        self.sprite_group.update(1)