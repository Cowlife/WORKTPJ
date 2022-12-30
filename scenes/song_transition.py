import time
import pygame

from pygame import sprite, image, mixer
from pygame.time import Clock
from pygame_widgets.progressbar import ProgressBar

import button_transitions
from animation_transition import AnimationTransitionComponent
from keys import keys, keys_damage
from player import ImageEntityModel, EntityModel, Entity, Spawner, Slime, Sorceror, Crystal, Heal
from scenes.menu import ScreenMenu
from scenes.parallax_storage import ImageryGroundExecution


class SongComponent:
    def __init__(self, screen, song_file, chars_selected, chars_data, enemies_list, enemy_data, result_search):

        self.screen = screen
        self.song_file = song_file
        self.chars_selected = chars_selected
        self.chars_data = chars_data
        self.enemies_list = enemies_list
        self.enemy_data = enemy_data
        self.result_search = result_search  # scenario, layers, counter_final
        self.spawner = Spawner()
        self.clock = Clock()
        self.pos_loader = 400  # [400, 500, 600] -> Important for position of Entities
        self.enemy_sprites = sprite.Group()
        self.sprite_group_list = [sprite.Group(), sprite.Group(), sprite.Group(), sprite.Group()]
        # index marking:
        # 0: moving sprites
        # 1: attacking sprites
        # 2: hurting sprites
        # 3: crystal sprites

    def spawner_entity_list(self, x, y, rects, spawner_marker, entity_list):
        key_pressers = pygame.Rect((x * 50) + 650, (y * 100) + 400, 25, 25)
        rects.append(key_pressers)
        spawner_instance = self.spawner.spawn_Entity(spawner_marker)
        entity_list.append(spawner_instance)

    def load(self, map, list_enemies):
        rects, entity_list = [], []
        info_spawner = self.enemy_data[5]
        mixer.music.load("musics/" + map + ".mp3")
        mixer.music.play()
        with open(f"charts/{map}.txt", 'r') as f:
            data = f.readlines()
        for y in range(len(data)):
            for x in range(len(data[y])):
                for i in range(len(info_spawner)):
                    if data[y][x] == info_spawner[i]:
                        self.spawner_entity_list(x, y, rects, list_enemies[i], entity_list)
        return rects, entity_list

    def non_existent_file(self):
        return FileNotFoundError

    def loading_singular_entity(self, imageEntityModel, frames_in_x_y, width, sprite_group, enemy_image, max_health, x_y_start):
        entityModel = EntityModel(imageEntityModel, frames_in_x_and_y=frames_in_x_y,
                                  width_height=width, x_y_start=x_y_start,
                                  max_health=max_health)
        if enemy_image is not None:
            enemy_types = {'crystal': Crystal((0, 0), entityModel, 'red', 100),
                           'dancing': Sorceror((0, 0), entityModel,
                                               entityModel.current_health),
                           'heal': Heal((0, 0), entityModel, 'heal', 100),
                           'slime': Slime((0, 0), entityModel), }
            entity = enemy_types.get(enemy_image, self.non_existent_file())
        else:
            entity = Entity((50, self.pos_loader), entityModel)

        sprite_group.add(entity)
        return entity

    def loading_entities(self, entities):
        for ent in entities:
            for i in ent:
                ind = ent.index(i)
                if entities.index(ent) == 0:
                    is_entire_is_flipped = [self.chars_data[ind][0][0], 'sprites_player', False]
                    # default false since it does not suit me flipping characters
                else:
                    is_entire_is_flipped = [self.enemy_data[2][ind], 'sprites_enemy', self.enemy_data[1][ind]]
                imageEntityModel = ImageEntityModel(entire=is_entire_is_flipped[0],
                                                    main_element=image.load(
                                                        f'assets/{is_entire_is_flipped[1]}/{i}.png'),
                                                    flip=is_entire_is_flipped[2])
                if entities.index(ent) == 0:
                    for value in range(len(self.chars_data[0])):
                        self.player = self.loading_singular_entity(imageEntityModel=imageEntityModel,
                                                                   frames_in_x_y=self.chars_data[ind][2][0][value],
                                                                   width=self.chars_data[ind][3][0][value],
                                                                   sprite_group=self.sprite_group_list[value],
                                                                   x_y_start=self.chars_data[ind][1][0][value],
                                                                   max_health=1000, enemy_image=None)
                    self.pos_loader += 100
                else:
                    enemy_image = i
                    self.loading_singular_entity(imageEntityModel=imageEntityModel,
                                                 frames_in_x_y=tuple(self.enemy_data[4][ind]),
                                                 width=tuple(self.enemy_data[3][ind]),
                                                 sprite_group=self.enemy_sprites,
                                                 enemy_image=enemy_image,
                                                 max_health=self.enemy_data[0][ind],
                                                 x_y_start=(0,0))

    def key_and_loop_handler(self, keys, keys_damage):
        k = pygame.key.get_pressed()
        for key in keys:
            if k[key.key]:
                pygame.draw.rect(self.screen, key.color1, key.rect)
                key.handled = False
            if not k[key.key]:
                pygame.draw.rect(self.screen, key.color2, key.rect)
                key.handled = True
        # now when we press our keys they will change color
        for key in keys_damage:
            if not k[key.key]:
                key.handled = True
        # damage infliction scenario

    def scene_transitor(self, dict_state, progress_state):
        pygame.display.flip()
        ProgressBar.hide(progress_state)
        fade_in_upper = button_transitions.FadeTransition(self.screen)
        fade_in_upper.black_out()
        st_menu = ScreenMenu()
        st_menu.executioner(True, dict_state, self.screen)

    def UnityExecutor(self):
        raise NotImplemented


