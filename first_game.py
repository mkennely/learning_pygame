# Moving around the grid is the same as in Java: top left is (0, 0) moving right is +X moving down is +Y

import pygame as pg
import ctypes
from os import listdir

user32 = ctypes.windll.user32
monitor_resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# initializes pygame
pg.init()

# character parameters
x = 50
y = 50
width = 20
height = 20
speed = 8
character_colour = (255, 105, 180)
character_dimensions = [x, y, width, height]

# Vars for tracking player movement
is_left = False
is_right = False
steps_taken = 0

# load character model images
walk_right = [pg.image.load('assets/' + the_file) for the_file in listdir('assets') if ('R' in the_file and 'E' not in the_file)]
walk_left = [pg.image.load('assets/' + the_file) for the_file in listdir('assets') if ('L' in the_file and 'E' not in the_file)]

# window/view port info. Screen_fill is colour used to redraw the screen after movement
window_width = monitor_resolution[0] // 2
window_height = monitor_resolution[1] // 2
window_dimensions = (window_width, window_height)
game_window = pg.display.set_mode(window_dimensions)

window_alive = True

window_title = 'Learning Pygame'
pg.display.set_caption(window_title)
screen_fill = (0, 0, 0)

# info used to track jump status
in_jump = False
jump_iter = speed

while window_alive:
    # using delay in place of a clock
    # 1/10 of a second
    pg.time.delay(100)

    # character coordinates are stored in the top left of the character

    for event in pg.event.get():
        if event.type == pg.QUIT:
            window_alive = False

    key_inputs = pg.key.get_pressed()

    # print(key_inputs)
    if key_inputs[pg.K_LEFT] and character_dimensions[0] > speed:
        character_dimensions[0] -= speed

    if key_inputs[pg.K_RIGHT] and character_dimensions[0] < window_width - character_dimensions[2] - speed:
        character_dimensions[0] += speed

    if not in_jump:
        if key_inputs[pg.K_SPACE]:
            in_jump = True
    else:
        if jump_iter >= speed * -1:
            character_dimensions[1] -= (jump_iter * abs(jump_iter)) / 2
            jump_iter -= 1
        else:
            jump_iter = speed
            in_jump = False

    game_window.fill(screen_fill)
    pg.draw.rect(game_window, character_colour, character_dimensions)
    pg.display.update()

pg.quit()

# Tutorial is going towards a platform game so character moves along the Y axis by jumping only
# if key_inputs[pg.K_UP] and character_dimensions[1] > speed:
#     character_dimensions[1] -= speed
#
# if key_inputs[pg.K_DOWN] and character_dimensions[1] < window_height - character_dimensions[3] - speed:
#     character_dimensions[1] += speed
