import pygame


def background(screen, clock):

    FPS = 60

    SCREEN_HEIGHT = 720

    ground_image = pygame.image.load("ground.png").convert_alpha()

    ground_width = ground_image.get_width()
    ground_height = ground_image.get_height()

    bg = pygame.image.load("plx-5.png").convert()

    # define game variables
    scroll = 0

    bg_images = []
    for i in range(1, 6):
        bg_image = pygame.image.load(f"plx-{i}.png").convert_alpha()
        bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()

    # game loop
    # run = True
    # while run:
    #
    #     clock.tick(FPS)
    #
    #     # draw world
    #     for x in range(150):
    #         speed = 1
    #         for i in bg_images:
    #             # printing ground tile
    #             screen.blit(ground_image, ((x * ground_width) - scroll * 2.5, SCREEN_HEIGHT - ground_height))
    #
    #             # printing background
    #             screen.blit(i, ((x * bg_width) - scroll * speed, 0))
    #             speed += 0.8
    #
    #     # scroll background
    #     scroll += 2
