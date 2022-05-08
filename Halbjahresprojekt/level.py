import pygame
from support import import_csv_layout
#write an import statement that imports tile_size from the Settings class of main.py
from main import Settings
from tiles import Tile

class Level():
    def __init__(self,level_data,surface):
        self.display_surface = surface

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")
    
    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != "-1":
                    x = col_index * Settings.tile_size
                    y = row_index * Settings.tile_size

                    if type == 'terrain':
                        sprite = Tile(Settings.tile_size,x,y)
                        sprite_group.add(sprite)


        return sprite_group

    def run(self):
        #running the level
        pass