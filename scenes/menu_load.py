import sys

import pygame

from scenes.button import Button


class HMenu:
    def __init__(self, x_pos, y_pos, font_size, color_base, color_hovering, screen):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = pygame.font.Font("assets/fonts/font.ttf", font_size)
        self.color_base = color_base
        self.color_hovering = color_hovering
        self.menu_mouse_pos = pygame.mouse.get_pos()
        self.screen = screen
        self.buttons = []

    def drawing_title(self, title, font_size_title, rect_cd, screen):
        text_menu = pygame.font.Font("assets/fonts/font.ttf", font_size_title).render(title, True, "#b68f40")
        rectangle_menu = text_menu.get_rect(center=rect_cd)
        screen.blit(text_menu, rectangle_menu)

    def inserting_asset_buttons(self, image_inputs, text_inputs, horizontal, separation):
        for x in text_inputs:
            for i in image_inputs:
                if image_inputs.index(i) == text_inputs.index(x):
                    print(image_inputs.index(i))
                    receiver = pygame.image.load(f"assets/global_images/{image_inputs[image_inputs.index(i)]}.png")

                    outlier = Button(image=receiver,
                                     pos=(self.x_pos, self.y_pos),
                                     text_input=x, font=self.font, base_color=self.color_base,
                                     hovering_color=self.color_hovering)
                    if horizontal:
                        self.x_pos += separation
                    else:
                        self.y_pos += separation
                    self.buttons.append(outlier)

    def button_hover_effect(self, screen):
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
                        print(result)
                        result.execute(self, self.buttons, self.menu_mouse_pos, self.screen)

    def struture_execution(self, title, font_size_title, rect_cd, image_inputs, text_inputs, horizontal, separation, screen):
        raise NotImplemented


class MainTransition(HMenu):
    def __init__(self, x_pos, initial_y_pos, font_size, color_base, color_hovering, mapping_globals, screen):
        super().__init__(x_pos, initial_y_pos, font_size, color_base, color_hovering, screen)
        self.mapping_globals = mapping_globals

    def struture_execution(self, title, font_size_title, rect_cd, image_inputs, text_inputs, horizontal, separation, screen):
        self.drawing_title(title, font_size_title, rect_cd, screen)
        self.inserting_asset_buttons(image_inputs, text_inputs, horizontal, separation)
        self.button_hover_effect(screen)
        self.handle_input(self.mapping_globals)
        # to set-up the screen
        pygame.display.flip()
