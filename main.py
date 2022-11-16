import pygame.font

from scenes.menu import main_menu

if __name__ == '__main__':
    pygame.font.init()
    pygame.display.set_caption("The Invisible Plateau of Music")
    main_menu()
