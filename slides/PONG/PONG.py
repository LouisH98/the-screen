import colorsys
import math
import random
from abc import ABC, abstractmethod
from typing import Tuple

import numpy
import slides.slide as base


class GameObject(ABC):

    def __init__(self):
        self.x: float = 0
        self.y: float = 0

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass


def get_random_colour():
    r, g, b = colorsys.hsv_to_rgb(random.uniform(0, 1), 1, 1)
    return [r * 255, g * 255, b * 255]


def get_random_velocity() -> Tuple[float, float]:
    direction = random.choice([-1, 1])

    def get_random_number(min=-1, max=1, forbidden=0):
        number = random.uniform(min, max)
        if number == forbidden:
            number += random.uniform(0.4, 1)
        return number

    return direction * random.uniform(0.4, 2), get_random_number()


class Paddle(GameObject):
    def __init__(self, game, start_position=(0, 0)):
        super().__init__()
        self.x = start_position[0]
        self.y = start_position[1]
        self.game = game
        self.size = 3
        self.colour = [255, 255, 255]
        self.max_speed = 1.8
        self.center = round(game.height / 2)

    def update(self):
        puck = self.game.game_objects[0]

        # check if puck is moving towards this paddle
        if self.x == 0 and puck.velocity[0] < 0:
            is_puck_moving_towards = True
        elif self.x != 0 and puck.velocity[0] > 0:
            is_puck_moving_towards = True
        else:
            is_puck_moving_towards = False

        # attempt to move towards the pucks y axis, capping top move speed
        if is_puck_moving_towards:
            if puck.y < self.y:
                self.y -= min(self.max_speed, self.y - puck.y)
            elif puck.y > self.y:
                self.y += min(self.max_speed, puck.y - self.y)
            else:
                self.y = puck.y
        else:
            # if return to center
            if self.center < self.y:
                self.y -= min(self.max_speed - 1, self.y - self.center)
            elif self.center > self.y:
                self.y += min(self.max_speed - 1, self.center - self.y)

    def draw(self):
        self.game.set_pixel(round(self.x), round(self.y), self.colour)
        self.game.set_pixel(round(self.x), max(0, round(self.y - 1)), self.colour)
        self.game.set_pixel(round(self.x), min(self.game.width - 1, round(self.y + 1)), self.colour)


class Puck(GameObject):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.velocity = []
        self.colour = [255, 255, 255]
        self.reset_position_and_velocity()

    def reset_position_and_velocity(self):
        vX, vY = get_random_velocity()
        self.velocity = [vX, vY]
        self.x = int(self.game.width / 2)
        self.y = int(self.game.height / 2)

    def update(self):
        future_x = self.x + self.velocity[0]
        future_y = self.y + self.velocity[1]

        if future_x >= self.game.width - 1 or future_x < 0:
            self.colour = get_random_colour()
            self.velocity[0] = self.velocity[0] * -1
        if future_y >= self.game.height - 1 or future_y < 0:
            self.velocity[1] = self.velocity[1] * -1

        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def draw(self):
        self.game.set_pixel(round(self.x), round(self.y), self.colour)


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = numpy.zeros((width, height, 3), dtype=int)

        self.game_objects = [Puck(self), Paddle(self), Paddle(self, (self.width - 1, 0))]

    def set_pixel(self, x, y, colour):
        self.matrix[x][y] = colour

    def draw_line(self):
        for y in range(self.height):
            if (y + 1) % 2 == 0:
                self.set_pixel(int(self.width / 2) - 1, y, [100, 100, 100])

    def tick(self):
        self.matrix = numpy.zeros((self.width, self.height, 3), dtype=int)
        self.draw_line()
        for game_object in self.game_objects:
            game_object.update()
            game_object.draw()
        return self.matrix


###
# PONG
# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# It plays itself!
###
class PONG(base.BaseSlide):
    def __init__(self):
        super().__init__()
        self.game = None
        self.use_pixels = False
        self.length = 700

    def init(self, width, height):
        self.game = Game(width, height)

    def get_buffer(self):
        return self.game.tick()
