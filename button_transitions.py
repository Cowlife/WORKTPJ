import sys

import pygame

import global_functions
import scenes.menu
import song_file


class FadeTransition:
    def __init__(self):
        global_functions.fade_in()


class ButtonTransition(FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        raise NotImplemented


class Play(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        FadeTransition.__init__(self)
        scenes.menu.play()


class Options(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        FadeTransition.__init__(self)
        scenes.menu.options()


class Menu(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        FadeTransition.__init__(self)
        scenes.menu.main_menu()


class Song(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        BG = pygame.image.load("assets/Background.png")
        FadeTransition.__init__(self)
        song_file.song(global_functions.screen, BG, 0)


class Quit(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        pygame.quit()
        sys.exit()
