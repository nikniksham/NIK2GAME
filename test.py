from MainClasss import Inventory, Item

inventory = Inventory((10, 5))
item = Item('sprite/Weapon_sprites/Desert Eagle.bmp', (0, 0), 'Оружие', 1, 'Оно стреляет', 1)
inventory.add_item(item)

print(inventory.inventory)