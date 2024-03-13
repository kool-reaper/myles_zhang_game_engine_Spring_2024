# This file was created by the one and only Myles Zhang
# My first source control edit!

# imports
import pygame as pg
from settings import *
from sprites import *
import sys
import random
from os import path
from time import sleep

# added this math function to round down the clock
from math import floor

# this 'cooldown' class is designed to help us control time
class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

# creating game class
class Game:
    # defining game class
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        self.gamestate = "mainmenu"
        self.load_data()
        # Player statistics
        self.gamelevel = 0
        self.coincount = 0

    # Loading map for the first time
    def load_map(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        with open(path.join(map_folder, 'map0.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        self.new()

    # Updating the map when the level changes
    def update_map(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        if self.player.changelevel == True:
            self.player.changelevel = False
            self.gamelevel += 1
            self.map_data = []
            with open(path.join(map_folder, 'map' + str(self.gamelevel) + '.txt'), 'rt') as f:
                for line in f:
                    self.map_data.append(line)
            self.new()

    # Load game assets
    def load_assets(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'player.png')).convert_alpha()
        self.playbtn_img = pg.image.load(path.join(img_folder, 'Play.png')).convert_alpha()
        self.playbtn = Button(self, 512, 544, self.playbtn_img, 1)
        self.youdied_img = pg.image.load(path.join(img_folder, 'youdied.jpg')).convert_alpha()
        self.youdiedbtn = Button(self, 512, 75, self.youdied_img, 1)

    # Load saved game data
    def load_data(self):
        self.map_data = []
        self.load_assets()
        self.load_map()

    # init all variables, setup groups, instantiate classes
    def new(self):
        self.spawnplacelist = []
        self.game_sprites = pg.sprite.Group()
        self.mainmenu_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'D':
                    Door(self, col, row)
                if tile == ".":
                    self.spawnplacelist.append((col, row))
        
        i = 1
        while i <= ENEMYCOUNT:
            tile = random.choice(self.spawnplacelist)
            Enemy(self, tile[0], tile[1])
            self.spawnplacelist.remove(tile)
            i += 1

    # run method
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.gamestate == "mainmenu":
                self.main_menu()
            if self.gamestate == "playing":
                self.update()
                self.draw()
            if self.gamestate == "gameover":
                self.gameover()

        while self.running:
            self.events()

    # quit function
    def quit(self):
        pg.quit()
        sys.exit()

    # updating the display and positions
    def update(self):
        self.game_sprites.update()
        self.update_map()

    # drawing the grid
    def draw_grid(self):
        for x in range (0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (x,0), (x, HEIGHT))
        for y in range (0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (0,y), (WIDTH, y))

    # drawing the display
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.game_sprites.draw(self.screen)
        self.draw_text(self.screen, "Coins: " + str(self.coincount), 42, BLACK, 1, 1)
        pg.display.flip()

    # input method
    def events(self):
        for event in pg.event.get():
            # quit method
            if event.type == pg.QUIT:
                self.quit()

    # Drawing text
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    # displaying start screen
    def main_menu(self):
        self.screen.fill(GRAY)
        if self.playbtn.draw(self.screen):
            self.gamestate = "playing"
        pg.display.flip()

    # death function
    def gameover(self):
        self.screen.fill(DARKGRAY)
        if self.youdiedbtn.draw(self.screen):
            self.gamestate = "mainmenu"
            self.coincount = 0
            self.gamelevel = 0
            self.new()
        pg.display.flip()

    # Showing the go screen

                

# Making and running the window
g = Game()
while True:
    g.run()