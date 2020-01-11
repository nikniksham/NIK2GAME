from MainClasss import *
from pygame import Surface, Rect


class ChunkObject:
    def __init__(self, info, coord):
        if type(info) == tuple:
            self.image = info[0]
            if info[1] is None:
                self.rect = Rect((coord[0], coord[1], self.image.get_size()[0], 30))
            else:
                self.rect = Rect((coord[0] + self.image.get_size()[0] // 2 - info[1], coord[1], info[1] * 2, 30))
        else:
            self.image = info
            self.rect = Rect((coord[0], coord[1], self.image.get_size()[0], 30))

        self.coord = coord[0], coord[1] - int(self.image.get_size()[1] - 30)
        self.types = ['object', 'Image', 'Static']
        self.layer = 0
        self.is_back_ground = False

    def get_rect(self):
        return self.rect

    def set_bg(self, val: bool):
        self.is_back_ground = bool(val)

    def get_is_bg(self):
        return self.is_back_ground

    def set_layer(self, layer):
        self.layer = layer

    def get_layer(self):
        return self.layer

    def get_mask(self):
        return Wonderful(Rect(self.coord, self.image.get_size()))

    def is_type(self, arg):
        return arg in self.types

    def get_image(self):
        return self.image

    def get_coord(self):
        return self.coord

    def get_coord_2(self):
        return self.rect.x, self.rect.y

    def get_coord_3(self):
        return self.coord[0] % 480, self.coord[1] % 480


class Chunk(MainObject):
    def __init__(self, coord):
        super().__init__()
        self.add_type('Chunk')
        self.surface = Surface((480, 480))
        self.bg_layer = Surface((480, 480))
        self.top_layer = Surface((480, 480))
        self.rect = Rect(coord, ((480, 480)))
        self.objects = []

    def add_object(self, info, layer, coord):
        block = ChunkObject(info, coord)
        if layer == 1:
            self.objects.append(block)
        else:
            self.surface.blit(block.get_image(), block.get_coord_3())

    def clear_chunk(self):
        self.objects = []

    def get_objects(self):
        return self.objects[:]

    def get_image(self):
        return self.surface

    def get_coord(self):
        return self.rect.x, self.rect.y


class MainChunk(MainObject):
    def __init__(self, size):
        super().__init__()
        self.add_type('MainChunk')
        self.map = [[]]
        self.size_chunk = (480, 480)
        self.size = size

    def add_chunk(self, chunk):
        self.map[-1].append(chunk)

    def next_string(self):
        self.map.append([])

    def set_clear_chunk(self, rect):
        coord = rect.x, rect.y
        size = rect.width, rect.height
        for y in range(coord[1] // self.size_chunk[1], (coord[1] + size[1]) // self.size_chunk[1] + 1):
            for x in range(coord[0] // self.size_chunk[0], (coord[0] + size[0]) // self.size_chunk[0] + 1):
                if 0 <= y < self.size[1] and 0 <= x < self.size[0]:
                    self.map[y][x].clear_chunk()

    def get_object(self, rect):
        res = []
        coord = rect.x, rect.y
        size = rect.width, rect.height
        for y in range(coord[1] // self.size_chunk[1], (coord[1] + size[1]) // self.size_chunk[1] + 1):
            for x in range(coord[0] // self.size_chunk[0], (coord[0] + size[0]) // self.size_chunk[0] + 1):
                if 0 <= y < self.size[1] and 0 <= x < self.size[0]:
                    res += self.map[y][x].get_objects()
        return res

    def get_image(self, rect):
        res = []
        fon = []
        coord = rect.x, rect.y
        size = rect.width, rect.height
        for y in range(coord[1] // self.size_chunk[1], (coord[1] + size[1] - 1) // self.size_chunk[1] + 1):
            for x in range(coord[0] // self.size_chunk[0], (coord[0] + size[0] - 1) // self.size_chunk[0] + 1):
                if 0 <= y < self.size[1] and 0 <= x < self.size[0]:
                    res += self.map[y][x].get_objects()
                    fon.append(self.map[y][x])
        return res, fon
