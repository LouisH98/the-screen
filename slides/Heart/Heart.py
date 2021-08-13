from pixel import Pixel
import slides.slide as base
import numpy
from math import *
from utils import normalise
import time

class CheckerBoard(base.BaseSlide):

    def get_pixel(self, x, y, _):
        R = ((x - 7.5) / 8) ** 4, s = (9 - y) / 8, R + (5 * s / 4 - sqrt(sqrt(R))) ** 2 - 0.8 + 0.3 * sin(5 * t)