from pixel import Pixel

def clamp_pixel(pixel):
    r = int(max(0, min(255, pixel.r)))
    g = int(max(0, min(255, pixel.g)))
    b = int(max(0, min(255, pixel.b)))
    return Pixel(pixel.x, pixel.y, r, g, b)