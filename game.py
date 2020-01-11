from create_level import *
from player import Player
from NPS_scripts import *
from main_window import run
from TestWeapon import *

pygame.init()
lol = pygame.display.set_mode((10, 10))
# загружаем нужные переменные
load_data()
KILLED_ZOMBIE = 0
LEVEL = 1
MAX_COUNT_ZOMBIE = 0
# размер одного бока
size = 30
# 1 чанк 16 на 16 картинок
# 1 чанк 480 на 480 пикселей
# 1 картинка 30 на 30 пикселей
# размер каты в мегачанках
chunk_count = ((0, 0), (1, 1))

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

# создаём самого героя
hero = Player('MainHero', (35, 35), 'person_sprites', 'Player')

# создаём сцену
scene = Level('first_scene', hero, main_chunk, camera)


def mission_1(then):
    zombie_group = BotGroup('enemy', 'Зомби')
    Desert_eagle = WeaponObj('sprite/Weapon_sprites/Desert Eagle.bmp', (360, 360), 'DesertEagle', 1, 'simple', 'simple',
                             2000, [120, 150], 60, then.screen, hero, 7, 90)
    AR15 = WeaponObj('sprite/Weapon_sprites/AR15.png', [100, 100], 'AR15', 1, 'simple', 'simple', 2500, [80, 100], 8,
                     then.screen, hero, 30, 180)
    healpoint_NPS = Image('sprite/NPS_sprites/healpoint_nps.bmp')
    then.scene.main_hero.weapon = AR15
    # bots = BotGroup('enemy', 'колючие платформы')
    # for x in range(300, 600, 60):
    #       print(bots.add_bot(EnemyBlock('sprite/blocks_sprites/spike.bmp', (x, 100), 1)))
    group_helper = GroupHelper()
    group_helper.summon(zombie_group, ['Zombie', 'sprite/Enemy_sprites/forward/Zombie/Zombie_forward_1.png',
                                       hero.get_coord(), 'Enemy_sprites', 'Zombie', 10, hero,  None, 'png'], MAX_COUNT_ZOMBIE)

    site_1 = Site()
    site = Site()
    build = Build((10, 100), 'sprite/Building_sprites/Palatka/camp_1.png', then.scene)
    site.add_object(build)
    build = Build((110, 100), 'sprite/Building_sprites/Palatka/camp_1.png', then.scene)
    # then.scene.main_chunk.set_clear_chunk(build.rect)
    site.add_object(build)
    build = Build((210, 100), 'sprite/Building_sprites/Palatka/camp_1.png', then.scene)
    site.add_object(build)
    build = Build((310, 100), 'sprite/Building_sprites/Palatka/camp_1.png', then.scene)
    site.add_object(build)
    build = Build((10, 300), 'sprite/Building_sprites/Palatka/camp_1.png', then.scene)
    site.add_object(build)
    build = Build((110, 300), 'sprite/Building_sprites/Palatka/camp_1.png', then.scene)
    then.scene.main_chunk.set_clear_chunk(build.rect)
    site.add_object(build)
    build = Build((210, 300), 'sprite/Building_sprites/Palatka/camp_1.png', then.scene)
    site.add_object(build)
    build = Build((310, 300), 'sprite/Building_sprites/Palatka/camp_1.png', then.scene)
    site.add_object(build)
    # print(len(bots.get_objects()))
    build = Build((10, 100), 'sprite\\Building_sprites\\House.png', then.scene, 'sprite/Building_sprites/House_in.png',
                  Rect((25, 120), (35, 70)))
    site_1.add_object(build)
    print(then.scene.add_bot_group(zombie_group))
    print(then.scene.add_site(site_1))


missions = [mission_1]
# запускаем игру
run(camera, scene, image_map, missions)