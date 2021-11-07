from yapsy.IPlugin import IPlugin
from pixel import Pixel


class BaseSlide(IPlugin):
    def __init__(self):
        super().__init__()
        self.height = 0
        self.width = 0
        self.buffer = []
        self.use_pixels = True
        self.done = False
        self.length = 500
        self.max_fps = 60

    def init(self, width, height):
        self.height = width
        self.width = height

    def get_pixel(self, x, y, iter):
        return Pixel(x, y, 0, 0, 255)


    def get_buffer(self):
        pass
