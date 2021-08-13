import slides.slide as base
from math import sin, atan2


class Test(base.BaseSlide):

    def get_pixel(self, x, y, t):
        value = sin(3**++x-atan2(x, x*(y) + 7)*3-(t / 5))
        normalised_value = ((value - -1) / (1 - -1))
        return normalised_value * 155, 255 - normalised_value * 255, 255 - t + normalised_value * 255
