from create_level import *
from player import Player
from NPS_scripts import *
from main_window import run

pygame.init()
lol = pygame.display.set_mode((10, 10))
# загружаем нужные переменные
load_data()
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

# загрузка картинок

# смерть персонажа
die_frames = ['Player_fall_1.bmp', 'Player_fall_2.bmp', 'Player_fall_5.bmp',
              'Player_fall_6.bmp', 'Player_die_1.bmp', 'Player_die_2.bmp', 'Player_die_3.bmp', 'Player_die_4.bmp',
              'Player_die_5.bmp', 'Player_die_6.bmp']

# выстрел из пистолета
shoot_image = ['Desert Eagle shoot 1.bmp', 'Desert Eagle shoot 2.bmp', 'Desert Eagle shoot 3.bmp',
               'Desert Eagle shoot 4.bmp', 'Desert Eagle shoot 5.bmp', 'Desert Eagle shoot 6.bmp',
               'Desert Eagle shoot 7.bmp', 'Desert Eagle shoot 8.bmp']


# создаём самого героя
hero = Player('MainHero', (35, 35), 'person_sprites', 'Player')

soldier_1 = WithSomeone('Soldier_1', 'sprite/NPS_sprites/forward/NPS_soldier_1/NPS_soldier_1_forward_1.bmp', (100, 100),
                        'NPS_sprites', 'NPS_soldier_1')
soldier_2 = WithSomeone('Soldier_1', 'sprite/NPS_sprites/forward/NPS_soldier_1/NPS_soldier_1_forward_1.bmp', (200, 100),
                        'NPS_sprites', 'NPS_soldier_1')
soldier_3 = WithSomeone('Soldier_1', 'sprite/NPS_sprites/forward/NPS_soldier_1/NPS_soldier_1_forward_1.bmp', (100, 200),
                        'NPS_sprites', 'NPS_soldier_1')
soldier_4 = WithSomeone('Soldier_1', 'sprite/NPS_sprites/forward/NPS_soldier_1/NPS_soldier_1_forward_1.bmp', (140, 90),
                        'NPS_sprites', 'NPS_soldier_1')
soldier_5 = WithSomeone('Soldier_1', 'sprite/NPS_sprites/forward/NPS_soldier_1/NPS_soldier_1_forward_1.bmp', (200, 200),
                        'NPS_sprites', 'NPS_soldier_1')
general = WithSomeone('General', 'sprite/NPS_sprites/forward/NPS_general/NPS_general_forward_1.bmp', (500, 500),
                      'NPS_sprites', 'NPS_general')

# создаём сцену
scene = Level('first_scene', hero, main_chunk)


def mission_1(then):
    #bots = BotGroup('enemy', 'колючие платформы')
    #for x in range(300, 600, 60):
        #print(bots.add_bot(EnemyBlock('sprite/blocks_sprites/spike.bmp', (x, 100), 1)))
    site = Site()
    build = Build((10, 100), 'sprite/Building_sprites/Palatka/camp_1.png')
    site.add_object(build)
    build = Build((110, 100), 'sprite/Building_sprites/Palatka/camp_1.png')
    then.scene.main_chunk.set_clear_chunk(build.rect)
    site.add_object(build)
    build = Build((210, 100), 'sprite/Building_sprites/Palatka/camp_1.png')
    site.add_object(build)
    build = Build((310, 100), 'sprite/Building_sprites/Palatka/camp_1.png')
    site.add_object(build)
    build = Build((10, 300), 'sprite/Building_sprites/Palatka/camp_1.png')
    site.add_object(build)
    build = Build((110, 300), 'sprite/Building_sprites/Palatka/camp_1.png')
    then.scene.main_chunk.set_clear_chunk(build.rect)
    site.add_object(build)
    build = Build((210, 300), 'sprite/Building_sprites/Palatka/camp_1.png')
    site.add_object(build)
    build = Build((310, 300), 'sprite/Building_sprites/Palatka/camp_1.png')
    site.add_object(build)
    # print(len(bots.get_objects()))
    print(then.scene.add_site(site))


missions = [mission_1]
# запускаем игру
run(camera, scene, image_map, missions)