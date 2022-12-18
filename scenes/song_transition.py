import time
import pygame
import pygame_widgets
from pygame import sprite, image, mixer
from pygame.time import Clock
from pygame_widgets.progressbar import ProgressBar

import button_transitions
from keys import keys
from player import ImageEntityModel, EntityModel, Entity, Spawner, Slime, Sorceror
from scenes.menu import ScreenMenu
from scenes.parallax_storage import ImageryGroundExecution
from scenes.states import FSM, Transition, Alive, Options, State


class SongComponent:
    def __init__(self, screen, song_file):

        clock = Clock()
        counter = 0
        image_loader = ['Bowser', 'Mario', 'Luigi']
        frames_in_x_y_model = [(16, 1), (12, 1), (12, 1)]
        width_model = [(1344, 70), (1008, 58), (1068, 75)]
        pos_loader = [400, 500, 600]
        frames_in_x_y_attack = [(9, 1), (4, 1), (4, 1)]
        width_attacks = [(999, 60), (448, 75), (444, 75)]
        start_pos_model = [(0, 0), (0, 0), (0, 0)]
        start_pos_attacks = [(26, 89), (0, 70), (0, 79)]
        moving_sprites = sprite.Group()
        attacking_sprites = sprite.Group()
        counter_final = 6

        self.clock = clock
        self.screen = screen
        self.song_file = song_file
        self.counter = counter
        self.image_loader = image_loader
        self.frames_in_x_y_model = frames_in_x_y_model
        self.width_model = width_model
        self.pos_loader = pos_loader
        self.frames_in_x_y_attack = frames_in_x_y_attack
        self.width_attacks = width_attacks
        self.start_pos_model = start_pos_model
        self.start_pos_attacks = start_pos_attacks
        self.moving_sprites = moving_sprites
        self.attacking_sprites = attacking_sprites
        self.counter_final = counter_final

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

    def load(self, map, spawner):
        rects, entity_list = [], []
        mixer.music.load("musics/" + map + ".mp3")
        mixer.music.play()
        with open(f"charts/{map}.txt", 'r') as f:
            data = f.readlines()
        enemyImageEntityModel = ImageEntityModel(False, image.load('assets/sprites_enemy/slime.png'), True)
        enemyEntityModel = EntityModel(enemyImageEntityModel, (2, 1), (90, 45))
        self.enemy_attack = Slime((400, 400), enemyEntityModel)
        enemyImageEntityModel2 = ImageEntityModel(True, image.load('assets/sprites_enemy/dancing.png'), True)
        enemyEntityModel2 = EntityModel(enemyImageEntityModel2, (10, 8), (880, 1280))
        self.enemy_attack2 = Sorceror((400, 400), enemyEntityModel2)
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] == '0':
                    key_pressers = pygame.Rect((x * 50) + 650, (y * 100) + 400, 25, 25)
                    rects.append(key_pressers)
                    spawner_instance = spawner.spawn_Entity(self.enemy_attack)
                    entity_list.append(spawner_instance)
                elif data[y][x] == '1':
                    key_pressers = pygame.Rect((x * 50) + 650, (y * 100) + 400, 25, 25)
                    rects.append(key_pressers)
                    spawner_instance = spawner.spawn_Entity(self.enemy_attack2)
                    entity_list.append(spawner_instance)
        return rects, entity_list

    def entity_loader(self):
        for i in self.image_loader:
            ind = self.image_loader.index(i)
            personImageEntityModel = ImageEntityModel(False, image.load(f'assets/sprites_player/{i}.png'))
            personEntityModel = EntityModel(personImageEntityModel, self.frames_in_x_y_model[ind],
                                            self.width_model[ind], self.start_pos_model[ind])
            self.player = Entity((50, self.pos_loader[ind]), personEntityModel)
            personEntityModelAttack = EntityModel(personImageEntityModel, self.frames_in_x_y_attack[ind],
                                                  self.width_attacks[ind], self.start_pos_attacks[ind])
            self.player_attack = Entity((50, self.pos_loader[ind]), personEntityModelAttack)
            self.moving_sprites.add(self.player)
            self.attacking_sprites.add(self.player_attack)

    def key_and_loop_handler(self):
        k = pygame.key.get_pressed()
        for key in keys:
            if k[key.key]:
                pygame.draw.rect(self.screen, key.color1, key.rect)
                key.handled = False
            if not k[key.key]:
                pygame.draw.rect(self.screen, key.color2, key.rect)
                key.handled = True
            # now when we press our keys they will change color

    def scene_transitor(self, counter):
        if counter == self.counter_final:
            pygame.display.flip()
            fade_in_upper = button_transitions.FadeTransition(self.screen)
            fade_in_upper.black_out()
            st_menu = ScreenMenu()
            st_menu.executioner(True, button_transitions.Globals.mapping_buttons_overlay, self.screen)

    def UnityExecutor(self):
        raise NotImplemented


class SongExecutor(SongComponent):
    def __init__(self, screen, song_file):
        super().__init__(screen, song_file)

    def UnityExecutor(self):
        self.entity_loader()

        spawner = Spawner()

        # Creating the sprites and groups
        # now we will create a map by making a txt file
        startTime = time.time()
        progressBar = ProgressBar(self.screen, 100, 100, 500, 40, lambda: (time.time() - startTime) / self.counter_final,
                                  curved=True)

        imagery = ImageryGroundExecution(0, "Jungle", 5, [(1280, 256), (844, 475)], self.screen, 0)

        mixer.init()
        map_rect = self.load(self.song_file, spawner)

        list_models = self.moving_sprites.sprites()
        list_attacks = self.attacking_sprites.sprites()
        while True:
            self.clock.tick(60)  # limit movement screen

            imagery.loop_executor()

            self.moving_sprites.update()
            self.attacking_sprites.update()
            self.player.update_health(self.screen)



            #self.player.get_damage(200)

            for i in range(-3, 0):
                if list_attacks[i].attack_animation:
                    self.player.get_health(200)
                    self.moving_sprites.remove(list_attacks[i])
                    self.moving_sprites.add(list_models[i])
                    list_attacks[i].current_sprite = 0
                    list_attacks[i].attack_stance = not list_attacks[i].attack_stance
                    list_attacks[i].attack_animation = not list_attacks[i].attack_animation

            for rect, test in zip(map_rect[0], map_rect[1]):
                # pygame.draw.rect(self.screen, (200, 0, 0), rect)
                self.screen.blit(test.image, rect)
                test.update()
                rect.x -= 5
                for key in keys:
                    if key.rect.colliderect(rect) and key.handled:  # not for actually skill
                        map_rect[0].remove(rect)
                        map_rect[1].remove(test)
                        # Transition(self._menu, self._options)
                        sound_effecting = pygame.mixer.Sound("assets/sound_effects/attack sound effect.wav")
                        key_list = [pygame.K_a, pygame.K_s, pygame.K_d]
                        for i in range(-3, 0):
                            if key.key == key_list[i]:
                                self.moving_sprites.remove(list_models[i])
                                self.moving_sprites.add(list_attacks[i])
                                list_attacks[i].current_sprite = 0
                                list_attacks[i].attack_stance = True
                        pygame.mixer.Sound.play(sound_effecting)
                        key.handled = True

            self.moving_sprites.draw(self.screen)

            self.scene_transitor(imagery.counter)

            # now we will loop through the keys and handle the events
            self.key_and_loop_handler()

            pygame.display.flip()
