import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, speed, *group):
        super().__init__(*group)
        self.image = image
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.speed = speed

    def move(self, x, y):
        self.rect = self.image.get_rect().move(self.pos[0] + x * self.speed,
                                               self.pos[1] + y * self.speed)
        self.pos = self.pos[0] + x * self.speed, self.pos[1] + y * self.speed
