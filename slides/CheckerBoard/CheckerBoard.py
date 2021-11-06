import slides.slide as base
import time

class CheckerBoard(base.BaseSlide):

    def get_pixel(self, x, y, _):
        x += 1
        y += 1
        t = time.time()
        value = ((int((x - 8) / y + t * 2))) & 1 ^ int(1 / y * 8) & int(1 * y / 5)
        value = value * 255
        return value, value, value
