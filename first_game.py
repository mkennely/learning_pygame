# Moving around the grid is the same as in Java: top left is (0, 0) moving right is +X moving down is +Y

import pygame as pg
import ctypes

user32 = ctypes.windll.user32
monitor_resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# initializes pygame
pg.init()

# character parameters
x = 50
y = 50
width = 20
height = 20
speed = 4
character_colour = (255, 105, 180)
character_dimensions = (x, y, width, height)

# window/view port info. Screen_fill is colour used to redraw the screen after movement
window_width = monitor_resolution[0] // 2
window_height = monitor_resolution[1] // 2
window_dimensions = (window_width, window_height)
game_window = pg.display.set_mode(window_dimensions)

window_alive = True

window_title = 'Learning Pygame'
pg.display.set_caption(window_title)
screen_fill = (0, 0, 0)

while window_alive:
    # using delay in place of a clock
    # 1/10 of a second
    pg.time.delay(100)

    # character coordinates are stored in the top left of the character
    character_dimensions = (x, y, width, height)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            window_alive = False

    key_inputs = pg.key.get_pressed()

    # print(key_inputs)
    if key_inputs[pg.K_LEFT]:
        x -= speed
        print("Helo")
        print(x)
    if key_inputs[pg.K_RIGHT]:
        x += speed
    if key_inputs[pg.K_UP]:
        y -= speed
    if key_inputs[pg.K_DOWN]:
        y += speed

    game_window.fill(screen_fill)
    pg.draw.rect(game_window, character_colour, character_dimensions)
    pg.display.update()

pg.quit()


