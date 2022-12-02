from pygame import image

from global_functions import screen
from scenes.menu_load import MainTransition


def transitory_menu(background_bool, mapping_globals, color="black"):
    while True:
        if background_bool:
            screen.blit(image.load(mapping_globals["menu_bg"]), (0, 0))
        else:
            screen.fill(color)
        t_menu = MainTransition(mapping_globals["pos"],
                                mapping_globals["initial_y_pos"],
                                mapping_globals["font_size"],
                                mapping_globals["color_base"],
                                mapping_globals["color_hovering"],
                                mapping_globals)
        # the last argument is just to detect the input
        t_menu.struture_execution(mapping_globals["title"],
                                  mapping_globals["font_size_title"],
                                  mapping_globals["rect_cd"],
                                  mapping_globals["image_inputs"],
                                  mapping_globals["text_inputs"])
