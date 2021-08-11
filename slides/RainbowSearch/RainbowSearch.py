import math

from pixel import Pixel
from utils import clamp
import slides.slide as base


# rainbow search spotlights
def rainbow_search(x, y, step):
    xs = math.sin((step) / 100.0) * 20.0
    ys = math.cos((step) / 100.0) * 20.0
    scale = ((math.sin(step / 60.0) + 1.0) / 5.0) + 0.2
    r = math.sin((x + xs) * scale) + math.cos((y + xs) * scale)
    g = math.sin((x + xs) * scale) + math.cos((y + ys) * scale)
    b = math.sin((x + ys) * scale) + math.cos((y + ys) * scale)
    return (r * 255, g * 255, b * 255)

class Demo(base.BaseSlide):
    def get_pixel(self, x, y, iter):
        r, g, b = rainbow_search(x, y, iter)
        r = clamp(r)
        g = clamp(g)
        b = clamp(b)
        return r, g, b

