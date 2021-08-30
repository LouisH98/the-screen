#!/usr/bin/env python3
from utils import clamp
import logging
try:
    import unicornhathd
except ImportError:
    from unicorn_hat_sim import unicornhathd

from yapsy.PluginManager import PluginManager
import time
import json

current_brightness = 0.6
current_slide_index = 0

width, height = unicornhathd.get_shape()

# get slides
slideManager = PluginManager()
slideManager.setPluginPlaces(["slides"])
slideManager.collectPlugins()

# init logging
error_log = logging.getLogger(__name__)
error_log.setLevel(logging.ERROR)
log_file_handler = logging.FileHandler('screen.log')
log_file_handler.setLevel(logging.DEBUG)
error_log.addHandler(log_file_handler)


def init_hat():
    unicornhathd.brightness(current_brightness)
    unicornhathd.clear()


# check config for slides to load'
def load_slides():
    slides = []
    with open('config.json') as config_file:
        config = json.load(config_file)
        if "enable_all" in config and config["enable_all"]:
            print("👋  Loading all slides")
            for slide in slideManager.getAllPlugins():
                slideManager.activatePluginByName(slide.name)
                slide.plugin_object.init(width, height)
                slides.append(slide)
                print("✔ " + slide.name)

        elif "enabled" in config and len(config["enabled"]) > 0:
            print("👋  Loading enabled slides")
            for slide in slideManager.getAllPlugins():
                if slide.name in config["enabled"]:
                    slideManager.activatePluginByName(slide.name)
                    slide.plugin_object.init(width, height)
                    slides.append(slide)
                    print("✔ " + slide.name)
    return slides


slides = load_slides()
crash_count = 0
max_crash_count = 5
print("Starting Slides...")


def main():
    last_loop = time.time()
    current_frames = 0
    if len(slides) > 0:
        try:
            while True:
                for slide in slides:
                    slide = slide.plugin_object
                    slide.init(width, height)
                    iteration = 0
                    # Break out of loop if the slide is done, or iteration limit exceeded
                    while (not slide.done) and iteration <= slide.length:
                        iteration += 1
                        if time.time() - last_loop > 1:
                            print("⚡ FPS: " + str(current_frames), end='\r')
                            current_frames = 0
                            last_loop = time.time()

                        unicornhathd.clear()

                        if not slide.use_pixels:
                            buffer = slide.get_buffer()

                        for x in range(width):
                            for y in range(height):
                                if slide.use_pixels:
                                    r, g, b = slide.get_pixel(x, y, i)
                                    unicornhathd.set_pixel(x, y, clamp(r), clamp(g), clamp(b))
                                else:
                                    r, g, b = buffer[x][y]
                                    unicornhathd.set_pixel(x, y, r, g, b)
                                    # unicornhathd.set_pixel(x, y, clamp(r), clamp(g), clamp(b))
                        unicornhathd.show()
                        current_frames += 1
        except KeyboardInterrupt:
            unicornhathd.off()
        except Exception as e:
            unicornhathd.off()
            logging.getLogger(__name__).error("Program crashed. Most likely a slide error: " + str(e))
            global crash_count
            if crash_count < max_crash_count:
                main()
                crash_count += 1
    else:
        print("No slides found. Ensure they are in /slides")


if __name__ == "__main__":
    # init screen and things
    init_hat()
    main()
