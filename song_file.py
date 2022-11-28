import pygame
import pygame_widgets
from pygame import mixer, image

import button_transitions
import global_functions
import scenes.menu
from keys import keys
from player import Player


def load(map):
    rects = []
    mixer.music.load("musics/" + map + ".mp3")
    mixer.music.play()
    f = open("charts/" + map + ".txt", 'r')
    data = f.readlines()
    for y in range(len(data)):
        for x in range(len(data[y])):

            if data[y][x] == '0':
                key_pressers = pygame.Rect(x * 100, y * 100, 50, 25)
                rects.append(key_pressers)
                print(key_pressers)
                key_pressers.move_ip(650, 400)
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


def song(screen, bg):
    mixer.init()
    counter = 0

    clock = pygame.time.Clock()
    # Creating the sprites and groups
    # now we will create a map by making a txt file
    map_rect = load("rythm test")

    font = pygame.font.Font("assets/font.ttf", 100)
    text = font.render(str(counter), True, (222, 109, 11))

    timer_event = pygame.USEREVENT + 1
    print(timer_event)
    pygame.time.set_timer(timer_event, 1000)

    global_functions.progressing(screen)

    SCREEN_HEIGHT = 720

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

    person = image.load('sprites_player/bowser_test.png')
    moving_sprites = pygame.sprite.Group()
    player = Player((50, 400), False, person, (1, 16), (1344, 70), (0, 0))
    player_attack = Player((50, 400), False, person, (1, 9), (999, 60), (26, 89))
    moving_sprites.add(player)

    while True:
        clock.tick(60)

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
                screen.blit(ground_image, ((x * ground_width) - scroll * 2.5, SCREEN_HEIGHT - ground_height))
                # printing background
                screen.blit(i, ((x * bg_width) - scroll * speed, 0))
                speed += 0.8

        # scroll background
        scroll += 2
        pygame_widgets.update(event)
        text_rect = text.get_rect()
        screen.blit(text, text_rect)

        player.move(0.5)
        player_attack.move(0.5)
        if player_attack.attack_animation:
            moving_sprites.remove(player_attack)
            moving_sprites.add(player)
            player_attack.current_sprite = 0
            player_attack.attack_stance = not player_attack.attack_stance
            player_attack.attack_animation = not player_attack.attack_animation
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
            rect.x -= 5
            for key in keys:
                if key.rect.colliderect(rect) and key.handled:
                    map_rect.remove(rect)
                    moving_sprites.remove(player)
                    moving_sprites.add(player_attack)
                    player_attack.current_sprite = 0
                    player_attack.attack_stance = True
                    sound_effecting = pygame.mixer.Sound("sound_effects/attack sound effect.wav")
                    pygame.mixer.Sound.play(sound_effecting)
                    key.handled = True
                    break

        if counter == 10:
            pygame.display.flip()
            global_functions.fade_in()
            scenes.menu.transitory_menu(True, button_transitions.Globals.mapping_buttons_overlay)

        pygame.display.flip()
