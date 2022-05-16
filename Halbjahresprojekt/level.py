import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size
from tiles import Tile, StaticTile

class Level():
    def __init__(self,level_data,surface, game):
        self.display_surface = surface
        self.game = game

        #CSV Layouts
        terrain_layout = import_csv_layout(level_data['terrain'])
        background_layout = import_csv_layout(level_data['bg'])
        ground_layout = import_csv_layout(level_data['ground'])
        #Sprites
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")
        self.backround_sprites = self.create_tile_group(background_layout, "bg")
        self.ground_sprites = self.create_tile_group(ground_layout, "ground")
    
    #Funktion zum erstellen der sprite Group für die jeweiligen Tiles
    def create_tile_group(self,layout,type):
        self.sprite_group = pygame.sprite.Group()

        #Loopt durch alle Spalten und zeilen in der CSV und multipliziert die index mit der Tile größe [0,0] * tile_size
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    #Types mit den jeweiligen Sprites
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic("C:/Users/nikbr/Desktop/MoonCaves1BTileset/caves_1b_tileset_compact.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = Tile(tile_size,x,y, tile_surface)
                        self.sprite_group.add(sprite)

                    if type == 'bg':
                        bg_tile_list = import_cut_graphic("C:/Users/nikbr/Desktop/MoonCaves1BTileset/caves_1b_tileset_compact.png")
                        tile_surface = bg_tile_list[int(val)]
                        sprite = Tile(tile_size,x,y, tile_surface)
                        self.sprite_group.add(sprite)
                    
                    if type == 'ground':
                        ground_tile_list = import_cut_graphic("C:/Users/nikbr/Desktop/MoonCaves1BTileset/caves_1b_tileset_compact.png")
                        tile_surface = ground_tile_list[int(val)]
                        sprite = Tile(tile_size,x,y, tile_surface)
                        self.sprite_group.add(sprite)


                    self.sprite_group.add(sprite)
        return self.sprite_group

    def run(self):
        self.game.background.draw(self.game.screen)
            #Background
        for tile in self.backround_sprites:
            tile.draw(self.game.scrolling_offset, self.display_surface)
            tile.updatee(1)
            #Terrain
        for tile in self.terrain_sprites:
            tile.draw(self.game.scrolling_offset , self.display_surface)
            tile.updatee(1)
        #Ground
        for tile in self.ground_sprites:
            tile.draw(self.game.scrolling_offset, self.display_surface)
            tile.updatee(1)