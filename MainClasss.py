import pygame
import random
from pygame.sprite import Sprite, collide_rect
from pygame import image, Rect, Surface
import math
from Framework import load_image
import os

lol = pygame.display.set_mode((10, 10))

# в этом файле реализуется логика взаимодействия объектов между собой
# убедительна просьба прочитать инструкцию перед написанием классов чтобы всем было удобнее
# 1) при создании класса вы наследуете свой класс от одного из этих классов
# это делается так
# class(класс от колторого вы наследуетесь):
# 2) первая строчка в __init__: super().__init__(атрибуты класса родителя)
# 3) вторая строчка self.add_type("название вашего класса") это нужно для того чтобы другие клаасы могли понимать что
# это за класс
# 4) перед написанием класса ознакомиться с иерархией и методами классов родитетелей (чтобы не написать несколько
# одинаковых методов)
# 5) это основной файл игры поэтому перед каждой строчкой должен быть коментарий
# # коментарий поясняющий работу следущей строки
# строка с кодом
# 6) проверять все аргументы на пренадлежность нужному типу будь то строка, число, дробь, или класс из этого или
# другого файла
# это делается так:
# object.is_type("тип объекта")  # проверяет то что класс написаный для игры является наследником или сам является этим
# классом
# type(object) возвращает Название класса, например: int, str, float
# 7) просьба написать инструкцию для вашего класса в файле class.py по образу и подобию написания инструкций тех классов
# спасибо что прочитали инструкцию!
# Пожалуйста O_o


def load_data():
    global ID
    global message
    message = False
    ID = [0]


def get_gipotinuza(coord_1, coord_2):
    kat_1 = abs(coord_1[0] - coord_2[0])
    kat_2 = abs(coord_1[1] - coord_2[1])
    gip = (kat_1 ** 2 + kat_2 ** 2) ** 0.5
    return gip


load_data()


