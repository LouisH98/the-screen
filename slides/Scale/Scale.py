import slides.slide as base
import time
import math
import colorsys

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class Scale(base.BaseSlide):
    def __init__(self):
        super().__init__()

    def init(self, width, height):
        self.width = width
        self.height = height

    def get_pixel(self, x, y, iter):
        iter = time.time() / 2

        value = math.sin(iter * x) + math.cos(iter * y)

        norm = ((value - -1) / (1 - -1)) / 2

        r, g, b = colorsys.hsv_to_rgb(norm, 1, 1)

        return r * 255, g * 255, b * 255
