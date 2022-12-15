import time
import pygame
import pygame_widgets
from pygame import sprite, image, mixer
from pygame.time import Clock
from pygame_widgets.progressbar import ProgressBar

import button_transitions
from keys import keys
from player import ImageEntityModel, EntityModel, Entity
from scenes.menu import ScreenMenu


class SongNote:
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
        counter_final = 100

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

    def progressing(self, screen):  # 0.1
        startTime = time.time()
        progressBar = ProgressBar(screen, 100, 100, 500, 40, lambda: (time.time() - startTime) / self.counter_final,
                                  curved=True)
        # /10 seconds
        return progressBar

    def load(self, map):
        rects = []
        mixer.music.load("musics/" + map + ".mp3")
        mixer.music.play()
        with open(f"charts/{map}.txt", 'r') as f:
            data = f.readlines()
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] == '0':
                    key_pressers = pygame.Rect((x * 50) + 650, (y * 100) + 400, 25, 25)
                    rects.append(key_pressers)
        return rects

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

    def player_drawer(self):

        self.entity_loader()

        enemyImageEntityModel = ImageEntityModel(False, image.load('assets/sprites_enemy/slime.png'), True)
        enemyEntityModel = EntityModel(enemyImageEntityModel, (2, 1), (90, 45))
        enemy_attack = Entity((400, 400), enemyEntityModel)

        # Creating the sprites and groups
        # now we will create a map by making a txt file

        font = pygame.font.Font("assets/fonts/font.ttf", 100)
        text = font.render(str(self.counter), True, (222, 109, 11))

        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event, 1000)

        self.progressing(self.screen)

        ground_image = pygame.image.load("scenario/ground.png").convert_alpha()
        ground_image = pygame.transform.scale(ground_image, (1280, 256))
        ground_width = ground_image.get_width()
        ground_height = ground_image.get_height()

        # define game variables
        scroll = 0

        bg_images = []
        for i in range(1, 6):
            bg_image = pygame.image.load(f"scenario/plx-{i}.png").convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (844, 475))
            bg_images.append(bg_image)
        bg_width = bg_images[0].get_width()

        mixer.init()
        map_rect = self.load(self.song_file)

        list_models = self.moving_sprites.sprites()
        list_attacks = self.attacking_sprites.sprites()

        while True:
            self.clock.tick(60)  # limit movement screen

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == timer_event:
                    self.counter += 1
                    text = font.render(str(self.counter), True, (222, 109, 11))

            self.screen.fill((0, 0, 0))

            # draw world
            for x in range(150):
                speed = 1
                for i in bg_images:
                    # printing ground tile
                    self.screen.blit(ground_image,
                                     ((x * ground_width) - scroll * 2.5, 720 - ground_height))  # screen height
                    # printing background
                    self.screen.blit(i, ((x * bg_width) - scroll * speed, 0))
                    speed += 0.8

            # scroll background
            scroll += 2

            pygame_widgets.update(event)
            text_rect = text.get_rect()
            self.screen.blit(text, text_rect)

            self.moving_sprites.update()
            self.attacking_sprites.update()

            if list_attacks[0].attack_animation:
                self.moving_sprites.remove(list_attacks[-3])
                self.moving_sprites.add(list_models[-3])
                list_attacks[-3].current_sprite = 0
                list_attacks[-3].attack_stance = not list_attacks[-3].attack_stance
                list_attacks[-3].attack_animation = not list_attacks[-3].attack_animation
            if list_attacks[1].attack_animation:
                self.moving_sprites.remove(list_attacks[-2])
                self.moving_sprites.add(list_models[-2])
                list_attacks[-2].current_sprite = 0
                list_attacks[-2].attack_stance = not list_attacks[-2].attack_stance
                list_attacks[-2].attack_animation = not list_attacks[-2].attack_animation
            if list_attacks[-1].attack_animation:
                self.moving_sprites.remove(list_attacks[-1])
                self.moving_sprites.add(list_models[-1])
                list_attacks[-1].current_sprite = 0
                list_attacks[-1].attack_stance = not list_attacks[-1].attack_stance
                list_attacks[-1].attack_animation = not list_attacks[-1].attack_animation

            for rect in map_rect:
                pygame.draw.rect(self.screen, (200, 0, 0), rect)
                self.screen.blit(enemy_attack.image, rect)
                enemy_attack.move_sprite(0.5)
                rect.x -= 5
                for key in keys:
                    if key.rect.colliderect(rect) and key.handled:  # not for actually skill
                        map_rect.remove(rect)
                        sound_effecting = pygame.mixer.Sound("assets/sound_effects/attack sound effect.wav")
                        key_list = [pygame.K_a, pygame.K_s, pygame.K_d]
                        if key.key == key_list[0]:
                            self.moving_sprites.remove(list_models[-3])
                            self.moving_sprites.add(list_attacks[-3])
                            list_attacks[-3].current_sprite = 0
                            list_attacks[-3].attack_stance = True
                        if key.key == key_list[1]:
                            self.moving_sprites.remove(list_models[-2])
                            self.moving_sprites.add(list_attacks[-2])
                            list_attacks[-2].current_sprite = 0
                            list_attacks[-2].attack_stance = True
                            print(list_attacks[1].attack_stance)
                        if key.key == key_list[-1]:
                            self.moving_sprites.remove(list_models[-1])
                            self.moving_sprites.add(list_attacks[-1])
                            list_attacks[-1].current_sprite = 0
                            list_attacks[-1].attack_stance = True

                        pygame.mixer.Sound.play(sound_effecting)
                        key.handled = True

            self.moving_sprites.draw(self.screen)
            if self.counter == self.counter_final:
                pygame.display.flip()
                # global_functions.fade_in()
                st_menu = ScreenMenu()
                st_menu.executioner(True, button_transitions.Globals.mapping_buttons_overlay, self.screen)

            # now we will loop through the keys and handle the events
            k = pygame.key.get_pressed()
            for key in keys:
                if k[key.key]:
                    pygame.draw.rect(self.screen, key.color1, key.rect)
                    key.handled = False
                if not k[key.key]:
                    pygame.draw.rect(self.screen, key.color2, key.rect)
                    key.handled = True
            # now when we press our keys they will change color

            pygame.display.flip()

    def UnityExecutor(self):
        raise NotImplemented


class SongExecutor(SongNote):
    def __init__(self, screen, song_file):
        super().__init__(screen, song_file)

    def UnityExecutor(self):
        self.player_drawer()
