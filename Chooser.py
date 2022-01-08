from Tile import Tile


class Chooser(Tile):
    def __init__(self, tile_image, pos_x, pos_y, level, *group):
        super().__init__(tile_image, pos_x, pos_y, *group)
        self.level = level
        self.image = tile_image[int(level[5])]
