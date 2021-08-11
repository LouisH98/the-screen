import slides.slide as base
from math import cos


class RandomRed(base.BaseSlide):
    def get_random_colour(self, x, y, t):
        t = t / 2
        x = cos(t + (x + y) + x * y) + 1
        return (x - 0) / (2 - 0) * 255

    def get_pixel(self, x, y, iter):
        random_val = self.get_random_colour(x, y, iter)
        return random_val, 0, 0
