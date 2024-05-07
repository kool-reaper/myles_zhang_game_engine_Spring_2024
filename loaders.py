# Imports
import pygame as pg
from settings import *
from sprites import *

# Imitialize pygame
pg.init()

# Load game buttons
playbtn_img = pg.image.load(path.join(img_folder, 'play.png')).convert_alpha()
playbtn = Button(playbtn_img)
restart_img = pg.image.load(path.join(img_folder, 'Restart.png')).convert_alpha()
restartbtn = Button(restart_img)
left_img = pg.image.load(path.join(img_folder, 'Leftbutton.png')).convert_alpha()
leftbtn = Button(left_img)
right_img = pg.image.load(path.join(img_folder, 'Rightbutton.png')).convert_alpha()
rightbtn = Button(right_img)
LBbutton_img = pg.image.load(path.join(img_folder, 'Leaderboardbutton.png')).convert_alpha()
LBbutton = Button(LBbutton_img)
infobutton_img = pg.image.load(path.join(img_folder, 'Infobutton.png')).convert_alpha()
infobutton = Button(infobutton_img)
startbtn_img = pg.image.load(path.join(img_folder, 'startbtn.png')).convert_alpha()
startbtn = Button(startbtn_img)

# Load player icons
Tyler_img = pg.image.load(path.join(img_folder, 'Tyler.png')).convert_alpha()
Tyler = Image(Tyler_img)
Adrian_img = pg.image.load(path.join(img_folder, 'Adrian.png')).convert_alpha()
Adrian = Image(Adrian_img)
Myles_img = pg.image.load(path.join(img_folder, 'Myles.png')).convert_alpha()
Myles = Image(Myles_img)
Ramiel_img = pg.image.load(path.join(img_folder, 'Rameil.png')).convert_alpha()
Rameil = Image(Ramiel_img)
Robbie_img = pg.image.load(path.join(img_folder, 'Robbie.png')).convert_alpha()
Robbie = Image(Robbie_img)

# Load other assets
LBbox_img = pg.image.load(path.join(img_folder, 'Leaderboardbox.png')).convert_alpha()
LBbox = Image(LBbox_img)
title_img = pg.image.load(path.join(img_folder, 'AE.png')).convert_alpha()
title = Image(title_img)
youlost_img = pg.image.load(path.join(img_folder, 'youlost.png')).convert_alpha()
youlost = Image(youlost_img)
roundcomplete_img = pg.image.load(path.join(img_folder, 'roundcomplete.png')).convert_alpha()
roundcomplete = Image(roundcomplete_img)
lifelost_img = pg.image.load(path.join(img_folder, 'lifelost.png')).convert_alpha()
lifelost = Image(lifelost_img)