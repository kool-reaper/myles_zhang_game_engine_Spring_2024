# This file was created by the one and only Myles Zhang

# Imports
import pygame as pg
from settings import *
from pygame.sprite import Sprite
from os import path

# Spritesheet class
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width, height))
        return image

# Player Class
class Player(Sprite):
    # Initialize class
    def __init__(self, game, x, y):
        self.groups = game.game_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.changelevel = 0
        self.p_pressed = False
        self.spritesheet = Spritesheet(path.join(img_folder, PLAYERSPRITESHEET))
        self.current_frame = 0
        self.last_update = 0
    def animate(self):
        if self.game.characternumber == 0:
            self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),  self.spritesheet.get_image(32, 0, 32, 32)]
        if self.game.characternumber == 1:
            self.standing_frames = [self.spritesheet.get_image(0, 32, 32, 32),  self.spritesheet.get_image(32, 32, 32, 32)]
        if self.game.characternumber == 2:
            self.standing_frames = [self.spritesheet.get_image(0, 96, 32, 32),  self.spritesheet.get_image(32, 96, 32, 32)]
        if self.game.characternumber == 3:
            self.standing_frames = [self.spritesheet.get_image(0, 128, 32, 32),  self.spritesheet.get_image(32, 128, 32, 32)]
        if self.game.characternumber == 4:
            self.standing_frames = [self.spritesheet.get_image(0, 64, 32, 32),  self.spritesheet.get_image(32, 64, 32, 32)]
        
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    # Checking which keys are pressed
    def getkeys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.game.playerspeed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.game.playerspeed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.game.playerspeed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.game.playerspeed
        if keys[pg.K_r]:
            self.game.gamestate = "mainmenu"
            self.game.coincount = 0
            self.game.gamelevel = 0
            self.game.enemycount = INITIALENEMYCOUNT
            self.game.coinspawncount = INITIALCOINCOUNT
            self.game.new(True)
        if keys[pg.K_p]:
            self.p_pressed = True
        if keys[pg.K_p] == False and self.p_pressed == True:
            self.p_pressed = False
            self.game.gamelevel = 0
            self.game.enemycount += 1
            self.game.update_map()
            self.game.new(True)
        if self.vx != 0 and self.vy != 0:
            # Yay math!
            self.vx *= 0.7071
            self.vy *= 0.7071

    # Collision with walls
    def collidewithwalls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # Collisions with objects
    def collidewithobj(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if group == self.game.coins:
                self.game.coincount += 1
            if group == self.game.doors:
                if self.game.powerscaling == True:
                    self.game.playerspeed += 10
                if self.game.gamelevel == MAXMAP:
                    self.game.gamestate = "gamewon"
                    if self.game.powerscaling == True:
                        self.game.coinspawncount += 1
                else:
                    self.changelevel = True
            if group == self.game.enemies:
                self.game.hp -= 1
                self.game.gamestate = "damaged"


    # Updating the sprite and checking for collisions
    def update(self):
        self.animate()
        self.getkeys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collidewithwalls('x')
        self.rect.y = self.y
        self.collidewithwalls('y')
        self.collidewithobj(self.game.coins, True)
        self.collidewithobj(self.game.doors, False)
        self.collidewithobj(self.game.enemies, False)

# Enemy Class
class Enemy (Sprite):
    # Initialize class
    def __init__(self, game, x, y):
        self.groups = game.game_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 300, 300
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 300
        if self.vx != 0 and self.vy != 0:
            # Yay math!
            self.vx *= 0.7071
            self.vy *= 0.7071

    # Enemy bouncing off of walls
    def collidewithwalls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = -self.vx
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = -self.vy
                self.rect.y = self.y

    # Updating the sprite and checking for collisions
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collidewithwalls("x")
        self.rect.y = self.y
        self.collidewithwalls("y")

# Wall Class
class Wall(Sprite):
    # Initialize Class
    def __init__(self, game, x, y):
        self.groups = game.game_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BEIGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Coin Class
class Coin(Sprite):
    # Initialize Class
    def __init__(self, game, x, y):
        self.groups = game.game_sprites, game.coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Door Class
class Door(Sprite):
    # Initialize Class
    def __init__(self, game, x, y):
        self.groups = game.game_sprites, game.doors
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Button Class
# Taken from a tutorial by Coding With Russ on Youtube: https://www.youtube.com/watch?v=G8MYGDf_9ho
# Changed the code to not give an output when holding click over button; Only gives one output when mouse is released
# This way, you cannot activate multiple buttons with one click
class Button():
    # Initialize Class
    def __init__(self, game, img, scale):
        height = img.get_height()
        width = img.get_width()
        self.game = game
        self.image = pg.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.clicked = False

    # Drawing the button
    def draw(self, surface, x, y):
        action = False

        # Finding mouse location
        mousepos = pg.mouse.get_pos()

        self.rect.midtop = (x,y)


        # Checking mouse and button status
        if self.rect.collidepoint(mousepos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = False
            if pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
        else:
            self.clicked = False

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Drawing the button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        # Return pressed or not pressed
        return action
    
# Image Class
class Image():
    # Initialize Class
    def __init__(self, game, img, scale):
        height = img.get_height()
        width = img.get_width()
        self.game = game
        self.image = pg.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

    # Displaying the Image
    def draw(self, surface, x, y):
        self.rect.midtop = (x,y)
        surface.blit(self.image, (self.rect.x, self.rect.y))