import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, speed, *group):
        super().__init__(*group)
        self.image_down = image[0]
        self.image_up = image[1]
        self.image_left = image[2]
        self.image_right = image[3]
        self.image = self.image_down
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.speed = speed

    def move(self, x, y):
        self.rect = self.image.get_rect().move(self.pos[0] + x * self.speed,
                                               self.pos[1] + y * self.speed)
        self.pos = self.pos[0] + x * self.speed, self.pos[1] + y * self.speed

    def rotate(self, rotation):
        if rotation == (0, -1):
            self.image = self.image_up
        elif rotation == (0, 1):
            self.image = self.image_down
        elif rotation == (1, 0):
            self.image = self.image_right
        elif rotation == (-1, 0):
            self.image = self.image_left
