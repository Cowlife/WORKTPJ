import pygame
from pygame import image, mixer
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import Button

from scenes.menu_load import MainTransition


class TransitoryMenu:
    def background_implementer(self, background_bool, mapping_globals, screen, color):
        if background_bool:
            screen.blit(image.load(mapping_globals["menu_bg"]), (0, 0))
        else:
            screen.fill(color)

    def menu_constructor(self, mapping_globals, screen, dropper_list=None):
        t_menu = MainTransition(mapping_globals["x_pos"],
                                mapping_globals["y_pos"],
                                mapping_globals["title"],
                                mapping_globals["font_size_title"],
                                mapping_globals["rect_cd"],
                                mapping_globals["image_inputs"],
                                mapping_globals["text_inputs"],
                                mapping_globals["color_base"],
                                mapping_globals["color_hovering"],
                                mapping_globals["font_size"],
                                mapping_globals["horizontal"],
                                mapping_globals["separation"],
                                screen)
        t_menu.struture_execution(mapping_globals, dropper_list)

    def dropdown_menu_executor(self, screen, list_selector, list_value, settings):
        dropdown_list, button_list = [], []
        if list_value is None:
            list_value = list_selector
        initial_pos = [settings["x_pos"], settings["y_pos"]]
        for i in range(settings["elements"]):
            dropdown = Dropdown(
                screen, initial_pos[0], initial_pos[1], settings["width"], settings["height"],
                name=settings["label"], choices=list_selector, colour=settings["colour"],
                borderRadius=settings["borderRadius"], values=list_value, direction=settings["direction"],
                textVAlign=settings["textVAlign"]
            )

            def printValue(default, file_acessor, i):
                if list_value == list_selector:
                    sound_effecting = mixer.Sound(f"{file_acessor}/{default}")
                    if dropdown_list[i].getSelected() is not None:
                        sound_effecting = mixer.Sound(f"{file_acessor}/{dropdown_list[i].getSelected()}.wav")
                    mixer.Sound.play(sound_effecting)
                else:
                    mixer.music.load(f"{file_acessor}/{default}")
                    if dropdown_list[i].getSelected() is not None:
                        mixer.music.load(f"{file_acessor}/{dropdown_list[i].getSelected()}.mp3")
                    mixer.music.play()


            if settings["vertical_separation"]:
                button_pos = [initial_pos[0] + settings["local_separation"], initial_pos[1]]
            else:
                button_pos = [initial_pos[0], initial_pos[1] + settings["local_separation"]]

            button = Button(
                screen, button_pos[0], button_pos[1],
                settings["pickButtonSize"][0], settings["pickButtonSize"][1], text=settings["pickButtonLabel"],
                font=pygame.font.Font('assets/fonts/titlefont.ttf', settings["pickButtonLabelSize"]),
                margin=20, inactiveColour=settings["pickColours"][0], pressedColour=settings["pickColours"][1],
                onClick=printValue, onClickParams=[settings["default"], settings["file_acessor"], i],
                radius=5, textVAlign=settings["pickVAlign"]
            )
            initial_pos[0] += settings["global_separation"]
            dropdown_list.append(dropdown)
            button_list.append(button)
        return dropdown_list, button_list

    def executioner(self, background_bool, mapping_globals, screen, **kwargs):
        raise NotImplemented


class ScreenMenu(TransitoryMenu):  # Default Menu
    def executioner(self, background_bool, mapping_globals, screen, **kwargs):
        color = kwargs.get('color', "black")
        list_selector = kwargs.get('list_selector', None)
        list_value = kwargs.get('list_value', None)
        settings = kwargs.get('settings', None)
        mixer.music.load(mapping_globals["music"])
        mixer.music.play()
        dropper_list = None
        if list_selector is not None:
            dropper_list = self.dropdown_menu_executor(screen, list_selector, list_value, settings)
        while True:
            self.background_implementer(background_bool, mapping_globals, screen, color)
            self.menu_constructor(mapping_globals, screen, dropper_list)
