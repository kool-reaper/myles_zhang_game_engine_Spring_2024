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
        # Player statistics
        self.gamelevel = 0
        self.coincount = 0
        self.coinspawncount = INITIALCOINCOUNT
        self.characternumber = 0
        self.characterlist = ["Tyler", "Adrian", "Myles"]
        self.load_assets()

    # Load game assets
    def load_assets(self):
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'player.png')).convert_alpha()
        self.playbtn_img = pg.image.load(path.join(img_folder, 'play.png')).convert_alpha()
        self.playbtn = Button(self, 512, 544, self.playbtn_img, 1)
        self.youdied_img = pg.image.load(path.join(img_folder, 'Gameover.png')).convert_alpha()
        self.youdiedimg = Image(self, 512, 75, self.youdied_img, 0.5)
        self.youwin_img = pg.image.load(path.join(img_folder, 'Youwin.jpg')).convert_alpha()
        self.youwinimg = Image(self, 518, 75, self.youwin_img, 2)
        self.restart_img = pg.image.load(path.join(img_folder, 'Restart.png')).convert_alpha()
        self.restartbtn = Button(self, 512, 550, self.restart_img, 3)
        self.left_img = pg.image.load(path.join(img_folder, 'Leftbutton.png')).convert_alpha()
        self.leftbtn = Button(self, 312, 224, self.left_img, 1)
        self.right_img = pg.image.load(path.join(img_folder, 'Rightbutton.png')).convert_alpha()
        self.rightbtn = Button(self, 712, 224, self.right_img, 1)
        self.Tyler_img = pg.image.load(path.join(img_folder, 'Tyler.png')).convert_alpha()
        self.Tyler = Image(self, 512, 200, self.Tyler_img, 4)
        self.Adrian_img = pg.image.load(path.join(img_folder, 'Adrian.png')).convert_alpha()
        self.Adrian = Image(self, 512, 200, self.Adrian_img, 4)
        self.Myles_img = pg.image.load(path.join(img_folder, 'Myles.png')).convert_alpha()
        self.Myles = Image(self, 512, 200, self.Myles_img, 4)


    # Loading map for the first time
    def load_map(self):
        self.gamelevel = 0
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        with open(path.join(map_folder, 'map0.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        self.enemycount = INITIALENEMYCOUNT
        self.new(False)

    # Updating the map when the level changes
    def update_map(self):
        map_folder = path.join(game_folder, 'maps')
        if self.player.changelevel == True:
            self.player.changelevel = False
            self.gamelevel += 1
            self.map_data = []
            with open(path.join(map_folder, 'map' + str(self.gamelevel) + '.txt'), 'rt') as f:
                for line in f:
                    self.map_data.append(line)
            self.new(False)

    # # Load saved game data
    # def load_data(self):
    #     self.map_data = []
    #     self.load_assets()
    #     self.load_map()

    # init all variables, setup groups, instantiate classes
    def new(self, reset):
        if reset == True:
            self.map_data = []
            game_folder = path.dirname(__file__)
            map_folder = path.join(game_folder, 'maps')
            with open(path.join(map_folder, 'map0.txt'), 'rt') as f:
                for line in f:
                    self.map_data.append(line)
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
                if tile == 'D':
                    Door(self, col, row)
                if tile == 'E':
                    Enemy(self, col, row)
                if tile == ".":
                    self.spawnplacelist.append((col, row))
        
        i = 1
        while i <= self.enemycount:
            enemytile = random.choice(self.spawnplacelist)
            print(str(enemytile))
            Enemy(self, enemytile[0], enemytile[1])
            self.spawnplacelist.remove(enemytile)
            i += 1
        

        if self.characternumber == 0:
            self.coinspawncount = 6
        o = 1
        while o <= self.coinspawncount:
            cointile = random.choice(self.spawnplacelist)
            Coin(self, cointile[0], cointile[1])
            self.spawnplacelist.remove(cointile)
            o += 1

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
            if self.gamestate == "gamewon":
                self.gamewon()

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
            self.map_data = []
            self.load_map()

        # Character selection
        if self.leftbtn.draw(self.screen):
            self.characternumber -= 1
        if self.rightbtn.draw(self.screen):
            self.characternumber += 1
        self.characternumber = self.characternumber % len(self.characterlist)

        if self.characternumber == 0:
            self.Tyler.draw(self.screen)
        elif self.characternumber == 1:
            self.Adrian.draw(self.screen)
        elif self.characternumber == 2:
            self.Myles.draw(self.screen)
        
        pg.display.flip()

    # death function
    def gameover(self):
        self.screen.fill(BLACK)
        self.youdiedimg.draw(self.screen)
        if self.restartbtn.draw(self.screen):
            self.coincount = 0
            self.gamelevel = 0
            self.enemycount = INITIALENEMYCOUNT
            self.update_map()
            self.new(True)
            self.gamestate = "mainmenu"
        pg.display.flip()

    # Win function
    def gamewon(self):
        self.screen.fill(BLACK)
        self.youwinimg.draw(self.screen)
        if self.restartbtn.draw(self.screen):
            self.gamelevel = 0
            self.enemycount += 1
            self.update_map()
            self.new(True)
            self.gamestate = "mainmenu"
        pg.display.flip()

    # Showing the go screen

                

# Making and running the window
g = Game()
while True:
    g.run()