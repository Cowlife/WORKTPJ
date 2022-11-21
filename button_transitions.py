import sys

import pygame

import global_functions
import scenes.menu


class FadeTransition:
    def __init__(self):
        self.fade_in = global_functions.fade_in()

    def get_fade_in(self):
        return self.fade_in


class ButtonTransition(FadeTransition):

    def __init__(self):
        super().__init__()

    def execute(self, buttons, menu_mouse_pos):
        raise NotImplemented


class Play(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        scenes.menu.play()


class Options(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        scenes.menu.options()


class Quit(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos):
        pygame.quit()
        sys.exit()
