from create_level import *
from player import Player
from win32api import GetSystemMetrics
from multiprocessing.pool import ThreadPool
from NPS_scripts import *
from TestWeapon import *

pool_1 = ThreadPool(processes=1)
pool_2 = ThreadPool(processes=1)

# загружаем нужные переменные
load_data()
# создание нужных переменных
# размер одного бока
size = 30
# берйм ваше разрешение вашего экрана
# size_screen = (GetSystemMetrics(0), GetSystemMetrics(1))

size_screen = (1920, 1080)

# 1 чанк 16 на 16 картинок
# 1 чанк 480 на 480 пикселей
# 1 картинка 30 на 30 пикселей
# размер каты в чанках
chunk_count = ((0, 0), (1, 1))
# size_screen = (1080, 720)

# camera
camera = Camera(size_screen, (0, 0, 0),
                border_map=(
                    -200, chunk_count[1][1] * 16 * 16 * size + 1000, -200, chunk_count[1][0] * 16 * 16 * size + 1000))

# walls
# создаём задний фон и объекты на переднем плане
# словарь картинок
slow = {'bn': [Image('sprite/blocks_sprites/back_1.bmp'), Image('sprite/blocks_sprites/block_3.bmp'),
               Image('sprite/blocks_sprites/back_2.bmp'), Image('sprite/blocks_sprites/back_4.bmp')],
        'tn': [(Image('sprite/blocks_sprites/tree.bmp'), 13), (Image('sprite/blocks_sprites/tree_1.bmp'), 7),
               (Image('sprite/blocks_sprites/stone_2.bmp'), None)],
        'cn': 0.01,
        'bs': [Image('sprite/blocks_sprites/sand_1.bmp')],
        'ts': [(Image('sprite/blocks_sprites/stone_1.bmp'), None), (Image('sprite/blocks_sprites/Cactus_1.bmp'), None)],
        'cs': 0.01}

