from MainClasss import *


class WeaponObj(Weapon):
    def __init__(self, image, coord, name, max_count, type_bullet, type_damage, attack_radius,
                 range_damage, attack_speed, screen, owner, holder, time_on_reload, camera, scene, info=''):
        super().__init__(image, coord, name, max_count, type_bullet, type_damage, attack_radius,
                         range_damage, attack_speed, owner, camera, scene, info)
        self.shoot_frames = []
        self.original_image = Image(image).get_image()
        self.add_type('Weapon')
        self.screen = screen
        self.holder = holder
        self.draw_f = False
        self.pause = 60
        self.count_shoot = 0
        self.time_on_reload = time_on_reload
        self.tick = 10000
        self.original_delay = attack_speed
        self.delay = attack_speed

    def rotate_image(self, angle):
        if angle != 0:
            if -3 <= angle <= 3:
                self.image = self.original_image
            elif abs(angle) >= 177:
                self.image = pygame.transform.flip(self.original_image, True, False)
            elif abs(angle) >= 90:
                self.image = pygame.transform.flip(self.original_image, False, True)
                self.image = pygame.transform.rotate(self.image, -angle)
            else:
                self.image = pygame.transform.rotate(self.original_image, -angle)

    def shoot_delay(self, scene):
        self.tick += 1
        self.check_reload()
        self.draw(scene)
        if self.tick >= self.delay:
            return True
        return False

    def draw(self, scene):
        if self.tick <= self.pause:
            if not self.draw_f:
                scene.add_object(self)
                self.draw_f = True
        else:
            if self.draw_f:
                scene.remove_object(self)
                self.draw_f = False

    def check_reload(self):
        if self.count_shoot % self.holder == 0:
            self.pause = self.time_on_reload
            self.rotate_image(0)
            self.delay = self.time_on_reload
        else:
            self.pause = 60
            self.delay = self.original_delay