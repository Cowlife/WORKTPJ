import sys

import pygame

import global_functions


class ButtonTransition:

    def execute(self, buttons, menu_mouse_pos, i):
        if buttons[i].checkForInput(menu_mouse_pos):
            global_functions.fade_in(1280, 720, global_functions.screen)


class Play(ButtonTransition):
    def execute(self, buttons, menu_mouse_pos, i):
        if buttons[i].checkForInput(menu_mouse_pos):
            # play()
            pass


class Options(ButtonTransition):
    def execute(self, buttons, menu_mouse_pos, i):
        if buttons[i].checkForInput(menu_mouse_pos):
            # options()
            pass


class Quit(ButtonTransition):
    def execute(self, buttons, menu_mouse_pos, i):
        if buttons[i].checkForInput(menu_mouse_pos):
            pygame.quit()
            sys.exit()
