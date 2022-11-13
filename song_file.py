import pygame
from pygame import mixer

from keys import keys


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
                key_pressers.move_ip(650, 350)
            elif data[y][x] == '=':
                key_pressers = pygame.Rect(x * 100 + 50, y * 100, 50, 25)
                key_pressers2 = pygame.Rect(x * 100 - 50, y * 100, 50, 25)
                rects.append(key_pressers)
                rects.append(key_pressers2)
                print(key_pressers)
                key_pressers.move_ip(550, 350)
                key_pressers2.move_ip(550, 350)
    return rects


def song(screen):
    mixer.init()

    clock = pygame.time.Clock()

    # Creating the sprites and groups

    # now we will create a map by making a txt file
    map_rect = load("rythm test")

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))

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
        clock.tick(60)
