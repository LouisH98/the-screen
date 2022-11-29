import slides.slide as base
import numpy as np
import random
import colorsys

TREE_COLOUR = [0, 255, 0]
STAR_COLOUR = [255,215,0]
STUMP_COLOUR = [139,69,19]


def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

class TreeLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = random.uniform(0, 1)

    def twinkle(self, matrix: np.ndarray):
        matrix[self.x][self.y] = hsv2rgb(self.colour, 1, 1)
        self.colour += 0.008
        if self.colour > 1:
            self.colour = 0

class ChristmasTree(base.BaseSlide):
    def __init__(self):
        super().__init__()
        self.use_pixels = False
        self.stump_height = 2

        self.width = 0
        self.height = 0
        self.matrix = np.zeros((0, 0, 3), dtype=int)
        self.tree = self.matrix
        self.lights = []


    def draw_tree(self):
        matrix = np.zeros((self.width, self.height, 3), dtype=int)
        indent = int((self.width - 1) / 2)
        for y in range(1, self.height - 2):
            for x in range(indent, self.width - indent):
                matrix[x][y] = TREE_COLOUR
            
            if y > 3 and y % 2 == 0:
                random_x = random.randrange(indent, self.width - indent)
                self.lights.append(TreeLight(random_x, y))

            if y % 3 == 0:
                indent += 1

            elif indent > 0:
                indent -= 1
        self.draw_star(matrix)
        self.draw_stump(matrix)
        return matrix

    def init(self, width, height):
        self.width = width
        self.height = height
        self.lights = []
        self.tree = self.draw_tree()
        self.matrix = np.copy(self.tree)


    def draw_star(self, matrix):
        star_start_x = int((self.width - 1) / 2)
        matrix[star_start_x][0] = STAR_COLOUR
        matrix[star_start_x +1][0] = STAR_COLOUR


    def draw_stump(self, matrix):
        stump_start_x = int((self.width - 1) / 2)
        for x in range(stump_start_x, stump_start_x + 2):
            for y in range(self.height - 1, self.height - 4, -1):
                matrix[x][y] = STUMP_COLOUR

    def draw_lights(self):
        for light in self.lights:
            light.twinkle(self.matrix)
            

    def get_buffer(self):
        self.matrix = np.copy(self.tree)
        self.draw_lights()
        return self.matrix
 