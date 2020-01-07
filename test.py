from MainClasss import Item, Inventory
import pygame
pygame.init()
sc = pygame.display.set_mode((10, 10))
inv = Inventory((2, 2))
for elem in inv.get_items():
    print(elem)
patron_1 = Item('sprite/blocks_sprites/back_1.bmp', (0, 0), 'патрон', 10, 'infa', 5)
print(inv.add_item(patron_1))
for elem in inv.get_items():
    print(elem)
patron_4 = Item('sprite/blocks_sprites/back_1.bmp', (0, 0), 'снаряд', 10, 'infa', 5)
print(inv.add_item(patron_4))
for elem in inv.get_items():
    print(elem)
patron_2 = Item('sprite/blocks_sprites/back_1.bmp', (0, 0), 'патрон', 10, 'infa', 5)
print(inv.add_item(patron_2))
for elem in inv.get_items():
    print(elem)
patron_3 = Item('sprite/blocks_sprites/back_1.bmp', (0, 0), 'патрон', 10, 'infa', 5)
print(inv.add_item(patron_3))
for elem in inv.get_items():
    print(elem)
patron_3 = Item('sprite/blocks_sprites/back_1.bmp', (0, 0), 'патрон', 10, 'infa', 5)
print(inv.add_item(patron_3))
for elem in inv.get_items():
    print(elem)
patron_3 = Item('sprite/blocks_sprites/back_1.bmp', (0, 0), 'патрон', 10, 'infa', 5)
print(inv.add_item(patron_3))
for elem in inv.get_items():
    print(elem)
patron_3 = Item('sprite/blocks_sprites/back_1.bmp', (0, 0), 'патрон', 10, 'infa', 5)
print(inv.add_item(patron_3))
for elem in inv.get_items():
    print(elem)
patron_3 = Item('sprite/blocks_sprites/back_1.bmp', (0, 0), 'патрон', 10, 'infa', 5)
print(inv.add_item(patron_3), 'fad')
for elem in inv.get_items():
    print(elem)