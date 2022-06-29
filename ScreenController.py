#!/usr/bin/env python3
from utils import clamp
import logging
from numpy import rot90, ndarray
from multiprocessing.connection import Client, Listener, Connection
from contextlib import ExitStack
import sys
try:
    import unicornhathd
except ImportError:
    from unicorn_hat_sim import unicornhathd

from sense_utils.SenseHelpers import get_rotation

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
        print(f"Set brightness to  {config['brightness']}")
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
    def __init__(self, is_server=False):
        self.slides = load_slides()
        self.crash_count = 0
        self.rotation = 90
        self.brightness = 0.5
        self.max_crash_count = 5
        self.current_slide_index = 0
        self.current_slide = self.slides[self.current_slide_index]
        self.auto_rotate = True
        self.is_server = is_server
        if is_server:
            self.parent_process = Listener(('localhost', 6001), authkey=b'the-screen')
            self.stream_communication =  Listener(('localhost', 6005), authkey=b'stream-the-screen')
            self.stream_client = None
        self.set_rotation(self.rotation)

    def get_status(self):
        return {
                "slide": self.current_slide.name,
                "brightness": self.brightness,
                "auto_rotate": self.auto_rotate,
                "rotation": self.rotation
                }

    def set_rotation(self, rotation=90):
        self.rotation = rotation
        unicornhathd.rotation(self.rotation)

    def next_slide(self):
        self.current_slide_index = (self.current_slide_index + 1) % len(self.slides)
        self.current_slide = self.slides[self.current_slide_index]
    
    def set_brightness(self, value: float):
        self.brightness = value
        unicornhathd.brightness(value)

    def set_slide(self, slide_name: str):
        slide = next((slide for slide in self.slides if slide.name == slide_name), None)
        if slide is not None:
            self.current_slide = slide

    def send_buffer_to_server(self, buffer):
        # send to parent if streaming active
        if self.stream_client:
            try:
                if isinstance(buffer, ndarray):
                    self.stream_client.send(rot90(buffer, 2 + self.rotation / 90).tolist())
                else:
                    self.stream_client.send(buffer)
            except Exception as e:
                print("Failed to send buffer...", e)

    def check_for_messages(self, client):
        # check for messages from server process - don't wait
        if client.poll(0):
            message, *value = client.recv().split()
            print("got message", message, value)
            if message == 'next_slide':
                self.next_slide()
                slide_name = self.current_slide.name
                return True
            elif message == 'get_slides':
                slide_name_list = list(map(lambda slide: slide.name, self.slides))
                print(slide_name_list)
                self.parent_process.send(slide_name_list)
            elif message == 'init-parent':
                self.parent_process = self.parent_process.accept()
            elif message == 'get_status':
                self.parent_process.send(self.get_status())
            elif message == 'set_brightness':
                self.set_brightness(float(value[0]))
            elif message == 'set_rotation':
                self.set_rotation(float(value[0]))
            elif message == 'set_auto_rotate':
                self.auto_rotate = value[0] == 'True'
                self.parent_process.send(self.auto_rotate)
            elif message == 'set_slide':
                slide = next((slide for slide in self.slides if slide.name == value[0]), None)
                self.auto_rotate = False
                if slide is not None:
                    self.current_slide = slide
                    self.parent_process.send(slide.name)
                    return True
                else:
                    self.parent_process.send(None)
            elif message == 'stream':
                print("waiting for connection")
                self.stream_client = self.stream_communication.accept()
                print("got connection")

            elif message == 'stop_stream':
                print("stopping stream")
                self.stream_client.close()
                self.stream_client = None

            else:
                self.parent_process.send(None)
        return False
                

    def start(self):
        last_loop = time.time()
        current_frames = 0
        if len(self.slides) > 0:
            with ExitStack() as stack:
                if self.is_server:
                    parent_conn = stack.enter_context(Client(('localhost', 6000), authkey=b'the-screen'))
                try:
                    while True:
                        if self.auto_rotate:
                            self.next_slide()
                        
                        slide = self.current_slide.plugin_object
                        slide.init(width, height)
                        iteration = 0

                        while not self.auto_rotate or ((not slide.done) and iteration <= slide.length):
                            slide = self.current_slide.plugin_object

                            begin_time = time.time()
                            iteration += 1
                            
                            self.rotation = get_rotation()
                            
                            if self.is_server:
                                # check for parent message
                                should_restart = self.check_for_messages(parent_conn)
                                if should_restart: 
                                    break

                            if begin_time - last_loop > 1:
                                
                                print(
                                    f"⚡ FPS: {str(current_frames)}, Target: {slide.max_fps}", end='\r')
                                current_frames = 0
                                last_loop = time.time()
                                
                                self.set_rotation(self.rotation)


                            unicornhathd.clear()

                            if not slide.use_pixels:
                                buffer = slide.get_buffer()

                            for x in range(width):
                                for y in range(height):
                                    if slide.use_pixels:
                                        r, g, b = slide.get_pixel(x, y, iteration)
                                        unicornhathd.set_pixel(x, y, clamp(r), clamp(g), clamp(b))
                                        buffer = unicornhathd.get_pixels()
                                    else:
                                        r, g, b = buffer[x][y]
                                        # unicornhathd.set_pixel(x, y, r, g, b)
                                        unicornhathd.set_pixel(x, y, clamp(r), clamp(g), clamp(b))
                                        


                            unicornhathd.show()
                            
                            self.send_buffer_to_server(buffer)
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
    controller = ScreenController()
    try:
        controller.start()
    except KeyboardInterrupt:
        print("Bye!")
        sys.exit(0)

