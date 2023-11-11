import math
from config import *


class Planet:
    def __init__(self, pos, speed, mass, radius):
        self.pos = pos
        self.speed = [speed[0] * TIMESTEP, speed[1] * TIMESTEP]
        self.mass = mass
        self.radius = radius
        self.speed_delta = [0, 0]

    def dist(self, other):
        return math.sqrt((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2)

    def interact(self, other):
        force = GRAVITY_CONST * (self.mass * other.mass / self.dist(other) ** 2)
        force /= self.mass

        dx = other.pos[0] - self.pos[0]
        dy = other.pos[1] - self.pos[1]
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi

        diff = [0, 0]
        diff[0] = math.cos(rads) * force * TIMESTEP
        diff[1] = -math.sin(rads) * force * TIMESTEP

        self.speed_delta[0] += diff[0]
        self.speed_delta[1] += diff[1]

    def apply(self):
        self.speed = [self.speed[0] + self.speed_delta[0], self.speed[1] + self.speed_delta[1]]
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.speed_delta = [0, 0]


class System:
    def __init__(self):
        self.planets = []

    def add(self, planet: Planet):
        self.planets.append(planet)

    def add_planet(self, pos, speed, radius, mass):
        self.planets.append(Planet(pos, speed, mass, radius))

    def iter(self):
        new_planets = []
        for i in range(len(self.planets)):
            flag = True
            new_planet = self.planets[i]
            for j in range(len(self.planets)):
                if i == j:
                    continue

                if self.planets[i].dist(self.planets[j]) <= self.planets[i].radius + self.planets[j].radius:
                    if self.planets[i].mass < self.planets[j].mass:
                        flag = False

            if flag:
                new_planets.append(self.planets[i])

        self.planets = new_planets

        for i in range(len(self.planets)):
            for j in range(len(self.planets)):
                if i == j:
                    continue

                self.planets[i].interact(self.planets[j])

        for i in range(len(self.planets)):
            self.planets[i].apply()
            # self.planets[i].pos[0] %= WIDTH
            # self.planets[i].pos[1] %= HEIGHT
