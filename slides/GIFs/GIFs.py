from time import sleep
import slides.slide as base
from PIL import Image 
import numpy



def get_images_in_dir(path):     
    from os import listdir
    from os.path import isfile, join, sep
    return  [Image.open(path + sep + f) for f in listdir(path) if isfile(join(path, f))]

class GIFs(base.BaseSlide):
    def __init__(self):
        super().__init__()
        self.use_pixels = False

    def init(self, width, height):
        self.width = width
        self.height = height
        self.images = []
        self.current_index = 0
        self.length = 500
        self.max_fps = 60
        self.images = get_images_in_dir("slides/GIFs/gifs")
        self.image_index = 0
        self.max_restart_count = 1
        self.restart_count = 0
        self.done = False

    def get_buffer(self):
        
        if self.restart_count >= self.max_restart_count:
            self.restart_count = 0
            self.image_index += 1

            if self.image_index > len(self.images) - 1:
                self.image_index = 0
                self.done = True

        image = self.images[self.image_index]
        try:
            image.seek(image.tell() + 1)
        except Exception:
            self.restart_count += 1
            image.seek(0)
        sleep(max(0, (image.info['duration'] / 1000) - 0.03))
        rgb_image = image.resize([16, 16], Image.ANTIALIAS).convert("RGB")
        return numpy.rot90(numpy.asarray(rgb_image))
