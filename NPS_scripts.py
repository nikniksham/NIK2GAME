from MainClasss import *

SPEED = 1


class WithSomeone(Person):
    def __init__(self, image, coord, frames_forward, frames_back, frames_left, frames_right, name='Hog', armor=None, hp=None):
        super().__init__(image, coord, 100, 100, 100, 100, name, frames_forward, frames_back, frames_left, frames_right,
                         'NPS', armor=armor)
        self.name = name
        self.add_type('NPS')
        self.die_f = False

    def update(self, someone, platforms):
        if not self.die_f:
            self.x_vel, self.y_vel = 0, 0
            if get_gipotinuza((self.rect.x, self.rect.y), (someone.rect.x, someone.rect.y)) > 90:
                if self.get_coord()[0] > someone.get_coord()[0] + 60:
                    self.x_vel = -SPEED
                elif self.get_coord()[0] < someone.get_coord()[0] - 60:
                    self.x_vel = SPEED
                if self.get_coord()[1] > someone.get_coord()[1] + 60:
                    self.y_vel = -SPEED
                elif self.get_coord()[1] < someone.get_coord()[1] - 60:
                    self.y_vel = SPEED
            self.rect.x += self.x_vel
            self.collide(self.x_vel, 0, platforms)
            self.rect.y += self.y_vel
            self.collide(0, self.y_vel, platforms)
            self.coord = self.rect.x, self.rect.y
            if self.name != 'Hog':
                self.draw()

    def draw_heal_point(self, camera, screen, image):
        rect = camera.object_coord(self.rect)
        screen.blit(image.get_image(), [rect[0] - 11, rect[1] - 19])
        if self.heal_point != 0:
            pygame.draw.polygon(screen, (255, 0, 0), ((rect[0] - 10, rect[1] - 11),
                                                      (rect[0] - 10, rect[1] - 18),
                                                      (rect[0] - 10 + 57 * (self.heal_point / self.max_heal_point), rect[1] - 18),
                                                      (rect[0] - 10 + 57 * (self.heal_point / self.max_heal_point), rect[1] - 11)))