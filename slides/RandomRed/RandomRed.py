from pixel import Pixel
import slides.slide as base
import numpy

class RandomRed(base.BaseSlide):

    def get_random_colour(self):
        return numpy.random.random() * 255

    def get_pixel(self, x, y, iter):
        return Pixel(x, y, self.get_random_colour())
