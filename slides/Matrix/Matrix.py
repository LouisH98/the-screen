import random
import numpy
import slides.slide as base
from random import randint

#
# Ported from Pimoroni Unicorn HAT example
# https://github.com/pimoroni/unicorn-hat/blob/master/examples/hat/matrix.py
# to Unicorn HAT HD by aburgess@gmail.com (https://github.com/Mutiny-Games)
# to this project (with some adaptions) by louisholdsworth@gmail.com

wrd_rgb = [
    [100, 255, 100], [0, 255, 0], [0, 235, 0], [0, 220, 0],
    [0, 185, 0], [0, 165, 0], [0, 128, 0], [0, 0, 0],
    [154, 173, 154], [0, 145, 0], [0, 125, 0], [0, 100, 0],
    [0, 80, 0], [0, 60, 0], [0, 40, 0], [0, 0, 0]
]

min_speed = 0.1
max_speed = 0.6
max_population = 10
blue_pilled_population = [[randint(0, 15), 15, random.uniform(min_speed, max_speed)]]


class Matrix(base.BaseSlide):
    def __init__(self):
        super().__init__()
        self.clock = 0
        self.use_pixels = False
        self.matrix = []

    def init(self, width, height):
        self.width = width
        self.height = height
        self.matrix = numpy.zeros((width, height, 3), dtype=int)

    def set_pixel(self, x, y, colour):
        self.matrix[x][y] = colour

    def get_buffer(self):
        self.matrix = numpy.zeros((self.width, self.height, 3), dtype=int)

        for person in blue_pilled_population:
            y = person[1]
            for rgb in wrd_rgb:
                if (y < 15) and (y >= 0):
                    self.set_pixel(person[0], int(y), [rgb[0], rgb[1], rgb[2]])
                y += 1
            person[1] -= person[2]

            if person[1] < 0 - len(wrd_rgb):
                person[1] = 15
                person[0] = randint(0, 15)

        self.clock += 1

        if len(blue_pilled_population) < max_population and self.clock % 5 == 0:
            blue_pilled_population.append([randint(0, 15), 15, random.uniform(min_speed, max_speed)])


        return numpy.flip(self.matrix)
