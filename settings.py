# this file was created by the one and only Myles Zhang

from os import path
import pygame as pg

# display settings
WIDTH = 1024
HEIGHT = 768
TILESIZE = 32
TITLE = "Ae"

# Colors
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHTGRAY = (150, 150, 150)
BGCOLOR = (135, 206, 235)
RED = (255, 100, 100)
BEIGE = (245, 245, 220)
GRAY = (206, 204, 197)
DARKGRAY = (25, 25, 25)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game settings
FPS = 144
PLAYER_SPEED = 300
INITIALENEMYCOUNT = 2
INITIALCOINCOUNT = 4
MAXMAP = 4
PLAYERSPRITESHEET = "spritesheet.png"
INITIALSTARTINGLIVES = 3
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

# Folder initialization
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
map_folder = path.join(game_folder, 'maps')