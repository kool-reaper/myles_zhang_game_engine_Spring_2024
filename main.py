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
        self.paused = False

        # Player statistics
        self.gamelevel = 0
        self.currmap = 0
        self.coincount = 0
        self.coinspawncount = INITIALCOINCOUNT
        self.characternumber = 0
        self.characterlist = ["Tyler", "Adrian", "Rameil", "Robbie", "Myles"]
        self.maplist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
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
        self.currmaplist = random.sample(self.maplist, 5)
        random.shuffle(self.currmaplist)
    
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
            self.draw_text(self.screen, "Extra coins", 42, BLACK, "tm", 512, 360)
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
            self.LBupdate()

        pg.display.flip()

    # Draw game over screen
    def gameover(self):
        self.screen.fill(BLACK)

        # Draw text
        self.draw_text(self.screen, "YOU DIED", 180, WHITE, "tm", 512, 200)
        self.draw_text(self.screen, "Final coin count: " + str(self.coincount), 90, WHITE, "tm", 512, 400)

        # Draw exit button
        if self.rightbtn.draw(self.screen, 512, 550, 1):
            self.LBcheck()

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