import pygame


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    def __init__(self, pos, fire, *group):
        super().__init__(*group)
        self.current = 0
        self.fire = fire
        self.image = fire[self.current]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.gravity = 0
        self.tick = 0

    def update(self):
        self.tick += 1
        if self.tick % 16 == 0 and self.current < len(self.fire) - 1:
            self.current += 1
            self.image = self.fire[self.current]
        if self.tick >= 64:
            self.kill()
