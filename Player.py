import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, speed, *group):
        super().__init__(*group)
        self.images = image
        self.speed = speed
        self.frames = []
        self.cut_sheet(image[0], 5, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.tick = 4

    def cut_sheet(self, sheet, columns, rows):
        print(sheet.get_width(), sheet.get_height())
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        print(self.rect.w, self.rect.h)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.tick += 1
        if self.tick >= 4:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.tick = 0

    def move(self, x, y):
        self.rect = self.image.get_rect().move(self.pos[0] + x * self.speed,
                                               self.pos[1] + y * self.speed)
        self.pos = self.pos[0] + x * self.speed, self.pos[1] + y * self.speed
        if self.cur_frame != 4:
            self.update()

    def rotate(self, move):
        if move == (0, -1):
            self.frames = []
            self.cut_sheet(self.images[1], 5, 1)
            self.cur_frame = 0
        elif move == (0, 1):
            self.frames = []
            self.cut_sheet(self.images[0], 5, 1)
            self.cur_frame = 0

