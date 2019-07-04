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

        if self.is_left:
            window.blit(orient_left[self.steps_taken // 3], (self.x, self.y))
            self.steps_taken += 1
        elif self.is_right:
            window.blit(orient_right[self.steps_taken // 3], (self.x, self.y))
            self.steps_taken += 1
        else:
            window.blit(orient_neutral, (self.x, self.y))


class Projectile(object):
    def __init__(self, x,y, radius, colour, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.direction = direction
        self.velocity = 8 * direction

    def draw(self, window):
        pg.draw.circle(window, self.color, (self.x, self.y), self.radius)


# load character model images
# these images are shown when the character is moving left
orient_right = [pg.image.load('assets/' + the_file) for the_file in listdir('assets') if ('R' in the_file and 'E' not in the_file)]
# character model is moving right
orient_left = [pg.image.load('assets/' + the_file) for the_file in listdir('assets') if ('L' in the_file and 'E' not in the_file)]
# character model is not moving or is jumping - tutorial says jumping, but I disagree
orient_neutral = pg.image.load('assets/standing.png')
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
    main_character.draw(game_window)
    pg.display.update()


main_character = Player(300, 410, 64, 64)
# the Main loop - as soon as the loop ends the game ends
while window_alive:
    # using delay in place of a clock
    # 1/10 of a second
    game_clock.tick(27)

    # character coordinates are stored in the top left of the character

    for event in pg.event.get():
        if event.type == pg.QUIT:
            window_alive = False

    key_inputs = pg.key.get_pressed()

    # print(key_inputs)
    if key_inputs[pg.K_LEFT] and main_character.x > main_character.velocity:
        main_character.x -= main_character.velocity
        main_character.set_left()

    elif key_inputs[pg.K_RIGHT] and main_character.x < window_width - main_character.width - main_character.velocity:
        main_character.x += main_character.velocity
        main_character.set_right()

    else:
        main_character.set_neutral()
        main_character.steps_taken = 0

    if not main_character.in_jump:
        if key_inputs[pg.K_SPACE]:
            main_character.in_jump = True
            main_character.set_neutral()
            main_character.steps_taken = 0
    else:
        if main_character.jump_iter >= -10:
            # if main_character.jump_iter >= main_character.velocity * -1:
            main_character.y -= (main_character.jump_iter * abs(main_character.jump_iter)) / 2
            main_character.jump_iter -= 1
        else:
            main_character.jump_iter = 10
            main_character.in_jump = False

    draw_game_window()

pg.quit()

# Tutorial is going towards a platform game so character moves along the Y axis by jumping only
# if key_inputs[pg.K_UP] and character_dimensions[1] > speed:
#     character_dimensions[1] -= speed
#
# if key_inputs[pg.K_DOWN] and character_dimensions[1] < window_height - character_dimensions[3] - speed:
#     character_dimensions[1] += speed
# pg.draw.rect(game_window, character_colour, character_dimensions)

