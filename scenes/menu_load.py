import sys

import pygame

from global_functions import screen
from scenes.button import Button


class HMenu:
    def __init__(self, x_pos, initial_y_pos, font_size, color_base, color_hovering):
        self.x_pos = x_pos
        self.initial_y_pos = initial_y_pos
        self.font = pygame.font.Font("assets/font.ttf", font_size)
        self.color_base = color_base
        self.color_hovering = color_hovering
        self.menu_mouse_pos = pygame.mouse.get_pos()
        self.buttons = []

    def drawing_title(self, title, font_size_title, rect_cd):
        text_menu = pygame.font.Font("assets/font.ttf", font_size_title).render(title, True, "#b68f40")
        rectangle_menu = text_menu.get_rect(center=rect_cd)
        screen.blit(text_menu, rectangle_menu)

    def inserting_asset_buttons(self, image_inputs, text_inputs):
        for x in text_inputs:
            for i in image_inputs:
                if image_inputs.index(i) == text_inputs.index(x):
                    receiver = pygame.image.load(f"assets/{image_inputs[image_inputs.index(i)]}.png")

                    outlier = Button(image=receiver,
                                     pos=(self.x_pos, self.initial_y_pos),
                                     text_input=x, font=self.font, base_color=self.color_base,
                                     hovering_color=self.color_hovering)
                    self.initial_y_pos += 150
                    self.buttons.append(outlier)

    def button_hover_effect(self):
        for button in self.buttons:
            button.changeColorAndCheckForInput(self.menu_mouse_pos)
            button.update(screen)

    def handle_input(self, mapping_globals):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.buttons:
                    if self.buttons[self.buttons.index(i)].changeColorAndCheckForInput(self.menu_mouse_pos):
                        result = mapping_globals[self.buttons.index(i)]
                        result.execute(self, self.buttons, self.menu_mouse_pos)

    def struture_execution(self, title, font_size_title, rect_cd, image_inputs, text_inputs):
        raise NotImplemented


class MainTransition(HMenu):
    def __init__(self, x_pos, initial_y_pos, font_size, color_base, color_hovering, mapping_globals):
        super().__init__(x_pos, initial_y_pos, font_size, color_base, color_hovering)
        self.mapping_globals = mapping_globals

    def struture_execution(self, title, font_size_title, rect_cd, image_inputs, text_inputs):
        self.drawing_title(title, font_size_title, rect_cd)
        self.inserting_asset_buttons(image_inputs, text_inputs)
        self.button_hover_effect()
        self.handle_input(self.mapping_globals)
        # to set-up the screen
        pygame.display.flip()
