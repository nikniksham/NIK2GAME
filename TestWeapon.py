from MainClasss import *


class WeaponObj(Weapon):
    def __init__(self, image, coord, name, max_count, type_bullet, type_damage, attack_radius,
                 range_damage, attack_speed, accuracy, owner, shoot_image, info='', screen=None, aim=None):
        super().__init__(image, coord, name, max_count, type_bullet, type_damage, attack_radius,
                         range_damage, attack_speed, accuracy, owner, info)
        self.shoot_frames = []
        self.original_image = Image(image)
        self.screen = screen
        self.aim = aim
        self.frame = 0
        self.event = 0
        for frame in shoot_image:
            self.shoot_frames.append(Image('sprite/Weapon_sprites/' + frame))

    def shoot(self):
        if self.frame < len(self.shoot_frames) - 2:
            if self.event == 5:
                self.frame += 1
                self.event = 0
                self.image = self.shoot_frames[self.frame].get_image()
            else:
                self.event += 1
        else:
            self.image = self.original_image.get_image()
            self.frame = 0
            self.event = 0

    def stop_shoot(self):
        if self.frame == 0 and self.event == 0:
            return True
        else:
            return False