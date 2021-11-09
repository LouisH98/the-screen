#!/usr/bin/env python3
from utils import clamp
import logging
import signal
import sys
try:
    import unicornhathd
except ImportError:
    from unicorn_hat_sim import unicornhathd

from yapsy.PluginManager import PluginManager
import time
import json
import threading 

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

# check config for slides to load
def load_slides():
    slides = []
    with open('config.json') as config_file:
        config = json.load(config_file)
        current_brightness = config['brightness']
        unicornhathd.brightness(current_brightness)
        if len(config['enabled']) == 0:
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
    
class ScreenController:
    def __init__(self):
        self.slides = load_slides()
        self.crash_count = 0
        self.max_crash_count = 5
        self.current_slide_index = 0
        self.current_slide = self.slides[self.current_slide_index]
        self.auto_rotate = False

    def next_slide(self):
        self.current_slide_index = (self.current_slide_index + 1) % len(self.slides)
        self.current_slide = self.slides[self.current_slide_index]
        self.current_slide.plugin_object.done = True

    def set_slide(self, slide_name: str):
        slide = next((slide for slide in self.slides if slide.name == slide_name), None)
        if slide is not None:
            self.current_slide = slide

    def start(self):
        last_loop = time.time()
        current_frames = 0
        if len(self.slides) > 0:
            try:
                while True:
                    if self.auto_rotate:
                        self.next_slide()

                    slide = self.current_slide.plugin_object
                    slide.init(width, height)
                    iteration = 0

                    while (not slide.done) and iteration <= slide.length:
                        begin_time = time.time()
                        iteration += 1

                        if begin_time - last_loop > 1:
                            print(f"⚡ FPS: {str(current_frames)}, Target: {slide.max_fps}" , end='\r')
                            current_frames = 0
                            last_loop = time.time()

                        unicornhathd.clear()

                        if not slide.use_pixels:
                            buffer = slide.get_buffer()

                        for x in range(width):
                            for y in range(height):
                                if slide.use_pixels:
                                    r, g, b = slide.get_pixel(x, y, iteration)
                                    unicornhathd.set_pixel(x, y, clamp(r), clamp(g), clamp(b))
                                else:
                                    r, g, b = buffer[x][y]
                                    # unicornhathd.set_pixel(x, y, r, g, b)
                                    unicornhathd.set_pixel(x, y, clamp(r), clamp(g), clamp(b))
                        unicornhathd.show()
                        current_frames += 1

                        # check to see if we need to sleep to keep to configured FPS
                        elapsed_seconds = time.time() - begin_time
                        if elapsed_seconds < 1/slide.max_fps:
                            time.sleep(1/slide.max_fps - elapsed_seconds)
            except KeyboardInterrupt:
                unicornhathd.off()
            except Exception as e:
                print(e)
                logging.getLogger(__name__).error("Program crashed. Most likely a slide error: " + str(e))
                if self.crash_count < self.max_crash_count:
                    self.crash_count += 1
                    self.start()
                else: 
                    unicornhathd.off()
                    sys.exit()
        else:
            print("No slides found. Ensure they are in /slides")



if __name__ == "__main__":
    # init screen and things
    controller = ScreenController()
    thread = threading.Thread(target=controller.start)
    thread.start()
    thread.join()