class Wonderful:
    def __init__(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect


class Timer:
    def __init__(self):
        self.types = ['Timer']
        self.ticks = self.time_sec = self.time_min = self.time_hour = self.time_day = 0
        self.stopwatch_ticks = 0
        self.max_fps = 80
        self.game = None
        self.f_stopwatch = False

    def update_timer(self):
        self.ticks += self.game.get_fps() / self.max_fps
        if self.f_stopwatch:
            self.stopwatch_ticks += self.game.get_fps() / self.max_fps

    def set_game(self, game):
        self.game = game

    def get_time(self):
        self.synchronization(self.ticks)
        return self.time_sec, self.time_min, self.time_hour, self.time_day

    def get_stopwatch_time(self):
        self.synchronization(self.stopwatch_ticks)
        return self.time_sec, self.time_min, self.time_hour, self.time_day

    def synchronization(self, ticks):
        self.time_sec = round(ticks / 60, 1)
        self.time_min = round(ticks / 3600, 1)
        self.time_hour = round(ticks / 216000, 1)
        self.time_day = round(ticks / 5184000, 1)

    def set_max_fps(self, fps):
        if fps > 0:
            self.max_fps = fps

    def start_stopwatch(self):
        self.f_stopwatch = True
        self.stopwatch_ticks = 0

    def stop_stopwatch(self):
        self.f_stopwatch = False
        self.synchronization(self.f_stopwatch)
        return self.time_sec, self.time_min, self.time_hour, self.time_day


class MainObject(Timer):
    def __init__(self):
        super().__init__()
        self.types = ['MainObject']

    def get_types(self):
        # получить типы
        return self.types

    def is_type(self, type):
        # проверить явлыется ли объект наследником даного типа
        return type in self.types

    def add_type(self, type):
        # добавить тип
        self.types.append(type)


class Image(MainObject, Sprite):
    def __init__(self, filename, transpote_color=(255, 255, 255), coord=(0, 0)):
        super().__init__()
        Sprite.__init__(self)
        # добавляем тип Image
        self.home = None
        self.add_type('Image')
        # загружаем изображение
        if type(filename) == str:
            self.image = image.load(filename).convert()
        else:
            self.image = filename
        # прямоугольник координат и размера rect
        self.coord = coord
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord
        self.image.set_colorkey(transpote_color)
        self.layer = 0
        self.is_back_ground = False

    def set_in_home(self, home):
        self.home = home

    def set_bg(self, val: bool):
        self.is_back_ground = bool(val)

    def get_is_bg(self):
        return self.is_back_ground

    def set_layer(self, layer):
        self.layer = layer

    def get_layer(self):
        return self.layer

    def get_mask(self):
        return Wonderful(Rect(self.get_coord(), self.image.get_size()))

    def set_coord(self, coord):
        self.coord = coord
        return self

    def get_size(self):
        # возвращаем размер изобрадения
        return self.image.get_size()

    def get_image(self):
        # возвращаем изображение
        return self.image

    def get_coord(self):
        # возвращает rect с координатами и размером объекта
        return self.rect.x, self.rect.y

    def get_rect(self):
        # возвращает прямоугольник объекта
        return self.rect


class Animation(Image):
    def __init__(self, way, speed, coord=(0, 0), color_key=(255, 255, 255)):
        files = list(os.walk(way))[0][-1]
        self.images = []
        for elem in files:
            self.images.append(Image(way + elem, transpote_color=color_key).get_image())
        super().__init__(self.images[0], transpote_color=color_key, coord=coord)
        self.frame = 0
        self.to_next_frame = 0
        self.speed = speed

    def update(self, *args):
        self.to_next_frame += 1
        if self.to_next_frame == self.speed:
            self.frame += 1
            if self.frame >= len(self.images) - 1:
                self.frame = 0
            self.to_next_frame = 0

    def get_image(self):
        return self.images[self.frame]

    def set_frame(self, index=0):
        if -1 < index < len(self.images):
            self.frame = index
        else:
            print('Ты скорее всего ошибся на единицу')
            quit()

    def set_speed(self, speed):
        if speed > 0:
            self.speed = speed
        else:
            print('Почему скорость отрицительная?')
            quit()


class Object(Image):
    def __init__(self, image, coord, transpote_color=(255, 255, 255)):
        if type(image) == str:
            super().__init__(image, transpote_color, coord)
        else:
            MainObject.__init__(self)
            self.image = image
            self.layer = 0
            self.is_back_ground = False
            self.home = None
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        # размер одной клетки на карте
        self.size_block = 30
        # добавляем в список типов тип Object
        self.add_type('Object')
        # список групп в которых состаит объект
        self.groups = []

    def add_group(self, group):
        # возвращает истину если группа добавлена и лож если не добавлена
        # добавление объекта в группу
        # проверяем что наследник класса Group
        if group.is_type('Group'):
            # если наследник класса то добаляем в список груп
            self.groups.append(group)
            return True
        else:
            # если не наследник класса Group возвращаем лож и не добавляем в список
            return False

    def get_group(self):
        # возвращаем список групп
        return self.groups

    def in_group(self, group):
        # возваращаем истину если состоит в группе лож если не состаит в группе
        return group in self.groups

    def remove_group(self, group):
        # если группа удалена из списка груп возвращается истина в обратном случае лож
        if self.in_group(group):
            # удаляем группу из списка групп и возвращаем истину
            self.groups.remove(group)
            return True
        else:
            # если элемента нет в списке групп то возвращаем лож
            return False


class Group(Object):
    def __init__(self, image, objects=[]):
        super().__init__(image, (0, 0))
        self.add_type('Group')
        # создаём список объектов в группе
        self.create_group(objects)
        # добавляем в список типов тип Group

    def create_group(self, objects):
        # список в котором хранятся все элементы группы
        self.objects = []
        # проходимся по объектам из списка объектов
        for object in objects:
            # пытаемся добавить объект в группу
            self.add_object(object)

    def get_object(self, type=None):
        # создаём список в каторый сохраним результат
        res_group = []
        # если есть фильтр
        if type is not None:
            for object in self.objects:
                # если объект подходит под условия
                if object.is_type(type):
                    # то дабовляем его в группу иначе пропускаем элемент
                    res_group.append(object)
        else:
            # иначе добавляем все объекты в res_group
            for object in self.objects:
                res_group.append(object)
        # возвращаем результат
        return res_group

    def add_object(self, object):
        # возвращает истину если объект добавен лож если нет
        if object.is_type('Object'):
            self.objects.append(object)
            object.add_group(self)
            return True
        else:
            return False

    def remove(self, object):
        # удалить объект из группы
        # пример объект сам удаляется из группы передав self
        # проверяем находится ли объект в группе
        if object in self.objects:
            # если get_coord() объект в группе то удаляем его из группы
            self.objects.remove(object)
            # и удаляем из списка групп в которых он состаит эту группу
            object.remove_group(self)
            return True
        return False

    def __str__(self):
        return f'Group: {self.get_group()}'


class BotGroup(MainObject):
    def __init__(self, type, name_group):
        super().__init__()
        self.add_type('Group')
        self.add_type('BotGroup')
        self.friendly = ''
        self.set_friednly(type)
        self.type_bots = name_group
        self.bots = []

    def set_friednly(self, type):
        if type in ['enemy', 'neutral']:
            self.friendly = type
            return True
        return False

    def get_friednly(self):
        return self.friendly

    def get_life_bot(self):
        count = 0
        for bot in self.bots:
            if not bot.die_f:
                count += 1
        return count

    def add_bot(self, *bots):
        for bot in bots:
            if bot.is_type('NPS'):
                self.bots.append(bot)

    def remove_bot(self, bot):
        if bot in self.bots:
            self.bots.remove(bot)
            return True
        return False

    def get_objects(self):
        return self.bots[:]

    def update(self, objects, main_group, camera):
        bots = self.get_objects()
        for bot in bots:
            bot.update(bots[:], objects, main_group, camera)
            if bot.die_tick >= 600:
                self.remove_bot(bot)


class Build(Object):
    def __init__(self, coord, image_out, scena, image_in=None, door_rect=None):
        # жутко не оптимизированая штука
        super().__init__(image_out, coord)
        self.set_layer(0)
        # рект объекта
        self.rect = Rect((coord[0], coord[1] + 10), (self.image.get_size()[0], self.image.get_size()[1] - 10))
        # перс в доме
        self.in_hom = False
        # тип здание для collision что-бы перс в доме рисовался певерх него
        self.add_type('Static')
        self.add_type('Build')
        # сцена для добовления на неё кнопки зайти в дом
        self.scena = scena
        # нажата ли кнопка войти
        self.join = False
        # отрисовывается ли кнопка
        self.button_drawing = False
        # если в дом можно зайти
        if image_in is not None and door_rect is not None:
            # можно ли войти  этот дом
            self.can_join = True
            # кортинка внутри
            self.image_in = load_image(image_in, (255, 255, 255))
            # картинка снаружи
            self.image_out = load_image(image_out)
            # рект двери, когда гг заходит в него, то отрисовывается кнопка
            door_rect.x, door_rect.y = door_rect.x + coord[0], door_rect.y + coord[1]
            # сохраняем рект двери
            self.door_rect = door_rect
            # если кортеж
            coord = list(coord)
            # смещаем координаты на 30 т к можем ходить за домом
            coord[1] += 30
            # кнопка
            self.button = ImageButton('sprite/buttons//door.png', (self.door_rect[0] - 30, self.door_rect[1]),
                                      self.open_door)
            # чтобыы кнопка отрисовывалась над домом
            self.button.set_layer(self.layer + 10)
            # чтены внутри
            # верхняя стена от верха до пона высота 35
            self.up_wall = Image(Surface((self.image_in.get_width(), 35)), coord=(coord[0], coord[1] - 30), transpote_color=(10, 10, 10))
            # левая стена, обычная слевая тена
            self.left_wall = Image(Surface((5, self.image_in.get_height() - 30)), coord=coord, transpote_color=(10, 10, 10))
            # правая стена -//-
            self.right_wall = Image(Surface((5, self.image_in.get_height() - 30)),
                                          coord=(coord[0] + self.image_in.get_width() - 5, coord[1]), transpote_color=(10, 10, 10))
            # нижняя стена -//-
            self.down_wall = Image(Surface((self.image_in.get_width(), 5)),
                                          coord=(coord[0], coord[1] + self.image_in.get_height() - 35), transpote_color=(10, 10, 10))
        # если в дом нельзя зайти
        else:
            # можно ди зайти в этот дом
            self.can_join = False

    def can_entering(self, object):
        # устанавливаем есть ли кто в доме
        self.set_in_hom()
        # вход в дом
        if self.can_join and self.door_rect.colliderect(object.get_rect()) and self.in_hom:
            object.rect.bottom = self.down_wall.rect.top
            object.rect.left = self.door_rect.left
            object.set_in_home(self)
            print(2)
            return True
        # выход из дома
        elif self.can_join and self.door_rect.colliderect(object.get_rect()) and not self.in_hom:
            object.rect.top = self.down_wall.rect.bottom
            object.rect.left = self.door_rect.left
            object.set_in_home(None)
            print(3)
            return True
        return False

    def get_coord(self):
        # для отрисовки
        return self.rect.x, self.rect.y - 10

    def get_rect(self):
        # для колизии
        return Rect(self.get_coord(), self.image.get_size())

    def set_in_hom(self):
        # если в дом можно зайти
        if self.can_join:
            self.in_hom = not self.in_hom
            # устанавливаем картинку
            if self.in_hom:
                self.image = self.image_in
            else:
                self.image = self.image_out

    def get_walls(self):
        # получить стены либо 1 либо 4 стены
        res = []
        if self.in_hom:
            res.append(self.left_wall)
            res.append(self.right_wall)
            res.append(self.up_wall)
            res.append(self.down_wall)
        else:
            res.append(self)
        return res

    def open_door(self):
        # asd функция кнопки
        self.join = True

    def update(self, objects, main_chunk, camera):
        if self.can_join:
            for object in objects:
                # если гг у двери и кнопка не отрисовывается
                if object.is_type('MainHero') and self.door_rect.colliderect(object.rect) and not self.button_drawing:
                    self.scena.add_button(self.button)
                    self.button_drawing = True
                # print(len(self.scena.main_group.buttons), self.in_hom, self.can_join, 'dasfgas')
                # если гг не у двери а кнопка отрисовывается
                if object.is_type('MainHero') and not self.door_rect.colliderect(object.rect) and self.button_drawing:
                    self.button_drawing = False
                    self.scena.remove_button(self.button)
                # входим в дом
                if object.is_type('MainHero') and self.join and self.can_entering(object):
                    self.button_drawing = False
                    self.scena.remove_button(self.button)
                    self.join = False


class PassiveAnimationBuild(Build):
    def __init__(self, way, speed, coord, scena, color_key=(255, 255, 255)):
        self.animation = Animation(way, speed, coord, color_key)
        super().__init__(coord, self.animation.get_image(), scena)

    def get_image(self):
        self.animation.update()
        return self.animation.get_image()


class Site(MainObject):
    def __init__(self, bot_group=None):
        super().__init__()
        self.add_type('Group')
        self.add_type('Site')
        self.objects = []
        self.builds = []
        if bot_group is not None and bot_group.is_type('BotGroup'):
            self.bots = bot_group
        else:
            self.bots = None

    def add_object(self, object):
        self.builds.append(object)

    def remove_object(self, object):
        if object in self.builds:
            self.builds.remove(object)
            return True
        return False

    def get_objects(self):
        res = self.builds[:]
        if self.bots is not None:
            res += self.bots.get_objects()
        return res

    def get_walls(self):
        res = self.objects[:]
        for build in self.builds:
            res += build.get_walls()
        return res

    def update(self, objects, main_chunk, camera):
        for build in self.builds:
            build.update(objects, main_chunk, camera)
        if self.bots is not None:
            self.bots.update(objects, main_chunk, camera)


class MainGroup(MainObject):
    def __init__(self, camera):
        super().__init__()
        self.add_type('Group')
        self.camera = camera
        self.all_objects = []
        self.buttons = []
        self.bullets = []
        self.bots = []
        self.team = []
        self.sites = []

    def add_buttons(self, button):
        self.buttons.append(button)

    def remove_button(self, button):
        if button in self.buttons:
            self.buttons.remove(button)
            return True
        return False

    def add_bot_group(self, bot_group):
        if bot_group.is_type('BotGroup'):
            self.bots.append(bot_group)
            return True
        return False

    def remove_bots_group(self, bots_group):
        if bots_group in self.bots:
            self.bots.remove(bots_group)
            return True
        return False

    def get_all_objects(self, person=True):
        res = self.all_objects[:]
        res += self.buttons[:]
        res += self.get_bots()
        res += self.bullets[:]
        if person:
            res += self.team[:]
        else:
            res += self.team[1:]
        for site in self.sites:
            res += site.get_objects()
        # print('количество объектов на сцене', len(res))
        return res

    def get_walls(self):
        res = self.all_objects[:]
        for site in self.sites:
            res += site.get_walls()
        return res

    def get_bullets(self):
        return self.bullets

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)

    def add_object(self, object):
        self.all_objects.append(object)

    def remove_object(self, object):
        self.all_objects.remove(object)

    def get_objects(self):
        return self.all_objects

    def get_bots(self, type=None):
        res = []
        for bots in self.bots:
            if type is None or type == bots.get_friednly(type):
                res += bots.get_objects()
        return res

    def add_to_team(self, object):
        self.team.append(object)

    def remove_from_team(self, object):
        if object in self.team:
            self.team.remove(object)
            return True
        return False

    def get_team(self):
        return self.team

    def add_site(self, site):
        if site.is_type('Site'):
            self.sites.append(site)
            return True
        return False

    def remove_site(self, site):
        if site in self.sites:
            self.sites.remove(site)
            return True
        return False

    def get_sites(self):
        return self.sites

    def get_to_update(self, *groups):
        res = self.get_all_objects()
        for group in groups:
            for elem in group:
                res.remove(elem)
        return res

    def get_bot_groups(self):
        return self.bots

    def button_update(self):
        for button in self.buttons:
            button.update(self.camera.get_coord())

    def update(self, main_chunk, camera):
        # qwerty
        objects = self.get_to_update(self.bullets, self.team, self.buttons)
        for bullet in self.bullets:
            res = bullet.update(objects[:], main_chunk)
            if res:
                self.remove_bullet(bullet)
        for group in self.get_bot_groups():
            objects = self.get_to_update(group.get_objects(), self.bullets)
            group.update(objects, main_chunk, camera)
        objects = self.get_all_objects()
        for bot in self.team[1:]:
            bot.update(objects[:], main_chunk, camera)
        for site in self.get_sites():
            site.update(objects[:], main_chunk, camera)


