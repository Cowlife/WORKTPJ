import pygame
from pygame import mixer

from keys import keys


def load(map, screen, bg, clock):
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
                key_pressers.move_ip(650, 350)
            elif data[y][x] == '=':  # starting rythm
                key_pressers = pygame.Rect(x * 100, y * 100, 50, 25)
                key_pressers2 = pygame.Rect(x * 100 + 50, y * 100, 50, 25)
                key_pressers3 = pygame.Rect(x * 100 + 100, y * 100, 50, 25)
                key_pressers4 = pygame.Rect(x * 100 + 130, y * 100, 50, 25)
                rects.append(key_pressers)
                rects.append(key_pressers2)
                rects.append(key_pressers3)
                rects.append(key_pressers4)
                print(key_pressers)
                key_pressers.move_ip(490, 350)
                key_pressers2.move_ip(490, 350)
                key_pressers3.move_ip(490, 350)
                key_pressers4.move_ip(490, 350)
            elif data[y][x] == 'l':
                key_pressers = pygame.Rect(x * 100 + 20, y * 100, 50, 25)
                rects.append(key_pressers)
                print(key_pressers)
                key_pressers.move_ip(650, 350)
            elif data[y][x] == 't':  # twice
                key_pressers = pygame.Rect(x * 100 + 50, y * 100, 50, 25)
                key_pressers2 = pygame.Rect(x * 100 + 110, y * 100, 50, 25)
                rects.append(key_pressers)
                rects.append(key_pressers2)
                print(key_pressers)
                key_pressers.move_ip(600, 350)
                key_pressers2.move_ip(600, 350)

    return rects


def song(screen, bg):
    mixer.init()

    clock = pygame.time.Clock()
    # Creating the sprites and groups
    # now we will create a map by making a txt file
    map_rect = load("rythm test", screen, bg, clock)

    font = pygame.font.Font("assets/font.ttf", 100)
    counter = 0
    text = font.render(str(counter), True, (222, 109, 11))

    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == timer_event:
                counter += 1
                text = font.render(str(counter), True, (222, 109, 11))
                if counter == 10:
                    print("Function")
                    # pygame.time.set_timer(timer_event, 0)

        screen.fill((0, 0, 0))
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

        pygame.display.update()

