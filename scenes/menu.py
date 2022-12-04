from pygame import image, sprite, mixer

from player import Entity
from scenes.menu_load import MainTransition


class TransitoryMenu:
    def background_implementer(self, background_bool, mapping_globals, screen, color="black"):
        if background_bool:
            screen.blit(image.load(mapping_globals["menu_bg"]), (0, 0))
        else:
            screen.fill(color)

    def menu_constructor(self, mapping_globals, screen):
        t_menu = MainTransition(mapping_globals["x_pos"],
                                mapping_globals["y_pos"],
                                mapping_globals["font_size"],
                                mapping_globals["color_base"],
                                mapping_globals["color_hovering"],
                                mapping_globals, screen)
        # the last argument is just to detect the input
        t_menu.struture_execution(mapping_globals["title"],
                                  mapping_globals["font_size_title"],
                                  mapping_globals["rect_cd"],
                                  mapping_globals["image_inputs"],
                                  mapping_globals["text_inputs"],
                                  mapping_globals["horizontal"],
                                  mapping_globals["separation"],
                                  screen)

    def executioner(self, background_bool, mapping_globals, screen, color="black"):
        raise NotImplemented


class ScreenMenu(TransitoryMenu):  # Default Menu
    def executioner(self, background_bool, mapping_globals, screen, color="black"):
        mixer.music.load(mapping_globals["music"])
        mixer.music.play()
        while True:
            self.background_implementer(background_bool, mapping_globals, screen, color)
            self.menu_constructor(mapping_globals, screen)

