import pygame


class Key:
    def __init__(self, x, y, color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x, self.y, 60, 40)
        self.handled = False


# now we will make a list of keys

keys = [
    Key(150, 400, (255, 0, 0), (220, 0, 0), pygame.K_a),
    Key(150, 500, (0, 255, 0), (0, 220, 0), pygame.K_s),
    Key(150, 600, (0, 0, 255), (0, 0, 220), pygame.K_d),
    # crystal frames
]

keys_damage = [
    Key(50, 400, (255, 0, 0), (220, 0, 0), pygame.K_a),
    Key(50, 500, (0, 255, 0), (0, 220, 0), pygame.K_s),
    Key(50, 600, (0, 0, 255), (0, 0, 220), pygame.K_d),
    # crystal frames
]