import slides.slide as base
import time

class CheckerBoard(base.BaseSlide):

    def get_pixel(self, x, y, _):
        x += 1
        y += 1
        t = time.time()
        #       (((x - 8) / y + t * 5) & 1 ^ 1 / y * 8 & 1) * y / 5
        value = ((int((x - 8) / y + t * 2))) & 1 ^ int(1 / y * 8) & int(1 * y / 5)
        value = (value / 4) * 255

        return value, value, value
