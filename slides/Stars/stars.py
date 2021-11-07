#!/usr/bin/env python

import random
import math
from helpers.unicornaa import UnicornAA
import slides.slide as base

BLUE_STAR = (50, 50, 255)
RED_STAR = (255, 50, 50)

star_count = 15
stars = []

brightness_multiplier = 1.2
scale = 2


def get_random_start_pos():
    return random.uniform(4 * scale, 11 * scale)


class Star:
    def __init__(self, x, y, z, col=(255, 255, 255)):
        self.x = x
        self.y = y
        self.z = z
        self.radius = 1
        if random.random() < 0.05:
            self.radius = 1
            if random.random() <= 0.05:
                self.col = RED_STAR
            else:
                self.col = BLUE_STAR
        else:
            self.col = col


class StarField(base.BaseSlide):
    def __init__(self):
        super().__init__()
        self.aa = UnicornAA(scale)

    def init(self, width, height):
        self.width = width
        self.height = height
        self.use_pixels = False
        self.star_speed = 0.01

        for i in range(0, star_count):
            star = Star(get_random_start_pos(), get_random_start_pos(), 0)
            stars.append(star)

    def get_buffer(self):
        self.aa.clear()
        global star_speed
        self.star_speed += 0.0001
        row_count = 0
        for i in range(0, star_count):
            if i % 16 * scale == 0:
                row_count += 1

            stars[i] = Star(
                stars[i].x + ((stars[i].x - 8.1 * scale) * self.star_speed),
                stars[i].y + ((stars[i].y - 8.1 * scale) * self.star_speed),
                stars[i].z + self.star_speed * 50)

            if stars[i].x < 0 or stars[i].y < 0 or stars[i].x > 16 * scale or stars[i].y > 16 * scale:
                stars[i] = Star(get_random_start_pos(), get_random_start_pos(), 0)

            brightness = ((stars[i].z - 0) / 255 - 0) * brightness_multiplier

            r, g, b = stars[i].col
            self.aa.drawCircle(math.fabs(stars[i].x), math.fabs(stars[i].y), stars[i].radius, r * brightness,
                               g * brightness, b * brightness)
        return self.aa.getPixels()
