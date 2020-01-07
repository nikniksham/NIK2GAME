from Framework import Application, Widget, load_image, scale_to, Text, create_text, ProgressBar
from win32api import GetSystemMetrics
import pygame


class Game(Application):
    def __init__(self, size_screen, camera, scene, full_screen=True):
        super().__init__(size_screen, full_screen)
        self.camera = camera
        self.scene = scene
        self.game_sceen = Widget(camera.draw(scene), (0, 0))
        self.add_widget(self.game_sceen, 0)
        self.hotceys = [pygame.K_F1]
        self.hero = scene.get_main_hero()

    def reset_cam(self):
        if self.pressed_key(self.hotceys[0]):
            self.camera.create()

    def hero_update(self):
        # стрельба
        #if self.mouse_pressed(1):
            #self.hero.weapon.spawn_bullet(self.camera, self.hero, 'sprite/bullets/standard_bullet.bmp', !!!!bulets)
        # ходьба и бег
        left = self.key_pressed(pygame.K_a)
        right = self.key_pressed(pygame.K_d)
        up = self.key_pressed(pygame.K_w)
        down = self.key_pressed(pygame.K_s)
        shift = self.key_pressed(pygame.K_LSHIFT) or self.key_pressed(pygame.K_RSHIFT)
        #self.hero.update(left, right, up, down, walls_group, enemy_group, shift)

    def draw_scene(self):
        pass


def run(camera, scene, map_image):
    size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))
    game = Game(size_screen, camera, scene, full_screen=True)
    REPOSITORY = 'sprite\\User_Interface\\'
    spase = 10
    slot = scale_to(load_image(REPOSITORY + 'enemy_slot.bmp', -1),
                    (int(size_screen[1] * 0.05), int(size_screen[1] * 0.05)))
    image_map = scale_to(map_image,
                         (int(size_screen[1] * 0.33), int(size_screen[1] * 0.33)))
    timate_image = scale_to(load_image(REPOSITORY + 'test name.png', -1),
                            (int(5 * size_screen[1] * 0.05), int(1.5 * size_screen[1] * 0.05)))
    game_event = scale_to(load_image(REPOSITORY + 'game event.png', -1),
                          (int(0.8 * size_screen[1] * 0.33), int(size_screen[1] * 0.33)))
    chat = scale_to(load_image(REPOSITORY + 'chat.png', -1),
                    (int(0.8 * size_screen[1] * 0.33), int(size_screen[1] * 0.33)))
    hp_line = scale_to(load_image(REPOSITORY + 'hael point_line.png', -1),
                       (int(size_screen[1] * 0.33), int(size_screen[1] * 0.05)))
    eat_line = scale_to(load_image(REPOSITORY + 'eat point_line.png', -1),
                        (int(size_screen[1] * 0.33), int(size_screen[1] * 0.05)))
    fon = load_image(REPOSITORY + 'fon2.png')

    hot_barr_1 = Widget(slot, (spase, spase))
    hot_barr_2 = Widget(slot, (spase * 2 + int(size_screen[1] * 0.05), spase))
    hot_barr_3 = Widget(slot, (spase * 3 + int(size_screen[1] * 0.05) * 2, spase))
    hot_barr_4 = Widget(slot, (spase * 4 + int(size_screen[1] * 0.05) * 3, spase))
    hot_barr_5 = Widget(slot, (spase * 5 + int(size_screen[1] * 0.05) * 4, spase))
    hot_barr_6 = Widget(slot, (spase * 6 + int(size_screen[1] * 0.05) * 5, spase))
    hot_barr_7 = Widget(slot, (spase * 7 + int(size_screen[1] * 0.05) * 6, spase))
    hot_barr_8 = Widget(slot, (spase * 8 + int(size_screen[1] * 0.05) * 7, spase))
    hot_barr_9 = Widget(slot, (spase * 9 + int(size_screen[1] * 0.05) * 8, spase))
    hot_barr_10 = Widget(slot, (spase * 10 + int(size_screen[1] * 0.05) * 9, spase))

    widget_map = Widget(image_map, (-spase, spase), is_zooming=True)

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
    game.run()