from MainClasss import *

SPEED = 2


class WithSomeone(Person):
    def __init__(self, name, image, coord, way_to_image, way_name, armor=None):
        super().__init__(image, coord, 100, 100, 100, 100, name, way_to_image, way_name, armor)
        self.name = name
        self.add_type('NPS')
        self.die_f = False
        self.random_point = [2500, 2500]

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
            self.draw()

    def mov_to_random_point(self, platforms):
        if not self.die_f:
            if self.get_coord()[0] > self.random_point[0]:
                self.x_vel = -SPEED
            elif self.get_coord()[0] < self.random_point[0]:
                self.x_vel = SPEED
            if self.get_coord()[1] > self.random_point[1]:
                self.y_vel = -SPEED
            elif self.get_coord()[1] < self.random_point[1]:
                self.y_vel = SPEED
            self.rect.x += self.x_vel
            self.collide(self.x_vel, 0, platforms)
            self.rect.y += self.y_vel
            self.collide(0, self.y_vel, platforms)
            self.coord = self.rect.x, self.rect.y
            self.draw()
            if self.get_coord()[0] == self.random_point[0] and self.get_coord()[1] == self.random_point[1]:
                self.random_point = [random.choice(range(5000)), random.choice(range(5000))]

    def draw_heal_point(self, camera, screen, image):
        rect = camera.object_coord(self.rect)
        screen.blit(image.get_image(), [rect[0] - 11, rect[1] - 19])
        if self.heal_point != 0:
            pygame.draw.polygon(screen, (255, 0, 0), ((rect[0] - 10, rect[1] - 11),
                                                      (rect[0] - 10, rect[1] - 18),
                                                      (rect[0] - 10 + 57 * (self.heal_point / self.max_heal_point), rect[1] - 18),
                                                      (rect[0] - 10 + 57 * (self.heal_point / self.max_heal_point), rect[1] - 11)))