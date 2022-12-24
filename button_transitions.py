import sys

import pygame
import pygame_widgets
from pygame import mixer
from pygame_menu import Menu

from database import DataBaseModel
from scenes.menu import ScreenMenu
from scenes.song_transition import SongExecutor
from selector_app import OptionBox


class FadeTransition:
    def __init__(self, screen):
        self.menu = ScreenMenu()
        self.screen = screen
        self.music_file = None
        self.character_files = []

    def black_out(self):
        fade = pygame.Surface((1280, 720))
        fade.fill((0, 0, 0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)


class ButtonTransition(FadeTransition):

    def input_db_handling(self, database_name):
        test = DataBaseModel('localhost', 'test', 'postgres', 'KAYN', 5432, database_name)
        test.retrieve('name')
        return test.lister

    def execute(self, buttons, menu_mouse_pos, screen):
        raise NotImplemented


class Play(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        mixer.music.stop()
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        dropdown = ButtonTransition.input_db_handling(self, '"Music_Database"')
        self.menu.executioner(True, Globals.mapping_buttons_play, screen,
                              list_selector=dropdown)


class Options(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        mixer.music.stop()
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        self.menu.executioner(False, Globals.mapping_buttons_options, screen, "white")


class MenuOption(ButtonTransition, FadeTransition):
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
        dropdown = ButtonTransition.input_db_handling(self, '"PygameMove"')
        self.menu.executioner(True, Globals.mapping_buttons_character_select, screen)


class Song(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen):
        mixer.music.stop()
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)
        song = SongExecutor(self.screen, "music3")
        song.UnityExecutor()


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
        0: MenuOption,
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
        0: MenuOption,
        1: CharacterSelect,
        "x_pos": 260,
        "y_pos": 620,
        "title": "Choose your own song.",
        "font_size_title": 45,
        "rect_cd": (640, 60),
        "image_inputs": ["Play", "Options"],
        "text_inputs": ["BACK", "TEST SONG"],
        "color_base": "#2596be",
        "color_hovering": "Red",
        "font_size": 50,
        "horizontal": True,
        "separation": 650,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/PlayHub.mp3"

    }
    mapping_buttons_victory_state = {
        0: MenuOption,
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
        "image_inputs": ["Play", "Start"],
        "text_inputs": ["BACK", "START"],
        "color_base": "#2596be",
        "color_hovering": "Yellow",
        "font_size": 50,
        "horizontal": True,
        "separation": 600,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/characterselect.mp3"
    }

    mapping_buttons_losing_state = {
        0: Song,
        1: Play,
        2: CharacterSelect,
        3: MenuOption,
        "x_pos": 640,
        "y_pos": 210,
        "title": "You took too much damage!",
        "font_size_title": 32,
        "rect_cd": (640, 50),
        "image_inputs": ["Play", "Start", "Quit", "Options"],  # ["Play", "Options", "Options", "Options"]
        "text_inputs": ["RESTART", "RETURN TO SONG SELECT", "RETURN TO CHARACTER SELECT", "RETURN TO MENU"],
        "color_base": "#2596be",
        "color_hovering": "Yellow",
        "font_size": 25,
        "horizontal": False,
        "separation": 150,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/PlayHub.mp3"
    }
