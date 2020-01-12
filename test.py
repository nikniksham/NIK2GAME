import pygame
from math import sin, cos

size_screen = (201, 201)
screen = pygame.display.set_mode(size_screen)
clock = pygame.time.Clock()

running = True
circles = []
angle = 1.57
vel_angle = 0
step = 0.52
vel = 0.87
r = 70
center = size_screen[0] // 2, size_screen[1] // 2

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                vel_angle -= vel
            elif event.button == 3:
                vel_angle += vel
    # обновление и отрисовка шаров
    t = clock.tick()
    if t and vel_angle:
        angle += vel_angle * t / 1000
        angle = angle if angle < 6.28 else 6.28 - angle
    pygame.draw.circle(screen, pygame.Color('white'), center, 10)
    pygame.draw.polygon(screen, pygame.color.Color('white'), (center, (center[0] - r * cos(angle),
                                                              center[1] + r * sin(angle)),
                                                              (center[0] - r * cos(angle + step),
                                                              center[1] + r * sin(angle + step))))
    pygame.draw.polygon(screen, pygame.color.Color('white'), (
        center, (center[0] - r * cos(angle + 2.09), center[1] + r * sin(angle + 2.09)),
        (center[0] - r * cos(angle + step + 2.09), center[1] + r * sin(angle + step + 2.09))))
    pygame.draw.polygon(screen, pygame.color.Color('white'), (
        center, (center[0] - r * cos(angle + 4.19), center[1] + r * sin(angle + 4.19)),
        (center[0] - r * cos(angle + step + 4.19), center[1] + r * sin(angle + step + 4.19))))

    pygame.display.flip()
