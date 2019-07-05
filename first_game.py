# Moving around the grid is the same as in Java: top left is (0, 0) moving right is +X moving down is +Y

import pygame as pg
import ctypes
from os import listdir

user32 = ctypes.windll.user32
monitor_resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# initializes pygame
pg.init()

game_clock = pg.time.Clock()


class Player(object):
    # load character model images
    # these images are shown when the character is moving left
    orient_right = [pg.image.load('assets/' + the_file) for the_file in listdir('assets') if
                    ('R' in the_file and 'E' not in the_file)]
    # character model is moving right
    orient_left = [pg.image.load('assets/' + the_file) for the_file in listdir('assets') if
                   ('L' in the_file and 'E' not in the_file)]
    # character model is not moving or is jumping - tutorial says jumping, but I disagree
    orient_neutral = pg.image.load('assets/standing.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.in_jump = False
        self.jump_iter = 10
        self.is_left = False
        self.is_right = False
        self.steps_taken = 0
        self.standing = True

    def set_left(self):
        self.is_left = True
        self.is_right = False

    def set_right(self):
        self.is_left = False
        self.is_right = True

    def set_neutral(self):
        self.is_left = False
        self.is_right = False

    def draw(self, window):
        if self.steps_taken + 1 >= 27:
            self.steps_taken = 0

        if not self.standing:
            if self.is_left:
                window.blit(self.orient_left[self.steps_taken // 3], (self.x, self.y))
                self.steps_taken += 1
            elif self.is_right:
                window.blit(self.orient_right[self.steps_taken // 3], (self.x, self.y))
                self.steps_taken += 1
        else:
            if self.is_right:
                window.blit(self.orient_right[0], (self.x, self.y))
            else:
                window.blit(self.orient_left[0], (self.x, self.y))


class Enemy(object):
    orient_right = [pg.image.load('assets/' + the_file) for the_file in listdir('assets') if ('R' in the_file and 'E' in the_file)]
    orient_left = [pg.image.load('assets/' + the_file) for the_file in listdir('assets') if ('L' in the_file and 'E' in the_file)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.step_count = 0
        self.velocity = 3

    def draw(self, window):
        self.move()
        if self.step_count + 1 >= 33:
            self.step_count = 0

        if self.velocity > 0:
            window.blit(self.orient_right[self.step_count // 3], (self.x, self.y))
            self.step_count += 1
        elif self.velocity < 0:
            window.blit(self.orient_left[self.step_count // 3], (self.x, self.y))
            self.step_count += 1

    def move(self):
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.step_count = 0
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.step_count = 0


class Projectile(object):
    def __init__(self, x, y, radius, colour, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.direction = direction
        self.velocity = 8 * direction

    def draw(self, window):
        pg.draw.circle(window, self.colour, (self.x, self.y), self.radius)


# general background
game_background = pg.image.load('assets/bg.jpg')


# window/view port info. Screen_fill is colour used to redraw the screen after movement
# window_width = monitor_resolution[0] // 2
# window_height = monitor_resolution[1] //
window_width, window_height = 500, 480

window_dimensions = (window_width, window_height)
game_window = pg.display.set_mode(window_dimensions)

window_alive = True

window_title = 'Learning Pygame'
pg.display.set_caption(window_title)
screen_fill = (0, 0, 0)


def draw_game_window():
    game_window.blit(game_background, (0, 0))
    ash.draw(game_window)
    gary.draw(game_window)

    for projectile in bullets_fired:
        projectile.draw(game_window)
    pg.display.update()


ash = Player(300, 410, 64, 64)
gary = Enemy(200, 410, 64, 64, 450)
bullets_fired = []

# the Main loop - as soon as the loop ends the game ends
while window_alive:
    # using delay in place of a clock
    # 1/10 of a second
    game_clock.tick(27)

    # character coordinates are stored in the top left of the character

    for event in pg.event.get():
        if event.type == pg.QUIT:
            window_alive = False

    for bullet in bullets_fired:
        if 1 < bullet.x < window_width - 1:  # screen boundaries
            bullet.x += bullet.velocity
        else:
            bullets_fired.pop(bullets_fired.index(bullet))

    key_inputs = pg.key.get_pressed()

    if key_inputs[pg.K_SPACE]:
        direction = -1 if ash.is_left else 1
        if len(bullets_fired) < 5:
            bullets_fired.append(Projectile(round(ash.x + ash.width // 2), round(ash.y + ash.height // 2), 6, (0, 0, 0), direction))
    # print(key_inputs)
    if key_inputs[pg.K_LEFT] and ash.x > ash.velocity:
        ash.x -= ash.velocity
        ash.set_left()
        ash.standing = False

    elif key_inputs[pg.K_RIGHT] and ash.x < window_width - ash.width - ash.velocity:
        ash.x += ash.velocity
        ash.set_right()
        ash.standing = False

    else:
        ash.standing = True
        ash.steps_taken = 0

    if not ash.in_jump:
        if key_inputs[pg.K_UP]:
            ash.in_jump = True
            # ash.set_neutral()
            ash.steps_taken = 0
    else:
        if ash.jump_iter >= -10:
            # if ash.jump_iter >= ash.velocity * -1:
            ash.y -= (ash.jump_iter * abs(ash.jump_iter)) / 2
            ash.jump_iter -= 1
        else:
            ash.jump_iter = 10
            ash.in_jump = False

    draw_game_window()

pg.quit()

# Tutorial is going towards a platform game so character moves along the Y axis by jumping only
# if key_inputs[pg.K_UP] and character_dimensions[1] > speed:
#     character_dimensions[1] -= speed
#
# if key_inputs[pg.K_DOWN] and character_dimensions[1] < window_height - character_dimensions[3] - speed:
#     character_dimensions[1] += speed
# pg.draw.rect(game_window, character_colour, character_dimensions)

