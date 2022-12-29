import sys

import pygame
import pygame_widgets
from pygame_widgets.widget import WidgetBase

from scenes.button import Button


class HMenu:
    def __init__(self, x_pos, y_pos, title, font_size_title, rect_cd,
                 image_inputs, text_inputs, color_base, color_hovering, font_size, horizontal, separation, screen):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.title = title
        self.font_size_title = font_size_title
        self.rect_cd = rect_cd
        self.image_inputs = image_inputs
        self.text_inputs = text_inputs
        self.color_base = color_base
        self.color_hovering = color_hovering
        self.font = pygame.font.Font("assets/fonts/font.ttf", font_size)
        self.horizontal = horizontal
        self.separation = separation
        self.screen = screen
        self.menu_mouse_pos = pygame.mouse.get_pos()
        self.buttons = []

    def drawing_title(self):
        text_menu = pygame.font.Font("assets/fonts/font.ttf", self.font_size_title).render(self.title, True, "#b68f40")
        rectangle_menu = text_menu.get_rect(center=self.rect_cd)
        self.screen.blit(text_menu, rectangle_menu)

    def inserting_asset_buttons(self):
        for x in self.text_inputs:
            for i in self.image_inputs:
                if self.image_inputs.index(i) == self.text_inputs.index(x):
                    receiver = pygame.image.load(
                        f"assets/global_images/{self.image_inputs[self.image_inputs.index(i)]}.png")
                    outlier = Button(image=receiver,
                                     pos=(self.x_pos, self.y_pos),
                                     text_input=x, font=self.font, base_color=self.color_base,
                                     hovering_color=self.color_hovering)
                    if self.horizontal:
                        self.x_pos += self.separation
                    else:
                        self.y_pos += self.separation
                    self.buttons.append(outlier)

    def button_hover_effect(self):
        for button in self.buttons:
            button.changeColorAndCheckForInput(self.menu_mouse_pos)
            button.update(self.screen)

    def handle_input(self, mapping_globals, dropdown, chars_selected, song_selected, song_selected_label, song_selected_layers, song_selected_song_end):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.buttons:
                    if self.buttons[self.buttons.index(i)].changeColorAndCheckForInput(self.menu_mouse_pos):
                        result = mapping_globals[self.buttons.index(i)]
                        if dropdown is not None:
                            for widget in dropdown:
                                for w in widget:
                                    WidgetBase.hide(w)
                        print(song_selected_layers)
                        result.execute(self, self.buttons, self.menu_mouse_pos, self.screen,
                                       characters=dropdown, chars=chars_selected,
                                       song_selected=song_selected, song_selected_label=song_selected_label,
                                       song_selected_layers=song_selected_layers, song_selected_song_end=song_selected_song_end)
        if dropdown is not None:
            pygame_widgets.update(events)

    def struture_execution(self, mapping_globals, dropdown, chars_selected,
                           song_selected, song_selected_label, song_selected_layer, song_selected_song_end):
        raise NotImplemented


class MainTransition(HMenu):
    def __init__(self, x_pos, y_pos, title, font_size_title, rect_cd, image_inputs, text_inputs, color_base,
                 color_hovering, font_size, horizontal, separation, screen):
        super().__init__(x_pos, y_pos, title, font_size_title, rect_cd, image_inputs, text_inputs, color_base,
                         color_hovering, font_size, horizontal, separation, screen)

    def struture_execution(self, mapping_globals, dropdown_list, chars_selected,
                           song_selected, song_selected_label, song_selected_layers, song_selected_song_end):
        self.drawing_title()
        self.inserting_asset_buttons()
        self.button_hover_effect()
        self.handle_input(mapping_globals, dropdown_list, chars_selected, song_selected, song_selected_label, song_selected_layers, song_selected_song_end)
        pygame.display.update()

        # to set-up the screen
