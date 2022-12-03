import time

import pygame
import pygame_widgets
from pygame import mixer, image
from pygame.time import Clock
from pygame_widgets.progressbar import ProgressBar
import button_transitions


from keys import keys
from player import Entity
from scenes.menu import ScreenMenu


def progressing(screen):  # 0.1
    startTime = time.time()
    progressBar = ProgressBar(screen, 100, 100, 500, 40, lambda: (time.time() - startTime) / 10, curved=False)
    # /10 seconds
    return progressBar


def load(map):
    rects = []
    mixer.music.load("musics/" + map + ".mp3")
    mixer.music.play()
    f = open("charts/" + map + ".txt", 'r')
    data = f.readlines()
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '0':
                key_pressers = pygame.Rect((x * 100) + 650, (y * 100) + 400, 50, 25)
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


class Song:
    def __init__(self, screen, song_file):
        pass


def song(screen, song_file):
    clock = Clock()
    counter = 0
    person = image.load('sprites_player/Bowser.png')
    person2 = image.load('sprites_player/Mario.png')
    person3 = image.load('sprites_player/Luigi.png')
    entity = image.load('sprites_enemy/slime.png')
    img_with_flip = pygame.transform.flip(entity, True, False)
    test_sprite = image.load('sprites_enemy/dancing.png')
    moving_sprites = pygame.sprite.Group()
    player = Entity((50, 400), False, person, (16, 1), (1344, 70), (0, 0))
    player_attack = Entity((50, 400), False, person, (9, 1), (999, 60), (26, 89))
    player2 = Entity((50, 500), False, person2, (12, 1), (1008, 58), (0, 0))
    player2_attack = Entity((50, 500), False, person2, (4, 1), (448, 75), (0, 70))
    player3 = Entity((50, 600), False, person3, (12, 1), (1068, 75), (0, 0))
    player3_attack = Entity((50, 600), False, person3, (4, 1), (444, 75), (0, 79))
    moving_sprites.add(player, player2, player3)
    enemy_attack = Entity((400, 400), False, img_with_flip, (2, 1), (90, 45), (0, 0))

    # Creating the sprites and groups
    # now we will create a map by making a txt file

    font = pygame.font.Font("assets/font.ttf", 100)
    text = font.render(str(counter), True, (222, 109, 11))

    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)

    progressing(screen)

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
    map_rect = load(song_file)
    while True:
        clock.tick(60)  # limit movement screen

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == timer_event:
                counter += 1
                print(counter)
                text = font.render(str(counter), True, (222, 109, 11))

        screen.fill((0, 0, 0))

        # draw world
        for x in range(150):
            speed = 1
            for i in bg_images:
                # printing ground tile
                screen.blit(ground_image,
                            ((x * ground_width) - scroll * 2.5, 720 - ground_height)) #screen height
                # printing background
                screen.blit(i, ((x * bg_width) - scroll * speed, 0))
                speed += 0.8

        # scroll background
        scroll += 2

        circle_radius_start = 160

        pygame_widgets.update(event)
        text_rect = text.get_rect()
        screen.blit(text, text_rect)

        player.move(0.5)
        player_attack.move(0.8)
        player2.move(0.5)
        player2_attack.move(0.5)
        player3.move(0.5)
        player3_attack.move(0.5)

        if player_attack.attack_animation:
            moving_sprites.remove(player_attack)
            moving_sprites.add(player)
            player_attack.current_sprite = 0
            player_attack.attack_stance = not player_attack.attack_stance
            player_attack.attack_animation = not player_attack.attack_animation
        if player2_attack.attack_animation:
            moving_sprites.remove(player2_attack)
            moving_sprites.add(player2)
            player2_attack.current_sprite = 0
            player2_attack.attack_stance = not player2_attack.attack_stance
            player2_attack.attack_animation = not player2_attack.attack_animation
        if player3_attack.attack_animation:
            moving_sprites.remove(player3_attack)
            moving_sprites.add(player3)
            player3_attack.current_sprite = 0
            player3_attack.attack_stance = not player3_attack.attack_stance
            player3_attack.attack_animation = not player3_attack.attack_animation
        moving_sprites.draw(screen)
        # now we will loop through the keys and handle the events
        k = pygame.key.get_pressed()
        for key in keys:
            if k[key.key]:
                pygame.draw.rect(screen, key.color1, key.rect)
                key.handled = False
            if not k[key.key]:
                pygame.draw.rect(screen, key.color2, key.rect)
                key.handled = True
            # now when we press our keys they will change color
        for rect in map_rect:
            pygame.draw.rect(screen, (200, 0, 0), rect)
            pygame.draw.circle(screen, (0, 255, 0), rect.center, circle_radius_start, 2)
            screen.blit(enemy_attack.image, rect)
            enemy_attack.move(0.5)
            rect.x -= 5
            for key in keys:
                if key.rect.colliderect(rect) and key.handled: # not for actually skill
                    map_rect.remove(rect)
                    if key.key == pygame.K_a:
                        moving_sprites.remove(player)
                        moving_sprites.add(player_attack)
                        player_attack.current_sprite = 0
                        player_attack.attack_stance = True
                        sound_effecting = pygame.mixer.Sound("sound_effects/attack sound effect.wav")
                    if key.key == pygame.K_s:
                        moving_sprites.remove(player2)
                        moving_sprites.add(player2_attack)
                        player2_attack.current_sprite = 0
                        player2_attack.attack_stance = True
                        sound_effecting = pygame.mixer.Sound("sound_effects/attack sound effect.wav")
                    if key.key == pygame.K_d:
                        moving_sprites.remove(player3)
                        moving_sprites.add(player3_attack)
                        player3_attack.current_sprite = 0
                        player3_attack.attack_stance = True
                        sound_effecting = pygame.mixer.Sound("sound_effects/attack sound effect.wav")
                    pygame.mixer.Sound.play(sound_effecting)
                    key.handled = True

        if counter == 10:
            pygame.display.flip()
            # global_functions.fade_in()
            st_menu = ScreenMenu()
            st_menu.executioner(True, button_transitions.Globals.mapping_buttons_overlay)

        pygame.display.flip()
