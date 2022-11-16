import pygame

from global_functions import screen, menu_bg
from scenes.menu_load import HMenu


def main_menu():
    while True:
        screen.blit(menu_bg, (0, 0))

        h_menu = HMenu(440, 250, ["PLAY", "OPTIONS", "QUIT"], menu_bg)
        h_menu.drawing_title("MAIN MENU")
        h_menu.inserting_asset_buttons()
        h_menu.button_hover_effect()

        h_menu.button_actions()

        # to set-up the screen
        pygame.display.update()
