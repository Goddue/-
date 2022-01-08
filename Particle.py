import pygame


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    def __init__(self, pos, dx, dy, fire, *group):
        super().__init__(*group)
        self.current = 0
        self.fire = fire
        self.image = fire[self.current]
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [0, 0]
        # и свои координаты
        self.rect.x, self.rect.y = pos
        self.gravity = 0
        self.tick = 0

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        self.tick += 1
        if self.tick % 20 == 0 and self.current < len(self.fire) - 1:
            self.current += 1
            self.image = self.fire[self.current]
        if self.tick >= 100:
            self.kill()
