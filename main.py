
import pygame.font
from pygame import mixer, font, DOUBLEBUF

from button_transitions import Globals
from scenes.menu import ScreenMenu

if __name__ == '__main__':
    font.init()
    pygame.display.set_caption("The Invisible Plateau of Music")
    sMenu = ScreenMenu()
    flags = DOUBLEBUF
    screen = pygame.display.set_mode((1280, 720), flags, 16)
    mixer.init()
    sMenu.execution(True, Globals.mapping_buttons_start, screen)
