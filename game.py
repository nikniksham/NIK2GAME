from create_level import *
from player import Player
from NPS_scripts import *
from main_window import run
from TestWeapon import *
from menu import run_menu

pygame.init()
# загружаем нужные переменные
load_data()
KILLED_ZOMBIE = 0
LEVEL = 1
# MAX_COUNT_ZOMBIE = 100
# размер одного бока
size = 30
# 1 чанк 16 на 16 картинок
# 1 чанк 480 на 480 пикселей
# 1 картинка 30 на 30 пикселей
# размер каты в мегачанках
chunk_count = ((0, 0), (2, 1))

run_menu()

# camera
camera = Camera(size_screen, (0, 0, 0))

# словарь картинок объектов мира
slow = {'bn': [Image('sprite/blocks_sprites/back_1.bmp').get_image(), Image('sprite/blocks_sprites/block_3.bmp').get_image(),
               Image('sprite/blocks_sprites/back_2.bmp').get_image(), Image('sprite/blocks_sprites/back_4.bmp').get_image()],
        'tn': [(Image('sprite/blocks_sprites/tree.bmp').get_image(), 13), (Image('sprite/blocks_sprites/tree_1.bmp').get_image(), 7),
               (Image('sprite/blocks_sprites/stone_2.bmp').get_image(), None)],
        'cn': 0.01}

map_slow = {'bn': [load_image('sprite\\blocks_sprites\\map_grass.png'), load_image('sprite\\blocks_sprites\\map_grass.png'),
                   load_image('sprite\\blocks_sprites\\map_grass.png'), load_image('sprite\\blocks_sprites\\map_grass.png')],
            'tn': [load_image('sprite\\blocks_sprites\\map_tree_1.png'), load_image('sprite\\blocks_sprites\\map_tree_2.png'),
                   load_image('sprite\\blocks_sprites\\map_stone.png')]}

# генерация мира
# image_map, main_chunk = make_level(slow, chunk_count, map_slow)
# загрузка мира
image_map, main_chunk = load_level('world_TEST.wrld', slow, map_slow)
# Создание group_helper - эта вещь помогает при спавне большого кол-ва одинаковых объектов
group_helper = GroupHelper()
# создаём самого героя
zombie_group = BotGroup('enemy', 'Зомби')
hero = Player('MainHero', (35, 35), 'person_sprites', 'Player')

# создаём сцену
scene = Level('first_scene', hero, main_chunk, camera)


class Missions:
    def __init__(self):
        self.summon_f = False

    def mission_1(self, then):
        Desert_eagle = WeaponObj('sprite/Weapon_sprites/Desert Eagle.bmp', (360, 360), 'DesertEagle', 1, 'simple',
                                 'simple', 2000, [1200, 1500], 60, then.screen, hero, 7, 90)
        AR15 = WeaponObj('sprite/Weapon_sprites/AR15.png', [100, 100], 'AR15', 1, 'simple', 'simple', 2500, [800, 1000],
                         3, then.screen, hero, 3000, 180)
        # bots = BotGroup('enemy', 'колючие платформы')
        # for x in range(300, 600, 60):
        #       print(bots.add_bot(EnemyBlock('sprite/blocks_sprites/spike.bmp', (x, 100), 1)))

        # then.scene.main_chunk.set_clear_chunk(build.rect)

        # print(len(bots.get_objects()))
        main_site = Site()
        build = Build(((3840, 3800)), 'sprite\\Building_sprites\\House.png', then.scene,
                      'sprite/Building_sprites/House_in.png', Rect((25, 120), (35, 70)))
        chest_1 = Chest('sprite/Interactive_objects/chest.bmp', ((3850, 3830)), scene, [Desert_eagle])
        main_site.add_object(build)
        main_site.add_object(chest_1)

        base = Site()
        main_home = Build((6840, 3900), 'sprite\\Building_sprites\\army tent.png', scene,
                          'sprite\\Building_sprites\\army_tent_in.png', Rect((35, 85), (35, 70)))
        base.add_object(main_home)
        chest_2 = Chest('sprite/Interactive_objects/chest.bmp', ((6850, 3930)), scene, [AR15])
        base.add_object(chest_2)
        bonfire = PassiveAnimationBuild('sprite/blocks_sprites/bonfire/', 7, (6855, 4060), scene)
        base.add_object(bonfire)
        palatka_1 = Build((6600, 3930), 'sprite/Building_sprites/Palatka/camp_1.png', scene)
        base.add_object(palatka_1)
        palatka_2 = Build((7100, 3880), 'sprite/Building_sprites/Palatka/camp_1.png', scene)
        base.add_object(palatka_2)
        palatka_3 = Build((6600, 4120), 'sprite/Building_sprites/Palatka/camp_1.png', scene)
        base.add_object(palatka_3)
        palatka_4 = Build((7100, 4080), 'sprite/Building_sprites/Palatka/camp_1.png', scene)
        base.add_object(palatka_4)
        palatka_5 = Build((6840, 4200), 'sprite/Building_sprites/Palatka/camp_1.png', scene)
        base.add_object(palatka_5)
        rect_2 = Rect((6600, 3880), (500, 400))
        then.scene.main_chunk.set_clear_chunk(build.get_rect())
        then.scene.main_chunk.set_clear_chunk(rect_2)
        print(then.scene.add_site(main_site))
        print(then.scene.add_site(base))

    def get_group(self):
        return zombie_group

    def wave(self, count, then):
        group_helper.summon(zombie_group, ['Zombie', 'sprite/Enemy_sprites/forward/Zombie/Zombie_forward_1.png',
                                           hero.get_coord(), 'Enemy_sprites', 'Zombie', 10, hero, camera, None, 'png'], count)
        if not self.summon_f:
            print(then.scene.add_bot_group(zombie_group))
            self.summon_f = True


# запускаем игру
run(camera, scene, Missions())