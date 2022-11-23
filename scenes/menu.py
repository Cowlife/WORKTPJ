import pygame

from global_functions import screen, menu_bg, Globals
from scenes.menu_load import HMenu


def main_menu():
    while True:
        screen.blit(menu_bg, (0, 0))

        h_menu = HMenu(440, 250, menu_bg, Globals.mapping_globals_start)
        h_menu.drawing_title("MAIN MENU", 100, (640, 100))
        h_menu.inserting_asset_buttons(["Play", "Options", "Quit"], ["PLAY", "OPTIONS", "QUIT"])
        h_menu.button_hover_effect()

        h_menu.handle_input()

        # to set-up the screen
        pygame.display.update()


def options():
    while True:
        screen.fill("white")

        h_menu = HMenu(640, 460, menu_bg, Globals.mapping_globals_options)
        h_menu.drawing_title("This is the OPTIONS screen.", 45, (640, 260))
        h_menu.inserting_asset_buttons(["Play"], ["BACK"])
        h_menu.button_hover_effect()

        h_menu.handle_input()

        pygame.display.update()


def play():
    while True:
        screen.fill("black")

        h_menu = HMenu(640, 360, menu_bg, Globals.mapping_globals_play)
        h_menu.drawing_title("This is the PLAY screen.", 45, (640, 260))
        h_menu.inserting_asset_buttons(["Play", "Options"], ["BACK", "TEST SONG"])
        h_menu.button_hover_effect()

        h_menu.handle_input()

        pygame.display.update()
