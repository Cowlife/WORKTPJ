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
        start_pos_attacks = [(26, 89), (0, 70), (0, 79)]
        moving_sprites = sprite.Group()
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
        self.start_pos_attacks = start_pos_attacks
        self.moving_sprites = moving_sprites
        self.counter_final = counter_final

    def progressing(self, screen):  # 0.1
        startTime = time.time()
        progressBar = ProgressBar(screen, 100, 100, 500, 40, lambda: (time.time() - startTime) / self.counter_final, curved=True)
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
                    key_pressers = pygame.Rect((x * 50) + 650, (y * 100) + 400, 50, 25)
                    rects.append(key_pressers)
                elif data[y][x] == '=':  # starting rythm
                    key_pressers = pygame.Rect(x * 100, y * 100, 50, 25)
                    key_pressers2 = pygame.Rect(x * 100 + 50, y * 100, 50, 25)
                    key_pressers3 = pygame.Rect(x * 100 + 100, y * 100, 50, 25)
                    key_pressers4 = pygame.Rect(x * 100 + 130, y * 100, 50, 25)
                    rects.append(key_pressers)
                    rects.append(key_pressers2)
                    rects.append(key_pressers3)
                    rects.append(key_pressers4)
                    key_pressers.move_ip(490, 400)
                    key_pressers2.move_ip(490, 400)
                    key_pressers3.move_ip(490, 400)
                    key_pressers4.move_ip(490, 400)
                elif data[y][x] == 'l':
                    key_pressers = pygame.Rect(x * 100 + 20, y * 100, 50, 25)
                    rects.append(key_pressers)
                    key_pressers.move_ip(650, 400)
                elif data[y][x] == 't':  # twice
                    key_pressers = pygame.Rect(x * 100 + 50, y * 100, 50, 25)
                    key_pressers2 = pygame.Rect(x * 100 + 110, y * 100, 50, 25)
                    rects.append(key_pressers)
                    rects.append(key_pressers2)
                    key_pressers.move_ip(600, 400)
                    key_pressers2.move_ip(600, 400)

        return rects

    def player_drawer(self):
        personImageEntityModel = ImageEntityModel(False, image.load('assets/sprites_player/Bowser.png'))
        personEntityModel = EntityModel(personImageEntityModel, (16, 1), (1344, 70))
        player = Entity((50, 400), personEntityModel)
        personEntityModelAttack = EntityModel(personImageEntityModel, (9, 1), (999, 60), (26, 89))
        player_attack = Entity((50, 400), personEntityModelAttack)
        #
        personImageEntityModel2 = ImageEntityModel(False, image.load('assets/sprites_player/Mario.png'))
        personEntityModel2 = EntityModel(personImageEntityModel2, (12, 1), (1008, 58))
        player2 = Entity((50, 500), personEntityModel2)
        personEntityModelAttack2 = EntityModel(personImageEntityModel2, (4, 1), (448, 75), (0, 70))
        player2_attack = Entity((50, 500), personEntityModelAttack2)

        personImageEntityModel3 = ImageEntityModel(False, image.load('assets/sprites_player/Luigi.png'))
        personEntityModel3 = EntityModel(personImageEntityModel3, (12, 1), (1068, 75))
        player3 = Entity((50, 600), personEntityModel3)
        personEntityModelAttack3 = EntityModel(personImageEntityModel3, (4, 1), (444, 75), (0, 79))
        player3_attack = Entity((50, 600), personEntityModelAttack3)

        enemyImageEntityModel = ImageEntityModel(False, image.load('assets/sprites_enemy/slime.png'), True)
        enemyEntityModel = EntityModel(enemyImageEntityModel, (2, 1), (90, 45))
        enemy_attack = Entity((400, 400), enemyEntityModel)

        self.moving_sprites.add(player, player2, player3)
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
        while True:
            self.clock.tick(60)  # limit movement screen

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == timer_event:
                    self.counter += 1
                    print(self.counter)
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

            circle_radius_start = 160

            pygame_widgets.update(event)
            text_rect = text.get_rect()
            self.screen.blit(text, text_rect)

            player.move_sprite(0.5)
            player_attack.move_sprite(0.8)
            player2.move_sprite(0.5)
            player2_attack.move_sprite(0.5)
            player3.move_sprite(0.5)
            player3_attack.move_sprite(0.5)

            if player_attack.attack_animation:
                self.moving_sprites.remove(player_attack)
                self.moving_sprites.add(player)
                player_attack.current_sprite = 0
                player_attack.attack_stance = not player_attack.attack_stance
                player_attack.attack_animation = not player_attack.attack_animation
            if player2_attack.attack_animation:
                self.moving_sprites.remove(player2_attack)
                self.moving_sprites.add(player2)
                player2_attack.current_sprite = 0
                player2_attack.attack_stance = not player2_attack.attack_stance
                player2_attack.attack_animation = not player2_attack.attack_animation
            if player3_attack.attack_animation:
                self.moving_sprites.remove(player3_attack)
                self.moving_sprites.add(player3)
                player3_attack.current_sprite = 0
                player3_attack.attack_stance = not player3_attack.attack_stance
                player3_attack.attack_animation = not player3_attack.attack_animation

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
            for rect in map_rect:
                pygame.draw.rect(self.screen, (200, 0, 0), rect)
                pygame.draw.circle(self.screen, (0, 255, 0), rect.center, circle_radius_start, 2)
                self.screen.blit(enemy_attack.image, rect)
                enemy_attack.move_sprite(0.5)
                rect.x -= 5
                for key in keys:
                    if key.rect.colliderect(rect) and key.handled:  # not for actually skill
                        map_rect.remove(rect)
                        if key.key == pygame.K_a:
                            self.moving_sprites.remove(player)
                            self.moving_sprites.add(player_attack)
                            player_attack.current_sprite = 0
                            player_attack.attack_stance = True
                            sound_effecting = pygame.mixer.Sound("assets/sound_effects/attack sound effect.wav")
                        if key.key == pygame.K_s:
                            self.moving_sprites.remove(player2)
                            self.moving_sprites.add(player2_attack)
                            player2_attack.current_sprite = 0
                            player2_attack.attack_stance = True
                            sound_effecting = pygame.mixer.Sound("assets/sound_effects/attack sound effect.wav")
                        if key.key == pygame.K_d:
                            self.moving_sprites.remove(player3)
                            self.moving_sprites.add(player3_attack)
                            player3_attack.current_sprite = 0
                            player3_attack.attack_stance = True
                            sound_effecting = pygame.mixer.Sound("assets/sound_effects/attack sound effect.wav")
                        pygame.mixer.Sound.play(sound_effecting)
                        key.handled = True
            self.moving_sprites.draw(self.screen)
            if self.counter == self.counter_final:
                pygame.display.flip()
                # global_functions.fade_in()
                st_menu = ScreenMenu()
                st_menu.executioner(True, button_transitions.Globals.mapping_buttons_overlay, self.screen)

            pygame.display.flip()

    def UnityExecutor(self):
        raise NotImplemented


class SongExecutor(SongNote):
    def __init__(self, screen, song_file):
        super().__init__(screen, song_file)

    def UnityExecutor(self):
        self.player_drawer()