class Level(MainObject):
    def __init__(self, name, main_hero, main_chunk, camera):
        self.main_chunk = ''
        self.add_main_chunk(main_chunk)
        super().__init__()
        # добавляем тип: Level
        self.add_type('Level')
        self.main_group = MainGroup(camera)
        self.main_group.add_to_team(main_hero)
        # название сцены
        self.name = name
        # размер угровня
        self.main_hero = main_hero

    def add_main_chunk(self, main_chunk):
        # если объект типа МainChunk то он нам подходит возвращаем истину в противоположном случае лож
        if main_chunk.is_type('MainChunk'):
            self.main_chunk = main_chunk
            return True
        return False

    def button_update(self):
        self.main_group.button_update()

    def add_button(self, button):
        self.main_group.add_buttons(button)

    def remove_button(self, button):
        self.main_group.remove_button(button)

    def add_bullet(self, bullet):
        self.main_group.add_bullet(bullet)

    def remove_bullet(self, bullet):
        self.main_group.remove_bullet(bullet)

    def get_map_images_objects(self, object):
        return self.main_chunk.get_image(object.get_rect())[0]

    def get_map_images_fon(self, object):
        return self.main_chunk.get_image(object.get_rect())[1]

    def get_objects(self, objects):
        return self.main_chunk.get_object(objects.get_rect())

    def get_bots(self, type=None):
        return self.main_group.get_bots(type)

    def add_bot_group(self, group):
        return self.main_group.add_bot_group(group)

    def remove_bots_group(self, group):
        return self.main_group.remove_bots_group(group)

    def add_object(self, object):
        self.main_group.add_object(object)

    def remove_object(self, object):
        self.main_group.remove_object(object)

    def add_site(self, site):
        return self.main_group.add_site(site)

    def remove_site(self, site):
        return self.main_group.remove_site(site)

    def get_object(self, object):
        # создаём список в который сохраняем результат
        res = []
        # проходимся по группам из списка групп
        res += self.main_group.get_all_objects()
        # print(f'объекты сцены: {len(res)}')
        res += self.get_map_images_objects(object)
        # возвращаем результат
        return res

    def get_walls(self, object):
        res = self.main_group.get_walls()
        res += self.main_chunk.get_object(object)
        return res

    def get_main_hero(self):
        # возвращаем главного героя сцены
        return self.main_hero

    def update(self, camera):
        self.main_group.update(self.main_chunk, camera)


