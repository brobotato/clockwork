import os
import sys
import copy
import pygame
from pygame.locals import *

pygame.init()
fps_clock = pygame.time.Clock()

display_width = 873
display_height = 546

title = 'Clockwork'
crashed = False

window_surface_obj = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(title)

black = pygame.Color(0, 0, 0)

font_obj = pygame.font.Font("resources/kenvector_future.ttf", 15)


# check if mouse click is in pixel range
def check_range(click_info):
    return (click_info[0] <= pygame.mouse.get_pos()[0] <= click_info[0] + click_info[2] * 48) and \
           (click_info[1] <= pygame.mouse.get_pos()[1] <= click_info[1] + click_info[3] * 48)


# rotate an image while keeping its center and size
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


# adds png to sprite dictionary
def update_dict(sprite_name, dict):
    dict[sprite_name] = pygame.image.load('resources/{0}.png'.format(sprite_name))


# just blit rewritten for convenience
def render(x, y, sprite):
    window_surface_obj.blit(sprite, (x, y))


# render a variable as text onscreen
def display_data(x, y, data):
    data_text = font_obj.render(str(data), True, black)
    render(x, y, data_text)


class Player:
    def __init__(self, x, y):
        self.moves = ['', '', '', '', '']
        self.attacks = ['', '', '', '', '']
        self.move_queue = ['', '', '', '', '']
        self.attack_queue = ['', '', '', '', '']
        self.x = x
        self.y = y
        self.move_index = 0
        self.attack_index = 0
        self.direction = None

    def reset(self):
        self.moves = ['', '', '', '', '']
        self.attacks = ['', '', '', '', '']

    def simulate(self, timer):
        temp_move = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0), '': (0, 0)}[self.moves[timer]]
        if (0 <= self.x + temp_move[0] <= 4) and (0 <= self.y + temp_move[1] <= 4):
            self.x += temp_move[0]
            self.y += temp_move[1]
            self.direction = self.attacks[timer]

    def tick(self, timer):
        temp_move = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0), '': (0, 0)}[self.move_queue[timer]]
        if (0 <= self.x + temp_move[0] <= 4) and (0 <= self.y + temp_move[1] <= 4):
            self.x += temp_move[0]
            self.y += temp_move[1]
            self.direction = self.attack_queue[timer]


# autofill dictionary with sprites from resources
sprite_dict = {}
for filename in os.listdir('resources'):
    if filename[-4:] == '.png':
        update_dict(filename[:-4], sprite_dict)

click_dict = {
    'view': (105, 363, 3, 1),
    'ready': (105, 444, 3, 1),
    'trash_move_0': (771, 54, 1, 1),
    'trash_attack_0': (771, 105, 1, 1),
    'trash_move_1': (771, 207, 1, 1),
    'trash_attack_1': (771, 258, 1, 1),
    'player_0_move_0': (462, 54, 1, 1),
    'player_0_move_1': (513, 54, 1, 1),
    'player_0_move_2': (564, 54, 1, 1),
    'player_0_move_3': (615, 54, 1, 1),
    'player_0_move_4': (666, 54, 1, 1),
    'player_0_attack_0': (462, 105, 1, 1),
    'player_0_attack_1': (513, 105, 1, 1),
    'player_0_attack_2': (564, 105, 1, 1),
    'player_0_attack_3': (615, 105, 1, 1),
    'player_0_attack_4': (666, 105, 1, 1),
    'player_1_move_0': (462, 207, 1, 1),
    'player_1_move_1': (513, 207, 1, 1),
    'player_1_move_2': (564, 207, 1, 1),
    'player_1_move_3': (615, 207, 1, 1),
    'player_1_move_4': (666, 207, 1, 1),
    'player_1_attack_0': (462, 258, 1, 1),
    'player_1_attack_1': (513, 258, 1, 1),
    'player_1_attack_2': (564, 258, 1, 1),
    'player_1_attack_3': (615, 258, 1, 1),
    'player_1_attack_4': (666, 258, 1, 1),
    'move_up': (462, 363, 1, 1),
    'move_right': (513, 363, 1, 1),
    'move_down': (564, 363, 1, 1),
    'move_left': (615, 363, 1, 1),
    'attack_up': (462, 444, 1, 1),
    'attack_right': (513, 444, 1, 1),
    'attack_down': (564, 444, 1, 1),
    'attack_left': (615, 444, 1, 1),
}

