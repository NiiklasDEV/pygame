import pygame
import os

class Settings(object):
    window_height = 800
    window_width = 1600
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    path_sound = os.path.join(path_file, "sounds")
    path_image_enemy = os.path.join(path_image, "enemy_images")
    path_image_hotdog = os.path.join(path_image, "hotdog_images")
    player_size = (64,64)
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
    vertical_tile_number = 25
    tile_size = 32
    screen_height = vertical_tile_number * tile_size