import slides.slide as base

class ColorGradient(base.BaseSlide):
    def get_pixel(self, x, y, iter):
        b = 255 - (y * x) # + iter
        return 0, 0, int(b)
        # return clamp_pixel(Pixel(x, y, 0, 0, b))