currently_clicked = ''
selected = [-54, -54]

player_0 = Player(0, 0)
player_1 = Player(4, 4)

current_player = 0
mouse_up = True

state = ''
timer = 0

tickcount = 0

while not crashed:
    tickcount += 1
    render(0, 0, sprite_dict['board'])
    render(105, 363, sprite_dict['view'])
    render(105, 444, sprite_dict['ready'])
    render(462, 363, rot_center(sprite_dict['move_arrow'], 90))
    render(513, 363, rot_center(sprite_dict['move_arrow'], 0))
    render(564, 363, rot_center(sprite_dict['move_arrow'], 270))
    render(615, 363, rot_center(sprite_dict['move_arrow'], 180))
    render(462, 444, rot_center(sprite_dict['attack_arrow'], 90))
    render(513, 444, rot_center(sprite_dict['attack_arrow'], 0))
    render(564, 444, rot_center(sprite_dict['attack_arrow'], 270))
    render(615, 444, rot_center(sprite_dict['attack_arrow'], 180))
    render(selected[0], selected[1], sprite_dict['selected'])
    display_data(0,0,state)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            mouse_up = True
    mouse_presses = pygame.mouse.get_pressed()
    if mouse_presses[0] and mouse_up and state == '':
        mouse_up = False
        for key in click_dict:
            if check_range(click_dict[key]):
                currently_clicked = key
                if "_move_" in key or "_attack_" in key:
                    selected = [click_dict[key][0], click_dict[key][1]]
                if 'player_' in key:
                    if 'move' in key:
                        exec("{0}.move_index = {1}".format(key[:8], key[-1]))
                    elif 'attack' in key:
                        exec("{0}.attack_index = {1}".format(key[:8], key[-1]))
                elif 'up' in key or 'right' in key or 'down' in key or 'left' in key:
                    if selected[1] < 200:
                        # the most ungodly line of code i have ever written
                        exec("player_{0}.{1}s[{2}] = \'{3}\'".format(str(current_player), key[:key.index('_')], str(
                            eval("player_{0}.{1}_index".format(str(current_player), key[:key.index('_')]))),
                                                                     key[key.index('_') + 1:]))
                        if eval("player_{0}.{1}_index < 4".format(str(current_player), key[:key.index('_')])) \
                                and selected[1] == {'move': 54, 'attack': 105}[key[:key.index('_')]]:
                            selected[0] += 51
                            exec("player_{0}.{1}_index += 1".format(str(current_player), key[:key.index('_')]))
                    else:
                        exec(
                            "player_{0}.{1}s[{2}] = \'{3}\'".format(str((current_player + 1) % 2), key[:key.index('_')],
                                                                    str(
                                                                        eval("player_{0}.{1}_index".format(
                                                                            str((current_player + 1) % 2),
                                                                            key[:key.index('_')]))),
                                                                    key[key.index('_') + 1:]))
                        if eval("player_{0}.{1}_index < 4".format(str((current_player + 1) % 2), key[:key.index('_')])) \
                                and selected[1] == {'move': 207, 'attack': 258}[key[:key.index('_')]]:
                            selected[0] += 51
                            exec(
                                "player_{0}.{1}_index += 1".format(str((current_player + 1) % 2), key[:key.index('_')]))
                elif 'trash' in key:
                    if selected[1] < 200:
                        if 'move' in key:
                            exec("player_{0}.moves[{1}] = \'\'".format(str(current_player), str(
                                eval("player_{0}.move_index".format(str(current_player), key[:key.index('_')])))))
                            if eval("player_{0}.move_index > 0".format(str(current_player))):
                                exec("player_{0}.move_index -= 1".format(str(current_player)))
                        elif 'attack' in key:
                            exec("player_{0}.attacks[{1}] = \'\'".format(str(current_player), str(
                                eval("player_{0}.attack_index".format(str(current_player))))))
                            if eval("player_{0}.attack_index > 0".format(str(current_player))):
                                exec("player_{0}.attack_index -= 1".format(str(current_player)))
                    else:
                        if 'move' in key:
                            exec("player_{0}.moves[{1}] = \'\'".format(str((current_player + 1) % 2), str(
                                eval("player_{0}.move_index".format(str((current_player + 1) % 2),
                                                                    key[:key.index('_')])))))
                            if eval("player_{0}.move_index > 0".format(str((current_player + 1) % 2))):
                                exec("player_{0}.move_index -= 1".format(str((current_player + 1) % 2)))
                        elif 'attack' in key:
                            exec("player_{0}.attacks[{1}] = \'\'".format(str((current_player + 1) % 2), str(
                                eval("player_{0}.attack_index".format(str((current_player + 1) % 2))))))
                            if eval("player_{0}.attack_index > 0".format(str((current_player + 1) % 2))):
                                exec("player_{0}.attack_index -= 1".format(str((current_player + 1) % 2)))
                elif key == 'view':
                    state = 'view'
                elif key == 'ready':
                    exec("player_{0}.move_queue = copy.deepcopy(player_{0}.moves)".format(str(current_player)))
                    exec("player_{0}.attack_queue = copy.deepcopy(player_{0}.attacks)".format(str(current_player)))
                    player_0.reset()
                    player_1.reset()
                    current_player = (current_player + 1) % 2
                    if current_player == 0:
                        state = 'ready'
                break
    if state == 'view':
        if tickcount % 15 == 0:
            if timer == 0:
                temp_0 = copy.deepcopy((player_0.x,player_0.y))
                temp_1 = copy.deepcopy((player_1.x,player_1.y))
            if timer == 5:
                timer = 0
                player_0.x,player_0.y = temp_0
                player_1.x,player_1.y = temp_1
                state = ''
            else:
                player_0.simulate(timer)
                player_1.simulate(timer)
                timer += 1
    if state == 'ready':
        if tickcount % 3 == 0:
            if timer == 5:
                timer = 0
                state = ''
            else:
                player_0.tick(timer)
                player_1.tick(timer)
                timer += 1
                if player_0.x == player_1.x - 1:
                    if player_0.direction == 'right':
                        if not player_1.direction == 'left':
                            state = 'Player 1 Win!'
                            player_0.tick(timer)
                            player_1.tick(timer)
                    elif player_1.direction == 'right':
                        state = 'Player 2 Win!'
                        player_0.tick(timer)
                        player_1.tick(timer)
                elif player_0.x == player_1.x + 1:
                    if player_0.direction == 'left':
                        if not player_1.direction == 'right':
                            state = 'Player 1 Win!'
                            player_0.tick(timer)
                            player_1.tick(timer)
                    elif player_1.direction == 'right':
                        state = 'Player 2 Win!'
                        player_0.tick(timer)
                        player_1.tick(timer)
                elif player_0.y == player_1.y + 1:
                    if player_0.direction == 'up':
                        if not player_1.direction == 'down':
                            state = 'Player 1 Win!'
                            player_0.tick(timer)
                            player_1.tick(timer)
                    elif player_1.direction == 'down':
                        state = 'Player 2 Win!'
                        player_0.tick(timer)
                        player_1.tick(timer)
                elif player_0.y == player_1.y - 1:
                    if player_0.direction == 'down':
                        if not player_1.direction == 'up':
                            state = 'Player 1 Win!'
                            player_0.tick(timer)
                            player_1.tick(timer)
                    elif player_1.direction == 'down':
                        state = 'Player 2 Win!'
                        player_0.tick(timer)
                        player_1.tick(timer)
    if current_player == 0:
        for x in range(0, 5):
            if player_0.moves[x] != '':
                render(462 + x * 51, 54, rot_center(sprite_dict['move_arrow'],
                                                    {'up': 90, 'right': 0, 'down': 270, 'left': 180}[
                                                        player_0.moves[x]]))
            if player_0.attacks[x] != '':
                render(462 + x * 51, 105, rot_center(sprite_dict['attack_arrow'],
                                                     {'up': 90, 'right': 0, 'down': 270, 'left': 180}[
                                                         player_0.attacks[x]]))
            if player_1.moves[x] != '':
                render(462 + x * 51, 207, rot_center(sprite_dict['move_arrow'],
                                                     {'up': 90, 'right': 0, 'down': 270, 'left': 180}[
                                                         player_1.moves[x]]))
            if player_1.attacks[x] != '':
                render(462 + x * 51, 258, rot_center(sprite_dict['attack_arrow'],
                                                     {'up': 90, 'right': 0, 'down': 270, 'left': 180}[
                                                         player_1.attacks[x]]))
    elif current_player == 1:
        for x in range(0, 5):
            if player_1.moves[x] != '':
                render(462 + x * 51, 54, rot_center(sprite_dict['move_arrow'],
                                                    {'up': 90, 'right': 0, 'down': 270, 'left': 180}[
                                                        player_1.moves[x]]))
            if player_1.attacks[x] != '':
                render(462 + x * 51, 105, rot_center(sprite_dict['attack_arrow'],
                                                     {'up': 90, 'right': 0, 'down': 270, 'left': 180}[
                                                         player_1.attacks[x]]))
            if player_0.moves[x] != '':
                render(462 + x * 51, 207, rot_center(sprite_dict['move_arrow'],
                                                     {'up': 90, 'right': 0, 'down': 270, 'left': 180}[
                                                         player_0.moves[x]]))
            if player_0.attacks[x] != '':
                render(462 + x * 51, 258, rot_center(sprite_dict['attack_arrow'],
                                                     {'up': 90, 'right': 0, 'down': 270, 'left': 180}[
                                                         player_0.attacks[x]]))
    render(54 + player_0.x * 51, 54 + player_0.y * 51, sprite_dict[('player', 'character')[current_player]])
    render(54 + player_1.x * 51, 54 + player_1.y * 51, sprite_dict[('character', 'player')[current_player]])
    if player_0.direction in ['up','right','down','left']:
        if player_0.direction == 'up':
            render(51 + player_0.x * 51, 51 + player_0.y * 51, sprite_dict['attack_1'])
        if player_0.direction == 'right':
            render(102 + player_0.x * 51, 51 + player_0.y * 51, sprite_dict['attack_0'])
        if player_0.direction == 'down':
            render(51 + player_0.x * 51, 102 + player_0.y * 51, sprite_dict['attack_1'])
        if player_0.direction == 'left':
            render(51 + player_0.x * 51, 51 + player_0.y * 51, sprite_dict['attack_0'])
    if player_1.direction in ['up','right','down','left']:
        if player_1.direction == 'up':
            render(51 + player_1.x * 51, 51 + player_1.y * 51, sprite_dict['attack_1'])
        if player_1.direction == 'right':
            render(102 + player_1.x * 51, 51 + player_1.y * 51, sprite_dict['attack_0'])
        if player_1.direction == 'down':
            render(51 + player_1.x * 51, 102 + player_1.y * 51, sprite_dict['attack_1'])
        if player_1.direction == 'left':
            render(51 + player_1.x * 51, 51 + player_1.y * 51, sprite_dict['attack_0'])
    pygame.display.update()
    fps_clock.tick(30)
