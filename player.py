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
    def __init__(self, imageentitymodel, frames_in_x_and_y, width_height, x_y_start=(0, 0), max_health=0, name='',
                 damage_amount=200):
        self.x_y_start = x_y_start
        self.frames_in_x_and_y = frames_in_x_and_y
        self.width_height = width_height
        self.main_element = imageentitymodel.get_main_element()
        self.entire = imageentitymodel.get_entire()
        self.max_health = max_health
        self.health_bar_length = 400
        self.current_health = max_health  # 200 for testing
        self.target_health = max_health
        self.name = name
        self.damage_amount = damage_amount


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, entitymodel) -> None:
        super().__init__()
        # animation variables
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
        # health variables
        self.max_health = entitymodel.max_health
        self.health_bar_length = entitymodel.health_bar_length
        self.current_health = entitymodel.current_health
        self.target_health = entitymodel.target_health
        self.name = entitymodel.name
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 20
        self.amount = entitymodel.damage_amount

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
                           int(self.frame_example)):
                #     In this case the other value of self.frames is used for starting position
                self.sprites.append(
                    self.entitymodel.main_element.subsurface(x, self.entitymodel.x_y_start[1], int(self.frame_example),
                                                             self.entitymodel.width_height[1]))

    def update(self) -> bool:
        return self.move_sprite(0.4)
        # return args(kwargs)

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def health_change_function(self, inc_dec, transition_color):
        self.current_health += self.health_change_speed * inc_dec
        transition_width = int((self.target_health - self.current_health) / self.health_ratio)
        transition_color_changer = transition_color
        return transition_width, transition_color_changer

    def text_printer(self, size, _text, color, pos, screen):
        self.font = pygame.font.Font("assets/fonts/font.ttf", size)
        self.text = self.font.render(_text, True, color)
        screen.blit(self.text, pos)

    def update_health(self, screen):
        result = [0, 0]
        self.text_printer(50, "Health", (222, 109, 11), (800, 20), screen)
        if self.current_health < self.target_health:
            result = self.health_change_function(1, (0, 255, 0))

        if self.current_health > self.target_health:
            result = self.health_change_function(-1, (255, 255, 0))

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(800, 100, health_bar_width, 25)
        transition_bar = pygame.Rect(health_bar.right, 100, result[0], 25)

        pygame.draw.rect(screen, (255, 0, 0), health_bar)
        pygame.draw.rect(screen, result[1], transition_bar)
        pygame.draw.rect(screen, (255, 255, 255), (800, 100, self.health_bar_length, 25), 4)

        self.text_printer(25, f"{self.current_health}/{self.max_health}", (44, 36, 199), (900, 100), screen)

    def clone(self):
        return NotImplemented


class Slime(Entity):
    def __init__(self, pos, entitymodel) -> None:
        super().__init__(pos, entitymodel)

    def clone(self) -> Entity:
        return Slime(self.pos, self.entitymodel)


class Sorceror(Entity):
    def __init__(self, pos, entitymodel, health) -> None:
        super().__init__(pos, entitymodel)
        self.health = health

    def clone(self) -> Entity:
        return Sorceror(self.pos, self.entitymodel, self.health)


class Crystal(Entity):
    def __init__(self, pos, entitymodel, name, amount) -> None:
        super().__init__(pos, entitymodel)
        self.name = name
        self.amount = amount

    def clone(self) -> Entity:
        return Crystal(self.pos, self.entitymodel, self.name, self.amount)


class Heal(Entity):
    def __init__(self, pos, entitymodel, name, amount) -> None:
        super().__init__(pos, entitymodel)
        self.name = name
        self.amount = amount

    def clone(self) -> Entity:
        return Crystal(self.pos, self.entitymodel, self.name, self.amount)


class Spawner:
    def spawn_Entity(self, prototype):
        return prototype.clone()
