from Framework import Application, Widget, load_image, scale_to, Text, create_text, ProgressBar
from win32api import GetSystemMetrics
import pygame
from MainClasss import Timer


class Slot(Widget):
    def __init__(self, image, coord, pos_inventory, inventory):
        super().__init__(image, coord)
        self.pos = pos_inventory
        self.inventory = inventory

    def get_surface(self):
        item = self.inventory.get_items(self.pos[0], self.pos[1])[:][0]
        if item is not None:
            image = self.images_orig[0]
            image.blit(item.get_image(), (0, 0))
            self.set_image(image)
        else:
            self.set_image(self.images_orig[0])
        return self.image


class GameScreen(Widget):
    def __init__(self, camera, scene,  coord, active=False, is_zooming=False, zoom=1, max_zoom=1, min_zoom=0.15, is_scrolling_x=False, is_scrolling_y=False, is_scroll_line_x=False, is_scroll_line_y=False, scroll_x=0, scroll_y=0, size=None, stock=True):
        surface = camera.draw(scene)
        self.camera = camera
        self.scene = scene
        super().__init__(surface, coord, active, is_zooming, zoom, max_zoom, min_zoom, is_scrolling_x, is_scrolling_y, is_scroll_line_x, is_scroll_line_y, scroll_x, scroll_y)

    def hero_update(self):
        # стрельба
        if self.app.hero.weapon is not None and self.get_active():
            print(self.get_active())
            self.app.hero.weapon.shoot(self.camera, self.app.mouse_pressed(1), self.app.hero, 'sprite/bullets/standard_bullet.bmp',
                                   self.scene)
        # ходьба и бег
        left = self.app.key_pressed(pygame.K_a)
        right = self.app.key_pressed(pygame.K_d)
        up = self.app.key_pressed(pygame.K_w)
        down = self.app.key_pressed(pygame.K_s)
        shift = self.app.key_pressed(pygame.K_LSHIFT) or self.app.key_pressed(pygame.K_RSHIFT)
        self.app.hero.update(left, right, up, down, self.scene.get_walls(self.app.hero.get_rect()), shift)

    def get_surface(self):
        self.hero_update()
        self.set_image(self.camera.draw(self.scene))
        return self.image


class Game(Application):
    def __init__(self, size_screen, camera, scene, missions, full_screen=True):
        super().__init__(size_screen, full_screen=full_screen)
        self.mission = missions
        self.mission_index = 0
        self.camera = camera
        self.timer = Timer()
        self.timer.set_game(self)
        self.scene = scene
        self.game_sceen = GameScreen(camera, scene, (0, 0), zoom=1, is_zooming=False, min_zoom=0.3, stock=False)
        self.add_widget(self.game_sceen, 0)
        self.hot_keys = [pygame.K_F1, pygame.K_RETURN, pygame.K_ESCAPE]
        self.draw_frs = Text('0', 30, (-10, 10))
        self.add_widget(self.draw_frs, 2)
        self.hero = scene.get_main_hero()
        self.lkm_used = False
        self.add_event(self.funks)
        self.add_event(self.update_interface)

    def funks(self):
        if self.key_pressed(self.hot_keys[0]):
            self.camera.create()
            self.update_screen(self.widht, self.height)
        elif self.key_pressed(self.hot_keys[1]) and self.mission_index == 0:
            self.mission[self.mission_index](self)
            self.mission_index += 1
        elif self.key_pressed(self.hot_keys[2]):
            self.running = False

    def update_interface(self):
        self.draw_frs.update_text(text=str(int(self.clock.get_fps())))
        self.lkm_used = False


def run(camera, scene, map_image, missions):
    size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))
    game = Game(size_screen, camera, scene, missions, full_screen=True)
    REPOSITORY = 'sprite\\User_Interface\\'
    spase = 10
    slot = scale_to(load_image(REPOSITORY + 'enemy_slot.bmp', -1),
                    (int(size_screen[1] * 0.05), int(size_screen[1] * 0.05)))
    #timate_image = scale_to(load_image(REPOSITORY + 'test name.png', -1),
     #                       (int(5 * size_screen[1] * 0.05), int(1.5 * size_screen[1] * 0.05)))
    #game_event = scale_to(load_image(REPOSITORY + 'game event.png', -1),
    #                      (int(0.8 * size_screen[1] * 0.33), int(size_screen[1] * 0.33)))
    #chat = scale_to(load_image(REPOSITORY + 'chat.png', -1),
    #                (int(0.8 * size_screen[1] * 0.33), int(size_screen[1] * 0.33)))
    #hp_line = scale_to(load_image(REPOSITORY + 'hael point_line.png', -1),
    #                   (int(size_screen[1] * 0.33), int(size_screen[1] * 0.05)))
    #eat_line = scale_to(load_image(REPOSITORY + 'eat point_line.png', -1),
    #                    (int(size_screen[1] * 0.33), int(size_screen[1] * 0.05)))

    inventory = scene.get_main_hero().inventory
    hot_barr_1 = Slot(slot, (spase, spase), (0, 0), inventory)
    hot_barr_2 = Slot(slot, (spase * 2 + int(size_screen[1] * 0.05), spase), (1, 0), inventory)
    hot_barr_3 = Slot(slot, (spase * 3 + int(size_screen[1] * 0.05) * 2, spase), (2, 0), inventory)
    hot_barr_4 = Slot(slot, (spase * 4 + int(size_screen[1] * 0.05) * 3, spase), (3, 0), inventory)
    hot_barr_5 = Slot(slot, (spase * 5 + int(size_screen[1] * 0.05) * 4, spase), (4, 0), inventory)
    hot_barr_6 = Slot(slot, (spase * 6 + int(size_screen[1] * 0.05) * 5, spase), (5, 0), inventory)
    hot_barr_7 = Slot(slot, (spase * 7 + int(size_screen[1] * 0.05) * 6, spase), (6, 0), inventory)
    hot_barr_8 = Slot(slot, (spase * 8 + int(size_screen[1] * 0.05) * 7, spase), (7, 0), inventory)
    hot_barr_9 = Slot(slot, (spase * 9 + int(size_screen[1] * 0.05) * 8, spase), (8, 0), inventory)
    hot_barr_10 = Slot(slot, (spase * 10 + int(size_screen[1] * 0.05) * 9, spase), (9, 0), inventory)

    widget_map = Widget(map_image, coord=(-spase, spase), zoom=0.17, max_zoom=0.18, min_zoom=0.1,  is_zooming=True, size=(int(size_screen[1] * 0.33), int(size_screen[1] * 0.33)), is_scrolling_x=True, is_scrolling_y=True)

    # timete_1 = Widget(timate_image, (int(size_screen[0] * 0.2), -spase))
    # timete_2 = Widget(timate_image, (int(size_screen[0] * 0.4), -spase))
    # timete_3 = Widget(timate_image, (int(size_screen[0] * 0.6), -spase))

    # event = Widget(game_event, (-spase, -spase))
    # chat = Widget(chat, (spase, -int(size_screen[1] * 0.3)))

    # hp_line = Widget(hp_line, (-spase, 2 * spase + int(size_screen[1] * 0.33)))
    # eat_line = Widget(eat_line, (-spase, 3 * spase + int(size_screen[1] * 0.33) + int(size_screen[1] * 0.05)))

    #game.add_widget(eat_line)
    #game.add_widget(hp_line)
    #game.add_widget(event)
    #game.add_widget(chat)
    #game.add_widget(timete_1)
    #game.add_widget(timete_2)
    #game.add_widget(timete_3)
    game.add_widget(widget_map)
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