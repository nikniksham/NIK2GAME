from Framework import Application, Widget, load_image, scale_to, Text, create_text, ProgressBar
from win32api import GetSystemMetrics
import pygame
from pygame import Surface
from MainClasss import Timer


REPOSITORY = 'sprite\\User_Interface\\'


# не оптимизировано и работает криво
# не использовать
class MapWidget(Widget):
    def __init__(self, image_map, coord, size):
        super().__init__(image_map, coord, is_zooming=True, zoom=0.1, is_scrolling_x=True, is_scrolling_y=True, size=size, stock=False)

    def update(self, event):
        pass

    def zoom_update(self, event):
        pass

    def set_image(self, image):
        self.image_orig = image
        surface = Surface(self.size)
        surface.blit(self.image_orig, (-self.scroll_x, -self.scroll_y))
        self.image = surface

    def zoom_into(self, into: bool):
        if into:
            self.zoom += self.zoom * 0.1
            if self.zoom > self.max_zoom:
                self.zoom = self.max_zoom
        else:
            self.zoom -= self.zoom * 0.1
            if self.zoom < self.min_zoom:
                self.zoom = self.min_zoom

    def get_surface(self):
        self.scroll_x, self.scroll_y = map(lambda a: a // 3, self.app.camera.get_coord())
        self.set_image(self.images_orig[0])
        return self.image


class Slot(Widget):
    def __init__(self, image, coord, pos_inventory, inventory):
        image = image.copy()
        self.size_image = image.get_size()
        super().__init__(image, coord)
        self.pos = pos_inventory
        self.inventory = inventory
        self.key = (pos_inventory[0] + 1) % 10

    def get_surface(self):
        item = self.inventory.get_items(self.pos[0], self.pos[1])[:][0]
        if item is not None:
            image = self.images_orig[0].copy()
            size = item.original_image.get_size()
            y = size[1] / size[0]
            image.blit(scale_to(item.original_image, (self.size_image[0] - 10, int(self.size_image[1] * y))), (5, (self.size_image[1] - int(self.size_image[1] * y)) // 3))
            count = create_text(str(item.get_count()), 15, (255, 255, 255))
            size = count.get_size()
            image.blit(count, (self.size_image[0] - size[0] - 5, self.size_image[1] - size[1] - 4))
            # лагакет
            # self.set_image(image)
            self.image = image
        else:
            self.image = self.images_orig[0]
        return self.image

    def update(self, event):
        print(self.pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.app.hero.in_hand_index = self.pos[0]



class GameScreen(Widget):
    def __init__(self, camera, scene,  coord, active=False, is_zooming=False, zoom=1, max_zoom=1, min_zoom=0.15,
                 is_scrolling_x=False, is_scrolling_y=False, is_scroll_line_x=False, is_scroll_line_y=False, scroll_x=0,
                 scroll_y=0, size=None, stock=True):
        surface = camera.draw(scene)
        self.camera = camera
        self.scene = scene
        super().__init__(surface, coord, active, is_zooming, zoom, max_zoom, min_zoom, is_scrolling_x, is_scrolling_y,
                         is_scroll_line_x, is_scroll_line_y, scroll_x, scroll_y)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.scene.button_update()

    def hero_update(self):
        # стрельба
        if self.app.hero.get_in_hand() is not None and self.app.hero.get_in_hand().is_type('Weapon') and  self.app.hero.home is None:
            self.app.hero.get_in_hand().shoot(self.camera, self.app.mouse_pressed(1), self.app.hero,
                                       'sprite/bullets/standard_bullet.bmp', self.scene)
        # ходьба и бег
        left = self.app.key_pressed(pygame.K_a)
        right = self.app.key_pressed(pygame.K_d)
        up = self.app.key_pressed(pygame.K_w)
        down = self.app.key_pressed(pygame.K_s)
        shift = self.app.key_pressed(pygame.K_LSHIFT) or self.app.key_pressed(pygame.K_RSHIFT)
        self.app.hero.update(left, right, up, down, self.scene.get_walls(self.app.hero.get_rect()), shift)

    def get_surface(self):
        self.hero_update()
        self.image = self.camera.draw(self.scene)
        return self.image


class Game(Application):
    def __init__(self, missions, size_screen, camera, scene, full_screen=True):
        super().__init__(size_screen, full_screen=full_screen)
        self.missions = missions
        self.mission_index = 0
        self.camera = camera
        self.timer = Timer()
        self.timer.set_game(self)
        self.one_wave = 100
        self.scene = scene
        space = 10
        red = (255, 0, 0)
        barr_back = load_image(REPOSITORY + 'barr back.png', -1)
        barr_back = scale_to(barr_back, (int(size_screen[1] * 0.33), 25))
        barr_top = load_image(REPOSITORY + 'barr_front.png', (255, 255, 255))
        barr_top = scale_to(barr_top, (int(size_screen[1] * 0.33), 25))
        self.hp_line = ProgressBar(barr_top, barr_back, (-space, -space), red, red, 1)
        self.game_screen = GameScreen(camera, scene, (0, 0), zoom=1, is_zooming=False, min_zoom=0.3, stock=False)
        self.add_widget(self.game_screen, 0)
        self.add_widget(self.hp_line)
        self.hot_keys = [pygame.K_F1, pygame.K_RETURN, pygame.K_ESCAPE]
        self.draw_time = Text('0', 30, (-80, 10))
        self.draw_frs = Text('0', 30, (-10, 10))
        self.add_widget(self.draw_frs, 2)
        self.add_widget(self.draw_time, 2)
        self.hero = scene.get_main_hero()
        self.lkm_used = False
        self.add_event(self.timer.update_timer)
        self.add_event(self.funks)
        self.add_event(self.update_interface)
        self.add_event(self.update_mission)

    def funks(self):
        if self.key_pressed(self.hot_keys[0]):
            self.camera.create()
            self.update_screen(self.widht, self.height)
        elif self.key_pressed(self.hot_keys[1]) and self.mission_index == 0:
            self.mission_index += 1
            self.missions.mission_1(self)
        elif self.key_pressed(self.hot_keys[2]):
            self.running = False

    def update_mission(self):
        self.draw_time.update_text(text=str(self.timer.get_time()[0]))
        if self.timer.get_time()[0] >= 20:
            pass
            # это на до заменить
            # group = self.missions.wave(0, self)

    def update_interface(self):
        self.draw_frs.update_text(text=str(int(self.clock.get_fps())))
        self.hp_line.update_bar(self.hero.heal_point / self.hero.max_heal_point)
        self.lkm_used = False

    def draw_scene(self):
        self.game_screen.set_image(self.camera.draw(self.scene))
        self.render(0)


def run(camera, scene, map_image, missions):
    size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))
    game = Game(missions, size_screen, camera, scene, full_screen=True)
    REPOSITORY = 'sprite\\User_Interface\\'
    space = 10
    slot = scale_to(load_image(REPOSITORY + 'enemy_slot.bmp', -1),
                    (int(size_screen[1] * 0.05), int(size_screen[1] * 0.05)))
    # timate_image = scale_to(load_image(REPOSITORY + 'test name.png', -1),
    #                        (int(5 * size_screen[1] * 0.05), int(1.5 * size_screen[1] * 0.05)))
    # game_event = scale_to(load_image(REPOSITORY + 'game event.png', -1),
    #                      (int(0.8 * size_screen[1] * 0.33), int(size_screen[1] * 0.33)))
    # chat = scale_to(load_image(REPOSITORY + 'chat.png', -1),
    #                (int(0.8 * size_screen[1] * 0.33), int(size_screen[1] * 0.33)))
    # hp_line = scale_to(load_image(REPOSITORY + 'hael point_line.png', -1),
    #                   (int(size_screen[1] * 0.33), int(size_screen[1] * 0.05)))
    # eat_line = scale_to(load_image(REPOSITORY + 'eat point_line.png', -1),
    #                    (int(size_screen[1] * 0.33), int(size_screen[1] * 0.05)))

    inventory = scene.get_main_hero().inventory
    hot_barr_1 = Slot(slot, (space, space), (0, 0), inventory)
    hot_barr_2 = Slot(slot, (space * 2 + int(size_screen[1] * 0.05), space), (1, 0), inventory)
    hot_barr_3 = Slot(slot, (space * 3 + int(size_screen[1] * 0.05) * 2, space), (2, 0), inventory)
    hot_barr_4 = Slot(slot, (space * 4 + int(size_screen[1] * 0.05) * 3, space), (3, 0), inventory)
    hot_barr_5 = Slot(slot, (space * 5 + int(size_screen[1] * 0.05) * 4, space), (4, 0), inventory)
    hot_barr_6 = Slot(slot, (space * 6 + int(size_screen[1] * 0.05) * 5, space), (5, 0), inventory)
    hot_barr_7 = Slot(slot, (space * 7 + int(size_screen[1] * 0.05) * 6, space), (6, 0), inventory)
    hot_barr_8 = Slot(slot, (space * 8 + int(size_screen[1] * 0.05) * 7, space), (7, 0), inventory)
    hot_barr_9 = Slot(slot, (space * 9 + int(size_screen[1] * 0.05) * 8, space), (8, 0), inventory)
    hot_barr_10 = Slot(slot, (space * 10 + int(size_screen[1] * 0.05) * 9, space), (9, 0), inventory)

    # widget_map = MapWidget(map_image, coord=(-space, space), size=(int(size_screen[1] * 0.33), int(size_screen[1] * 0.33)))

    # timete_1 = Widget(timate_image, (int(size_screen[0] * 0.2), -spase))
    # timete_2 = Widget(timate_image, (int(size_screen[0] * 0.4), -spase))
    # timete_3 = Widget(timate_image, (int(size_screen[0] * 0.6), -spase))

    # event = Widget(game_event, (-spase, -spase))
    # chat = Widget(chat, (spase, -int(size_screen[1] * 0.3)))

    # eat_line = Widget(eat_line, (-spase, 3 * spase + int(size_screen[1] * 0.33) + int(size_screen[1] * 0.05)))

    # game.add_widget(eat_line)
    # game.add_widget(event)
    # game.add_widget(chat)
    # game.add_widget(timete_1)
    # game.add_widget(timete_2)
    # game.add_widget(timete_3)
    # game.add_widget(widget_map)
    game.add_widget(hot_barr_1)
    game.add_widget(hot_barr_2)
    game.add_widget(hot_barr_3)
    game.add_widget(hot_barr_4)
    game.add_widget(hot_barr_5)
    game.add_widget(hot_barr_6)
    game.add_widget(hot_barr_7)
    game.add_widget(hot_barr_8)
    game.add_widget(hot_barr_9)
    game.add_widget(hot_barr_10)
    game.update_screen(game.widht, game.height)
    game.run()