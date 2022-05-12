import pygame
import os

class Settings(object):
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    path_sound = os.path.join(path_file, "sounds")
    path_image_enemy = os.path.join(path_image, "enemy_images")
    path_image_player = os.path.join(path_image, "player_images")
    player_size = (43,43)
    enemy_size = (64,64)
    platform_size = (100,100)
    pygame.font.init()
    global tile_size
    tile_size = 75
    font = pygame.font.SysFont("Comic Sans MS", 30)
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)
    black = (0,0,0)
    title = "Galaxy Jump"
    vertical_tile_number = 11
    tile_size = 32
    window_height = vertical_tile_number * tile_size
    window_width = 1200