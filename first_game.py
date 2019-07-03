import pygame as pg
import ctypes

user32 = ctypes.windll.user32
monitor_resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen_fill = (0, 0, 0)

# initializes pygame
pg.init()

# window/view port info
window_dimensions = (monitor_resolution[0] // 2, monitor_resolution[1] // 2)
window_title = 'Learning Pygame'

# character parameters
x = 50
y = 50
width = 20
height = 20
speed = 4
character_colour = (255, 105, 180)
character_dimensions = (x, y, width, height)


window_alive = True

game_window = pg.display.set_mode(window_dimensions)

pg.display.set_caption(window_title)

while window_alive:
    # using delay in place of a clock
    # 1/10 of a second
    pg.time.delay(100)

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


