import pygame


from scenes.menu_load import HMenu


class MainTransition:
    def __init__(self, x_pos, initial_y_pos, mapping_globals):
        h_menu = HMenu(x_pos, initial_y_pos, mapping_globals)
        self.h_menu = h_menu

    def draw(self, title, font_size, rect_cd, image_inputs, text_inputs):
        self.h_menu.drawing_title(title, font_size, rect_cd)
        self.h_menu.inserting_asset_buttons(image_inputs, text_inputs)
        self.h_menu.button_hover_effect()
        self.h_menu.handle_input()
        # to set-up the screen
        pygame.display.update()
