# The Screen™ (not really TM)

Made for the [Pimoroni Unicorn Hat HD](https://shop.pimoroni.com/products/unicorn-hat-hd), this program loads "slides" and rotates between them at runtime. Each slide returns a 2D numpy array, which is then sent over to the Hat.

In this repo, you'll find some slides already created:
- Game of Life
- Wolfram's Cellular Automata
- PONG
- Matrix
- Stars 
- and a few others, taken from Unicorn Hat HD examples

Slides planned:
- Pendulum Simulation
- Snake
- Weather Forecast
- Sand/Water automata

## Slides
To create a slide, first create a folder with the slide name. Inside that folder, then create a python file with the same name, and another file with the same name, but the extension should be '.yapsy-plugin'

The python file should include a class that inherits from slide.BaseSlide, this file defines some class attributes, along with two methods:

1. init - called with width and height info
2. get_pixel - For pixel shading. called when slide.use_pixels = true. This will provide a function to a pixel, give x, y, and time as t. 
3. get_buffer - For when you want to handle the entire matrix generation. Used in more complicated slides, such that the slide can operate on the raw matrix, and return it as numpy 2d array for display. (the format of this: [[255, 0, 0], [0, 255, 0]... for each line])
