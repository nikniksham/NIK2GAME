from MainClasss import *

SPEED = 1


class WithSomeone(Person):
    def __init__(self, name, image, coord, way_to_image, way_name, level, aim, camera, armor=None, type='bmp'):
        bonus = (level - 1) * level * 2
        self.camera = camera
        super().__init__(image, coord, 100 + bonus, 100 + bonus, 100, 100, name, way_to_image, way_name, armor, type)
        self.f_x_1 = self.f_x_2 = self.f_y_1 = self.f_y_2 = False
        self.count_x = 0
        self.count_y = 0
        self.aim = aim
        self.tick = 0
        self.name = name
        self.distance = 0
        self.y_v = self.x_v = 0
        self.frame_die = 0
        self.f_n_y = False
        self.die_frames = []
        for i in range(1, len(os.listdir(path=f'sprite/{way_to_image}/die/{way_name}/')) + 1):
            self.die_frames.append(Image(f'sprite/{way_to_image}/die/{way_name}/{way_name}_die_{i}.{type}'))
        self.die_tick = 0
        self.f_n_x = False
        self.add_type('NPS')
        self.die_f = False
        self.rect = Rect((self.coord[0] + 0, self.coord[1] + 25, 20, 5))
        self.c_die = False
        self.random_point = [2500, 2500]

    def update(self, bots, objects, main_group, camera):
        someone = self.aim
        self.x_vel = 0
        self.y_vel = 0
        platforms = main_group.get_object(self.camera.get_rect())
        for object in objects:
            if object.is_type('Build'):
                platforms.append(object)
        # platforms = main_group.get_object(self.rect) + objects
        # platforms.remove(self.aim)
        if not self.die_f:
            self.x_vel, self.y_vel = 0, 0
            if get_gipotinuza((self.rect.x, self.rect.y), (someone.rect.x, someone.rect.y)) > self.distance and\
                    not self.f_x_1 and not self.f_x_2 and not self.f_y_1 and not self.f_y_2:
                if self.get_coord()[0] > someone.get_coord()[0] + self.distance:
                    self.x_vel = -SPEED
                elif self.get_coord()[0] < someone.get_coord()[0] - self.distance:
                    self.x_vel = SPEED
                if self.get_coord()[1] > someone.get_coord()[1] + self.distance:
                    self.y_vel = -SPEED
                elif self.get_coord()[1] < someone.get_coord()[1] - self.distance:
                    self.y_vel = SPEED
            if self.name == 'Zombie':
                if self.rect.colliderect(someone.rect):
                    someone.damage(0.1)
            self.check_move_1(platforms)
            self.draw()
        else:
            self.die_animation()

    def get_coord(self):
        return self.rect.x, self.rect.y - 25

    def get_rect(self):
        return Rect(self.rect.x, self.rect.y - 25, 20, 30)

    def mov_to_point(self, platforms):
        self.x_vel = 0
        self.y_vel = 0
        if not self.die_f:
            if not self.f_x_1 and not self.f_x_2 and not self.f_y_1 and not self.f_y_2:
                if self.get_coord()[0] > self.random_point[0]:
                    self.x_vel = -SPEED
                elif self.get_coord()[0] < self.random_point[0]:
                    self.x_vel = SPEED
                if self.get_coord()[1] > self.random_point[1]:
                    self.y_vel = -SPEED
                elif self.get_coord()[1] < self.random_point[1]:
                    self.y_vel = SPEED
            self.check_move_1(platforms)
            self.coord = self.rect.x, self.rect.y
            self.draw()
            if self.random_point[0] - 30 < self.get_coord()[0] < self.random_point[0] + 30 and \
                    self.random_point[1] - 30 < self.get_coord()[1] < self.random_point[1] + 30:
                self.random_point = [random.choice(range(5000)), random.choice(range(5000))]
        else:
            self.die_animation()

    def die_animation(self):
        self.tick += 1
        if self.tick >= 15:
            self.tick = 0
            if self.frame_die >= len(self.die_frames) - 1:
                self.image = self.die_frames[self.frame_die].get_image()
            else:
                self.frame_die += 1
                self.image = self.die_frames[self.frame_die].get_image()
        self.die_tick += 1

    def check_move_1(self, platforms):
        self.rect.x += self.x_vel
        x = self.rect.x
        self.collide(self.x_vel, 0, platforms)
        x2 = self.rect.x
        self.rect.y += self.y_vel
        y = self.rect.y
        self.collide(0, self.y_vel, platforms)
        y2 = self.rect.y
        x_vel, y_vel = 0, 0
        if x > x2:
            self.f_x_1 = True
        elif x < x2:
            self.f_x_2 = True
        if y > y2:
            self.f_y_1 = True
        elif y < y2:
            self.f_y_2 = True
        if self.f_x_1 or self.f_x_2:
            if self.count_x >= 90:
                self.f_x_1 = self.f_x_2 = False
                self.count_x = 0
                self.f_n_x = False
            else:
                self.count_x += 1
        if self.f_y_1 or self.f_y_2:
            if self.count_y >= 90:
                self.f_y_1 = self.f_y_2 = False
                self.count_y = 0
                self.f_n_y = False
            else:
                self.count_y += 1
        if self.f_x_1 or self.f_x_2:
            if self.f_y_1:
                y_vel = SPEED
            elif self.f_y_2:
                y_vel = -SPEED
            else:
                if self.get_coord()[1] > self.random_point[1] and not self.f_n_x:
                    y_vel = -SPEED
                elif self.get_coord()[1] < self.random_point[1]:
                    self.f_n_x = True
                    y_vel = SPEED
                else:
                    self.f_n_x = True
                    y_vel = SPEED
        elif self.f_y_1 or self.f_y_2:
            if self.f_x_1:
                x_vel = SPEED
            elif self.f_x_2:
                x_vel = -SPEED
            else:
                if self.get_coord()[0] > self.random_point[0] and not self.f_n_y:
                    x_vel = -SPEED
                elif self.get_coord()[0] < self.random_point[0]:
                    self.f_n_y = True
                    x_vel = SPEED
                else:
                    self.f_n_y = True
                    x_vel = SPEED
        if x_vel != 0 or y_vel != 0:
            self.rect.x += x_vel
            x = self.rect.x
            self.collide(x_vel, 0, platforms)
            x2 = self.rect.x
            self.rect.y += y_vel
            y = self.rect.y
            self.collide(0, y_vel, platforms)
            y2 = self.rect.y
            if x_vel != 0:
                self.x_vel = x_vel
            if y_vel != 0:
                self.y_vel = y_vel
            if x > x2:
                self.f_x_1 = True
            elif x < x2:
                self.f_x_2 = True
            if y > y2:
                self.f_y_1 = True
            elif y < y2:
                self.f_y_2 = True

    def check_move_2(self, platforms):
        self.f_x_1 = self.f_x_2 = self.f_y_1 = self.f_y_2 = False
        x_vel = y_vel = 0
        move = False
        print(self.x_vel, self.y_vel, '___1___')
        self.rect.x += self.x_vel
        x = self.rect.x
        self.collide(self.x_vel, 0, platforms)
        x2 = self.rect.x
        self.rect.y += self.y_vel
        y = self.rect.y
        self.collide(0, self.y_vel, platforms)
        y2 = self.rect.y
        print(x, x2, y, y2)
        if x > x2:
            self.f_x_1 = True
        elif x < x2:
            self.f_x_2 = True
        if y > y2:
            self.f_y_1 = True
        if y < y2:
            self.f_y_2 = True
        if not self.f_x_1 and not self.f_x_2:
            self.rect.x -= self.x_vel
        if not self.f_y_1 and not self.f_y_2:
            self.rect.y -= self.y_vel
        print(self.x_v, self.y_v)
        print(self.f_x_1, self.f_x_2, self.f_y_1, self.f_y_2, '___2___')
        if self.f_x_1 or self.f_x_2:
            move = True
            if self.f_y_1 or self.f_y_2:
                if self.f_y_1:
                    print(1, '___3___')
                    y_vel = -SPEED
                elif self.f_y_2:
                    print(2, '___3___')
                    y_vel = SPEED
            elif self.y_v == 0:
                if self.y_vel == 0:
                    print(3, '___3___')
                    y_vel = random.choice([SPEED, -SPEED])
                    self.y_v = y_vel
                else:
                    print(4, '___3___')
                    y_vel = self.y_vel
                    self.y_v = self.y_vel
            elif self.y_v != 0:
                print(11, '___3___')
                y_vel = self.y_v
        else:
            if self.x_v == 0:
                x_vel = self.x_vel
                if self.f_y_1 or self.f_y_2:
                    self.x_v = self.x_vel
            else:
                x_vel = self.x_v
            print(5, '___3___')
        if self.f_y_1 or self.f_y_2:
            if not move:
                if self.f_x_1 or self.f_x_2:
                    if self.f_x_1 and x_vel == 0:
                        print(6, '___3___')
                        x_vel = -SPEED
                    elif self.f_x_2 and x_vel == 0:
                        print(7, '___3___')
                        x_vel = SPEED
                elif self.x_v == 0:
                    if self.x_vel == 0 and x_vel == 0:
                        print(8, '___3___')
                        x_vel = random.choice([SPEED, -SPEED])
                        self.x_v = x_vel
                    else:
                        if x_vel == 0:
                            print(9, '___3___')
                            x_vel = self.x_vel
                            self.x_v = self.x_vel
                elif self.x_v != 0:
                    print(12, '___3___')
                    x_vel = self.x_v
        else:
            if self.y_v == 0:
                print(1)
                y_vel = self.y_vel
                if self.f_x_1 or self.f_x_2:
                    self.y_v = self.y_vel
            else:
                y_vel = self.y_v
                print(2)
            print(10, '___3___')
        if self.x_vel != 0 and not self.f_x_1 and not self.f_x_2 and not self.f_y_1 and not self.f_y_2:
            self.y_v = self.x_v = 0
        self.x_vel = x_vel
        self.y_vel = y_vel
        print(self.x_vel, self.y_vel, '___4___')
        self.rect.x += self.x_vel
        self.collide(self.x_vel, 0, platforms)
        self.rect.y += self.y_vel
        self.collide(0, self.y_vel, platforms)

    def draw_heal_point(self, camera, screen, image):
        if self.heal_point != 0:
            rect = camera.object_coord(self.rect)
            screen.blit(image.get_image(), [rect[0] - 11, rect[1] - 19])
            pygame.draw.polygon(screen, (255, 0, 0), ((rect[0] - 10, rect[1] - 11),
                                                      (rect[0] - 10, rect[1] - 18),
                                                      (rect[0] - 10 + 57 * (self.heal_point / self.max_heal_point), rect[1] - 18),
                                                      (rect[0] - 10 + 57 * (self.heal_point / self.max_heal_point), rect[1] - 11)))


class GroupHelper:
    def __init__(self):
        pass

    def summon(self, group, object_list, quantity):
        name, image, coord, way_to_image, way_name, level, aim, camera, armor, type = object_list
        for _ in range(quantity):
            group.add_bot(WithSomeone(name, image, [coord[0] + random.choice(range(-1000, 1000)),
                                         coord[1] + random.choice(range(-1000, 1000))], way_to_image, way_name, level, aim, camera, armor, type))