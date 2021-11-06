import colorsys
import random
from random import choice
import slides.slide as base
import numpy as np


def int_to_bin_list(number: int):
    return [int(x) for x in bin(number)[2:]]


class WolframCA(base.BaseSlide):
    def __init__(self):
        super().__init__()
        self.current_generation = []
        self.rule = []
        self.matrix = []
        self.use_pixels = False
        self.rules = [30, 90, 60, 105, 139]
        self.index = 0
        self.current_colour = 0
        self.length = 350
        self.max_fps = 30
        
    def init(self, width, height):
        self.width = width
        self.height = height
        self.current_generation = [0, 0, 0, 0, 1, 0, 0, 0]
        self.matrix = np.zeros((width, height, 3), dtype=int)
        bin_list = int_to_bin_list(choice(self.rules))
        while len(bin_list) < 8:
            bin_list.insert(0, 0)
        self.rule = bin_list

    def get_rule_result(self, a, b, c):
        index = int(str(a) + str(b) + str(c), 2)
        return self.rule[index]

    def convert_to_rgb(self, generation):
        rgb_gen = [[0, 0, 0] for _ in range(self.width)]

        r, g, b = colorsys.hsv_to_rgb(self.current_colour, 1, 1)
        self.current_colour += 0.01
        if self.current_colour >= 1:
            self.current_colour = 0

        for i in range(len(generation)):
            if generation[i] == 1:
                rgb_gen[i] = [r*255, g*255, b*255]
        return rgb_gen

    def do_generation(self):
        new_gen = [0 for _ in range(self.width)]
#        new_gen = np.zeros(self.width, dtype=int)
        current_gen = self.current_generation
#        np.zeros(self.width, dtype=int)

        for i in range(len(current_gen)):
            center = current_gen[i]

            if i == 0:
                left = 0
                right = current_gen[i + 1]

            elif i == len(current_gen) - 1:
                left = current_gen[i - 1]
                right = 0
            else:
                left = current_gen[i - 1]
                right = current_gen[i + 1]

            new_gen[i] = self.get_rule_result(left, center, right)

        if self.index >= self.height:
            self.matrix = self.matrix[1::]
            self.matrix = np.append(self.matrix, [self.convert_to_rgb(new_gen)], axis=0)
        else:
            self.matrix[self.index] = self.convert_to_rgb(new_gen)
            self.index += 1

        self.current_generation = new_gen

        if np.sum(self.matrix) == 0:
            self.init(self.width, self.height)

        return self.matrix

    def get_buffer(self):
        return np.rot90(self.do_generation())
