import sys

import pygame

import song_file
from scenes.menu import ScreenMenu

from sprites_player.database import DataBaseModel


class FadeTransition:
    def __init__(self, screen):
        self.menu = ScreenMenu()
        self.screen = screen

    def black_out(self):
        fade = pygame.Surface((1280, 720))
        fade.fill((0, 0, 0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)


class ButtonTransition(FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        raise NotImplemented


class Play(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        self.menu.executioner(False, Globals.mapping_buttons_play, screen)


class Options(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        self.menu.executioner(False, Globals.mapping_buttons_options, "white", screen)


class Menu(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        self.menu.executioner(True, Globals.mapping_buttons_start, screen)


class Song(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        # song = SongChart()
        # song.play()
        test = DataBaseModel('localhost', 'test', 'postgres', 'KAYN', 5432)
        test.retrieve()
        print(f'{test.lister}namor')
        song_file.song(self.screen, "music3")


class Quit(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
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
        "color_hovering": "Green",
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
