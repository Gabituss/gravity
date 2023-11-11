import random

import pygame
from math import sqrt
from random import randint
from config import *
from simulator import System, Planet


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    offset = [0, 0]

    system = System()

    for i in range(100):
        x = randint(-WIDTH * 2, WIDTH * 2)
        y = randint(-HEIGHT * 2, HEIGHT * 2)
        speedx = randint(-3000, 3000)
        speedy = randint(-3000, 3000)
        mass = randint(100, 10000000)
        radius = mass ** (1/5)

        system.add_planet([x, y], [speedx, speedy], radius, mass)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            offset[0] += SPEED / FPS
        if keys[pygame.K_d]:
            offset[0] -= SPEED / FPS
        if keys[pygame.K_w]:
            offset[1] += SPEED / FPS
        if keys[pygame.K_s]:
            offset[1] -= SPEED / FPS

        screen.fill((0, 0, 0))
        offx = offset[0] % CELL_SIZE
        offy = offset[1] % CELL_SIZE
        for j in range(-1, WIDTH // CELL_SIZE + 2):
            pygame.draw.line(screen, [122, 122, 122], [CELL_SIZE * j + offx, 0], [CELL_SIZE * j + offx, HEIGHT])
        for j in range(-1, HEIGHT // CELL_SIZE + 2):
            pygame.draw.line(screen, [122, 122, 122], [0, CELL_SIZE * j + offy], [WIDTH, CELL_SIZE * j + offy])

        system.iter()
        for planet in system.planets:
            pygame.draw.circle(screen,
                               (255, 255, 255),
                               (planet.pos[0] + offset[0], planet.pos[1] + offset[1]),
                               planet.radius)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
