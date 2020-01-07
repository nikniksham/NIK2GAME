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
slow = {'bn': [Image('sprite/blocks_sprites/back_1.bmp'), Image('sprite/blocks_sprites/block_3.bmp'),
               Image('sprite/blocks_sprites/back_2.bmp'), Image('sprite/blocks_sprites/back_4.bmp')],
        'tn': [(Image('sprite/blocks_sprites/tree.bmp'), 13), (Image('sprite/blocks_sprites/tree_1.bmp'), 7),
               (Image('sprite/blocks_sprites/stone_2.bmp'), None)],
        'cn': 0.05}

map_slow = {'bn': [load_image('sprite\\blocks_sprites\\map_grass.png'), load_image('sprite\\blocks_sprites\\map_grass.png'),
               load_image('sprite\\blocks_sprites\\map_grass.png'), load_image('sprite\\blocks_sprites\\map_grass.png')],
        'tn': [load_image('sprite\\blocks_sprites\\map_tree_1.png'), load_image('sprite\\blocks_sprites\\map_tree_2.png'),
               load_image('sprite\\blocks_sprites\\map_stone.png')],
        'cn': 0.05}

# генерация мира
# walls_group, bg_group, image_map = make_level(slow, chunk_count, map_slow)
# загрузка мира
# не анимировано!!
walls_group, bg_group, image_map = load_level('world_TEST.wrld', slow, map_slow)

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

# создаём сцену
scene = Level('first_scene', hero)

# добавляем чанк переднего плана
scene.add_main_chunk(walls_group)
# добавляем чанк заднего плана
scene.add_main_chunk(bg_group)


def mission_1(then):
    bots = Site()
    for x in range(300, 600, 100):
        bots.add_object()


missions = [mission_1]
# запускаем игру
run(camera, scene, image_map, missions)