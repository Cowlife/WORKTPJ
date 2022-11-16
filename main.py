import pygame.font

from song_file import main_menu

if __name__ == '__main__':
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menu")
    bg = pygame.image.load("assets/Background.png")
    main_menu(screen, bg)
