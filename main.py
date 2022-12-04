import pygame.font
from pygame import mixer

from button_transitions import Globals
from scenes.menu import ScreenMenu

if __name__ == '__main__':
    pygame.font.init()
    pygame.display.set_caption("The Invisible Plateau of Music")
    sMenu = ScreenMenu()
    screen = pygame.display.set_mode((1280, 720))
    mixer.init()
    sMenu.executioner(True, Globals.mapping_buttons_start, screen)
