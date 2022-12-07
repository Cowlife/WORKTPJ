import math

import pygame
from pygame import image


class ImageEntityModel:
    def __init__(self, entire, main_element, flip=False):
        self._main_element = main_element
        self._entire = entire
        self._flip = flip

    def get_main_element(self):
        if self._flip:
            self._main_element = pygame.transform.flip(self._main_element, True, False)
        return self._main_element

    def get_entire(self):
        return self._entire


class EntityModel:
    def __init__(self, imageentitymodel, frames_in_x_and_y, width_height, x_y_start=(0, 0)):
        self.x_y_start = x_y_start
        self.frames_in_x_and_y = frames_in_x_and_y
        self.width_height = width_height
        self.main_element = imageentitymodel.get_main_element()
        self.entire = imageentitymodel.get_entire()


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, entitymodel) -> None:
        super().__init__()
        self.pos = pos
        self.entitymodel = entitymodel
        self.attack_animation = False
        self.attack_stance = False
        self.sprites = []
        self.frames = math.prod(self.entitymodel.frames_in_x_and_y)
        self.rows = self.entitymodel.width_height[0] / self.entitymodel.frames_in_x_and_y[1]
        self.columns = self.entitymodel.width_height[1] / self.entitymodel.frames_in_x_and_y[0]
        self.frame_example = self.entitymodel.width_height[0] / self.entitymodel.frames_in_x_and_y[0]
        self.spritesheet_list()
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos[0], pos[1]]

    def move_sprite(self, speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            if not self.attack_stance:
                self.current_sprite = 0
            else:
                self.attack_animation = True
            return self.attack_animation
        self.image = self.sprites[int(self.current_sprite)]

    def spritesheet_list(self):
        if self.entitymodel.entire:
            for x in range(self.frames):
                self.sprites.append(
                    self.entitymodel.main_element.subsurface(
                        (x % self.entitymodel.frames_in_x_and_y[1]) * self.rows,
                        (x // self.entitymodel.frames_in_x_and_y[1]) * self.columns,
                        self.rows, self.columns))

        else:
            for x in range(self.entitymodel.x_y_start[0], self.entitymodel.width_height[0],
                           int(self.frame_example)):  # [1344, 84]
                #     In this case the other value of self.frames is used for starting position
                self.sprites.append(
                    self.entitymodel.main_element.subsurface(x, self.entitymodel.x_y_start[1], int(self.frame_example),
                                                             self.entitymodel.width_height[1]))

    def clone(self):
        return NotImplemented


class Slime(Entity):
    def __init__(self, pos, entitymodel) -> None:
        super().__init__(pos, entitymodel)

    def clone(self) -> Entity:
        return Slime(self.pos, self.entitymodel)


class Sorceror(Entity):
    def __init__(self, pos, entitymodel) -> None:
        super().__init__(pos, entitymodel)

    def clone(self) -> Entity:
        return Sorceror(self.pos, self.entitymodel)


class Spawner:
    def spawn_Entity(self, prototype):
        return prototype.clone()


def main():
    enemyImageEntityModel = ImageEntityModel(False, image.load('assets/sprites_enemy/slime.png'), True)
    enemyEntityModel = EntityModel(enemyImageEntityModel, (2, 1), (90, 45))
    slime = Slime((400, 400), enemyEntityModel)
    spawner = Spawner()

    spawner.spawn_Entity(slime)
    print(spawner.spawn_Entity(slime))


if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    main()

