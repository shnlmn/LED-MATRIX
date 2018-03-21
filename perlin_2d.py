from numpy import *
from PIL import Image
from noise import pnoise3

import time

from neopixel import *

import argparse
import signal
import sys
def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 250     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# w = 144 # width of pixel matrix
# h = int(LED_COUNT/w) # height of pixel matrix
#
# def interp(val, smin=0.0, smax=100.0, tmin=0.0, tmax=1.0):
w = 12 # width of pixel matrix
h = 16 # height of pixel matrix
mag = 10 # magnification/scale of perlin field
octaves = 2
timing = 0.001
min_bright = 0
max_bright = 255
x_drift = 0
y_drift = 1000
x_stretch = 1
y_stretch = 1
red_offset = 1000
green_offset = 100

def interp(val, smin=0.0, smax=100.0, tmin=0.0, tmax=1.0, power=1):
    return((((abs(val)-smin)*(tmax-tmin))/(smax-smin))+tmin)

def reset_strip():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))

def display_img(count, strip):
    span = w*h
    img_rgb_matrix = [[]] *span # construct matrix to hold rgb vals
    for i in range(h):
        for j in range(w):
            led_index = LED_COUNT - int(i*w+j) -1
            y_dir, x_dir = i * mag + 1 + (count * y_drift), j * mag + 1 + (count * x_drift)
            blueColor   = int(interp(pnoise3(
                              float(y_dir)/span,
                              float(x_dir)/span,
                              float(count),
                              octaves=octaves),
                              0, 1.0, 50, 255))

            redColor    = int(interp(pnoise3(
                              float(y_dir+400)/span,
                              float(x_dir+400)/span,
                              float(count),
                              octaves=octaves),
                              0, 1.0, 50, 255))

            greenColor  = int(interp(pnoise3(
                              float(y_dir+200)/span,
                              float(x_dir+200)/span,
                              float(count),
                              octaves=octaves),
                              0, 1.0, 50, 255))

            strip.setPixelColor(led_index, Color(redColor,blueColor,greenColor))

    strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()
    count = 0

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    while True:
        display_img(count, strip)
        count += timing
    #print(array(img))
