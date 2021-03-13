from yapsy.IPlugin import IPlugin
from pixel import Pixel
import random

class TestSlide(IPlugin):
    def __init__(self):
        super().__init__()
        self.height = 0
        self.width = 0

    def init(self, width, height):
        self.height = width
        self.width = height

    def get_random_colour(self):
        return random.randint(0, 255)
    def get_buffer(self, iter):

        buffer = [[Pixel(x, y, self.get_random_colour(), self.get_random_colour(), self.get_random_colour()) for x in range(self.width)] for y in range(self.height)]
        return buffer
