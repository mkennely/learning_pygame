# Moving around the grid is the same as in Java: top left is (0, 0) moving right is +X moving down is +Y

import pygame as pg
import ctypes
from os import listdir

user32 = ctypes.windll.user32
monitor_resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# initializes pygame
pg.init()

game_clock = pg.time.Clock()

# character parameters
x = 50
y = 400
width = 64
height = 64
speed = 8
character_colour = (255, 105, 180)
character_dimensions = [x, y, width, height]

# Vars for tracking player movement
is_left = False
is_right = False
steps_taken = 0

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

# info used to track jump status
in_jump = False
jump_iter = speed


def draw_game_window():
    global steps_taken
    game_window.blit(game_background, (0, 0))

    if steps_taken + 1 >= 27:
        steps_taken = 0

    if is_left:
        game_window.blit(orient_left[steps_taken//3], (character_dimensions[0], character_dimensions[1]))
        steps_taken += 1
    elif is_right:
        game_window.blit(orient_right[steps_taken//3], (character_dimensions[0], character_dimensions[1]))
        steps_taken += 1
    else:
        game_window.blit(orient_neutral, (character_dimensions[0], character_dimensions[1]))
    pg.display.update()


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
    if key_inputs[pg.K_LEFT] and character_dimensions[0] > speed:
        character_dimensions[0] -= speed
        is_left = True
        is_right = False

    elif key_inputs[pg.K_RIGHT] and character_dimensions[0] < window_width - character_dimensions[2] - speed:
        character_dimensions[0] += speed
        is_left = False
        is_right = True

    else:
        is_left = False
        is_right = False
        steps_taken = 0

    if not in_jump:
        if key_inputs[pg.K_SPACE]:
            in_jump = True
            is_left = False
            is_right = False
            steps_taken = 0
    else:
        if jump_iter >= speed * -1:
            character_dimensions[1] -= (jump_iter * abs(jump_iter)) / 2
            jump_iter -= 1
        else:
            jump_iter = speed
            in_jump = False

    draw_game_window()

pg.quit()

# Tutorial is going towards a platform game so character moves along the Y axis by jumping only
# if key_inputs[pg.K_UP] and character_dimensions[1] > speed:
#     character_dimensions[1] -= speed
#
# if key_inputs[pg.K_DOWN] and character_dimensions[1] < window_height - character_dimensions[3] - speed:
#     character_dimensions[1] += speed
# pg.draw.rect(game_window, character_colour, character_dimensions)

