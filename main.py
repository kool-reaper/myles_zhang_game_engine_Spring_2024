# This file was created by the one and only Myles Zhang
# With help from Ai and Youtube
# My first source control edit!

# Imports
import pygame as pg
from settings import *
from sprites import *
import sys
import random
from os import path
import os
from time import sleep
import json
from math import floor

# This 'cooldown' class is designed to help us control time
class Cooldown():
    # Sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # Ticking ensures the timer is counting...
    # Must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # Resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # Sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

# Creating game class
class Game:
    # Defining game class
    def __init__(self):
        # General game initialization
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        # Game states
        self.running = True
        self.gamestate = "mainmenu"

        # Player statistics
        self.gamelevel = 0
        self.coincount = 0
        self.coinspawncount = INITIALCOINCOUNT
        self.characternumber = 0
        self.characterlist = ["Tyler", "Adrian", "Rameil", "Robbie", "Myles"]
        self.hp = INITIALSTARTINGLIVES
        self.enemycount = INITIALENEMYCOUNT
        self.playerspeed = PLAYER_SPEED
        self.powerscaling = False
        self.username = ''
        self.coinbar = 0
        
        # Load game assets
        self.load_assets()

    # Load game assets
    def load_assets(self):
        # Load assets
        self.player_img = pg.image.load(path.join(img_folder, 'player.png')).convert_alpha()
        self.playbtn_img = pg.image.load(path.join(img_folder, 'play.png')).convert_alpha()
        self.playbtn = Button(self, self.playbtn_img)
        self.restart_img = pg.image.load(path.join(img_folder, 'Restart.png')).convert_alpha()
        self.restartbtn = Button(self, self.restart_img)
        self.left_img = pg.image.load(path.join(img_folder, 'Leftbutton.png')).convert_alpha()
        self.leftbtn = Button(self, self.left_img)
        self.right_img = pg.image.load(path.join(img_folder, 'Rightbutton.png')).convert_alpha()
        self.rightbtn = Button(self, self.right_img)
        self.Tyler_img = pg.image.load(path.join(img_folder, 'Tyler.png')).convert_alpha()
        self.Tyler = Image(self, self.Tyler_img)
        self.Adrian_img = pg.image.load(path.join(img_folder, 'Adrian.png')).convert_alpha()
        self.Adrian = Image(self, self.Adrian_img)
        self.Myles_img = pg.image.load(path.join(img_folder, 'Myles.png')).convert_alpha()
        self.Myles = Image(self, self.Myles_img)
        self.Ramiel_img = pg.image.load(path.join(img_folder, 'Rameil.png')).convert_alpha()
        self.Rameil = Image(self, self.Ramiel_img)
        self.Robbie_img = pg.image.load(path.join(img_folder, 'Robbie.png')).convert_alpha()
        self.Robbie = Image(self, self.Robbie_img)
        self.LBbox_img = pg.image.load(path.join(img_folder, 'Leaderboardbox.png')).convert_alpha()
        self.LBbox = Image(self, self.LBbox_img)
        self.LBbutton_img = pg.image.load(path.join(img_folder, 'Leaderboardbutton.png')).convert_alpha()
        self.LBbutton = Button(self, self.LBbutton_img)


    # Load map for the first time
    def load_map(self):
        # Open and read map
        with open(path.join(map_folder, 'map0.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

        # Create map
        self.new()

    # Updating the map when the level changes
    def update_map(self):
        # Open and read map
        if self.player.changelevel == True:
            self.player.changelevel = False
            self.gamelevel += 1
            self.map_data = []
            with open(path.join(map_folder, 'map' + str(self.gamelevel) + '.txt'), 'rt') as f:
                for line in f:
                    self.map_data.append(line)
            self.new()

    # Init all variables, setup groups, instantiate classes
    def new(self):
        # Reload spawnpoints
        self.spawnplacelist = []

        # Initialize groups
        self.game_sprites = pg.sprite.Group()
        self.mainmenu_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.doors = pg.sprite.Group()

        # Read map
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
                    # Add . tiles to potential spawnpoints
                    self.spawnplacelist.append((col, row))
        
        # Spawn enemies
        i = 1
        while i <= self.enemycount:
            # Find random spawnpoint, remove spawnpoint from list to prevent overlap
            enemytile = random.choice(self.spawnplacelist)
            Enemy(self, enemytile[0], enemytile[1])
            self.spawnplacelist.remove(enemytile)
            i += 1
        
        # Spawn coins
        o = 1
        while o <= self.coinspawncount:
            # Find random spawnpoint, remove spawnpoint from list to prevent overlap
            cointile = random.choice(self.spawnplacelist)
            Coin(self, cointile[0], cointile[1])
            self.spawnplacelist.remove(cointile)
            o += 1

    # run method
    def run(self):
        self.playing = True
        while self.playing:
            # Tick the clock
            self.dt = self.clock.tick(FPS) / 1000
            self.events()

            # Display screens depending on gamestate
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
            if self.gamestate == "LBentry":
                self.LBentry()

        # Load events
        while self.running:
            self.events()

    # Quit function
    def quit(self):
        pg.quit()
        sys.exit()

    # Update display and positions
    def update(self):
        self.game_sprites.update()
        self.update_map()

    # Draw grid
    def draw_grid(self):
        for x in range (0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (x,0), (x, HEIGHT))
        for y in range (0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (0,y), (WIDTH, y))

    # Draw ingame display
    def draw(self):
        # Draw ingame assets
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.game_sprites.draw(self.screen)

        # Draw statistics trackers
        self.draw_text(self.screen, "Coins: " + str(self.coincount), 42, BLACK, "tl", 48, 32)
        self.draw_text(self.screen, "Lives: " + str(self.hp), 42, BLACK, "tl", 50, 96)

        pg.display.flip()

    # Input method
    def events(self):
        for event in pg.event.get():
            # Quit method
            if event.type == pg.QUIT:
                self.quit()
            
            # Text entry method
            elif event.type == pg.KEYDOWN:
                if self.gamestate == "LBentry":
                    if event.key == pg.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        # Restrain too long usernames
                        if len(self.username) < 10:
                            self.username += event.unicode

    # Draw text
    def draw_text(self, surface, text, size, color, tltm, x, y):
        # Initialize text variables
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        # Figure out whether coordinates are from left or centered
        if tltm == "tl":
            text_rect.topleft = (x,y)
        if tltm == "tm":
            text_rect.midtop = (x,y)
        
        surface.blit(text_surface, text_rect)

    # Reset game/player variables
    def resetvar(self):
        self.playerspeed = PLAYER_SPEED
        self.coinspawncount = INITIALCOINCOUNT
        self.enemycount = INITIALENEMYCOUNT
        self.hp = INITIALSTARTINGLIVES
        self.gamelevel = 0
        self.coincount = 0
        self.powerscaling = False
        self.username = ""

    # Character effects
    def charactereffects(self):
        if self.characternumber == 0:
            self.coinspawncount = 6
        if self.characternumber == 1:
            self.playerspeed = 350
        if self.characternumber == 2:
            self.hp = 5
        if self.characternumber == 3:
            self.powerscaling = True
        if self.characternumber == 4:
            self.playerspeed = 250
            self.hp = 2

    # Display main menu screen
    def main_menu(self):
        self.screen.fill(GRAY)

        # Draw play button
        if self.playbtn.draw(self.screen, 512, 544, 1):
            self.gamestate = "playing"
            self.map_data = []
            self.charactereffects()
            self.load_map()

        # Character selection
        if self.leftbtn.draw(self.screen, 312, 224, 1):
            self.characternumber -= 1
        if self.rightbtn.draw(self.screen, 712, 224, 1):
            self.characternumber += 1
        self.characternumber = self.characternumber % len(self.characterlist)

        # Character selection display and descriptions
        if self.characternumber == 0:
            self.Tyler.draw(self.screen, 512, 200, 4)
            self.draw_text(self.screen, "Tyler", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Spawns 2 extra coins", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 1:
            self.Adrian.draw(self.screen, 512, 200, 4)
            self.draw_text(self.screen, "Adrian", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Speed bonus", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 2:
            self.Rameil.draw(self.screen, 512, 200, 4)
            self.draw_text(self.screen, "Rameil", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Extra lives", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 3:
            self.Robbie.draw(self.screen, 512, 200, 4)
            self.draw_text(self.screen, "Robbie", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Power scaling", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 4:
            self.Myles.draw(self.screen, 512, 200, 4)
            self.draw_text(self.screen, "Myles", 42, BLACK, "tm", 512, 130)
            self.draw_text(self.screen, "Challenge character", 42, BLACK, "tm", 512, 360)
        
        # Draw leaderbaord button
        if self.LBbutton.draw(self.screen, 512, 644, 1):
            self.gamestate = "leaderboard"

        pg.display.flip()

    # Display leaderboard
    def leaderboard(self):
        self.screen.fill(GRAY)

        # Draw leaderboard boxes
        self.LBbox.draw(self.screen, 356, 50, 1.5)
        self.LBbox.draw(self.screen, 668, 50, 1.5)
        self.LBbox.draw(self.screen, 356, 185, 1.5)
        self.LBbox.draw(self.screen, 668, 185, 1.5)
        self.LBbox.draw(self.screen, 356, 320, 1.5)
        self.LBbox.draw(self.screen, 668, 320, 1.5)
        self.LBbox.draw(self.screen, 356, 455, 1.5)
        self.LBbox.draw(self.screen, 668, 455, 1.5)
        self.LBbox.draw(self.screen, 356, 590, 1.5)
        self.LBbox.draw(self.screen, 668, 590, 1.5)

        # Open leaderboard file
        if os.path.exists("leaderboard.json") and os.path.getsize("leaderboard.json") > 0:
            with open("leaderboard.json", 'r') as file:
                data = json.load(file)
        else: 
            data = []
        
        # Draw leaderboard info
        for entry in data:
            # Find where the information should be drawn
            placement = data.index(entry)
            if placement % 2 == 0:
                x = 356
            else:
                x = 668
            y = 50 + (floor((placement) / 2) * 135)

            # Give names to unnamed placements
            if entry["username"] == "":
                username = "Unnamed Player"
            else:
                username = entry["username"]

            # Draw username and score information
            self.draw_text(self.screen, username, 32, WHITE, "tl", x - 100, y + 10)
            self.draw_text(self.screen, str(entry["score"]), 32, WHITE, "tl", x - 100, y + 52)

            # Draw character used
            characternumber = entry["character"]
            if characternumber == 0:
                self.Tyler.draw(self.screen, x + 80, y + 60, 1)
            elif characternumber == 1:
                self.Adrian.draw(self.screen, x + 80, y + 60, 1)
            elif characternumber == 2:
                self.Rameil.draw(self.screen, x + 80, y + 60, 1)
            elif characternumber == 3:
                self.Robbie.draw(self.screen, x + 80, y + 60, 1)
            elif characternumber == 4:
                self.Myles.draw(self.screen, x + 80, y + 60, 1)
                
        # Draw exit button
        if self.leftbtn.draw(self.screen, 150, 50, 1):
            self.gamestate = "mainmenu"

        pg.display.flip()

    # Leaderboard input
    def LBentry(self):
        self.screen.fill(BLACK)

        # Draw text
        self.draw_text(self.screen, "TOP 10 SCORE!", 150, WHITE, "tm", 512, 100)
        self.draw_text(self.screen, "Enter name:", 90, WHITE, "tm", 512, 250)
       
        # Display typing
        self.draw_text(self.screen, self.username, 90, WHITE, "tm", 512, 350)
        
        # Draw restart button
        if self.restartbtn.draw(self.screen, 512, 550, 1):
            # Organize data to be saved
            LBdata = {
                "username": self.username,
                "score": self.coincount,
                "character": self.characternumber
                }
            
            # Open leaderboard file
            if os.path.exists("leaderboard.json") and os.path.getsize("leaderboard.json") > 0:
                with open("leaderboard.json", 'r') as file:
                    data = json.load(file)
            else: 
                data = []

            # Append current data
            data.append(LBdata)

            # Sort leaderboard data by greatest to least score
            data.sort(key = lambda x: x['score'], reverse=True)

            # Remove last entry if there are more than 10 scores
            if len(data) > 10:
                data.pop()

            # Replace leaderbaord data
            with open('leaderboard.json', "w") as LBfile:
                json.dump(data, LBfile, indent = 4)

            # Reset game
            self.resetvar()
            self.gamestate = "mainmenu"

        pg.display.flip()

    # Draw game over screen
    def gameover(self):
        self.screen.fill(BLACK)

        # Draw text
        self.draw_text(self.screen, "YOU DIED", 180, WHITE, "tm", 512, 200)
        self.draw_text(self.screen, "Final coin count: " + str(self.coincount), 90, WHITE, "tm", 512, 400)

        # Draw exit button
        if self.rightbtn.draw(self.screen, 512, 550, 1):
            self.update_map()
            self.new()

            # Open leaderboard file
            if os.path.exists("leaderboard.json") and os.path.getsize("leaderboard.json") > 0:
                with open("leaderboard.json", 'r') as file:
                    data = json.load(file)
            else: 
                data = []

            # Read leaderboard score information
            scorelist = []
            for entry in data:
                score = entry["score"]
                scorelist.append(int(score))

            # Enter current data
            scorelist.append(self.coincount)

            # Organize scores from highest to lowest
            scorelist.sort(reverse = True)

            # Allow new leaderboard entry if there are less than 10 total entries
            if len(scorelist) <= 10:
                self.gamestate = "LBentry"
            # Deny new leaderboard entry if current score is the lowest or equal to the lowest score
            elif scorelist[-1] == self.coincount:
                self.resetvar()
                self.gamestate = "mainmenu"
            # Allow new leaderboard entry if current score surpasses last place
            else:
                self.gamestate = "LBentry"

        pg.display.flip()

    # Draw life lost screen
    def lifelost(self):
        self.screen.fill(BLACK)
        
        # Draw text
        self.draw_text(self.screen, "LIFE LOST", 180, WHITE, "tm", 512, 200)
        self.draw_text(self.screen, str(self.hp) + " REMAINING", 180, WHITE, "tm", 512, 350)

        # Draw restart button
        if self.restartbtn.draw(self.screen, 512, 550, 1):
            self.update_map()
            self.new()
            self.gamestate = "playing"

        pg.display.flip()

    # Win function
    def gamewon(self):
        self.screen.fill(BLACK)

        # Draw text
        self.draw_text(self.screen, "ROUND", 180, WHITE, "tm", 512, 200)
        self.draw_text(self.screen, "COMPLETE", 180, WHITE, "tm", 512, 350)

        # Draw continue button
        if self.rightbtn.draw(self.screen, 512, 550, 1):
            # Reset to level 1
            self.gamelevel = 0

            # Increaes enemy count per level
            self.enemycount += 1

            # Update map and gamestate
            self.update_map()
            self.new()
            self.gamestate = "playing"

        pg.display.flip()

    # Showing the go screen

# Making and running the window
g = Game()
while True:
    g.run()