class Camera(MainObject):
    def __init__(self, size_screen, bg_color):
        super().__init__()
        # создаём таймер
        self.clock = pygame.time.Clock()
        # добавляем тип Camera
        self.add_type('Camera')
        # размер экрана
        self.size_screen = size_screen
        # цвет заднего фона
        self.bg_color = bg_color
        # создаём экран
        pygame.init()
        self.screen = Surface(self.size_screen)
        # координаты левого верхнего угла
        self.coord = (0, 0)

    def get_rect(self):
        return Rect(self.get_coord(), self.get_size_screen())

    def get_size_screen(self):
        # получить размер экрана
        return self.size_screen

    def get_coord(self):
        # получить координаты левой верхней по которым расположен экран
        return self.coord

    def get_screen_coord(self, main_hero_coord):
        # находим левый верхний угол экрана при данном положении главного героя
        self.coord = [main_hero_coord[0] - self.size_screen[0] // 2 + 15, main_hero_coord[1] - self.size_screen[1] // 2 + 15]

    def create(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def object_coord(self, coord):
        # вычисляем координаты на экране относительно персонажа
        return coord[0] - self.coord[0], coord[1] - self.coord[1]

    def draw(self, level):
        # заливаем экран цветом заднего фона
        self.screen.fill(self.bg_color)
        # находим левый верхний угол экрана при данном положении главного героя
        self.get_screen_coord(level.get_main_hero().get_rect())
        level.update(self)
        count = 0
        for image in level.get_map_images_fon(self):
            count += 1
            self.screen.blit(image.get_image(), self.object_coord(image.get_coord()))

        layers = {}
        keys = []
        for object in level.get_object(self):
            if object.get_layer() not in layers:
                keys.append(object.get_layer())
                layers[object.get_layer()] = [object]
            else:
                layers[object.get_layer()].append(object)
        keys.sort()
        for key in keys:
            for object in layers[key]:
                count += 1
                self.screen.blit(object.get_image(), self.object_coord(object.get_coord()))
        # print(f'отрисовывается {count} объектов')
        # обнавляем экран
        # poop = draw.circle(self.screen, (255, 0, 0), (self.size_screen[0] // 2, self.size_screen[1] // 2), 15)
        # line_1 = draw.line(self.screen, (0, 0, 0), (0, 0), (self.size_screen[0], self.size_screen[1]), 5)
        # line_2 = draw.line(self.screen, (0, 0, 0), (self.size_screen[0], 0), (0, self.size_screen[1]), 5)
        # заголовк программы количество кадров в секунду и количество предметов на сцене
        # обнавляем экран
        # ограничиваем количество кадров в секунду до 120
        return self.screen


class Item(Object):
    def __init__(self, image, coord, name, max_count, info='', count=0):
        self.original_image = Image(image).get_image().copy()
        super().__init__(image, coord)
        global ID
        self.add_type('Item')
        # максимальное количество предметов данного типа
        self.max_count = max_count
        # количество объектов данного типа
        self.count = count
        # создаём ID
        self.ID = ID[-1] + 1
        ID.append(self.ID)
        # задаём информацию об объекте
        self.info_object = info
        # задаём имя объекта
        self.name = name

    def get_count(self):
        # возвращает количество предметов данного типа
        return self.count

    def add_count(self, item):
        # складываем предметы
        # проверяем то что другой объект точно такогоже типа как и этот предмет
        if item.is_type(self.get_types()[-1]):
            # добавляем в этот объект тот объект
            self.count += item.get_count()
            # если количество предмета получилось больше его максимального количества
            if self.count > self.max_count:
                # устанавливаем количество предметов остаток который не влез в этот предмет
                item.set_count(self.count - self.max_count)
                # устанавливаем количество предметов на максимальный уровень
                self.set_count(self.max_count)
            else:
                # устанавливаем другомы предмету количество равное 0
                item.set_count(0)

    def set_count(self, count):
        # низкоуровневая функция
        # используется для задания количества предметов объекта
        self.count = count

    def set_info(self, info):
        # возвращает истину если получилось лож если нет
        if type(info) == str:
            self.info_object = info
            return True
        return False

    def info(self):
        return self.info_object
        # возвращает информацию об объекте

    def get_name(self):
        # возвращает имя объекта
        return self.name

    def __str__(self):
        return f'type {self.get_name()}, count {self.get_count()}'


class Inventory:
    def __init__(self, size, items=[]):
        self.size_inventory = size
        self.inventory = []
        for _ in range(size[1]):
            self.inventory.append([])
            for _ in range(size[0]):
                if len(items) > 0:
                    self.inventory[-1].append(items[-1])
                    items.pop(-1)
                else:
                    self.inventory[-1].append(None)

    def get_items(self, x=None, y=None):
        res = []
        if x is not None and y is not None:
            res.append(self.inventory[y][x])
        elif x is not None:
            for y in range(self.size_inventory[1]):
                res.append(self.inventory[y][x])
        elif y is not None:
            for x in range(self.size_inventory[0]):
                res.append(self.inventory[y][x])
        else:
            for y in range(self.size_inventory[1]):
                for x in range(self.size_inventory[0]):
                    if self.inventory[y][x] is not None:
                        res.append(self.inventory[y][x])
        return res

    def add_item(self, item, pos=None):
        if pos is None:
            for y in range(self.size_inventory[1]):
                for x in range(self.size_inventory[0]):
                    if self.inventory[y][x] is None:
                        self.inventory[y][x] = item
                        return True
                    if self.inventory[y][x].get_name() == item.get_name():
                        self.inventory[y][x].add_count(item)
                        if item.get_count() == 0:
                            return True
            return item
        else:
            item = Item('ads', (123, 213), 'sg', 10)
            if self.inventory[pos[1]][pos[0]] is None:
                self.inventory[pos[1]][pos[0]] = item
            elif item.get_name() == self.inventory[pos[1]][pos[0]].get_name():
                self.inventory[pos[1]][pos[0]].add_count(item)
                if item.get_count() > 0:
                    return item
                else:
                    return True
            else:
                ret_item = self.inventory[pos[1]][pos[0]]
                self.inventory[pos[1]][pos[0]] = item
                return ret_item

    def remove_item(self, item, pos=None):
        if pos is None:
            for y in range(self.size_inventory[1]):
                for x in range(self.size_inventory[0]):
                    if self.inventory[y][x] == item:
                        self.inventory[y][x] = None
                        return item
        else:
            if self.get_items(pos[0], pos[1])[0] == item:
                self.inventory[pos[1]][pos[0]] = None
                return item
        return False

    def get_size(self):
        return self.size_inventory


class Chest(Build):
    def __init__(self, image_close, coord, scena, inventory=[]):
        # asf
        super().__init__(coord, image_close, scena)
        self.inventory = inventory
        self.button_in_drawing = False
        self.button_out_drawing = False
        self.activity = False
        self.do_it = False
        image_1 = Image('sprite/Interactive_objects/chest_put.bmp').get_image()
        image_2 = Image('sprite/Interactive_objects/chest_take.bmp').get_image()
        self.button_out = ImageButton(image_1, coord, self.out_items)
        self.button_out.set_layer(self.get_layer() + 1)
        self.button_in = ImageButton(image_2, coord, self.in_items)
        self.button_in.set_layer(self.get_layer() + 1)

    def out_items(self):
        #print('out')
        #print(self.activity)
        self.do_it = True

    def in_items(self):
        #print('in')
        #print(self.activity)
        self.do_it = True

    def update(self, objects, main_chunk, camera):
        for object in objects:
            if object.is_type('MainHero'):
                # print(len(self.scena.main_group.buttons), self.rect.colliderect(object.get_rect()), not self.button_out_drawing, not self.activity)
                if not self.button_in_drawing and self.activity and self.rect.colliderect(object.get_rect()):
                    self.scena.add_button(self.button_in)
                    self.scena.remove_button(self.button_out)
                    self.button_in_drawing = True
                    self.button_out_drawing = False
                elif not self.button_out_drawing and not self.activity and self.rect.colliderect(object.get_rect()):
                    self.scena.add_button(self.button_out)
                    self.scena.remove_button(self.button_in)
                    self.button_out_drawing = True
                    self.button_in_drawing = False
                elif self.do_it and self.rect.colliderect(object.get_rect()):
                    if self.activity:
                        for item in object.inventory.get_items():
                            self.inventory.append(object.inventory.remove_item(item))
                        # print(self.inventory, 101)
                    else:
                        for elem in self.inventory:
                            object.inventory.add_item(elem)
                    self.activity = not self.activity
                    self.do_it = False
                elif not self.rect.colliderect(object.get_rect()):
                    self.scena.remove_button(self.button_in)
                    self.scena.remove_button(self.button_out)
                    self.button_out_drawing = False
                    self.button_in_drawing = False


# исправил на:
# self.armor += upgrade_point
# всегда в клаасах пиши
# self.add_type('Armor') всесто армор мазвание класса
# чем отличается:
# self.armor = armor
# от
# self.armor_heal_point = armor_hp
# и что такое и чем отличается
# self.armor - bool, int, str?
class Armor(Item):
    def __init__(self, image, coord, name, max_count, armor, armor_hp, armor_max_hp, info=''):
        # тип объекта: Armor
        # Я исправил heat_point на heal_point, тк heat_point переводится как: 'тепловая точка'
        super().__init__(image, coord, name, max_count, info)
        self.add_type('Armor')
        #  параметр: защита
        self.armor = armor
        #  параметр: максимальное здоровье брони
        self.armor_max_heal_point = armor_max_hp
        # параметр: здоровье брони
        self.armor_heal_point = armor_hp

    def get_armor(self):
        # возвращает защиту
        return self.armor

    def armor_upgrade(self, upgrade_point):
        # улучшает защиту, пример: ты пошёл к механику, он улучшил тебе броню, добавил очки защиты
        if type(upgrade_point) == int:
            self.armor_max_heal_point += upgrade_point
            self.armor += upgrade_point

    def armor_downgrade(self, downgrade_point):
        # ухудшает защиту, пример: ты снял улучшение, у тебя убавились очки защиты
        if type(downgrade_point) == int:
            self.armor_max_heal_point -= downgrade_point
            if self.armor > self.armor_max_heal_point:
                self.armor = self.armor_max_heal_point

    def get_armor_hp(self):
        # возвращяет здороье бронижелета
        return self.armor_heal_point

    def armor_damage(self, damage):
        # ломает бронижелет на N очков
        # проверка на то что damage число
        if type(damage) == float:
            damage = int
        if type(damage) == int:
            # нанесёный урон не может опустить уровень жизней ниже нуля
            if self.armor_heal_point - damage > 0:
                self.armor_heal_point -= damage
            else:
                self.armor_heal_point = 0

    def armor_repair(self, repair_point):
        # чинит бронижелет на N очков, но не больше, чем максимальное здоровье
        if self.armor_heal_point + repair_point > self.armor_max_heal_point:
            self.armor_heal_point = self.armor_max_heal_point
        else:
            self.armor_heal_point += repair_point


class Bullet(Item):
    def __init__(self, image, coord, name, max_count, type_bullet, weapon, x_vel=None, y_vel=None, attack_radius=None, info=''):
        super().__init__(image, coord, name, max_count, info)
        # добавляем тип: Bullet
        self.weapon = weapon
        self.coord = coord
        self.attack_radius = attack_radius
        self.start_pos = coord[:]
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.bullet = 0
        self.list_bullet = []
        self.add_type('Bullet')
        self.type_bullet = type_bullet

    def get_coord(self):
        return self.coord

    def get_type_bullet(self):
        # возвращает тип снаряда
        return self.type_bullet

    def update(self, objects, main_chunk):
        # qwerty
        self.coord[0] += self.x_vel
        self.coord[1] += self.y_vel
        self.rect.x, self.rect.y = self.coord
        if get_gipotinuza(self.coord, self.start_pos) >= self.attack_radius:
            return True
        for object in objects:
            if self.rect.colliderect(object.get_rect()):
                if object.is_type('HealPointObject'):
                    if object.die_f:
                        continue
                    else:
                        self.weapon.damage(object)
                if not object.is_type('Weapon'):
                    return True
        for object in main_chunk.get_object(self.rect):
            if self.rect.colliderect(object.get_rect()):
                return True
        return False


class Weapon(Bullet):
    def __init__(self, image, coord, name, max_count, type_bullet, type_damage, attack_radius,
                 range_damage, attack_speed, owner, info=''):
        # тип объекта: Weapon
        super().__init__(image, coord, name, max_count, type_bullet, info)
        self.add_type('Weapon')
        # типы урона: knife, firearm, missile, ret_damage
        self.type_damage = type_damage
        # Дальность атаки
        self.attack_radius = attack_radius
        # кортеж из чисел (минимальный урон, максимальный урон)
        self.range_damage = range_damage
        # скорость атаки
        self.attack_speed = attack_speed
        # точность оружия
        # Владелец
        self.owner = owner

    def shoot(self, camera, shoot_bool:bool, hero, image, scene):
        shoot_f = shoot_bool
        angle = 0
        if shoot_f:
            if hero.get_in_hand().shoot_delay(scene):
                hero.get_in_hand().count_shoot += 1
                hero.get_in_hand().tick = 0
                angle = hero.get_in_hand().spawn_bullet(camera, hero, image, scene)
        else:
            hero.get_in_hand().shoot_delay(scene)
        hero.get_in_hand().set_coord([hero.get_coord()[0] - 3, hero.get_coord()[1] + 7])
        hero.get_in_hand().rotate_image(angle)

    def spawn_bullet(self, camera, hero, image, scene):
        self.bullet += 1
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coord_person = camera.object_coord(hero.get_coord())
        mouse_x -= 5
        mouse_y -= 10
        coord = hero.get_coord()
        sin, cos, rad = hero.get_in_hand().flight_path([mouse_x, mouse_y], coord_person)
        angle = int(rad * 180 / math.pi)
        x_vel, y_vel = 10 * cos, 10 * sin
        # print(self.bullet, 'пуля')
        scene.add_bullet(Bullet(image, [coord[0] + 5, coord[1] + 10], 'bullet', 10, 'standard', hero.get_in_hand(), x_vel, y_vel, self.attack_radius))
        return angle

    def get_bullet_count(self):
        # идём в инвентарь берём патроны и возвращаем количество патронов нужного типа
        # if enemy.is_type('MovingObject'):
        pass

    def damage(self, enemy):
        damage = random.choice(range(self.range_damage[0], self.range_damage[1]))
        # print('Нанесенно', damage, 'урона')
        enemy.damage(damage, enemy)

    def flight_path(self, mouse_pos, hero_pos):
        x, y = hero_pos
        m_x, m_y = mouse_pos
        rad = math.atan2(m_y - y, m_x - x)
        sin = math.sin(rad)
        cos = math.cos(rad)
        return sin, cos, rad


class Tile(pygame.sprite.Sprite):
    def __init__(self, rect, mask_sprites):
        super().__init__(mask_sprites)
        self.rect = rect


class HealPointObject(Object):
    def __init__(self, image, coord, hp, max_heal_point):
        # объект типа: HealPointObject
        # print(image, coord, size)
        super().__init__(image, coord)
        self.add_type('HealPointObject')
        # максимальное количество жизней
        self.max_heal_point = max_heal_point
        # количество жизней
        self.heal_point = hp

    def get_hp(self):
        # возвращает кол-во хп
        return self.heal_point

    def get_max_hp(self):
        return self.max_heal_point

    def damage(self, damage, enemy=None):
        # наносит урон игроку (уменьшает запас хп)
        if damage > self.heal_point:
            self.heal_point = 0
            if enemy is not None:
                enemy.die()
        else:
            self.heal_point -= damage
        # print('Осталось', self.heal_point, 'hp')

    def heal(self, heal_point):
        # восстанавливает количесто хп, но не больше max_heal_point
        if int(heal_point) == int:
            if self.heal_point + heal_point > self.max_heal_point:
                self.heal_point = self.max_heal_point
            else:
                self.heal_point += heal_point

    def set_hp(self, number):
        # изменяет число хп на number
        if type(number) == int:
            self.heal_point = number

    def heal_point_upgrade(self, upgrade_point):
        # увеличевает кол-во хп у персонажа, например:  у персонажа повысился уровень, вырасло максимальное кол-во хп
        if type(upgrade_point) == int:
            self.max_heal_point += upgrade_point
            self.heal_point = self.max_heal_point

    def heal_point_downgrade(self, downgrade_point):
        # у персонажа уменьшилось макимальное кол-во хп, например: он устал, максимальное кол-во хп уменьшено
        if type(downgrade_point) == int:
            self.max_heal_point -= downgrade_point
            if self.heal_point > self.max_heal_point:
                self.heal_point = self.max_heal_point
            # self.heal_point -= downgrade_point


class MovingObject(HealPointObject):
    def __init__(self, image, coord, hp, max_heal_point, armor, food, max_food_point):
        # тип объекта: MovingObject
        super().__init__(image, coord, hp, max_heal_point)
        self.add_type('MovingObject')
        # очки еды
        self.food = food
        # максимальное количество еды
        self.max_food_point = max_food_point
        # это делается так
        if armor is not None and armor.is_type('Armor'):
            self.armor = armor
        else:
            self.armor = None
        # столкновение с одной из сторон
        self.collision_x_site = 0
        self.collision_y_site = 0
        self.x_vel = 0
        self.y_vel = 0
        # В self.armor записывается объект типа armor (класс находится выше)
        # объект у которого есть броня и голод

    def get_food(self):
        # возвращает уровень еды
        return self.food

    def get_max_food(self):
        return self.max_food_point

    def eat(self, food_point):
        # персонаж употребляет что-то, что восстанавливает уровень еды, но не больше, чем self.max_food_point
        if self.food + food_point > self.max_food_point:
            self.food = self.max_food_point
        else:
            self.food += food_point

    def set_food(self, n):
        self.food = n

    def hunger(self, n):
        if self.food <= n:
            self.food = 0
        else:
            self.food -= n

    def get_armor(self):
        # получить броню объекта может быть None
        return self.armor

    def collide(self, x_vel, y_vel, platforms):
        # проверка столкновения
        # если скорость по горизонту не равна нулю
        if x_vel != 0:
            # столкновений по оси икс нет
            self.collision_x_site = 0
        # если скорость по оси игрик не равна нулю
        elif y_vel != 0:
            # столкновений по оси игрик нет
            self.collision_y_site = 0
        # проходимся по списку стен с которыми можем столкнуться
        for pl in platforms:
            # если столкнулись
            if collide_rect(self, pl):
                # если скорость по оси икс больше 0
                if x_vel > 0:
                    # правая сторона равна левой строне объекта с которым мы столкнулись
                    self.rect.right = pl.rect.left
                    # столкновение справа
                    self.collision_x_site = 2
                # если скорость по оси икс меньше 0
                elif x_vel < 0:
                    # левая сторона объекта равна правой стороне объекта
                    self.rect.left = pl.rect.right
                    # столкновение слева
                    self.collision_x_site = 1
                # если скорость по оси игрик больше 0
                elif y_vel > 0:
                    # низ объекта равен верху объекта с которым чтолкнулись
                    self.rect.bottom = pl.rect.top
                    # столкновение снизу
                    self.collision_y_site = 2
                # если скорость по оси игрик меньше 0
                elif y_vel < 0:
                    # верх объекта равен инзу объекта с котрым столкнулись
                    self.rect.top = pl.rect.bottom
                    # столкновение сверху
                    self.collision_y_site = 1
            rect = self.rect
            self.rect = self.get_rect()
            # не лезь оно потом когда-нибудь заработает))
            # не фиксить я потом придумаю чтонибудь)
            # ты точно понял что не надо фиксить?
            # ты точно, точно понял?
            if collide_rect(self, pl.get_mask()):
                # если ты в доме то твой слой равен слою
                if self.home == pl:
                    self.set_layer(pl.get_layer() + 1)
                # если объект статичный то мы меняем только свой слой
                elif pl.is_type('Static'):
                    # мы перед статичным объектом
                    if pl.get_layer() + 1 > self.get_layer() and self.rect.bottom > pl.get_mask().rect.bottom:
                        self.set_layer(pl.get_layer() + 1)
                    # мы за статичным объектом
                    elif pl.get_layer() - 1 < self.get_layer() and self.rect.bottom < pl.get_mask().rect.bottom:
                        self.set_layer(pl.get_layer() - 1)
                # если это не статичный объект
                else:
                    # мы перед объектом
                    if self.get_layer() + 1 > pl.get_layer() and self.rect.bottom > pl.get_mask().rect.bottom:
                        pl.set_layer(self.get_layer() + 1)
                    # мы за объектом
                    elif pl.get_layer() + 1 > self.get_layer() and self.rect.bottom < pl.get_mask().rect.bottom:
                        self.set_layer(pl.get_layer() + 1)
            self.rect = rect


class AnimationObject(MovingObject):
    def __init__(self, images, coord, hp, max_heal_point, food, max_food_point, way_to_image, way_name, armor=None,
                 type='bmp'):
        self.die_f = False
        super().__init__(images, coord, hp, max_heal_point, armor, food, max_food_point)
        self.add_type('AnimationObject')
        self.die_frames = []
        self.way_name = way_name
        self.eat = 0
        self.die_frame = 0
        self.count_die_frames = 0
        # столкновение с одной из сторон
        self.collision_x_site = 0
        self.collision_y_site = 0
        # ускорение на одной из сторон
        self.x_vel = 0
        self.y_vel = 0

        # sites moving lists
        self.count_next_frame = 0
        self.frame = 0
        self.frames_forward = []
        self.frames_back = []
        self.frames_left = []
        self.frames_right = []

        # ускорение объекта (бег)
        self.speed_boost = False
        # downloading sprites
        self.way_to_image = way_to_image
        types = ['forward', 'back', 'left', 'right']
        for elem in types:
            for i in range(1, len(os.listdir(path=f'sprite/{way_to_image}/{elem}/{way_name}')) + 1):
                if elem == 'forward':
                    self.frames_forward.append(
                        Image(f'sprite/{way_to_image}/{elem}/{way_name}/{way_name}_{elem}_{i}.{type}'))
                if elem == 'back':
                    self.frames_back.append(Image(f'sprite/{way_to_image}/{elem}/{way_name}/{way_name}_{elem}_{i}.{type}'))
                if elem == 'left':
                    self.frames_left.append(Image(f'sprite/{way_to_image}/{elem}/{way_name}/{way_name}_{elem}_{i}.{type}'))
                if elem == 'right':
                    self.frames_right.append(
                        Image(f'sprite/{way_to_image}/{elem}/{way_name}/{way_name}_{elem}_{i}.{type}'))

    def die(self, filename=None, die_frames=None):
        self.die_f = True
        if die_frames is not None:
            for elem in die_frames[0]:
                self.die_frames.append(Object(filename + elem, (120, 120)))

    def draw(self):
        # если не столкнулись справа и ускарение направлено вправо
        if self.die_f is False:
            if self.x_vel == 0 and self.y_vel == 0:
                self.image = self.frames_forward[0].get_image()
            elif self.x_vel > 0 and not self.collision_x_site == 2:
                # переключаем на следующий кадр анимации ходьбы вправо
                self.image = self.frames_right[self.frame].get_image()
            # если не столкнулись слева и ускарение направлено влево
            elif self.x_vel < 0 and not self.collision_x_site == 1:
                # переключаем на следующий кадр анимации ходьбы влево
                self.image = self.frames_left[self.frame].get_image()
            # если не столкнулись снизу и ускарение направлено вниз
            elif self.y_vel > 0 and not self.collision_y_site == 2:
                # переключаем на следующий кадр анимации ходьбы вниз
                self.image = self.frames_forward[self.frame].get_image()
            # если не столкнулись сверху и скарение направлени вверх
            elif self.y_vel < 0 and not self.collision_y_site == 1:
                # переключаем на следующий кадр анимации ходьбы вверх
                self.image = self.frames_back[self.frame].get_image()
            # столкнулись слева
            elif self.collision_x_site == 1:
                # смотрим в стену слева
                self.image = self.frames_left[0].get_image()
            # если не столкнулись справа
            elif self.collision_x_site == 2:
                # смотрим в стенку справ
                self.image = self.frames_right[0].get_image()
            # если не столкнулись снизу
            elif self.collision_y_site == 2:
                # смотрим вниз
                self.image = self.frames_forward[0].get_image()
            # если не столкнулись сверху
            elif self.collision_y_site == 1:
                # то смотрим вверх
                self.image = self.frames_back[0].get_image()
            # переключиться на следующий кадр
            self.next_frame()
        else:
            self.image = self.die_frames[self.die_frame].get_image()
            self.next_die_frame()

    def resurrection(self):
        self.die_f = False
        self.set_food(self.get_max_food())
        self.die_frame = 0
        self.count_die_frames = 0
        self.set_hp(self.get_max_hp())
        self.rect.x, self.rect.y = (15, 15)

    def get_die(self):
        return self.die_f

    def next_die_frame(self):
        self.count_die_frames += 1
        if self.count_die_frames > 20 and self.die_frame < 9:
            self.count_die_frames = 0
            self.die_frame += 1

    def next_frame(self):
        # то как мы переключаем кадра в зависимости от типа перемещения
        # если бежим то быстрее если идём то медленее
        self.count_next_frame += 1
        if (self.count_next_frame > 4 and not self.speed_boost) or (self.count_next_frame > 2 and self.speed_boost):
            self.count_next_frame = 0
            self.frame += 1

        # если включён последний кадр перематываем в начало
        if self.frame == len(self.frames_forward) - 1:
            # устанавливаем первый кадр
            self.frame = 0


class Person(AnimationObject):
    def __init__(self, image, coord, hp, max_heal_point, food, max_food_point, name, way_to_image, way_name,
                 armor=None, type='bmp'):
        # тип объекта: Person
        super().__init__(image, coord, hp, max_heal_point, food, max_food_point, way_to_image, way_name, armor, type)
        self.add_type('Person')
        self.name = name
        # имя персонажа

    def get_name(self):
        # возвращает имя персонажа
        return self.name

    def set_name(self, new_name):
        # меняет имя персонажа
        if type(new_name) == str:
            self.name = new_name


class Eat(Item):
    def __init__(self, image, coord, name, max_count, hp, food, owner, armor=0, info=''):
        # объект типа: Eat
        super().__init__(image, coord, name, max_count, info)
        self.add_type('Eat')
        self.heal_point = hp
        self.armor = armor
        self.food = food
        # количество жизней, брони, голода которые он востанавливает (уменьшает)
        self.owner = owner
        # владелец еды

    def use(self):
        # поесть
        self.owner.eat(self.food)
        if self.heal_point >= 0:
            self.owner.heal(self.heal_point)
        else:
            self.owner.damage(abs(self.heal_point))
        if self.armor > 0:
            self.owner.armor.repair(self.armor)
        elif self.armor < 0:
            self.owner.armor.damage(abs(self.armor))


class EnemyBlock(Object):
    def __init__(self, filename, coord, damag, negative_effect=None):
        super().__init__(filename, coord)
        self.damag = damag
        self.add_type('enemy_spike')
        self.add_type('NPS')
        self.negative_effect = negative_effect
        self.coord = coord
        self.set_bg(True)

    def update(self, bots, objects, main_group, camera):
        for object in objects:
            if self.rect.colliderect(object.get_rect()) and object.is_type('HealPointObject'):
                self.attack(object)

    def attack(self, enemy):
        enemy.damage(self.damag)


class ImageButton(Object):
    def __init__(self, images, coord, action):
        super().__init__(images, coord)
        self.coord = coord
        self.action = action
        self.add_type('Static')

    def update(self, zero_coord):
        # asd
        pos_mouse = pygame.mouse.get_pos()
        pos = (zero_coord[0] + pos_mouse[0], zero_coord[1] + pos_mouse[1])
        # если кнопка льпущена и нажата на кнопку
        if self.rect.collidepoint(pos):
            self.action()
