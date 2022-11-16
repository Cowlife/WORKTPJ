import sys

import pygame

import scenes.menu
from scenes.button import Button
from global_functions import get_font, fade_in, screen
from song_file import song


class HMenu:
    def __init__(self, pos_x, initial_pos_y, bg):
        self.bg = bg
        self.pos_x = pos_x
        self.initial_pos_y = initial_pos_y
        self.font = get_font(50)
        self.color_base = "#2596be"
        self.color_hovering = "Red"
        self.menu_mouse_pos = pygame.mouse.get_pos()
        self.buttons = []

    def drawing_title(self, title, font_size, rect_cd):
        text_menu = get_font(font_size).render(title, True, "#b68f40")
        rectangle_menu = text_menu.get_rect(center=rect_cd)
        screen.blit(text_menu, rectangle_menu)

    def inserting_asset_buttons(self, image_inputs, text_inputs):
        for x in text_inputs:
            for i in image_inputs:
                if image_inputs.index(i) == text_inputs.index(x):
                    receiver = pygame.image.load(f"assets/{image_inputs[image_inputs.index(i)]}.png")

                    outlier = Button(image=receiver,
                                     pos=(self.pos_x, self.initial_pos_y),
                                     text_input=x, font=self.font, base_color=self.color_base,
                                     hovering_color=self.color_hovering)
                    self.initial_pos_y += 150
                    self.buttons.append(outlier)

    def button_hover_effect(self):
        for button in self.buttons:
            button.changeColor(self.menu_mouse_pos)
            button.update(screen)

    def button_actions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons[0].checkForInput(self.menu_mouse_pos):
                    fade_in(1280, 720, screen)
                    scenes.menu.play()
                if self.buttons[1].checkForInput(self.menu_mouse_pos):
                    fade_in(1280, 720, screen)
                    scenes.menu.options()
                if self.buttons[2].checkForInput(self.menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

    def button_actions2(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons[0].checkForInput(self.menu_mouse_pos):
                    scenes.menu.main_menu()

    def button_actions3(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons[0].checkForInput(self.menu_mouse_pos):
                    scenes.menu.main_menu()
                if self.buttons[1].checkForInput(self.menu_mouse_pos):
                    BG = pygame.image.load("assets/Background.png")
                    fade_in(1280, 720, screen)
                    song(screen, BG, 0)
