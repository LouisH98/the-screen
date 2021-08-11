from pixel import Pixel

def clamp_pixel(pixel):
    r = int(max(0, min(255, pixel.r)))
    g = int(max(0, min(255, pixel.g)))
    b = int(max(0, min(255, pixel.b)))
    return Pixel(pixel.x, pixel.y, r, g, b)

def normalise(val, min, max):
    if min < 0:
        diff = +(0 - min)
        min += diff
        max += diff
        val += diff
    return val - min / max - min

def clamp(val):
    return int(max(0, min(255, val)))
