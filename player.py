import math

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, entire, main_element, frames_in_x_and_y, width_height, x_y_start=(1, 1)):
        super().__init__()
        self.entire = entire
        self.attack_stance = False
        self.frames_in_x_and_y = frames_in_x_and_y  # total sprites
        self.width_height = width_height
        self.attack_animation = False
        self.sprites = []
        self.frames = math.prod(frames_in_x_and_y)
        self.rows = self.width_height[0] / frames_in_x_and_y[1]
        self.columns = self.width_height[1] / frames_in_x_and_y[0]
        self.frame_example = self.width_height[0] / frames_in_x_and_y[0]
        self.x_y_start = x_y_start
        self.main_element = main_element
        self.spritesheet_list()
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos[0], pos[1]]

    def move(self, speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            if not self.attack_stance:
                self.current_sprite = 0
            else:
                self.attack_animation = True
            return self.attack_animation
        self.image = self.sprites[int(self.current_sprite)]

    def spritesheet_list(self):
        if self.entire:
            for x in range(self.frames):
                self.sprites.append(
                    self.main_element.subsurface(
                        (x % self.frames_in_x_and_y[1]) * self.rows,
                        (x // self.frames_in_x_and_y[1]) * self.columns,
                        self.rows, self.columns))

        else:
            for x in range(self.x_y_start[0], self.width_height[0], int(self.frame_example)):  # [1344, 84]
                #     In this case the other value of self.frames is used for starting position
                self.sprites.append(
                    self.main_element.subsurface(x, self.x_y_start[1], int(self.frame_example), self.width_height[1]))

