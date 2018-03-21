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
LED_COUNT      = 25 # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

h = 5 # height of pixel matrix
w = int(LED_COUNT/h)  # width of pixel matrix
host = '10.0.0.41'
led_vars = {
        "mag":1,
        "octaves": 2,
        "timing":0.0015,
        "min_bright":0,
        "max_bright":1.0,
        "x_drift":0,
        "y_drift":10,
        'x_stretch':1,
        'y_stretch':1,
        'blue_offset' : 1000,
        'red_offset' : 1000,
        'green_offset' : 100,
        'red_bright' : 255,
        'blue_bright' : 255,
        'green_bright' :255
        }
#octaves = 4
port = 5555


async def listen(websocket, path):
    received = await websocket.recv()
    command, value = received.split(":")
    led_vars[command] = float(value)
    print("< {}:{}".format(command, value))

async def build_matrix(count,red_bright, blue_bright, green_bright, mag, octaves,timing, min_bright, max_bright, x_drift,
                        y_drift, x_stretch, y_stretch, red_offset, green_offset, blue_offset):
    await asyncio.sleep(0)
    global led_vars

    def interp(val, smin=0.0, smax=100.0, tmin=0.0, tmax=1.0):
        if (tmin > tmax):
            tmin = tmax
        return((((abs(val)-smin)*(tmax-tmin))/(smax-smin))+tmin)
    span = w*h
    img_rgb_matrix = [[]]*span
    for i in range(h):
        for j in range(w):
            led_index = (w*h)-1 - int(i*w+j)
            if i%2 == 0:
                j = (w-1)-j
            y_dir, x_dir = i*mag+1+(count*y_drift), j*mag+1+(count*x_drift)
            blueColor   = int(interp(pnoise3(
                              float(y_dir)/span,
                              float(x_dir)/span,
                              float(count),
                              octaves=octaves),
                              0, 1.0, min_bright*255, blue_bright*max_bright))

            redColor    = int(interp(pnoise3(
                              float(y_dir+red_offset)/span,
                              float(x_dir+red_offset)/span,
                              float(count), octaves=octaves),
                              0, 1.0, min_bright*255, red_bright*max_bright))

            greenColor  = int(interp(pnoise3(
                              float(y_dir+green_offset)/span,
                              float(x_dir+green_offset)/span,
                              float(count), octaves=octaves),
                              0, 1.0, min_bright*255, green_bright*max_bright))

            strip.setPixelColor(led_index,
                                Color(redColor, greenColor, blueColor ))
    strip.show()

async def display_img(strip):
    count = 0
    while 1:
        await build_matrix(count, **led_vars)
        count += led_vars['timing']

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    start_server = websockets.serve(listen, host, 5555)
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(start_server, display_img(strip)))
    loop.run_until_complete(asyncio.gather(start_server, display_img(strip)))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()
