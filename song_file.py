import sys

import pygame
import pygame_widgets
from pygame import mixer

from button import Button
from keys import keys
from global_functions import progressing, fade_in, get_font
from menu_load import HMenu


def main_menu(screen, bg):
    while True:
        screen.blit(bg, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        h_menu = HMenu("Play Rect", 640, 250)
        h_menu.create_buttons()

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(440, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Red")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(440, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="Red")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(440, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Red")

        # Draw Title
        screen.blit(MENU_TEXT, MENU_RECT)

        # hover effect
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # button actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    fade_in(1280, 720, screen)
                    play(screen)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    fade_in(1280, 720, screen)
                    options(screen, bg)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # to set-up the screen
        pygame.display.update()


def play(SCREEN):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY SCREEN.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK2 = Button(image=None, pos=(640, 360),
                            text_input="TEST SONG", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_BACK2.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK2.update(SCREEN)

        for button in [PLAY_BACK2]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    BG = pygame.image.load("assets/Background.png")
                    main_menu(SCREEN, BG)
                if PLAY_BACK2.checkForInput(PLAY_MOUSE_POS):
                    BG = pygame.image.load("assets/Background.png")
                    fade_in(1280, 720, SCREEN)
                    song(SCREEN, BG, 0)

        pygame.display.update()


def options(SCREEN, BG):
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS SCREEN.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(SCREEN, BG)

        pygame.display.update()


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


def song(screen, bg, counter):
    mixer.init()

    clock = pygame.time.Clock()
    # Creating the sprites and groups
    # now we will create a map by making a txt file
    map_rect = load("rythm test")

    font = pygame.font.Font("assets/font.ttf", 100)
    text = font.render(str(counter), True, (222, 109, 11))

    timer_event = pygame.USEREVENT + 1
    print(timer_event)
    pygame.time.set_timer(timer_event, 1000)

    progressing(screen)

    SCREEN_HEIGHT = 720

    ground_image = pygame.image.load("ground.png").convert_alpha()
    ground_image = pygame.transform.scale(ground_image, (1280, 256))
    ground_width = ground_image.get_width()
    ground_height = ground_image.get_height()

    # define game variables
    scroll = 0

    bg_images = []
    for i in range(1, 6):
        bg_image = pygame.image.load(f"plx-{i}.png").convert_alpha()
        bg_image = pygame.transform.scale(bg_image, (844, 475))
        bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()

    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == timer_event:
                counter += 1
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
                    sound_effecting = pygame.mixer.Sound("sound_effects/attack sound effect.wav")
                    pygame.mixer.Sound.play(sound_effecting)
                    key.handled = True
                    break

        if counter == 10:
            pygame_widgets.update(event)
            pygame.display.update()
            fade_in(1280, 720, screen)
            bg_rect = bg.get_rect()
            screen.blit(bg, bg_rect)
            font = pygame.font.Font("assets/font.ttf", 64)
            text_surface = font.render("Level Complete!", True, "white")
            text_rect = text_surface.get_rect()
            text_rect.midtop = (640, SCREEN_HEIGHT / 4)
            screen.blit(text_surface, text_rect)

            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            fade_in(1280, 720, screen)
                            BG = pygame.image.load("assets/Background.png")
                            pygame.display.flip()
                            main_menu(screen, BG)

        pygame.display.update()
