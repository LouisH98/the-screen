import time
import slides.slide as base
import numpy as np
from operator import eq

ALIVE = [255, 255, 255]
DEAD = [0, 0, 0]


def get_random_grid(width, height):
    return np.random.randint(2, size=(width, height))


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
        self.history = []
        self.length = 450

        # how many generations 2x repeaters are allowed to carry on for
        # game will reset after repeat_count >= max_repeat_count
        self.repeat_count = 0
        self.max_repeat_count = 20

        # how many times can we run the game?
        self.max_num_iterations = 2
        self.current_iteration_count = 0

    def init(self, width, height):
        super().init(width, height)
        self.grid = get_random_grid(width, height)
        self.history = []
        self.repeat_count = 0
        self.current_iteration_count = 0
        self.done = False

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
        rgb_grid = [[0, 0, 0] * self.width for i in range(self.height)]
        if len(self.history) > 1:
            history = self.history[1]
            for x in range(0, self.width):
                for y in range(0, self.height):
                    cell = grid[x][y]
                    # Cell has come alive
                    if history[x][y] == 0 and cell == 1:
                        rgb_grid[x][y] = [42, 252, 152]
                    # Cell has died
                    elif history[x][y] == 1 and cell == 0:
                        rgb_grid[x][y] = [25, 100, 200]
                    # Cell has continued living
                    elif cell == 1:
                        rgb_grid[x][y] = ALIVE
                    else:
                        rgb_grid[x][y] = DEAD
        else:
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

        # Check for only still life
        if np.array_equal(self.grid, self.new_grid):
            self.init(self.width, self.height)
            self.current_iteration_count += 1
            time.sleep(1)
        else:
            # check for repeaters
            self.history.append(self.grid)
            self.grid = self.new_grid.copy()
            if len(self.history) > 2:
                self.history.pop(0)
            if all(map(eq, self.grid.flat, self.history[0].flat)):
                self.repeat_count += 1
                if self.repeat_count > self.max_repeat_count:
                    self.init(self.width, self.height)
                    self.current_iteration_count += 1

    def get_buffer(self):
        self.do_generation()
        converted = self.convert_to_rgb(self.grid)

        if self.current_iteration_count >= self.max_num_iterations:
            self.done = True

        return converted
