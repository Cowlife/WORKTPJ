from global_functions import screen, menu_bg
from scenes.menu_transition import MainTransition


def transitory_menu(background_bool, mapping_globals, color="black"):
    while True:
        if background_bool:
            screen.blit(menu_bg, (0, 0))
        else:
            screen.fill(color)
        t_menu = MainTransition(mapping_globals.get("pos"), mapping_globals.get("initial_y_pos"), mapping_globals)
        t_menu.draw(mapping_globals.get("title"),
                    mapping_globals.get("font_size"),
                    mapping_globals.get("rect_cd"),
                    mapping_globals.get("image_inputs"),
                    mapping_globals.get("text_inputs"))
