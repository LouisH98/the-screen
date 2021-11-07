import slides.slide as base
import math

class Swirly(base.BaseSlide):

    def init(self, width, height):
        super().init(width, height)
        self.width = width
        self.height = height

    # twisty swirly goodness
    def swirl(self, x, y, step):
        x -= (self.width / 2)
        y -= (self.height / 2)
        dist = math.sqrt(pow(x, 2) + pow(y, 2)) / 2.0
        angle = (step / 10.0) + (dist * 1.5)
        s = math.sin(angle)
        c = math.cos(angle)
        xs = x * c - y * s
        ys = x * s + y * c
        r = abs(xs + ys)
        r = r * 12.0
        r -= 20
        return (r, r + (s * 130), r + (c * 130))

    def get_pixel(self, x, y, iter):
        return self.swirl(x, y, iter)
