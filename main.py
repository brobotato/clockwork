import os
import sys

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
        self.x = x
        self.y = y
        self.move_index = 0
        self.attack_index = 0
        self.direction = None


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
player_1 = Player(5, 5)

current_player = 0
mouse_up = True

while not crashed:
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
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            mouse_up = True
    mouse_presses = pygame.mouse.get_pressed()
    key_presses = pygame.key.get_pressed()
    if key_presses[pygame.K_SPACE] != 0:
        pass
    if mouse_presses[0] and mouse_up:
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
                        if eval("player_{0}.{1}_index < 4".format(str(current_player), key[:key.index('_')])):
                            selected[0] += 51
                            exec("player_{0}.{1}_index += 1".format(str(current_player), key[:key.index('_')]))
                    else:
                        exec("player_{0}.{1}s[{2}] = \'{3}\'".format(str(current_player+1%2), key[:key.index('_')], str(
                            eval("player_{0}.{1}_index".format(str(current_player+1%2), key[:key.index('_')]))),
                                                                     key[key.index('_') + 1:]))
                        if eval("player_{0}.{1}_index < 4".format(str(current_player+1%2), key[:key.index('_')])):
                            selected[0] += 51
                            exec("player_{0}.{1}_index += 1".format(str(current_player+1%2), key[:key.index('_')]))
                elif 'trash' in key:
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
                break
    display_data(0, 0, player_0.moves)
    display_data(0, 15, player_0.attacks)
    display_data(0, 30, player_1.moves)
    display_data(0, 45, player_1.attacks)
    pygame.display.update()
    fps_clock.tick(30)
