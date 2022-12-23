import time
import pygame

from pygame import sprite, image, mixer
from pygame.time import Clock
from pygame_widgets.progressbar import ProgressBar

import button_transitions
from keys import keys, keys_damage
from player import ImageEntityModel, EntityModel, Entity, Spawner, Slime, Sorceror, Crystal
from scenes.menu import ScreenMenu
from scenes.parallax_storage import ImageryGroundExecution
from scenes.states import FSM, Transition, Alive, Options, State


class SongComponent:
    def __init__(self, screen, song_file):

        clock = Clock()
        counter = 0
        image_loader = ['Bowser', 'Mario', 'Luigi']  # [400, 500, 600]

        frames_in_x_y_model = [(16, 1), (12, 1), (12, 1)]
        frames_in_x_y_attack = [(9, 1), (4, 1), (4, 1)]
        frames_in_x_y_hurt = [(9, 1), (3, 1), (3, 1)]
        frames_in_x_y_crystal = [(12, 1), (4, 1), (4, 1)]

        width_model = [(1344, 70), (1008, 58), (1068, 75)]
        width_attacks = [(999, 60), (448, 75), (444, 75)]
        width_hurt = [(675, 62), (260, 44), (285, 59)]
        width_crystal = [(912, 75), (308, 48), (348, 59)]

        start_pos_model = [(0, 0), (0, 0), (0, 0)]
        start_pos_attacks = [(26, 89), (0, 70), (0, 79)]
        start_pos_hurt = [(0, 165), (0, 174), (0, 180)]
        start_pos_crystal = [(0, 229), (77, 244), (20, 246)]

        counter_final = 10

        frames_in_x_y_enemy = [(2, 1), (10, 8), (4, 1)]
        width_enemy = [(90, 45), (880, 1280), (256, 64)]

        self.clock = clock
        self.screen = screen
        self.song_file = song_file
        self.counter = counter
        self.image_loader = image_loader

        self.frames_in_x_y_model = frames_in_x_y_model
        self.frames_in_x_y_attack = frames_in_x_y_attack
        self.frames_in_x_y_hurt = frames_in_x_y_hurt
        self.frames_in_x_y_crystal = frames_in_x_y_crystal

        self.width_model = width_model
        self.width_attacks = width_attacks
        self.width_hurt = width_hurt
        self.width_crystal = width_crystal

        self.start_pos_model = start_pos_model
        self.start_pos_attacks = start_pos_attacks
        self.start_pos_hurt = start_pos_hurt
        self.start_pos_crystal = start_pos_crystal

        self.pos_loader = 400

        self.frames_in_x_y_list = [frames_in_x_y_model, frames_in_x_y_attack, frames_in_x_y_hurt, frames_in_x_y_crystal]
        self.width_list = [width_model, width_attacks, width_hurt, width_crystal]
        self.start_pos_list = [start_pos_model, start_pos_attacks, start_pos_hurt, start_pos_crystal]

        self.counter_final = counter_final

        self.width_enemy = width_enemy
        self.frames_in_x_y_enemy = frames_in_x_y_enemy
        self.moving_sprites = sprite.Group()
        self.attacking_sprites = sprite.Group()
        self.hurting_sprites = sprite.Group()
        self.crystal_sprites = sprite.Group()
        self.sprite_group_list = [self.moving_sprites, self.attacking_sprites, self.hurting_sprites,
                                  self.crystal_sprites]
        self.enemy_loader = ['slime', 'dancing', 'crystal']
        self.health_enemies = [0, 300, 0]
        self.entire = [False, True, False]
        self.flipper = [True, True, False]
        self.enemy_sprites = sprite.Group()

        self._menu = Alive()
        self._options = Options()
        self._dead = State("Dead")
        self.states = [self._menu, self._options, self._dead]
        self.transitions = {
            "rest": Transition(self._menu, self._options),
            "engage": Transition(self._options, self._menu),
            "harakiri": Transition(self._options, self._dead)
        }

        self.fsm = FSM(self.states, self.transitions)

    def spawner_entity_list(self, x, y, rects, spawner, spawner_marker, entity_list):
        key_pressers = pygame.Rect((x * 50) + 650, (y * 100) + 400, 25, 25)
        rects.append(key_pressers)
        spawner_instance = spawner.spawn_Entity(spawner_marker)
        entity_list.append(spawner_instance)

    def load(self, map, spawner, list_enemies):
        rects, entity_list = [], []
        info_spawner = ['0', '1', 'c']
        mixer.music.load("musics/" + map + ".mp3")
        mixer.music.play()
        with open(f"charts/{map}.txt", 'r') as f:
            data = f.readlines()
        for y in range(len(data)):
            for x in range(len(data[y])):
                for i in range(len(info_spawner)):
                    if data[y][x] == info_spawner[i]:
                        self.spawner_entity_list(x, y, rects, spawner, list_enemies[i], entity_list)
        return rects, entity_list

    def non_existent_file(self):
        return FileNotFoundError

    def loading_singular_player(self, personImageEntityModel, ind, frames_in_x_y, width, start_pos, sprite_group):
        personEntityModel = EntityModel(personImageEntityModel, frames_in_x_y[ind],
                                        width[ind], start_pos[ind], max_health=1000)
        player = Entity((50, self.pos_loader), personEntityModel)
        sprite_group.add(player)
        return player

    def loading_players(self):
        for i in self.image_loader:
            ind = self.image_loader.index(i)
            personImageEntityModel = ImageEntityModel(False, image.load(f'assets/sprites_player/{i}.png'))
            for a in range(len(self.start_pos_list)):
                self.player = self.loading_singular_player(personImageEntityModel, ind, self.frames_in_x_y_list[a],
                                                           self.width_list[a], self.start_pos_list[a],
                                                           self.sprite_group_list[a])
            self.pos_loader += 100

    def loading_enemies(self):
        for z in self.enemy_loader:
            ind = self.enemy_loader.index(z)
            enemyImageEntityModel = ImageEntityModel(self.entire[ind], image.load(f'assets/sprites_enemy/{z}.png'),
                                                     self.flipper[ind])

            self.enemyEntityModel = EntityModel(enemyImageEntityModel, self.frames_in_x_y_enemy[ind],
                                                self.width_enemy[ind],
                                                max_health=self.health_enemies[ind])
            self.funcs = {'slime': Slime((0, 0), self.enemyEntityModel),
                          'dancing': Sorceror((0, 0), self.enemyEntityModel, self.enemyEntityModel.current_health),
                          'crystal': Crystal((0, 0), self.enemyEntityModel)}
            self.enemy_attack = self.funcs.get(z, self.non_existent_file())
            self.enemy_sprites.add(self.enemy_attack)

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

    def scene_transitor(self, dict_state):
        pygame.display.flip()
        fade_in_upper = button_transitions.FadeTransition(self.screen)
        fade_in_upper.black_out()
        st_menu = ScreenMenu()
        st_menu.executioner(True, dict_state, self.screen)

    def UnityExecutor(self):
        raise NotImplemented


