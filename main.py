import pygame.font

from button_transitions import Globals
from scenes.menu import transitory_menu

if __name__ == '__main__':
    pygame.font.init()
    pygame.display.set_caption("The Invisible Plateau of Music")
    transitory_menu(True, Globals.mapping_buttons_start)
