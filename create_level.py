from Chunk import *
from random import randrange, random
from pygame import Rect
from Framework import Application, Widget, AnimationWidgets, load_image, scale_to, Text, ProgressBar
from win32api import GetSystemMetrics

height_barr = 35
offset_from_the_sides = 110
from_bottom = -12
WHITE = (255, 255, 255)
REPOSITORY = 'sprite\\User_Interface\\'

size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))


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


class Load(Application):
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
    image = scale_to(image, (GetSystemMetrics(0), GetSystemMetrics(1)))
    bg = Widget(image, (0, 0), is_zooming=False)

    barr_top = load_image(REPOSITORY + 'barr_front.png', (255, 255, 255))
    barr_top = scale_to(barr_top, (GetSystemMetrics(0) - 2 * offset_from_the_sides, height_barr))
    barr_back = load_image(REPOSITORY + 'barr back.png', -1)
    barr_back = scale_to(barr_back, (GetSystemMetrics(0) - 2 * offset_from_the_sides, height_barr))
    barr = ProgressBar(barr_top, barr_back, (offset_from_the_sides, from_bottom), from_color=(255, 0, 0), to_color=(0, 255, 0))

    text_prozent = Text('', height_barr, (GetSystemMetrics(0) - offset_from_the_sides + 5, from_bottom + 2), color=(100, 255, 100))
    barr.add_display(text_prozent)

    animation = AnimationWidgets([load_image(REPOSITORY + '0.png', -1), load_image(REPOSITORY + '1.png', -1), load_image(REPOSITORY + '2.png', -1), load_image(REPOSITORY + '3.png', -1)], (10, from_bottom), 0.65)

    app = Load(size_screen, chunk_count, slow, barr, FULLSCREEN=True)

    app.add_widget(bg, 0)
    app.add_widget(barr)
    app.add_widget(text_prozent)
    app.add_widget(animation)
    barr.update_bar(0)

    app.run()
    return load_level(app.name_world, slow, map_slow)


def load_chunk(world, coord, pos):
    start_pos = pos[:]
    size_cell = 30
    chunk = Chunk(coord[:])
    chunk_bg = ChunkBG(coord[:])
    for _ in range(16):
        for _ in range(16):
            if world[pos[1]][pos[0]][1] is not None:
                wall = Wall(world[pos[1]][pos[0]][1], (pos[0] * size_cell, pos[1] * size_cell))
                chunk.add_object(wall)
            wall_bg = Wall(world[pos[1]][pos[0]][0].image, (pos[0] * size_cell, pos[1] * size_cell))
            chunk_bg.add_object(wall_bg)
            # добавляем размер болка по иксу (сдивагаемся на один блок враво)
            pos[0] += 1
        # переходим на новую строку изображений \n
        # на одну строку вниз
        pos[1] += 1
        # в начало ряда
        pos[0] = start_pos[0]
    chunk.check_cilision()
    chunk_bg.check_cilision()
    return chunk, chunk_bg


def load_big_chunk(world, coord, pos):
    last_pos = pos[:]
    start_coord = coord[:]
    big_chunk = BigChunk(coord[:])
    big_chunk_bg = BigChunk(coord[:])
    # по игрику
    for _ in range(16):
        # по иксу
        for _1 in range(16):
            chunk, chunk_bg = load_chunk(world, coord[:], pos[:])
            # добавляем чанк в список чанков с которыми объект может столкнуться стену
            big_chunk.add_chunk(chunk)
            # добавляем чанк в список чанков заднего фона
            big_chunk_bg.add_chunk(chunk_bg)
            # передвигаемся на один чанк вправо
            coord[0] += 480
            pos[0] += 16
        # переходим на новую строку чанков
        # в начало строки
        pos[0] = last_pos[0]
        coord[0] = start_coord[0]
        # переходим на новую строку
        pos[1] += 16
        coord[1] += 480
    return big_chunk, big_chunk_bg


def load_level(file, slow, map_slow):
    with open(file, 'r') as kart:
        world = kart.read()
        size, map_world = world[:world.find('\n')], world[world.find('\n') + 1:]
        size = list(map(int, size.split('x')))
    count = 0
    size_map = [size[0] // 256, size[1] // 256]
    size_block_on_map = 10
    world = [[]]
    surface_map = Surface((size[0] * size_block_on_map, size[1] * size_block_on_map))
    for y, string in enumerate(map_world.split('\n')):
        for x, elem in enumerate(string.split('\t')):
            count += 1
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
                world[-1].append((slow[key_bg][int(index_bg)], slow[key][int(index)]))
                surface_map.blit(map_slow[key][int(index)], ((x + 0) * size_block_on_map, (y + 0) * size_block_on_map))
            else:
                world[-1].append((slow[key_bg][int(index_bg)], None))
                surface_map.blit(map_slow[key_bg][int(index_bg)], ((x + 0) * size_block_on_map, (y + 0) * size_block_on_map))
        world.append([])
    pygame.image.save(surface_map, 'day.png')
    coord = [0, 0]
    pos = [0, 0]
    # размер одного блока
    # список чанков с которыми объект может столкнуться
    walls_group = MainChunk()
    # список чанков на заднего фона
    bg_walls_group = MainChunk()
    for _ in range(size_map[1]):
        for _ in range(size_map[0]):
            big_chunk, big_chunk_bg = load_big_chunk(world, coord[:], pos[:])
            walls_group.add_chunk(big_chunk)
            bg_walls_group.add_chunk(big_chunk_bg)
            coord[0] += 7680
        coord[0] = 0
        coord[1] += 7680
    # возвращаем список список чанков с которыми объект может столкнуться и список чанков на заднего фона
    return walls_group, bg_walls_group, surface_map
