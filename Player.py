import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, leng, *group):
        super().__init__(*group)
        self.image = image
        self.leng = 32
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            leng * pos_x + 16, leng * pos_y + 16)

    def move(self, x, y, lmove):
        if x != 0:
            lmove = x, lmove[1]
        if y != 0:
            lmove = lmove[0], y
        print(lmove)
        self.rect = self.image.get_rect().move(self.pos[0] * self.leng * 2 + (32 * x) + 16 * lmove[0] + 16,
                                               self.pos[1] * self.leng * 2 + (32 * y) + 16 * lmove[1] + 16)
        self.pos = self.pos[0] + x * 0.5, self.pos[1] + y * 0.5
