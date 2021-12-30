import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, leng, *group):
        super().__init__(*group)
        self.image = image
        self.leng = leng
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            leng * pos_x + 10, leng * pos_y + 15)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(x * self.leng + 10, y * self.leng + 15)
        self.pos = x, y
