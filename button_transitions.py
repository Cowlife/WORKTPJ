import sys

import pygame

from global_functions import fade_in, screen
from scenes.options import options
from scenes.play import play


class ButtonTransition:

    def execute(self, buttons, menu_mouse_pos, i):
        if buttons[i].checkForInput(menu_mouse_pos):
            fade_in(1280, 720, screen)


class Play(ButtonTransition):
    def execute(self, buttons, menu_mouse_pos, i):
        play(screen)


class Options(ButtonTransition):
    def execute(self, buttons, menu_mouse_pos, i):
        options(screen)


class Quit(ButtonTransition):
    def execute(self, buttons, menu_mouse_pos, i):
        pygame.quit()
        sys.exit()

