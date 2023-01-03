import sys

import pygame
from pygame import mixer

from database import DataBaseModel
from dropdown_settings import DropdownSettings
from scenes.menu import ScreenMenu
from scenes.song_transition import SongExecutor


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

    def kwarg_handling(self):
        pass

    def fade_in(self, screen):
        mixer.music.stop()
        FadeTransition.__init__(self, screen)
        FadeTransition.black_out(self)

    def input_db_handling(self, database_name, variables_search, **kwargs):
        scenario = kwargs.get('scenario', None)
        order = kwargs.get('order', False)
        test = DataBaseModel('localhost', 'test', 'postgres', 'KAYN', 5432, database_name)
        test.retrieve(variables_search, list_results=scenario, order=order)
        return test.lister

    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        raise NotImplemented


class Play(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        ButtonTransition.fade_in(self, screen)
        dropdown = ButtonTransition.input_db_handling(self, '"Music_Database"',
                                                      ['name', 'file_name', 'song_end', 'dificulty', 'layers'])
        self.menu.execution(True, Globals.mapping_buttons_play, screen,
                            list_selector=dropdown[0], list_value=dropdown[1],
                            list_end_song=dropdown[2], list_dificulty=dropdown[3],
                            list_layers=dropdown[4],
                            settings=DropdownSettings.mapping_songs)


class Options(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        ButtonTransition.fade_in(self, screen)
        self.menu.execution(False, Globals.mapping_buttons_options, screen, color="white")


class MenuOption(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        ButtonTransition.fade_in(self, screen)
        self.menu.execution(True, Globals.mapping_buttons_start, screen)


class CharacterSelect(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        song_selected = kwargs.get('song_selected', None)
        song_selected_label = kwargs.get('song_selected_label', None)
        song_selected_layers = kwargs.get('song_selected_layers', None)
        song_selected_song_end = kwargs.get('song_selected_song_end', None)
        ButtonTransition.fade_in(self, screen)
        if song_selected is not None:
            dropdown = ButtonTransition.input_db_handling(self, '"PygameMove"', ['name'])
            self.menu.execution(True, Globals.mapping_buttons_character_select, screen,
                                list_selector=dropdown[0], settings=DropdownSettings.mapping_characters,
                                song_selected=song_selected, song_selected_label=song_selected_label,
                                song_selected_layers=song_selected_layers,
                                song_selected_song_end=song_selected_song_end)
        else:
            print("You must select a song!")
            self.menu.execution(True, Globals.mapping_buttons_start, screen)


class Song(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        chars = kwargs.get('chars', None)
        song_selected = kwargs.get('song_selected', None)
        song_selected_label = kwargs.get('song_selected_label', None)
        song_selected_layers = kwargs.get('song_selected_layers', None)
        song_selected_song_end = kwargs.get('song_selected_song_end', None)
        scenario_search = ButtonTransition.input_db_handling(self, '"Music_Database"', ['scenario'],
                                                             scenario=f"'{song_selected_label}'")[0]
        scenario_search.extend([song_selected_layers, song_selected_song_end])
        print(scenario_search)
        ButtonTransition.fade_in(self, screen)
        chars_data = [ButtonTransition.input_db_handling(self, '"PygameMove"',
                                                         ['entire_sheet', 'x_y_start_m_a_h_c',
                                                          'frames_in_x_in_y_m_a_h_c', 'width_height_m_a_h_c'],
                                                         scenario=f"'{ch}'") for ch in chars]
        if len(chars_data) != 3:
            print("You must select at least 3 characters!")
            self.menu.execution(True, Globals.mapping_buttons_start, screen)
        else:
            enemy_data = ButtonTransition.input_db_handling(self, '"Enemy_Database"',
                                                            ['name', 'health', 'flipper', 'entire_sheet', 'width_enemy',
                                                             'frames_in_x_y_enemy', 'symbol'], order=True)
            enemies_list = enemy_data[0]
            enemy_data.remove(enemies_list)
            song = SongExecutor(self.screen, song_selected, chars, chars_data, enemies_list, enemy_data,
                                scenario_search, song_selected_label)
            song.UnityExecutor()


class Quit(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
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
        # 0: Song -> Restart Attempt
        0: Play,
        1: CharacterSelect,
        2: MenuOption,
        "x_pos": 640,
        "y_pos": 210,
        "title": "You took too much damage!",
        "font_size_title": 32,
        "rect_cd": (640, 50),
        "image_inputs": ["Play", "Start", "Quit"],  # ["Play", "Options", "Options", "Options"]
        "text_inputs": ["RETURN TO SONG SELECT", "RETURN TO CHARACTER SELECT", "RETURN TO MENU"],
        "color_base": "#2596be",
        "color_hovering": "Yellow",
        "font_size": 25,
        "horizontal": False,
        "separation": 150,
        "menu_bg": "assets/global_images/Background.png",
        "music": "assets/music/PlayHub.mp3"
    }
