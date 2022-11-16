import sys

import pygame

import scenes.menu
from scenes.button import Button
from global_functions import get_font, fade_in
from song_file import song


def play(SCREEN):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY SCREEN.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK2 = Button(image=None, pos=(640, 360),
                            text_input="TEST SONG", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_BACK2.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK2.update(SCREEN)

        for button in [PLAY_BACK2]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    scenes.menu.main_menu()
                if PLAY_BACK2.checkForInput(PLAY_MOUSE_POS):
                    BG = pygame.image.load("assets/Background.png")
                    fade_in(1280, 720, SCREEN)
                    song(SCREEN, BG, 0)

        pygame.display.update()
