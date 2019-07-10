import pygame as pg

from pygame.locals import *
from random import randrange

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
        # self.hitbox = (x, y, width, height)


class Player(BaseGameObject):
    run = [pg.image.load(os.path.join('assets', str(x) + '.png')) for x in range(8, 16)]
    jump = [pg.image.load(os.path.join('assets', str(x) + '.png')) for x in range(1, 8)]
    slide = [pg.image.load(os.path.join('assets', 'S1.png')), pg.image.load(os.path.join('assets', 'S2.png')),
             pg.image.load(os.path.join('assets', 'S2.png')), pg.image.load(os.path.join('assets', 'S2.png')),
             pg.image.load(os.path.join('assets', 'S2.png')), pg.image.load(os.path.join('assets', 'S2.png')),
             pg.image.load(os.path.join('assets', 'S2.png')), pg.image.load(os.path.join('assets', 'S2.png')),
             pg.image.load(os.path.join('assets', 'S3.png')), pg.image.load(os.path.join('assets', 'S4.png')),
             pg.image.load(os.path.join('assets', 'S5.png'))]
    fall = pg.image.load(os.path.join('assets', '0.png'))
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
        self.falling = False
        self.hitbox = (x, y, width, height)

    def draw(self, win):
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif 20 < self.slideCount < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1

        elif self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)
        pg.draw.rect(win, (255, 0, 0), self.hitbox, 1)


class Saw(BaseGameObject):
    img = [pg.image.load(os.path.join('assets', f'SAW{x}.png')) for x in range(0, 4)]

    def __init__(self, x, y, width, height):
        BaseGameObject.__init__(self, x, y, width, height)
        self.hitbox = (x, y, width, height)
        self.rotate_count = 0

    def draw(self, window):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height)
        if self.rotate_count >= 8:
            self.rotate_count = 0
        window.blit(pg.transform.scale(self.img[self.rotate_count // 2], (64, 64)), (self.x, self.y))
        self.rotate_count += 1
        pg.draw.rect(window, (255, 0, 0), self.hitbox, 2)


class Spike(Saw):

    img = pg.image.load(os.path.join('assets', 'spike.png'))

    def draw(self, window):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        window.blit(self.img, (self.x, self.y))
        pg.draw.rect(window, (255, 0, 0), self.hitbox, 2)


def draw_window():
    game_window.blit(background, (bgX, 0))
    game_window.blit(background, (bgX2, 0))
    dino.draw(game_window)

    for obstacle in obstacles:
        obstacle.draw(game_window)
    pg.display.update()


# every half a second this event is triggered and when it's triggered it ups the clock speed
pg.time.set_timer(USEREVENT+1, 500)

pg.time.set_timer(USEREVENT+2, randrange(2000, 3500))
run_game = True
clock_speed = 30
dino = Player(200, 313, 64, 64)
x_delta = 1.4

obstacles = []
while run_game:
    draw_window()

    for obstacle in obstacles:
        obstacle.x -= x_delta
        if obstacle.x < obstacle.width * -1:
            obstacles.pop(obstacles.index(obstacle))

    bgX -= x_delta
    bgX2 -= x_delta

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
        if event.type == USEREVENT+2:

            random_decider = randrange(0, 2)
            random_saw = Saw(810, 310, 64, 64)
            random_spike = Spike(810, 0, 48, 320)

            if random_decider == 0:
                obstacles.append(random_saw)
            else:
                obstacles.append(random_spike)

    key_strokes = pg.key.get_pressed()

    if key_strokes[pg.K_SPACE] or key_strokes[pg.K_UP]:
        if not dino.jumping:
            dino.jumping = True

    if key_strokes[pg.K_DOWN]:
        if not dino.sliding:
            dino.sliding = True

    game_clock.tick(clock_speed)
