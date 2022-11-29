import time

import pygame
from pygame_widgets.progressbar import ProgressBar

width_var = 1280
height_var = 720
screen_vars = (width_var, height_var)
screen = pygame.display.set_mode(screen_vars)
menu_bg = pygame.image.load("assets/Background.png")


def progressing(screen):  # 0.1
    startTime = time.time()
    progressBar = ProgressBar(screen, 100, 100, 500, 40, lambda: (time.time() - startTime) / 10, curved=False)
    # /10 seconds
    return progressBar


def fade_in():
    fade = pygame.Surface(screen_vars)
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)





