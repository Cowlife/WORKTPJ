import sys

import pygame

from scenes.button import Button
from global_functions import get_font, fade_in, screen
from scenes.options import options
from scenes.play import play


class HMenu:
    def __init__(self, pos_x, initial_pos_y, text_inputs, bg):
        self.bg = bg
        self.pos_x = pos_x
        self.initial_pos_y = initial_pos_y
        self.text_inputs = text_inputs
        self.font = get_font(50)
        self.color_base = "#2596be"
        self.color_hovering = "Red"
        self.menu_mouse_pos = pygame.mouse.get_pos()
        self.buttons = []

    def drawing_title(self, title):
        text_menu = get_font(100).render(title, True, "#b68f40")
        rectangle_menu = text_menu.get_rect(center=(640, 100))
        screen.blit(text_menu, rectangle_menu)

    def inserting_asset_buttons(self):
        image_inputs = ["Play Rect", "Options Rect", "Quit Rect"]
        for i in image_inputs:
            outlier = Button(image=pygame.image.load(f"assets/{image_inputs[image_inputs.index(i)]}.png"),
                             pos=(self.pos_x, self.initial_pos_y),
                             text_input=i, font=self.font, base_color=self.color_base,
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
                for i in self.buttons:
                    if self.buttons[0].checkForInput(self.menu_mouse_pos):
                        fade_in(1280, 720, screen)
                        play(screen)
                    if self.buttons[1].checkForInput(self.menu_mouse_pos):
                        fade_in(1280, 720, screen)
                        options(screen)
                    if self.buttons[2].checkForInput(self.menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
