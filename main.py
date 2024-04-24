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
        self.gamestate = "leaderboard"
        # Player statistics
        self.gamelevel = 0
        self.coincount = 0
        self.coinspawncount = INITIALCOINCOUNT
        self.characternumber = 0
        self.characterlist = ["Tyler", "Adrian", "Rameil", "Robbie", "Myles"]
        self.hp = INITIALSTARTINGLIVES
        self.playerspeed = PLAYER_SPEED
        self.powerscaling = False
        self.load_assets()

    # Load game assets
    def load_assets(self):
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'player.png')).convert_alpha()
        self.playbtn_img = pg.image.load(path.join(img_folder, 'play.png')).convert_alpha()
        self.playbtn = Button(self, self.playbtn_img, 1)
        self.restart_img = pg.image.load(path.join(img_folder, 'Restart.png')).convert_alpha()
        self.restartbtn = Button(self, self.restart_img, 1)
        self.left_img = pg.image.load(path.join(img_folder, 'Leftbutton.png')).convert_alpha()
        self.leftbtn = Button(self, self.left_img, 1)
        self.right_img = pg.image.load(path.join(img_folder, 'Rightbutton.png')).convert_alpha()
        self.rightbtn = Button(self, self.right_img, 1)
        self.Tyler_img = pg.image.load(path.join(img_folder, 'Tyler.png')).convert_alpha()
        self.Tyler = Image(self, self.Tyler_img, 4)
        self.Adrian_img = pg.image.load(path.join(img_folder, 'Adrian.png')).convert_alpha()
        self.Adrian = Image(self, self.Adrian_img, 4)
        self.Myles_img = pg.image.load(path.join(img_folder, 'Myles.png')).convert_alpha()
        self.Myles = Image(self, self.Myles_img, 4)
        self.Ramiel_img = pg.image.load(path.join(img_folder, 'Rameil.png')).convert_alpha()
        self.Rameil = Image(self, self.Ramiel_img, 4)
        self.Robbie_img = pg.image.load(path.join(img_folder, 'Robbie.png')).convert_alpha()
        self.Robbie = Image(self, self.Robbie_img, 4)
        self.LBbox_img = pg.image.load(path.join(img_folder, 'Leaderboardbox.png')).convert_alpha()
        self.LBbox = Image(self, self.LBbox_img, 1.5)
        self.LBbutton_img = pg.image.load(path.join(img_folder, 'Leaderboardbutton.png')).convert_alpha()
        self.LBbutton = Button(self, self.LBbutton_img, 1)


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
            if self.gamestate == "damaged":
                if self.hp == 0:
                    self.gameover()
                else:
                    self.lifelost()
            if self.gamestate == "gamewon":
                self.gamewon()
            if self.gamestate == "leaderboard":
                self.leaderboard()

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
        self.draw_text(self.screen, "Coins: " + str(self.coincount), 42, BLACK, "tl", 48, 32)
        self.draw_text(self.screen, "Lives: " + str(self.hp), 42, BLACK, "tl", 50, 96)
        pg.display.flip()

    # input method
    def events(self):
        for event in pg.event.get():
            # quit method
            if event.type == pg.QUIT:
                self.quit()

    # Drawing text
    def draw_text(self, surface, text, size, color, tltm, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if tltm == "tl":
            text_rect.topleft = (x,y)
        if tltm == "tm":
            text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

    # reset variables upon game restart
    def resetvar(self):
        self.playerspeed = PLAYER_SPEED
        self.coinspawncount = INITIALCOINCOUNT
        self.enemycount = INITIALENEMYCOUNT
        self.hp = INITIALSTARTINGLIVES
        self.gamelevel = 0
        self.coincount = 0
        self.powerscaling = False

    # Character effects
    def charactereffects(self):
        if self.characternumber == 0:
            self.coinspawncount = 6
        if self.characternumber == 1:
            self.playerspeed = 350
        if self.characternumber == 2:
            self.hp = 4
        if self.characternumber == 3:
            self.powerscaling = True
        if self.characternumber == 4:
            self.playerspeed = 250
            self.hp = 2

    # displaying start screen
    def main_menu(self):
        self.screen.fill(GRAY)
        if self.playbtn.draw(self.screen, 512, 544):
            self.gamestate = "playing"
            self.map_data = []
            self.charactereffects()
            self.load_map()

        # Character selection
        if self.leftbtn.draw(self.screen, 312, 224):
            self.characternumber -= 1
        if self.rightbtn.draw(self.screen, 712, 224):
            self.characternumber += 1
        self.characternumber = self.characternumber % len(self.characterlist)

        if self.characternumber == 0:
            self.Tyler.draw(self.screen, 512, 200)
            self.draw_text(self.screen, "Tyler", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Spawns 2 extra coins", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 1:
            self.Adrian.draw(self.screen, 512, 200)
            self.draw_text(self.screen, "Adrian", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Speed bonus", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 2:
            self.Rameil.draw(self.screen, 512, 200)
            self.draw_text(self.screen, "Rameil", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Extra life", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 3:
            self.Robbie.draw(self.screen, 512, 200)
            self.draw_text(self.screen, "Robbie", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Power scaling", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 4:
            self.Myles.draw(self.screen, 512, 200)
            self.draw_text(self.screen, "Myles", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Challenge character", 42, BLACK, "tm", 512, 360)
        
        if self.LBbutton.draw(self.screen, 512, 644):
            self.gamestate = "leaderboard"

        pg.display.flip()

    def leaderboard(self):
        self.screen.fill(GRAY)

        self.LBbox.draw(self.screen, 356, 50)
        self.LBbox.draw(self.screen, 668, 50)
        self.LBbox.draw(self.screen, 356, 185)
        self.LBbox.draw(self.screen, 668, 185)
        self.LBbox.draw(self.screen, 356, 320)
        self.LBbox.draw(self.screen, 668, 320)
        self.LBbox.draw(self.screen, 356, 455)
        self.LBbox.draw(self.screen, 668, 455)
        self.LBbox.draw(self.screen, 356, 590)
        self.LBbox.draw(self.screen, 668, 590)

        if self.leftbtn.draw(self.screen, 150, 50):
            self.gamestate = "mainmenu"

        pg.display.flip()

    # death function
    def gameover(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "YOU DIED", 180, WHITE, "tm", 512, 200)
        self.draw_text(self.screen, "Final coin count: " + str(self.coincount), 90, WHITE, "tm", 512, 400)
        if self.restartbtn.draw(self.screen, 512, 550):
            self.resetvar()
            self.update_map()
            self.new(True)
            self.gamestate = "mainmenu"
        pg.display.flip()

    # life lost function
    def lifelost(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "LIFE LOST", 180, WHITE, "tm", 512, 200)
        self.draw_text(self.screen, str(self.hp) + " REMAINING", 180, WHITE, "tm", 512, 350)
        if self.restartbtn.draw(self.screen, 512, 550):
            self.update_map()
            self.new(False)
            self.gamestate = "playing"
        pg.display.flip()

    # Win function
    def gamewon(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "ROUND", 180, WHITE, "tm", 512, 200)
        self.draw_text(self.screen, "COMPLETE", 180, WHITE, "tm", 512, 350)
        if self.rightbtn.draw(self.screen, 512, 550):
            self.gamelevel = 0
            self.enemycount += 1
            self.update_map()
            self.new(True)
            self.gamestate = "playing"
        pg.display.flip()

    # Showing the go screen

                

# Making and running the window
g = Game()
while True:
    g.run()