import sys

import pygame

from global_functions import screen, get_font
from scenes.button import Button


class HMenu:
    def __init__(self, pos_x, initial_pos_y, mapping_globals):
        self.pos_x = pos_x
        self.initial_pos_y = initial_pos_y
        self.font = get_font(50)
        self.color_base = "#2596be"
        self.color_hovering = "Red"
        self.menu_mouse_pos = pygame.mouse.get_pos()
        self.buttons = []
        self.mapping_globals = mapping_globals

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
            button.changeColorAndCheckForInput(self.menu_mouse_pos)
            button.update(screen)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.buttons:
                    if self.buttons[self.buttons.index(i)].changeColorAndCheckForInput(self.menu_mouse_pos):
                        result = self.mapping_globals[self.buttons.index(i)]
                        result.execute(self, self.buttons, self.menu_mouse_pos)


