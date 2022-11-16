import time

import pygame
from pygame_widgets.progressbar import ProgressBar

from button_transitions import Play, Options, Quit

screen = pygame.display.set_mode((1280, 720))
menu_bg = pygame.image.load("assets/Background.png")


def progressing(screen):  # 0.1
    startTime = time.time()
    progressBar = ProgressBar(screen, 100, 100, 500, 40, lambda: (time.time() - startTime) / 10, curved=False)
    # /10 seconds
    return progressBar


def fade_in(width, height, screen):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Globals:
    mapping_globals = {
        "0": Play,
        "1": Options,
        "2": Quit,
    }
