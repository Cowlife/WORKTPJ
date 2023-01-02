import pygame
import pygame_widgets
from pygame.event import Event

from keys import keys


class ImageryComponent:
    def __init__(self, counter, text_image, layers, images_sizes, screen, scroll):
        self.text_image = text_image
        self.layers = layers
        self.images_sizes = images_sizes
        self.counter = counter
        self.screen = screen
        self.scroll = scroll
        self.font = pygame.font.Font("assets/fonts/font.ttf", 100)
        self.text = self.font.render(str(counter), True, (222, 109, 11))
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        self.bg_images = []

    def image_loader(self, filename, indexor):
        ground_image = pygame.image.load(
            f"scenario/{self.text_image}/{filename}.png").convert_alpha()  # ground and plx-i
        ground_image = pygame.transform.scale(ground_image, self.images_sizes[indexor])
        return ground_image

    def time_loop(self, timer_event, font):
        event = Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == timer_event:
                self.counter += 1
                self.text = font.render(str(self.counter), True, (222, 109, 11))
            if event.type == pygame.KEYDOWN:
                for _key in keys:
                    if event.key == _key.key:
                        pygame.draw.rect(self.screen, _key.color1, _key.rect)
                        _key.handled = not _key.handled

        return self.text, event

    def world_drawer(self, bg_images, bg_width, ground_image, ground_width, ground_height, scroll):
        for x in range(150):  # adding elements
            speed = 1
            for i in bg_images:
                # printing ground tile
                self.screen.blit(ground_image,
                                 ((x * ground_width) - scroll * 2.5, 720 - ground_height))  # screen height
                # printing background
                self.screen.blit(i, ((x * bg_width) - scroll * speed, 0))
                speed += 0.8

    def loop_executor(self):
        raise NotImplemented


class ImageryGroundExecution(ImageryComponent):
    def __init__(self, counter, text_image, layers, images_sizes, screen, scroll):
        super().__init__(counter, text_image, layers, images_sizes, screen, scroll)
        self.ground_image = self.image_loader("ground", 0)
        self.ground_w_h = [self.ground_image.get_width(), self.ground_image.get_height()]
        for i in range(1, layers + 1):
            parallax_background = self.image_loader(f"plx-{i}", 1)
            self.bg_images.append(parallax_background)
        self.bg_width = parallax_background.get_width()

    def loop_executor(self):
        timer_clock = self.time_loop(self.timer_event, self.font)
        self.screen.fill((0, 0, 0))
        self.world_drawer(self.bg_images, self.bg_width, self.ground_image, self.ground_w_h[0], self.ground_w_h[1],
                          self.scroll)
        pygame_widgets.update(timer_clock[1])
        self.screen.blit(timer_clock[0], timer_clock[0].get_rect())
        self.scroll += 2