class SongExecutor(SongComponent):
    def __init__(self, screen, song_file, chars_selected, chars_data, enemies_list, enemy_data, result_search):
        super().__init__(screen, song_file, chars_selected, chars_data, enemies_list, enemy_data, result_search)

    def UnityExecutor(self):

        # Entity Loader Component
        self.loading_entities([self.chars_selected, self.enemies_list])

        # Progress Bar Component
        startTime = time.time()
        progressBar = ProgressBar(self.screen, 100, 100, 500, 40,
                                  lambda: (time.time() - startTime) / self.result_search[2],
                                  curved=False)

        # Scenario Component
        imagery = ImageryGroundExecution(0, self.result_search[0], self.result_search[1], [(1280, 256), (844, 475)],
                                         self.screen, 0)

        list_enemies = self.enemy_sprites.sprites()
        map_rect = self.load(self.song_file, list_enemies)

        list_of_sprites = [self.sprite_group_list[spr].sprites() for spr in range(len(self.sprite_group_list))]
        animation_transition = AnimationTransitionComponent(self.sprite_group_list, list_of_sprites)

        while True:
            self.clock.tick(60)  # limit movement screen

            imagery.loop_executor()

            for animation_index in range(len(self.sprite_group_list)):  # giving movement to all sprites
                self.sprite_group_list[animation_index].update()

            self.player.update_health(self.screen)

            for i in range(-3, 0):
                for lst_spr in range(1, len(list_of_sprites)):
                    if list_of_sprites[lst_spr][i].attack_animation:
                        animation_transition.update_animation(lst_spr, i, True)

            for rect, enemy in zip(map_rect[0], map_rect[1]):
                if rect.x < self.screen.get_size()[0]:
                    pygame.draw.rect(self.screen, (200, 0, 0), rect)
                    self.screen.blit(enemy.image, rect)
                    enemy.text_printer(25, f"{int(enemy.target_health / 200) + 1}", (222, 109, 11), rect, self.screen)
                # counters to stronger enemies
                enemy.update()
                rect.x -= 5
                for key in zip(keys, keys_damage):
                    if key[0].rect.colliderect(rect) and not key[0].handled:  # not for actually skill
                        enemy.get_damage(200)

                        if enemy.target_health > 0:
                            rect.x += 100
                        else:
                            map_rect[0].remove(rect)
                            map_rect[1].remove(enemy)

                        # Transition(self._menu, self._options)
                        sound_effecting = pygame.mixer.Sound("assets/sound_effects/attack sound effect.wav")

                        for i in range(-3, 0):
                            if enemy.name == 'red':
                                if key[0].key == keys[i].key:
                                    animation_transition.update_animation(3, i)
                            elif enemy.name == 'heal':
                                if key[0].key == keys[i].key:
                                    self.player.get_health(enemy.amount)
                                    animation_transition.update_animation(3, i)
                            else:
                                if key[0].key == keys[i].key:
                                    animation_transition.update_animation(1, i)

                        pygame.mixer.Sound.play(sound_effecting)
                        key[0].handled = True
                    elif key[1].rect.colliderect(rect) and key[1].handled:
                        self.player.get_damage(enemy.amount)
                        map_rect[0].remove(rect)
                        map_rect[1].remove(enemy)

                        sound_effecting = pygame.mixer.Sound("assets/sound_effects/damage sound effect.wav")

                        for i in range(-3, 0):
                            if key[1].key == keys_damage[i].key:
                                animation_transition.update_animation(2, i)
                        pygame.mixer.Sound.play(sound_effecting)

            self.sprite_group_list[0].draw(self.screen)

            if imagery.counter == self.result_search[2]:
                self.scene_transitor(button_transitions.Globals.mapping_buttons_victory_state, progressBar)
            if self.player.current_health == 0:
                self.scene_transitor(button_transitions.Globals.mapping_buttons_losing_state, progressBar)

            # now we will loop through the keys and handle the events
            self.key_and_loop_handler(keys, keys_damage)

            pygame.display.flip()
