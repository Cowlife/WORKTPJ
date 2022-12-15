import sys

import pygame
from pygame import mixer

import song_file
from scenes.menu import ScreenMenu

from database import DataBaseModel
from scenes.song_transition import SongExecutor


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

    def transition(self):
        pass

    def execute(self, buttons, menu_mouse_pos, screen):
        raise NotImplemented


class Play(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        mixer.music.stop()
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        self.menu.executioner(False, Globals.mapping_buttons_play, screen)


class Options(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        mixer.music.stop()
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        self.menu.executioner(False, Globals.mapping_buttons_options, screen, "white")


class Menu(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        mixer.music.stop()
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        self.menu.executioner(True, Globals.mapping_buttons_start, screen)


class CharacterSelect(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        mixer.music.stop()
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        test = DataBaseModel('localhost', 'test', 'postgres', 'KAYN', 5432)
        test.retrieve('name')
        self.menu.executioner(True, Globals.mapping_buttons_character_select, screen,
                              list_selector=test.lister)


class CharacterSelectButton(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        pass


class Add(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        print("Addte")


class Subtract(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        pass


class Song(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        mixer.music.stop()
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        song = SongExecutor(self.screen, "music3")
        song.player_drawer()


class Quit(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        pygame.quit()
        sys.exit()


class Globals:
    mapping_buttons_start = {
        0: Play,
        1: Options,
        2: Quit,
        "x_pos": 440,
        "y_pos": 250,
        "title": "MAIN MENU",
        "font_size_title": 100,
        "rect_cd": (640, 100),
        "image_inputs": ["Play", "Options", "Quit"],
        "text_inputs": ["PLAY", "OPTIONS", "QUIT"],
        "color_base": "#2596be",
        "color_hovering": "Green",
        "font_size": 50,
        "horizontal": False,
        "separation": 150,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/Menu.mp3"
    }
    mapping_buttons_options = {
        0: Menu,
        "x_pos": 640,
        "y_pos": 460,
        "title": "This is the OPTIONS screen.",
        "font_size_title": 45,
        "rect_cd": (640, 260),
        "image_inputs": ["Play"],
        "text_inputs": ["BACK"],
        "color_base": "#2596be",
        "color_hovering": "Red",
        "font_size": 50,
        "horizontal": False,
        "separation": 150,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/PlayHub.mp3"
    }
    mapping_buttons_play = {
        0: Menu,
        1: CharacterSelect,
        "x_pos": 640,
        "y_pos": 360,
        "title": "This is the PLAY screen.",
        "font_size_title": 45,
        "rect_cd": (640, 260),
        "image_inputs": ["Play", "Options"],
        "text_inputs": ["BACK", "TEST SONG"],
        "color_base": "#2596be",
        "color_hovering": "Red",
        "font_size": 50,
        "horizontal": False,
        "separation": 150,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/PlayHub.mp3"

    }
    mapping_buttons_overlay = {
        0: Menu,
        "x_pos": 640,
        "y_pos": 620,
        "title": "Level Complete!",
        "font_size_title": 64,
        "rect_cd": (640, 100),
        "image_inputs": ["Play"],
        "text_inputs": ["BACK"],
        "color_base": "#2596be",
        "color_hovering": "Red",
        "font_size": 50,
        "horizontal": False,
        "separation": 150,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/PlayHub.mp3"

    }
    mapping_buttons_character_select = {
        0: Play,
        1: Song,
        "x_pos": 340,
        "y_pos": 610,
        "title": "Choose your characters!",
        "font_size_title": 32,
        "rect_cd": (640, 50),
        "image_inputs": ["Play", "Start", "Left", "Right"],
        "text_inputs": ["BACK", "START", "<-", "->"],
        "color_base": "#2596be",
        "color_hovering": "Yellow",
        "font_size": 50,
        "horizontal": True,
        "separation": 600,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/characterselect.mp3"
    }

    mapping_buttons_character_select_button = {
        0: Add,
        1: Subtract,
        "x_pos": 160,
        "y_pos": 320,
        "title": "",
        "font_size_title": 0,
        "rect_cd": (0, 0),
        "image_inputs": ["Left", "Right"],
        "text_inputs": ["<-", "->"],
        "color_base": "#2596be",
        "color_hovering": "Yellow",
        "font_size": 25,
        "horizontal": True,
        "separation": 350,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/PlayHub.mp3"
    }
