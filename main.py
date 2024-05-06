# This file was created by the one and only Myles Zhang
# With help from Ai and Youtube
# My first source control edit!

# Imports
import pygame as pg
from settings import *
from sprites import *
from loaders import *
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
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        # Game states
        self.running = True
        self.gamestate = "startscreen"
        self.paused = False

        # Player statistics
        self.gamelevel = 0
        self.currmap = 0
        self.coincount = 0
        self.coinspawncount = INITIALCOINCOUNT
        self.characternumber = 0
        self.characterlist = ["Tyler", "Adrian", "Rameil", "Robbie", "Myles"]
        self.maplist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
        self.currmaplist = []
        self.hp = INITIALSTARTINGLIVES
        self.enemycount = INITIALENEMYCOUNT
        self.playerspeed = PLAYER_SPEED
        self.powerscaling = False
        self.username = ''
        self.coinbar = 0

    # Load map for the first time
    def load_map(self):
        # Store last played map
        if self.currmaplist != []:
            lastmap = self.currmaplist[-1]
        else:
            lastmap = None

        # Reload maps
        self.currmaplist = random.sample(self.maplist, 5)
        random.shuffle(self.currmaplist)
        print(self.currmaplist)

        # Keep reloading maps to prevent repeat levels
        while self.currmaplist[0] == lastmap:
            self.currmaplist = random.sample(self.maplist, 5)
            random.shuffle(self.currmaplist)
            print(self.currmaplist)

        # Open and read map
        self.currmap = 0
        self.map_data = []
        with open(path.join(map_folder, 'map' + str(self.currmaplist[0]) + '.txt'), 'rt') as f:
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
            self.currmap += 1
            self.map_data = []
            with open(path.join(map_folder, 'map' + str(self.currmaplist[self.currmap % 5]) + '.txt'), 'rt') as f:
                for line in f:
                    self.map_data.append(line)
            self.new()

    # Init all variables, setup groups, instantiate classes
    def new(self):
        # Reload spawnpoints
        self.enemyspawnplacelist = []
        self.coinspawnplacelist = []

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
                    # Add . tiles to potential coin + enemy spawnpoints
                    self.enemyspawnplacelist.append((col, row))
                    self.coinspawnplacelist.append((col, row))
                if tile == "-":
                    # Add - tiles to potential coin spawnpoints
                    self.coinspawnplacelist.append((col, row))
        
        # Spawn enemies
        i = 1
        while i <= self.enemycount:
            # Find random spawnpoint, remove spawnpoint from list to prevent overlap
            enemytile = random.choice(self.enemyspawnplacelist)
            Enemy(self, enemytile[0], enemytile[1])
            self.enemyspawnplacelist.remove(enemytile)
            self.coinspawnplacelist.remove(enemytile)
            i += 1
        
        # Spawn coins
        o = 1
        while o <= self.coinspawncount:
            # Find random spawnpoint, remove spawnpoint from list to prevent overlap
            cointile = random.choice(self.coinspawnplacelist)
            Coin(self, cointile[0], cointile[1])
            self.coinspawnplacelist.remove(cointile)
            o += 1

    # Run method
    def run(self):
        self.playing = True
        while self.playing:
            # Tick the clock
            self.dt = self.clock.tick(FPS) / 1000
            self.events()

            # Display screens depending on gamestate
            if self.gamestate == "startscreen":
                self.startscreen()
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
            if self.gamestate == "info":
                self.infoscreen()

        # Load events
        while self.running:
            self.events()

    # Quit method
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
            pg.draw.line(SCREEN, LIGHTGRAY, (x,0), (x, HEIGHT))
        for y in range (0, WIDTH, TILESIZE):
            pg.draw.line(SCREEN, LIGHTGRAY, (0,y), (WIDTH, y))

    # Draw ingame display
    def draw(self):
        # Draw ingame assets
        SCREEN.fill(BGCOLOR)
        self.draw_grid()
        self.game_sprites.draw(SCREEN)

        # Draw paused screen
        if self.paused == True:
            self.pausedstate()
        else:
            # Draw statistics trackers
            self.draw_text(SCREEN, "Coins: " + str(self.coincount), 42, BLACK, "tl", 48, 32)
            self.draw_text(SCREEN, "Lives: " + str(self.hp), 42, BLACK, "tl", 50, 96)

        pg.display.flip()

    # Input method
    def events(self):
        for event in pg.event.get():
            # Quit method
            if event.type == pg.QUIT:
                self.quit()
            
            # Text entry method
            elif event.type == pg.KEYDOWN:

                # Text entry for entering usernames
                if self.gamestate == "LBentry":
                    if event.key == pg.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pg.K_RETURN:
                        pass
                    else:
                        # Restrain too long usernames
                        if len(self.username) < 10:
                            self.username += event.unicode

                if self.gamestate == "playing":
                    # Escape to pause
                    if event.key == pg.K_ESCAPE:
                        if self.paused == False:
                            self.paused = True
                        else:
                            self.paused = False

                    # r to restart
                    if event.key == pg.K_r:
                        self.gamestate = "mainmenu"
                        self.resetvar()

                # Character selection
                if self.gamestate == "mainmenu":
                    if event.key == pg.K_LEFT:
                        self.characternumber -= 1
                    if event.key == pg.K_RIGHT:
                        self.characternumber += 1

                # QOL buttons
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    if self.gamestate == "mainmenu":
                        self.gamestate = "playing"
                        self.paused == False
                        self.map_data = []
                        self.charactereffects()
                        self.load_map()        
                    elif self.gamestate == "damaged":
                        if self.hp == 0:
                            self.LBcheck()
                        else:
                            self.update_map()
                            self.new()
                            self.gamestate = "playing"
                    elif self.gamestate == "gamewon":
                        self.gamelevel = 0
                        self.enemycount += 1
                        self.update_map()
                        self.new()
                        self.gamestate = "playing"
                    elif self.gamestate == "LBentry":
                        self.LBupdate()
                if event.key == pg.K_ESCAPE:
                    if self.gamestate == "leaderboard":
                        self.gamestate = "mainmenu"
                    if self.gamestate == "info":
                        self.gamestate = "mainmenu"

    # Check if score is high enough for leaderboard
    def LBcheck(self):
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

    # Update leaderboard
    def LBupdate(self):
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
            self.coinspawncount = 5
        if self.characternumber == 1:
            self.playerspeed = 360
        if self.characternumber == 2:
            self.hp = 5
        if self.characternumber == 3:
            self.powerscaling = True
        if self.characternumber == 4:
            self.playerspeed = 240
            self.hp = 2

    # Display paused screen
    def pausedstate(self):
        pausedbg = pg.Surface((1024, 768), pg.SRCALPHA)
        pausedbg.fill((206, 204, 197, 128))
        SCREEN.blit(pausedbg, (0, 0))
        self.draw_text(SCREEN, "PAUSED", 150, BLACK, "tm", 512, 300)
        self.draw_text(SCREEN, "press escape to continue", 30, BLACK, "tm", 512, 470)

    # Display start screen
    def startscreen(self):
        SCREEN.fill(GRAY)
        self.draw_text(SCREEN, "AE", 200, BLACK, "tm", 512, 200)

        # Draw play button
        if playbtn.draw(SCREEN, 512, 444, 1):
            self.gamestate = "mainmenu"
            self.map_data = []
            self.charactereffects()
            self.load_map()

        pg.display.flip()

    # Display main menu screen
    def main_menu(self):
        SCREEN.fill(GRAY)

        # Draw play button
        if playbtn.draw(SCREEN, 512, 544, 1):
            self.gamestate = "playing"
            self.map_data = []
            self.charactereffects()
            self.load_map()
            self.paused = False

        # Character selection
        if leftbtn.draw(SCREEN, 312, 224, 1):
            self.characternumber -= 1
        if rightbtn.draw(SCREEN, 712, 224, 1):
            self.characternumber += 1
        self.characternumber = self.characternumber % len(self.characterlist)

        # Character selection display and descriptions
        if self.characternumber == 0:
            Tyler.draw(SCREEN, 512, 200, 4)
            self.draw_text(SCREEN, "Tyler", 42, BLACK, "tm", 512, 130)
            self.draw_text(SCREEN, "Extra coins", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 1:
            Adrian.draw(SCREEN, 512, 200, 4)
            self.draw_text(SCREEN, "Adrian", 42, BLACK, "tm", 512, 130)
            self.draw_text(SCREEN, "Speed bonus", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 2:
            Rameil.draw(SCREEN, 512, 200, 4)
            self.draw_text(SCREEN, "Rameil", 42, BLACK, "tm", 512, 130)
            self.draw_text(SCREEN, "Extra lives", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 3:
            Robbie.draw(SCREEN, 512, 200, 4)
            self.draw_text(SCREEN, "Robbie", 42, BLACK, "tm", 512, 130)
            self.draw_text(SCREEN, "Power scaling", 42, BLACK, "tm", 512, 360)
        elif self.characternumber == 4:
            Myles.draw(SCREEN, 512, 200, 4)
            self.draw_text(SCREEN, "Myles", 42, BLACK, "tm", 512, 130)
            self.draw_text(SCREEN, "Challenge character", 42, BLACK, "tm", 512, 360)
        
        # Draw leaderbaord button
        if LBbutton.draw(SCREEN, 512, 644, 1):
            self.gamestate = "leaderboard"

        # Draw information button
        if infobutton.draw(SCREEN, 100, 644, 1):
            self.gamestate = "info"

        pg.display.flip()

    # Display information screen
    def infoscreen(self):
        SCREEN.fill(GRAY)

        # How to play
        self.draw_text(SCREEN, "How 2 play:", 50, BLACK, "tl", 170, 50)
        self.draw_text(SCREEN, "Collect yellow coins for score", 30, BLACK, "tl", 170, 100)
        self.draw_text(SCREEN, "Reach green door to move to next level", 30, BLACK, "tl", 170, 130)
        self.draw_text(SCREEN, "Hitting a red enemy damages you", 30, BLACK, "tl", 170, 160)
        self.draw_text(SCREEN, "Top 10 scores make it to the leaderboard", 30, BLACK, "tl", 170, 190)
        self.draw_text(SCREEN, "An enemy is added every round (or 5 levels)", 30, BLACK, "tl", 170, 220)

        # Controls explanation
        self.draw_text(SCREEN, "Controls:", 50, BLACK, "tl", 170, 300)
        self.draw_text(SCREEN, "WASD or arrowkeys to move", 30, BLACK, "tl", 170, 350)
        self.draw_text(SCREEN, "r to restart", 30, BLACK, "tl", 170, 380)

        # Detailed character information
        self.draw_text(SCREEN, "Character information:", 50, BLACK, "tl", 170, 460)
        self.draw_text(SCREEN, "Tyler spawns one extra coin per level", 30, BLACK, "tl", 170, 510)
        self.draw_text(SCREEN, "Adrian is about 20% faster", 30, BLACK, "tl", 170, 540)
        self.draw_text(SCREEN, "Ramiel has 2 extra lives", 30, BLACK, "tl", 170, 570)
        self.draw_text(SCREEN, "Robbie gains 1% speed per level and an extra spawned coin per 10 levels", 30, BLACK, "tl", 170, 600)
        self.draw_text(SCREEN, "Note: Robbie's speed is capped at 20%", 30, BLACK, "tl", 170, 630)
        self.draw_text(SCREEN, "Myles has 1 less life and is 20% slower", 30, BLACK, "tl", 170, 660)

        # Draw exit button
        if leftbtn.draw(SCREEN, 85, 50, 1):
            self.gamestate = "mainmenu"

        pg.display.flip()

    # Display leaderboard
    def leaderboard(self):
        SCREEN.fill(GRAY)

        # Draw leaderboard boxes
        LBbox.draw(SCREEN, 356, 50, 1.5)
        LBbox.draw(SCREEN, 668, 50, 1.5)
        LBbox.draw(SCREEN, 356, 185, 1.5)
        LBbox.draw(SCREEN, 668, 185, 1.5)
        LBbox.draw(SCREEN, 356, 320, 1.5)
        LBbox.draw(SCREEN, 668, 320, 1.5)
        LBbox.draw(SCREEN, 356, 455, 1.5)
        LBbox.draw(SCREEN, 668, 455, 1.5)
        LBbox.draw(SCREEN, 356, 590, 1.5)
        LBbox.draw(SCREEN, 668, 590, 1.5)

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
            self.draw_text(SCREEN, username, 32, WHITE, "tl", x - 100, y + 10)
            self.draw_text(SCREEN, str(entry["score"]), 32, WHITE, "tl", x - 100, y + 52)

            # Draw character used
            characternumber = entry["character"]
            if characternumber == 0:
                Tyler.draw(SCREEN, x + 80, y + 60, 1)
            elif characternumber == 1:
                Adrian.draw(SCREEN, x + 80, y + 60, 1)
            elif characternumber == 2:
                Rameil.draw(SCREEN, x + 80, y + 60, 1)
            elif characternumber == 3:
                Robbie.draw(SCREEN, x + 80, y + 60, 1)
            elif characternumber == 4:
                Myles.draw(SCREEN, x + 80, y + 60, 1)
                
        # Draw exit button
        if leftbtn.draw(SCREEN, 85, 50, 1):
            self.gamestate = "mainmenu"

        pg.display.flip()

    # Leaderboard input
    def LBentry(self):
        SCREEN.fill(BLACK)

        # Draw text
        self.draw_text(SCREEN, "TOP 10 SCORE!", 150, WHITE, "tm", 512, 100)
        self.draw_text(SCREEN, "Enter name:", 90, WHITE, "tm", 512, 250)
       
        # Draw text box
        pg.draw.rect(SCREEN, (255, 255, 255), (200, 350, 624, 100), 3)

        # Display typing
        self.draw_text(SCREEN, self.username, 90, WHITE, "tm", 512, 350)
        
        # Draw restart button
        if restartbtn.draw(SCREEN, 512, 550, 1):
            self.LBupdate()

        pg.display.flip()

    # Draw game over screen
    def gameover(self):
        SCREEN.fill(BLACK)

        # Draw text
        self.draw_text(SCREEN, "YOU DIED", 180, WHITE, "tm", 512, 200)
        self.draw_text(SCREEN, "Final coin count: " + str(self.coincount), 90, WHITE, "tm", 512, 400)

        # Draw exit button
        if rightbtn.draw(SCREEN, 512, 550, 1):
            self.LBcheck()

        pg.display.flip()

    # Draw life lost screen
    def lifelost(self):
        SCREEN.fill(BLACK)
        
        # Draw text
        self.draw_text(SCREEN, "LIFE LOST", 180, WHITE, "tm", 512, 200)
        self.draw_text(SCREEN, str(self.hp) + " REMAINING", 180, WHITE, "tm", 512, 350)

        # Draw restart button
        if restartbtn.draw(SCREEN, 512, 550, 1):
            self.update_map()
            self.new()
            self.gamestate = "playing"

        pg.display.flip()

    # Win function
    def gamewon(self):
        SCREEN.fill(BLACK)

        # Draw text
        self.draw_text(SCREEN, "ROUND", 180, WHITE, "tm", 512, 200)
        self.draw_text(SCREEN, "COMPLETE", 180, WHITE, "tm", 512, 350)

        # Draw continue button
        if rightbtn.draw(SCREEN, 512, 550, 1):
            # Reset to level 1
            self.gamelevel = 0
            self.player.changelevel = False

            # Increaes enemy count per level
            self.enemycount += 1

            # Update map and gamestate
            self.load_map()
            self.new()
            self.gamestate = "playing"

        pg.display.flip()

    # Showing the go screen

# Making and running the window
g = Game()
while True:
    g.run()