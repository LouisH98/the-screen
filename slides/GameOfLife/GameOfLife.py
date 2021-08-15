import random
import time

import slides.slide as base
import numpy as np

ALIVE = [255, 255, 255]
DEAD = [0, 0, 0]


def get_random_grid(width, height):
    return np.random.randint(2, size=(width, height))
    # grid = [[[] for x in range(0, width)] for y in range(0, height)]
    # for x in range(0, width):
    #     for y in range(0, height):
    #         if random.random() > 0.5:
    #             grid[x][y] = 1
    #         else:
    #             grid[x][y] = 0
    # return grid


glider = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


###
# Game of Life Rules
# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
###
class GameOfLife(base.BaseSlide):
    def __init__(self):
        super().__init__()
        self.use_pixels = False
        self.grid = []
        self.new_grid = []

    def init(self, width, height):
        super().init(width, height)
        self.grid = get_random_grid(width, height)
        # self.grid = np.asarray(glider)
        self.new_grid = self.grid.copy()

    def get_neighbour_count(self, grid, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                count += grid[(x + i + self.width) % self.width][(y + j + self.height) % self.height]
        return count

    # Does the same as get_neighbour_count but is faster...
    def get_neighbour_fast(self, grid, x, y):
        count = 0
        count += grid[(x - 1 + self.width) % self.width][(y - 1 + self.height) % self.height]
        count += grid[(x + self.width) % self.width][(y - 1 + self.height) % self.height]
        count += grid[(x + 1 + self.width) % self.width][(y - 1 + self.height) % self.height]
        count += grid[(x - 1 + self.width) % self.width][(y + self.height) % self.height]
        count += grid[(x + 1 + self.width) % self.width][(y + self.height) % self.height]
        count += grid[((x - 1 + self.width) % self.width) % self.height][(y + 1 + self.height) % self.height]
        count += grid[(x + self.width) % self.width][(y + 1 + self.height) % self.height]
        count += grid[(x + 1 + self.width) % self.width][(y + 1 + self.height) % self.height]
        return count

    def convert_to_rgb(self, grid):
        # rgb_grid = [[[] for x in range(0, self.width)] for y in range(0, self.height)]
        rgb_grid = [[0] * self.width for i in range(self.height)]
        for x in range(0, self.width):
            for y in range(0, self.height):
                if grid[x][y] == 1:
                    rgb_grid[x][y] = ALIVE
                else:
                    rgb_grid[x][y] = DEAD

        return rgb_grid

    def do_generation(self):
        self.new_grid = self.grid.copy()

        for x in range(0, self.width):
            for y in range(0, self.height):
                # neighbour_count = self.get_neighbour_count(self.grid, x, y)
                neighbour_count = self.get_neighbour_fast(self.grid, x, y)

                # if cell is alive
                if self.grid[x][y] == 1:
                    # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                    if neighbour_count < 2:
                        self.new_grid[x][y] = 0
                    # Any live cell with two or three live neighbours lives on to the next generation.
                    elif neighbour_count == 2 or neighbour_count == 3:
                        self.new_grid[x][y] = 1
                    # Any live cell with more than three live neighbours dies, as if by overpopulation.
                    elif neighbour_count > 3:
                        self.new_grid[x][y] = 0
                else:
                    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                    if neighbour_count == 3:
                        self.new_grid[x][y] = 1

        if np.array_equal(self.grid, self.new_grid):
            self.init(self.width, self.height)
            time.sleep(1)
        else:
            self.grid = self.new_grid.copy()

    def get_buffer(self):

        self.do_generation()
        converted = self.convert_to_rgb(self.grid)

        return converted
