# This file was created by the one and only Myles Zhang

# Imports
import pygame as pg
from settings import *
from pygame.sprite import Sprite

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

    # Checking which keys are pressed
    def getkeys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if keys[pg.K_r]:
            self.game.gamestate = "mainmenu"
            self.game.coincount = 0
            self.game.gamelevel = 0
            self.game.new()
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
                self.changelevel = True
            if group == self.game.enemies:
                self.game.gamestate = "gameover"

    # Updating the sprite and checking for collisions
    def update(self):
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
class Button():
    def __init__(self, game, x, y, img, scale):
        height = img.get_height()
        width = img.get_width()
        self.game = game
        self.image = pg.transform.scale(img, (int(width + scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x,y)
        self.clicked = False

    # Drawing the button
    def draw(self, surface):
        action = False

        # Finding mouse location
        mousepos = pg.mouse.get_pos()

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