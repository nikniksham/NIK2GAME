from Chunk import *
from random import choice, random
from pygame import Rect
from Framework import Application, Widget, AnimationWidgets, load_image, scale_to, Text, ProgressBar
from win32api import GetSystemMetrics


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


height_barr = 35
offset_from_the_sides = 110
from_bottom = -12
REPOSITORY = 'date'
WHITE = (255, 255, 255)

size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))


class Load(Application):
    def __init__(self, size_screen, size_world, FULLSCREEN=False, fill_color=(0, 0, 0)):
        super().__init__(size_screen, fill_color, FULLSCREEN)
        self.size_world = size_world

app = Application(size_screen, full_screen=True)

image = load_image('fon 1.png')
image = scale_to(image, (GetSystemMetrics(0), GetSystemMetrics(1)))
bg = Widget(image, (0, 0), is_zooming=False)

barr_top = load_image('barr_front.png', (255, 255, 255))
barr_top = scale_to(barr_top, (GetSystemMetrics(0) - 2 * offset_from_the_sides, height_barr))
barr_back = load_image('barr back.png', -1)
barr_back = scale_to(barr_back, (GetSystemMetrics(0) - 2 * offset_from_the_sides, height_barr))
barr = ProgressBar(barr_top, barr_back, (offset_from_the_sides, from_bottom), from_color=(255, 0, 0), to_color=(0, 255, 0))

prozent = '100%'
text_prozent = Text(prozent, height_barr, (GetSystemMetrics(0) - offset_from_the_sides + 5, from_bottom + 2), color=(100, 255, 100))
barr.add_display(text_prozent)

animation = AnimationWidgets([load_image('0.png', -1), load_image('1.png', -1), load_image('2.png', -1), load_image('3.png', -1)], (10, from_bottom), 0.65)

app.add_widget(bg, 0)
app.add_widget(barr)
app.add_widget(text_prozent)
app.add_widget(animation)
barr.update_bar(0)

app.run()
