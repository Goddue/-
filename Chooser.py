from Tile import Tile


class Chooser(Tile):
    def __init__(self, tile_image, pos_x, pos_y, levels, *group):
        super().__init__(tile_image, pos_x, pos_y, *group)
        self.level = levels[0]
        self.save = levels[1]
        self.image = tile_image[int(levels[0][5])]
