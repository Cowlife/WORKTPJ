import pygame
from pygame import image, mixer
from pygame_widgets.button import Button

from customdropdown import CustomDropdown
from scenes.menu_load import MainTransition


class TransitoryMenu:
    def background_implementer(self, background_bool, mapping_globals, screen, color):
        if background_bool:
            screen.blit(image.load(mapping_globals["menu_bg"]), (0, 0))
        else:
            screen.fill(color)

    def menu_constructor(self, mapping_globals, screen, **kwargs):
        dropper_list = kwargs.get('dropper_list', None)
        chars_selected = kwargs.get('chars_selected', [])
        song_selected = kwargs.get('song_selected', [])
        song_selected_label = kwargs.get('song_selected_label', [])
        song_selected_layers = kwargs.get('song_selected_layers', [])
        song_selected_song_end = kwargs.get('song_selected_song_end', [])
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
        t_menu.struture_execution(mapping_globals, dropper_list, chars_selected,
                                  song_selected, song_selected_label, song_selected_layers, song_selected_song_end)

    def printChar(self, screen, dropper_element):
        imp = pygame.image.load(f"assets/gifs/{dropper_element.getSelected()}.png").convert()
        image = pygame.transform.scale(imp, (200, 200))
        screen.blit(image, (dropper_element.getX() - 25, dropper_element.getY() + 100))
        return dropper_element.getSelected()

    def printinfo(self, screen, dropper_element):
        pygame.draw.rect(screen, (78, 176, 194), pygame.Rect(120, 180, 1050, 350))
        font = pygame.font.Font("assets/fonts/font.ttf", 30)
        text_dificulty = font.render(f"Dificulty: {dropper_element.getDificulty()}", True, (78, 176, 0))
        text_end_song = font.render(f"Duration: {dropper_element.getEndSong()}", True, (78, 176, 0))
        screen.blit(text_dificulty, (150, 200))
        screen.blit(text_end_song, (150, 250))
        return dropper_element.getSelected(), dropper_element.getChoiceName(), dropper_element.getLayer(), dropper_element.getEndSong()

    def dropdown_menu_executor(self, screen, list_selector, list_value, settings, **kwargs):
        list_extras = [kwargs.get('list_dificulty', None),
                       kwargs.get('list_end_song', None),
                       kwargs.get('list_layers', None)]
        dropdown_list, button_list = [], []
        if list_value is None:
            list_value = list_selector
        initial_pos = [settings["x_pos"], settings["y_pos"]]
        for i in range(settings["elements"]):
            dropdown = CustomDropdown(
                screen, initial_pos[0], initial_pos[1], settings["width"], settings["height"],
                name=settings["label"], choices=list_selector, colour=settings["colour"],
                borderRadius=settings["borderRadius"], values=list_value, direction=settings["direction"],
                textVAlign=settings["textVAlign"], dificulty_choices=list_extras[0], end_song_choices=list_extras[1],
                layer_choices=list_extras[2])

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

    def execution(self, background_bool, mapping_globals, screen, **kwargs):
        raise NotImplemented


class ScreenMenu(TransitoryMenu):  # Default Menu
    def execution(self, background_bool, mapping_globals, screen, **kwargs):
        color = kwargs.get('color', "black")
        list_selector = kwargs.get('list_selector', None)
        list_value = kwargs.get('list_value', None)
        settings = kwargs.get('settings', None)
        list_optionals = [kwargs.get('list_dificulty', None),
                          kwargs.get('list_end_song', None),
                          kwargs.get('list_layers', None), ]
        # Separating song_selected from list_optionals in order to separate globals lists from selected elements
        mixer.music.load(mapping_globals["music"])
        mixer.music.play()
        dropper_list = None
        song_selected = [kwargs.get('song_selected', None),
                         kwargs.get('song_selected_label', None),
                         kwargs.get('song_selected_layers', 0),
                         kwargs.get('song_selected_song_end', 0)]
        if list_selector is not None:
            dropper_list = self.dropdown_menu_executor(screen, list_selector, list_value, settings,
                                                       list_dificulty=list_optionals[0],
                                                       list_end_song=list_optionals[1],
                                                       list_layers=list_optionals[2])
        while True:
            self.background_implementer(background_bool, mapping_globals, screen, color)
            chars_selected = []

            if dropper_list is not None:
                for i in range(settings["elements"]):
                    if dropper_list[0][i].getSelected() is not None:
                        if all(v is not None for v in list_optionals):
                            song_selected = self.printinfo(screen, dropper_list[0][i])
                        else:
                            list_chars = self.printChar(screen, dropper_list[0][i])
                            chars_selected.append(list_chars)
            self.menu_constructor(mapping_globals, screen, dropper_list=dropper_list,
                                  chars_selected=chars_selected,
                                  song_selected=song_selected[0],
                                  song_selected_label=song_selected[1],
                                  song_selected_layers=song_selected[2],
                                  song_selected_song_end=song_selected[3])