if chunk_count == ((0,), (1, 1)):
    chunk_count_1 = (chunk_count[0], (chunk_count[1][0], chunk_count[1][1] // 2))
    chunk_count_2 = ((chunk_count[1][0], chunk_count[1][1] // 2), chunk_count[1])
    print(chunk_count_1, chunk_count_2, 'gff')

    # start threads
    async_result = pool_1.apply_async(make_level, (list(slow.keys()), slow, chunk_count_1))
    async_result_1 = pool_2.apply_async(make_level, (list(slow.keys()), slow, chunk_count_2))
    # join threads to the main thread
    walls_group, bg_group = async_result.get()
    walls_group_1, bg_group_1 = async_result_1.get()
    print(walls_group_1, bg_group_1, walls_group == bg_group, walls_group == walls_group_1)
    print(len(walls_group.chunks), 'l')
    walls_group = walls_group + walls_group_1
    print(len(walls_group.chunks), 'll')
    print(len(bg_group.chunks), 'lll')
    bg_group = bg_group + bg_group_1
    print(bg_group)
    print(len(bg_group.chunks), 'llll')
    print(type(walls_group))
else:
    walls_group, bg_group = make_level(list(slow.keys()), slow, chunk_count)
# создание героя

# картинки в для анимаций
# движение вперёд
# смерть
screen = camera.get_screen()

die_frames = ['Player_fall_1.bmp', 'Player_fall_2.bmp', 'Player_fall_5.bmp',
              'Player_fall_6.bmp', 'Player_die_1.bmp', 'Player_die_2.bmp', 'Player_die_3.bmp', 'Player_die_4.bmp',
              'Player_die_5.bmp', 'Player_die_6.bmp']
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
spike = EnemyBlock('sprite/blocks_sprites/spike.bmp', (480, 720), 1)
spike2 = EnemyBlock('sprite/blocks_sprites/spike.bmp', (600, 720), 1)
spike3 = EnemyBlock('sprite/blocks_sprites/spike.bmp', (720, 720), 1)
spike4 = EnemyBlock('sprite/blocks_sprites/spike.bmp', (840, 720), 1)
enemy_group = Group('sprite/blocks_sprites/spike.bmp', [spike, spike2, spike3, spike4])
NPS_group = Group('sprite/NPS_sprites/forward/NPS_soldier_1/NPS_soldier_1_forward_1.bmp',
                  [soldier_1, soldier_2, soldier_3, soldier_4, soldier_5, general])# создаём сцену (карту)
# создаём сцену
scene = Level('sprite/blocks_sprites/block_1.bmp', 'first_scene',
              (chunk_count[0] * 16 * 16 * size, chunk_count[0] * 16 * 16 * size))
# добавляем чанки
# добавляем чанк заднего фона
# scene.add_object(soldier_1)
scene.add_main_chunk(bg_group)
scene.add_group(NPS_group)
# добавляем чанк переднего плана
scene.add_main_chunk(walls_group)
scene.add_object(hero)
Desert_eagle = WeaponObj('sprite/Weapon_sprites/Desert Eagle.bmp', (360, 360), 'DesertEagle', 1, 'simple', 'simple',
                         2000, [50, 70], 200, 1, None, shoot_image, screen=screen, aim=hero)
scene.add_object(Desert_eagle)
# добавляем главного героя
# устанавливаем главного героя главным героем
scene.set_main_hero(hero)
healpoint_NPS = Image('sprite/NPS_sprites/healpoint_nps.bmp')
bullets = Group('sprite/bullets/standard_bullet.bmp')
scene.add_group(bullets)
resurrection = ImageButton('sprite/User_Interface/resurrection.bmp', (size_screen[0] // 2 - 100, size_screen[1] // 2 - 100))
scene.add_group(enemy_group)
heal_point = Image('sprite/User_Interface/heal_point.bmp')
# цикл работает
run = True
coord = [(int(size_screen[0] - 500), int(size_screen[1] - 160)), (int(size_screen[0] - 790), int(size_screen[1] - 160))]
hero.weapon = Desert_eagle


def print_text(message, x, y, font_style='arial.ttf', font_size=30, font_color=(0, 0, 0)):
    font_type = pygame.font.Font(font_style, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


# в какую сторону он движется
shoot_f = f = left = right = up = down = shift = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # движение персанажа
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_w:
                up = True
            if event.key == pygame.K_s:
                down = True
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift = True
            if f:
                f = False
                camera.create()
            if event.key == 311:
                f = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_s:
                down = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift = False
            if f:
                f = False
                if event.key == 311:
                    f = True
                camera.create()
        if event.type == pygame.MOUSEBUTTONDOWN and hero.weapon is not None:
            if event.button == 1 and not shoot_f:
                shoot_f = True
                hero.weapon.spawn_bullet(camera, hero, 'sprite/bullets/standard_bullet.bmp', bullets)
    if shoot_f:
        Desert_eagle.shoot()
        if Desert_eagle.stop_shoot():
            shoot_f = False
    hero.weapon.bullets_move(bullets, scene, camera, hero.weapon)
    # обнавляем главного героя (двигаем и анимируем)
    camera.draw(scene)
    hero.update(left, right, up, down, walls_group, enemy_group, shift)
    camera.draw_interface(heal_point, [hero.get_hp(), hero.get_max_hp()], [hero.get_food(), hero.get_max_food()], coord)
    x, y = hero.get_coord()
    if hero.get_hp() <= 0 and hero.get_die() is False:
        hero.die('sprite/person_sprites/', [die_frames])
    if hero.get_die():
        resurrection.draw(hero.resurrection, screen)
    Desert_eagle.set_coord([hero.get_coord()[0] + 5, hero.get_coord()[1] + 8])
    soldier_1.update(general, walls_group)
    soldier_1.draw_heal_point(camera, screen, healpoint_NPS)
    soldier_2.update(general, walls_group)
    soldier_2.draw_heal_point(camera, screen, healpoint_NPS)
    soldier_3.update(general, walls_group)
    soldier_3.draw_heal_point(camera, screen, healpoint_NPS)
    soldier_4.update(general, walls_group)
    soldier_4.draw_heal_point(camera, screen, healpoint_NPS)
    soldier_5.update(general, walls_group)
    soldier_5.draw_heal_point(camera, screen, healpoint_NPS)
    general.mov_to_random_point(walls_group)
    general.draw_heal_point(camera, screen, healpoint_NPS)
    print_text(str(int(camera.clock.get_fps())), size_screen[0] - 250, 120, font_color=(255, 255, 0))
    # отрисовываем сцену
    pygame.display.flip()