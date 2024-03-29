# Moving around the grid is the same as in Java: top left is (0, 0) moving right is +X moving down is +Y

import pygame as pg
import ctypes
from os import listdir

user32 = ctypes.windll.user32
monitor_resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# initializes pygame
pg.init()

game_clock = pg.time.Clock()

bullet_sound = pg.mixer.Sound('assets/bullet.wav')
hit_sound = pg.mixer.Sound('assets/hit.wav')

loop_music = pg.mixer.music.load('assets/music.mp3')
pg.mixer.music.play(-1)


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
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.score = 0

    def enemy_struck(self):
        self.score += 1

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
                window.blit(self.orient_left[self.steps_taken // 3], (self.x, self.y))  # Cycles through the 9 walking animations
                self.steps_taken += 1
            elif self.is_right:
                window.blit(self.orient_right[self.steps_taken // 3], (self.x, self.y))
                self.steps_taken += 1
        else:  # blit the character standing still
            if self.is_right:
                window.blit(self.orient_right[0], (self.x, self.y))
            else:
                window.blit(self.orient_left[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pg.draw.rect(game_window, (255, 0, 0), self.hitbox, 2)

    def collide(self):
        # once character collides with the goblin they are reset
        self.x = 60
        self.y = 410
        self.steps_taken = 0  # starts the image cycle over so the character isn't blitted mid-stride
        self.score -= 5
        self.in_jump = False
        self.jump_iter = 10
        collision_font = pg.font.SysFont('arial', 100)
        collision_text = collision_font.render('-5', 1, (255, 0, 0))
        game_window.blit(collision_text, (window_width // 2 - collision_text.get_width() // 2, window_height // 2))
        pg.display.update()
        crude_clock = 0
        while crude_clock < 100:
            pg.time.delay(10)
            crude_clock += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    crude_clock = 301
                    pg.quit()


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
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.is_visible = True

    def draw(self, window):
        self.move()
        if self.is_visible:
            if self.step_count + 1 >= 33:
                self.step_count = 0

            if self.velocity > 0:
                window.blit(self.orient_right[self.step_count // 3], (self.x, self.y))
                self.step_count += 1
            elif self.velocity < 0:
                window.blit(self.orient_left[self.step_count // 3], (self.x, self.y))
                self.step_count += 1

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pg.draw.rect(game_window, (255, 0, 0), self.hitbox, 2)

            pg.draw.rect(game_window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pg.draw.rect(game_window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 5 * self.health, 10))

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

    def is_hit(self):
        hit_sound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.is_visible = False
        print('Score!')


# When you draw a circle the x,y is in the center of the circle, not the top left
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
    score_text = score_font.render('Score: ' + str(ash.score), 1, (0, 0, 0))
    game_window.blit(score_text, (330, 10))
    ash.draw(game_window)
    gary.draw(game_window)

    for projectile in bullets_fired:
        projectile.draw(game_window)
    pg.display.update()


ash = Player(300, 410, 64, 64)
gary = Enemy(200, 410, 64, 64, 450)
bullets_fired = []
shot_loop = 0
score_font = pg.font.SysFont('arial', 30, True)
# the Main loop - as soon as the loop ends the game ends
while window_alive:
    # using delay in place of a clock
    # 1/10 of a second
    game_clock.tick(27)

    if gary.is_visible:
        if ash.hitbox[1] < gary.hitbox[1] + gary.hitbox[3] and ash.hitbox[1] + ash.hitbox[3] > gary.hitbox[1]:
            if ash.hitbox[0] < gary.hitbox[0] + gary.hitbox[2] and ash.hitbox[0] + ash.hitbox[2] > gary.hitbox[0]:
                ash.collide()

    if shot_loop > 0:
        shot_loop += 1
    if shot_loop > 3:
        shot_loop = 0
    # character coordinates are stored in the top left of the character

    for event in pg.event.get():
        if event.type == pg.QUIT:
            window_alive = False

    for bullet in bullets_fired:
        # left side is bottom of the bullet above the bottom of the hitbox
        # right side is top of the bullet beneath the top of the hitbox
        if bullet.y - bullet.radius < gary.hitbox[1] + gary.hitbox[3] and bullet.y + bullet.radius > gary.hitbox[1]:
            if bullet.x - bullet.radius < gary.hitbox[0] + gary.hitbox[2] and bullet.x + bullet.radius > gary.hitbox[0]:
                gary.is_hit()
                ash.enemy_struck()
                bullets_fired.pop(bullets_fired.index(bullet))

        if 1 < bullet.x < window_width - 1:  # screen boundaries
            bullet.x += bullet.velocity
        else:
            bullets_fired.pop(bullets_fired.index(bullet))

    key_inputs = pg.key.get_pressed()

    if key_inputs[pg.K_SPACE] and shot_loop == 0:
        bullet_sound.play()
        direction = -1 if ash.is_left else 1
        if len(bullets_fired) < 5:
            bullets_fired.append(Projectile(round(ash.x + ash.width // 2), round(ash.y + ash.height // 2), 6, (0, 0, 0), direction))

        shot_loop = 1

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

