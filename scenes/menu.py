import pygame
from pygame import image, mixer
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import Button

from scenes.menu_load import MainTransition


class TransitoryMenu:
    def background_implementer(self, background_bool, mapping_globals, screen, color="black"):
        if background_bool:
            screen.blit(image.load(mapping_globals["menu_bg"]), (0, 0))
        else:
            screen.fill(color)

    def menu_constructor(self, mapping_globals, screen, dropper=None):
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
        t_menu.struture_execution(mapping_globals, dropper)


    def dropdown_menu_executor(self, screen, list_selector):
        dropdown = Dropdown(
            screen, 120, 310, 150, 50, name='Select Character',
            choices=list_selector, colour=(200, 0, 0),
            borderRadius=3, values=list_selector, direction='down', textVAlign='bottom'
        )

        def printValue():
            sound_effecting = mixer.Sound("assets/sound_narrators/CharacterChoice.wav")
            if dropdown.getSelected() is not None:
                sound_effecting = mixer.Sound(f"assets/sound_narrators/{dropdown.getSelected()}.wav")
            mixer.Sound.play(sound_effecting)
            print(dropdown.getSelected())

        button = Button(
            screen, 120, 400, 150, 50, text='Pick', fontSize=30,
            margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
            radius=5, onClick=printValue, font=pygame.font.Font('assets/fonts/titlefont.ttf', 10),
            textVAlign='bottom'
        )
        return dropdown, button
    def executioner(self, background_bool, mapping_globals, screen,
                    color="black", list_selector=None):
        raise NotImplemented


class ScreenMenu(TransitoryMenu):  # Default Menu
    def executioner(self, background_bool, mapping_globals, screen,
                    color="black", list_selector=None):
        mixer.music.load(mapping_globals["music"])
        mixer.music.play()
        dropper = None
        if list_selector is not None:
            dropper = self.dropdown_menu_executor(screen, list_selector)
        while True:
            self.background_implementer(background_bool, mapping_globals, screen, color)
            self.menu_constructor(mapping_globals, screen, dropper)
