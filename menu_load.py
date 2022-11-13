import pygame

from button import Button


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class HMenu:
    def __init__(self, image, pos_x, initial_pos_y):
        self.image = pygame.image.load("assets/" + image + ".png")
        self.pos_x = pos_x
        self.initial_pos_y = initial_pos_y
        self.font = get_font(75)
        self.color_base = "#2596be"
        self.color_hovering = "Red"
        self.text_inputs = ["PLAY", "OPTIONS", "QUIT"]

    def create_buttons(self):
        for i in self.text_inputs:
            buttons = []
            outlier = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(self.pos_x, self.initial_pos_y),
                             text_input=i, font=self.font, base_color=self.color_base,
                             hovering_color=self.color_hovering)
            self.initial_pos_y += 150
            buttons.append(outlier)
        return buttons
