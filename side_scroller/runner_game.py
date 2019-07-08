import pygame as pg
from pygame.locals import *

import os
import sys
import math

pg.init()

window_dimensions = (800, 447)
game_window = pg.display.set_mode(window_dimensions)
pg.display.set_caption('Side Scroller')

background = pg.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = background.get_width()

clock = pg.time.Clock()


class Player(object):
    run = [pg.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pg.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    slide = [pg.image.load(os.path.join('images', 'S1.png')), pg.image.load(os.path.join('images', 'S2.png')),
             pg.image.load(os.path.join('images', 'S2.png')), pg.image.load(os.path.join('images', 'S2.png')),
             pg.image.load(os.path.join('images', 'S2.png')), pg.image.load(os.path.join('images', 'S2.png')),
             pg.image.load(os.path.join('images', 'S2.png')), pg.image.load(os.path.join('images', 'S2.png')),
             pg.image.load(os.path.join('images', 'S3.png')), pg.image.load(os.path.join('images', 'S4.png')),
             pg.image.load(os.path.join('images', 'S5.png'))]
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, win):
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1