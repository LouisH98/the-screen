import unicornhathd
from os.path import dirname, basename, isfile, join
import glob
from yapsy.PluginManager import PluginManager
import time
from pixel import Pixel

current_brightness = 0.5
current_slide_index = 0

width, height = unicornhathd.get_shape()

# get slides
slideManager = PluginManager()
slideManager.setPluginPlaces(["slides"])
slideManager.collectPlugins()

for slide in slideManager.getAllPlugins():
    slideManager.activatePluginByName(slide.name)
    slide.plugin_object.init(width, height)


def init_hat():
    unicornhathd.brightness(current_brightness)
    unicornhathd.clear()


slides = slideManager.getAllPlugins()

length = 200
step = 1


def main():
    if len(slides) > 0:
        try:
            while True:
                for slide in slides:
                    print("Slide: " + slide.name)
                    slide = slide.plugin_object
                    for i in range(0, length, step):
                        buffer = slide.get_buffer()
                        for x in range(width):
                            for y in range(height):
                                if slide.use_pixels:
                                    pixel = slide.get_pixel(x, y, i)
                                    unicornhathd.set_pixel(pixel.x, pixel.y, pixel.r, pixel.g, pixel.b)
                                else:
                                    pixel = buffer[x][y]
                                    unicornhathd.set_pixel(pixel.x, pixel.y, pixel.r, pixel.g, pixel.b)

                        unicornhathd.show()
        except KeyboardInterrupt:
            unicornhathd.off()
    else:
        print("No slides found. Ensure they are in /slides")


if __name__ == "__main__":
    # init screen and things
    init_hat()
    main()