class SongExecutor(SongComponent):
    def __init__(self, screen, song_file):
        super().__init__(screen, song_file)

    def UnityExecutor(self):
        self.loading_players()
        self.loading_enemies()

        spawner = Spawner()

        # Creating the sprites and groups
        # now we will create a map by making a txt file
        startTime = time.time()
        progressBar = ProgressBar(self.screen, 100, 100, 500, 40,
                                  lambda: (time.time() - startTime) / self.counter_final,
                                  curved=False)
        progressBar.draw()

        imagery = ImageryGroundExecution(0, "Jungle", 5, [(1280, 256), (844, 475)], self.screen, 0)

        mixer.init()
        list_enemies = self.enemy_sprites.sprites()
        map_rect = self.load(self.song_file, spawner, list_enemies)

        # list_of_sprites[0] = self.sprite_group_list[0].sprites()
        # list_of_sprites[1] = self.sprite_group_list[1].sprites()
        # list_of_sprites[2] = self.sprite_group_list[2].sprites()
        # list_crystal = self.sprite_group_list[3].sprites()

        # list_of_sprites = []
        # for spr in range(len(self.sprite_group_list)):
        #     list_of_sprites.append(self.sprite_group_list[spr].sprites())

        list_of_sprites = [self.sprite_group_list[spr].sprites() for spr in range(len(self.sprite_group_list))]

        while True:
            self.clock.tick(60)  # limit movement screen

            imagery.loop_executor()

            self.sprite_group_list[0].update()  # moving sprites
            self.sprite_group_list[1].update()  # attacking sprites
            self.sprite_group_list[2].update()
            self.player.update_health(self.screen)

            # self.player.get_damage(200)

            for i in range(-3, 0):
                if list_of_sprites[1][i].attack_animation:
                    self.player.get_health(200)
                    self.sprite_group_list[0].remove(list_of_sprites[1][i])
                    self.sprite_group_list[0].add(list_of_sprites[0][i])
                    list_of_sprites[1][i].current_sprite = 0
                    list_of_sprites[1][i].attack_stance = not list_of_sprites[1][i].attack_stance
                    list_of_sprites[1][i].attack_animation = not list_of_sprites[1][i].attack_animation
                if list_of_sprites[2][i].attack_animation:
                    self.sprite_group_list[0].remove(list_of_sprites[2][i])
                    self.sprite_group_list[0].add(list_of_sprites[0][i])
                    list_of_sprites[2][i].current_sprite = 0
                    list_of_sprites[2][i].attack_stance = not list_of_sprites[2][i].attack_stance
                    list_of_sprites[2][i].attack_animation = not list_of_sprites[2][i].attack_animation

            for rect, enemy in zip(map_rect[0], map_rect[1]):
                pygame.draw.rect(self.screen, (200, 0, 0), rect)
                self.screen.blit(enemy.image, rect)

                enemy.text_printer(25, f"{int(enemy.target_health / 200) + 1}", (222, 109, 11), rect, self.screen)
                # counters to stronger enemies
                enemy.update()
                rect.x -= 5
                for key in keys:
                    if key.rect.colliderect(rect) and not key.handled:  # not for actually skill
                        enemy.get_damage(200)
                        if enemy.target_health > 0:
                            rect.x += 100
                        else:
                            map_rect[0].remove(rect)
                            map_rect[1].remove(enemy)

                        # Transition(self._menu, self._options)
                        sound_effecting = pygame.mixer.Sound("assets/sound_effects/attack sound effect.wav")
                        key_list = [pygame.K_a, pygame.K_s, pygame.K_d]
                        for i in range(-3, 0):
                            if key.key == key_list[i]:
                                self.sprite_group_list[0].remove(list_of_sprites[0][i])
                                self.sprite_group_list[0].add(list_of_sprites[1][i])
                                list_of_sprites[1][i].current_sprite = 0
                                list_of_sprites[1][i].attack_stance = True
                        pygame.mixer.Sound.play(sound_effecting)
                        key.handled = True
                for key in keys_damage:
                    if key.rect.colliderect(rect) and key.handled:
                        self.player.get_damage(200)
                        map_rect[0].remove(rect)
                        map_rect[1].remove(enemy)

                        sound_effecting = pygame.mixer.Sound("assets/sound_effects/damage sound effect.wav")
                        key_list = [pygame.K_a, pygame.K_s, pygame.K_d]
                        for i in range(-3, 0):
                            if key.key == key_list[i]:
                                self.sprite_group_list[0].remove(list_of_sprites[0][i])
                                self.sprite_group_list[0].add(list_of_sprites[2][i])
                                list_of_sprites[2][i].current_sprite = 0
                                list_of_sprites[2][i].attack_stance = True
                        pygame.mixer.Sound.play(sound_effecting)

            self.sprite_group_list[0].draw(self.screen)

            if imagery.counter == self.counter_final:
                self.scene_transitor(button_transitions.Globals.mapping_buttons_victory_state)
            if self.player.current_health == 0:
                self.scene_transitor(button_transitions.Globals.mapping_buttons_losing_state)

            # now we will loop through the keys and handle the events
            self.key_and_loop_handler(keys, keys_damage)

            pygame.display.flip()
