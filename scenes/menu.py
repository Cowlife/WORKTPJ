from global_functions import screen, menu_bg
from scenes.menu_transition import MainTransition


def transitory_menu(background_bool, mapping_globals, color="black"):
    while True:
        if background_bool:
            screen.blit(menu_bg, (0, 0))
        else:
            screen.fill(color)
        t_menu = MainTransition(mapping_globals["pos"], mapping_globals["initial_y_pos"], mapping_globals)
        # the last argument is just to detect the input
        t_menu.draw(mapping_globals["title"],
                    mapping_globals["font_size"],
                    mapping_globals["rect_cd"],
                    mapping_globals["image_inputs"],
                    mapping_globals["text_inputs"])
