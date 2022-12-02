import sys

import pygame

import global_functions
import scenes.menu
import song_file
from scenes.song_transition import SongChart
from sprites_player.database import DataBaseModel


class FadeTransition:
    def __init__(self):
        fade = pygame.Surface((1280, 720))
        fade.fill((0, 0, 0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            global_functions.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)


class ButtonTransition(FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        raise NotImplemented


class Play(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        FadeTransition.__init__(self)
        scenes.menu.transitory_menu(False, Globals.mapping_buttons_play)


class Options(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        FadeTransition.__init__(self)
        scenes.menu.transitory_menu(False, Globals.mapping_buttons_options, "white")


class Menu(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        FadeTransition.__init__(self)
        scenes.menu.transitory_menu(True, Globals.mapping_buttons_start)


class Song(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        FadeTransition.__init__(self)
        #song = SongChart()
        #song.play()
        test = DataBaseModel('localhost', 'test', 'postgres', 'KAYN', 5432)
        test.retrieve()
        print(f'{test.lister}namor')
        song_file.song(global_functions.screen, 0, "music3")


class Quit(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        pygame.quit()
        sys.exit()


class Globals:
    mapping_buttons_start = {
        0: Play,
        1: Options,
        2: Quit,
        "pos": 440,
        "initial_y_pos": 250,
        "title": "MAIN MENU",
        "font_size_title": 100,
        "rect_cd": (640, 100),
        "image_inputs": ["Play", "Options", "Quit"],
        "text_inputs": ["PLAY", "OPTIONS", "QUIT"],
        "color_base": "#2596be",
        "color_hovering": "Red",
        "font_size": 50,
        "menu_bg": "assets/Background.png",
    }
    mapping_buttons_options = {
        0: Menu,
        "pos": 640,
        "initial_y_pos": 460,
        "title": "This is the OPTIONS screen.",
        "font_size_title": 45,
        "rect_cd": (640, 260),
        "image_inputs": ["Play"],
        "text_inputs": ["BACK"],
        "color_base": "#2596be",
        "color_hovering": "Red",
        "font_size": 50,
        "menu_bg": "assets/Background.png",
    }
    mapping_buttons_play = {
        0: Menu,
        1: Song,
        "pos": 640,
        "initial_y_pos": 360,
        "title": "This is the PLAY screen.",
        "font_size_title": 45,
        "rect_cd": (640, 260),
        "image_inputs": ["Play", "Options"],
        "text_inputs": ["BACK", "TEST SONG"],
        "color_base": "#2596be",
        "color_hovering": "Red",
        "font_size": 50,
        "menu_bg": "assets/Background.png",
    }
    mapping_buttons_overlay = {
        0: Menu,
        "pos": 640,
        "initial_y_pos": 620,
        "title": "Level Complete!",
        "font_size_title": 64,
        "rect_cd": (640, 100),
        "image_inputs": ["Play"],
        "text_inputs": ["BACK"],
        "color_base": "#2596be",
        "color_hovering": "Red",
        "font_size": 50,
        "menu_bg": "assets/Background.png",
    }
