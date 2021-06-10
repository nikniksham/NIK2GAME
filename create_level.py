from Chunk import *
from random import randrange, random
from pygame import Rect
from Framework import Application, Widget, AnimationWidgets, load_image, scale_to, Text, ProgressBar

height_barr = 35
offset_from_the_sides = 110
from_bottom = -12
WHITE = (255, 255, 255)
REPOSITORY = 'sprite\\User_Interface\\'

size_screen = (1920, 1080)


class Wall:
    def __init__(self, info, coord):
        if type(info) == tuple:
            self.image = info[0].get_image()
            if info[1] is None:
                self.rect = Rect((coord[0], coord[1], self.image.get_size()[0], 30))
            else:
                self.rect = Rect((coord[0] + self.image.get_size()[0] // 2 - info[1], coord[1], info[1] * 2, 30))
        else:
            self.image = info
            self.rect = Rect((coord[0], coord[1], self.image.get_size()[0], 30))

        self.coord = coord[0], coord[1] - int(self.image.get_size()[1] - 30)
        self.types = ['object', 'Image']
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


class Map(Widget):
    def __init__(self, map, surface):
        pass


class Create(Application):
    def __init__(self, size_screen, size_world, slow,  bar, FULLSCREEN=False, fill_color=(0, 0, 0)):
        super().__init__(size_screen, fill_color, FULLSCREEN)
        self.count = 0
        self.bar = bar
        self.name_world = 'world_TEST.wrld'
        size_world = size_world[1]
        self.end_coord = (size_world[0] * 256, size_world[1] * 256)
        with open(self.name_world, 'w') as world:
            world.write(f'{self.end_coord[0]}x{self.end_coord[1]}\n')
        self.size_world = size_world
        new_slow = {}
        for key, val in slow.items():
            if 'n' in key:
                if 'c' != key[0]:
                    new_slow[key] = len(val)
                else:
                    new_slow[key] = val
        self.slow = new_slow
        for key, val in self.slow.items():
            if 'b' == key[0]:
                self.block_bg = (key, val)
            if 't' == key[0]:
                self.block = (key, val)
            if 'c' == key[0]:
                self.compression = val
        self.creating_coord = [0, 0]
        self.add_event(self.generate_256)

    def generate_256(self):
        with open(self.name_world, 'a') as world:
            for i in range(256):
                # переключаемся на слой ниже если прошлый закончили
                if self.creating_coord[0] + 1 > self.end_coord[0]:
                    self.creating_coord[1] += 1
                    # если сгенерировали последний слой
                    if self.creating_coord[1] == self.end_coord[1]:
                        self.running = False
                        break
                    world.write('\n')
                    # переключаем коретку на новую строку если закончили эту строку
                    self.creating_coord[0] = 0
                else:
                    self.creating_coord[0] += 1
                if self.compression >= random():
                    world.write(f'{self.block_bg[0]}{randrange(self.block_bg[1])} {self.block[0]}{randrange(self.block[1])}\t')
                else:
                    world.write(f'{self.block_bg[0]}{randrange(self.block_bg[1])} None\t')
                self.count += 1

        self.bar.update_bar(self.count / (self.end_coord[1] * self.end_coord[0]))


def make_level(slow, chunk_count, map_slow):
    image = load_image(REPOSITORY + 'fon 1.png')
    image = scale_to(image, (size_screen[0], size_screen[1]))
    bg = Widget(image, (0, 0), is_zooming=False)

    barr_top = load_image(REPOSITORY + 'barr_front.png', (255, 255, 255))
    barr_top = scale_to(barr_top, (size_screen[0] - 2 * offset_from_the_sides, height_barr))
    barr_back = load_image(REPOSITORY + 'barr back.png', -1)
    barr_back = scale_to(barr_back, (size_screen[0] - 2 * offset_from_the_sides, height_barr))
    barr = ProgressBar(barr_top, barr_back, (offset_from_the_sides, from_bottom), from_color=(255, 0, 0), to_color=(0, 255, 0))

    text_prozent = Text('', height_barr, (size_screen[0] - offset_from_the_sides + 5, from_bottom + 2), color=(100, 255, 100))
    barr.add_display(text_prozent)

    animation = AnimationWidgets([load_image(REPOSITORY + '0.png', -1), load_image(REPOSITORY + '1.png', -1), load_image(REPOSITORY + '2.png', -1), load_image(REPOSITORY + '3.png', -1)], (10, from_bottom), 0.65)

    app = Create(size_screen, chunk_count, slow, barr, FULLSCREEN=True)

    app.add_widget(bg, 0)
    app.add_widget(barr)
    app.add_widget(text_prozent)
    app.add_widget(animation)
    barr.update_bar(0)

    app.run()
    return load_level(app.name_world, slow, map_slow)


class Load(Application):
    def __init__(self, size_screen, slow, map_slow, bar, file, full_screen=True):
        super().__init__(size_screen, full_screen=full_screen)
        with open(file, 'r') as kart:
            world = kart.read()
            size, self.map_world = world[:world.find('\n')], world[world.find('\n') + 1:]
            self.size = list(map(int, size.split('x')))
        self.bar = bar
        self.coord = [0, 0]
        self.count = 0
        self.pos = [0, 0]
        self.size_cell_map = 10
        self.map_image = Surface((self.size[0] * self.size_cell_map, self.size[1] * self.size_cell_map))
        self.main_chunk = MainChunk(list(map(lambda x: x // 16, self.size)))
        self.slow = slow
        self.world = []
        self.map_slow = map_slow
        self.add_event(self.load_chunk)
        for y, string in enumerate(self.map_world.split('\n')):
            self.world.append([])
            for x, elem in enumerate(string.split('\t')):
                if elem == '':
                    continue
                block_bg, block = elem.split(' ')
                key_bg, key, index_bg, index = '', '', '', ''
                for sumw in block_bg:
                    if sumw.isdigit():
                        index_bg += sumw
                    else:
                        key_bg += sumw
                if block != 'None':
                    for sumw in block:
                        if sumw.isdigit():
                            index += sumw
                        else:
                            key += sumw
                    self.world[-1].append((slow[key_bg][int(index_bg)], slow[key][int(index)]))
                    self.map_image.blit(map_slow[key][int(index)],
                                     ((x + 0) * self.size_cell_map, (y + 0) * self.size_cell_map))
                else:
                    self.world[-1].append((slow[key_bg][int(index_bg)], None))
                    self.map_image.blit(map_slow[key_bg][int(index_bg)],
                                     ((x + 0) * self.size_cell_map, (y + 0) * self.size_cell_map))

    def load_chunk(self):
        chunk = Chunk(self.coord)
        for dy in range(16):
            for dx in range(16):
                blocks = self.world[self.pos[1] + dy][self.pos[0] + dx]
                chunk.add_object(blocks[0], 0, (self.coord[0] + dx * 30, self.coord[1] + dy * 30))
                if blocks[1] is not None:
                    chunk.add_object(blocks[1], 1, (self.coord[0] + dx * 30, self.coord[1] + dy * 30))
        self.count += 1
        self.main_chunk.add_chunk(chunk)
        if [self.pos[0] + 16, self.pos[1] + 16] == list(self.size):
            self.running = False
        self.coord[0] += 480
        self.pos[0] += 16
        self.bar.update_bar(self.count / ((self.size[1] // 16) * (self.size[0] // 16)))
        if self.pos[0] == self.size[0]:
            self.main_chunk.next_string()
            self.coord[0] = 0
            self.pos[0] = 0
            self.coord[1] += 480
            self.pos[1] += 16

    def quit(self):
        return self.map_image, self.main_chunk


def load_level(file, slow, map_slow):
    image = load_image(REPOSITORY + 'fon 1.png')
    image = scale_to(image, (size_screen[0], size_screen[1]))
    bg = Widget(image, (0, 0), is_zooming=False)

    barr_top = load_image(REPOSITORY + 'barr_front.png', (255, 255, 255))
    barr_top = scale_to(barr_top, (size_screen[0] - 2 * offset_from_the_sides, height_barr))
    barr_back = load_image(REPOSITORY + 'barr back.png', -1)
    barr_back = scale_to(barr_back, (size_screen[0] - 2 * offset_from_the_sides, height_barr))
    barr = ProgressBar(barr_top, barr_back, (offset_from_the_sides, from_bottom), from_color=(255, 0, 0),
                       to_color=(0, 255, 0))

    text_prozent = Text('', height_barr, (size_screen[0] - offset_from_the_sides + 5, from_bottom + 2),
                        color=(100, 255, 100))
    barr.add_display(text_prozent)

    animation = AnimationWidgets([load_image(REPOSITORY + '0.png', -1), load_image(REPOSITORY + '1.png', -1),
                                  load_image(REPOSITORY + '2.png', -1), load_image(REPOSITORY + '3.png', -1)],
                                 (10, from_bottom), 0.65)

    app = Load(size_screen, slow, map_slow, barr, file, full_screen=True)

    app.add_widget(bg, 0)
    app.add_widget(barr)
    app.add_widget(text_prozent)
    app.add_widget(animation)
    barr.update_bar(0)

    res = app.run()
    return res