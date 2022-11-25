import math

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, entire, main_element, frames_in_x_and_y, width_height, sub_surfaces=1):
        super().__init__()
        self.entire = entire
        self.frames_in_x_and_y = frames_in_x_and_y  # total sprites
        self.width_height = width_height
        self.attack_animation = False
        self.sprites = []
        self.frames = math.prod(frames_in_x_and_y)
        self.rows = self.width_height[0] / frames_in_x_and_y[0]
        self.columns = self.width_height[1] / frames_in_x_and_y[1]
        self.sub_surfaces = sub_surfaces
        self.frame_example = self.width_height[0] / sub_surfaces

        if entire:
            for x in range(self.frames):
                self.sprites.append(
                    main_element.subsurface(
                        (x % frames_in_x_and_y[0]) * self.rows,
                        (x // frames_in_x_and_y[0]) * self.columns,
                        self.rows, self.columns))

        else:
            for x in range(0, self.width_height[0], int(self.frame_example)):  # [1344, 84]
                #     In this case the other value of self.frames is used for starting position
                self.sprites.append(
                    main_element.subsurface(x, self.frames_in_x_and_y[1], int(self.frame_example), self.width_height[1]))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos[0], pos[1]]

    def attack(self, speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
            self.attack_animation = False
        self.image = self.sprites[int(self.current_sprite)]