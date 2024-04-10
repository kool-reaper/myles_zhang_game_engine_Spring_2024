# Loop through a list

import pygame as pg
from settings import *

clock = pg.time.Clock()

frames = ["frame1", "frame2", "frame3", "frame4"]

print(len(frames))

frames_length = len(frames)

print(frames[frames_length - 1])

currframe = 0

then = 0

while True:
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - then > 1000:
        then = now
        print(frames[currframe])
        if currframe == frames_length - 1:
            currframe = 0
        else:
            currframe += 1
    