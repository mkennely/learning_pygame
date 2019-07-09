import pygame as pg
from pygame.locals import *

import os
import sys
import math

pg.init()

window_dimensions = (800, 447)
game_window = pg.display.set_mode(window_dimensions)
pg.display.set_caption('Side Scroller')

# the way this works is that it blits the background twice
# it blits the background in its starting position and then again at the horizontal edge of it
# as you update the X and X2 it is constantly reblitting the two images
background = pg.image.load(os.path.join('assets', 'bg.png')).convert()
bgX = 0
bgX2 = background.get_width()
background_width = background.get_width()

game_clock = pg.time.Clock()


class BaseGameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Player(BaseGameObject):
    run = [pg.image.load(os.path.join('assets', str(x) + '.png')) for x in range(8, 16)]
    jump = [pg.image.load(os.path.join('assets', str(x) + '.png')) for x in range(1, 8)]
    slide = [pg.image.load(os.path.join('assets', 'S1.png')), pg.image.load(os.path.join('assets', 'S2.png')),
             pg.image.load(os.path.join('assets', 'S2.png')), pg.image.load(os.path.join('assets', 'S2.png')),
             pg.image.load(os.path.join('assets', 'S2.png')), pg.image.load(os.path.join('assets', 'S2.png')),
             pg.image.load(os.path.join('assets', 'S2.png')), pg.image.load(os.path.join('assets', 'S2.png')),
             pg.image.load(os.path.join('assets', 'S3.png')), pg.image.load(os.path.join('assets', 'S4.png')),
             pg.image.load(os.path.join('assets', 'S5.png'))]
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        BaseGameObject.__init__(self, x, y, width, height)
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


def draw_window():
    game_window.blit(background, (bgX, 0))
    game_window.blit(background, (bgX2, 0))
    dino.draw(game_window)
    pg.display.update()


pg.time.set_timer(USEREVENT+1, 500)
run_game = True
clock_speed = 30
dino = Player(200, 313, 64, 64)
while run_game:
    draw_window()

    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < background_width * -1:
        bgX = background_width
    if bgX2 < background_width * -1:
        bgX2 = background_width

    # event loop for keeping game window open/running
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_game = False
            pg.quit()
            quit()
        if event.type == USEREVENT+1:
            clock_speed += 1

    key_strokes = pg.key.get_pressed()

    if key_strokes[pg.K_SPACE] or key_strokes[pg.K_UP]:
        if not dino.jumping:
            dino.jumping = True

    if key_strokes[pg.K_DOWN]:
        if not dino.sliding:
            dino.sliding = True

    game_clock.tick(clock_speed)
