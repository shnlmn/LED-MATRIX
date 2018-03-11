from numpy import *
from PIL import Image
from noise import pnoise3
import socket
import time
import threading
import websockets
import asyncio

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
LED_COUNT      = 200      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

h = 5 # height of pixel matrix
w = int(200/h) # width of pixel matrix
mag = 5 # magnification/scale of perlin field
octaves = 2
timing = 0.005
min_bright = 0
max_bright = 255
x_drift = 1000
y_drift = 200
host = '10.0.0.41'
#host = '127.0.0.1'
port = 5555

red_bright, blue_bright, green_bright = [x for x in [max_bright]*3]
iCommand = []

class LED_Server(asyncio.Protocol):

def interp(val, smin=0.0, smax=100.0, tmin=0.0, tmax=1.0):
    return((((abs(val)-smin)*(tmax-tmin))/(smax-smin))+tmin)


def build_matrix(count, iComm):
    global y_drift, red_bright, blue_bright, green_bright
    global iCommand # set this to clear the iCommand list after it has been used
    if len(iComm) > 0:
        if iComm[0] == 'r':
            green_bright = 0
            red_bright= 255;
            blue_bright = 0
        elif iComm[0] == 'g':
            red_bright = 0
            green_bright = 255
            blue_bright= 0
        elif iComm[0] == 'b':
            red_bright = 0
            blue_bright = 255
            green_bright = 0
        else:
            try:
                y_drift = int(iComm[0])
            except:
                print("did not recognize command")
    iCommand = []
    span = w*h
    img_rgb_matrix = [[]]*span
    for i in range(h):
        for j in range(w):
            led_index = (w*h)-1 - int(i*w+j)
            y_dir, x_dir = i*mag+1+(count*y_drift), j*mag+1+(count*x_drift)
            blueColor   = int(interp(pnoise3(
                              float(y_dir)/span,
                              float(x_dir)/span,
                              float(count),
                              octaves=octaves),
                              0, 1.0, min_bright, blue_bright))

            redColor    = int(interp(pnoise3(
                              float(y_dir+100)/span,
                              float(x_dir+100)/span,
                              float(count), octaves=octaves),
                              0, 1.0, min_bright, red_bright))

            greenColor  = int(interp(pnoise3(
                              float(y_dir+200)/span,
                              float(x_dir+200)/span,
                              float(count), octaves=octaves),
                              0, 1.0, min_bright, green_bright))

            strip.setPixelColor(led_index,
                                Color(redColor, blueColor, greenColor))
    strip.show()

async def display_img(strip):
    count = 0
    while 1:
        await asyncio.sleep(0)
        build_matrix(count, iCommand)
        count += timing
    c.close()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).

    loop = asyncio.get_event_loop()
    strip.begin()
    display_img(strip)

