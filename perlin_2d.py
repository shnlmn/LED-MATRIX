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
LED_COUNT      = 192# Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

w = 12 # width of pixel matrix
h = 16 # height of pixel matrix
mag = 5 # magnification/scale of perlin field
octaves = 4
timing = 0.002
min_bright = 50
max_bright = 255
x_drift = 0
y_drift = 1000
x_stretch = 5
y_stretch = 1
red_offset = 1000
green_offset = 100
def interp(val, smin=0.0, smax=100.0, tmin=0.0, tmax=1.0):
    return((((abs(val)-smin)*(tmax-tmin))/(smax-smin))+tmin)

def reset_strip():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))

def build_matrix(count):
    span = w*h
    img_rgb_matrix = [[]]*span
    for i in range(h):
        for j in range(w):
            led_index = (w*h)-1 - int(i*w+j)

            if i%2 == 0:
                j = (w-1)-j
            y,x = i*y_stretch, j*x_stretch
  	    #print(led_index)
            y_dir, x_dir = y*mag+1+(count*y_drift), x*mag+1+(count*x_drift)
            blueColor   = int(interp(
                            pnoise3(
                                float(y_dir)/span,
                                float(x_dir)/span,
                                float(count),
                                octaves=octaves),
                            0, 1.0, min_bright, max_bright))
            redColor    = int(interp(
                            pnoise3(
                                float(y_dir+red_offset)/span,
                                float(x_dir+red_offset)/span,
                                float(count),
                                octaves=octaves),
                            0, 1.0, min_bright, max_bright))
            greenColor  = int(interp(
                            pnoise3(float(y_dir+green_offset)/span,
                                float(x_dir+green_offset)/span,
                                float(count),
                                octaves=octaves),
                            0, 1.0, min_bright, max_bright))

            strip.setPixelColor(led_index, Color(redColor, blueColor, greenColor))
    strip.show()

def display_img(strip):
    count = 0
    while 1:
        build_matrix(count)
        count += timing
        #reset_strip()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()
    counter = 0

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).


    strip.begin()
    display_img(strip)

