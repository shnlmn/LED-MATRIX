""" XMAS DISPLAY

This is intended to replicate the twinkle of lights on a christmas display. 

"""

from numpy import *
from noise import pnoise3
import socket
import time
import websockets
import socket
import asyncio
import config
from neopixel import *

import argparse
import signal
import sys

args = {}

def get_ip():
    """ go through hostnames, kick out '127.0.0.1', return IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def signal_handler(signal, frame):
    colorWipe(strip, Color(0,0,0))
    sys.exit(0)

# Collect info from argument
parser = argparse.ArgumentParser()
parser.add_argument('-c', action='store_true', help='clear the display on exit')
parser.add_argument('profile', type=str, help='profile name from config.json')
args = parser.parse_args()
if not args.profile:
    print("no profile")
if args.c:
    signal.signal(signal.SIGINT, signal_handler)


# load fixture details from config
fixture = config.load(args.profile)
h = fixture["h"] # height of pixel matrix
w = fixture["w"]  # width of pixel matrix

# get host dynamically
host = get_ip() 

# starting values for screen
led_vars = {
        "mag":1,
        "octaves": 2,
        "timing":0.002,
        "min_bright": 0,
        "max_bright":1.0,
        "x_drift":0,
        "y_drift":10,
        'x_stretch':1,
        'y_stretch':3,
        'blue_offset' : 1000,
        'red_offset' : 1000,
        'green_offset' : 100,
        'red_bright' : 255,
        'blue_bright' : 255,
        'green_bright' :255
        }
#octaves = 4
port = 5555

# start async websocket listening - print out command recieved
async def listen(websocket, path):
    received = await websocket.recv()
    command, value = received.split(":")
    led_vars[command] = float(value)
    print("< {}:{}".format(command, value))

# meat of script. Takes the settings for perlin and sets values for each led.  
async def build_matrix(count,red_bright, blue_bright,
        green_bright, mag, octaves,timing, min_bright, max_bright, x_drift, 
        y_drift, x_stretch, y_stretch, red_offset, green_offset, blue_offset):
    
    # Don't remember why this was necessary, think it is a workaround.
    await asyncio.sleep(0)
    global led_vars

    # basic linear interpolation
    def interp(val, smin=0.0, smax=100.0, tmin=0.0, tmax=1.0):
        if (tmin > tmax):
            tmin = tmax
        return((((abs(val)-smin)*(tmax-tmin))/(smax-smin))+tmin)
    
    span = fixture['LED_COUNT']
    img_rgb_matrix = [[]]*span

    # iterate through entire matrix, applying perlin settings to each LED
    for i in range(h):
        for j in range(w):
            led_index = (w*h)-1 - int(i*w+j)
            if i%2 == 0:
                j = (w-1)-j
            y_dir, x_dir = i*mag+1+(count*y_drift), j*mag+1+(count*x_drift)
            blueColor   = int(interp(pnoise3(
                              float(y_dir+blue_offset)/span,
                              float(x_dir+blue_offset)/span,
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

            
# Take the led matrix and display the values
async def display_img(strip):
    count = 0
    while 1:
        await build_matrix(count, **led_vars)
        count += led_vars['timing']
        strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(fixture["LED_COUNT"], fixture["LED_PIN"], fixture["LED_FREQ_HZ"],
            fixture["LED_DMA"], fixture["LED_INVERT"], fixture["LED_BRIGHTNESS"], 
            fixture["LED_CHANNEL"], ws.WS2811_STRIP_RGB)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    start_server = websockets.serve(listen, host, 5555)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(start_server, display_img(strip)))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()
