from numpy import *
from PIL import Image
from noise import pnoise2

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

w = 144 # width of pixel matrix
h = int(LED_COUNT/w) # height of pixel matrix
img_rgb_matrix = [[[] for x in range(h)] for y in range(w)] # construct matrix to hold rgb vals

def interp(val, smin=0.0, smax=100.0, tmin=0.0, tmax=1.0):
    return((((abs(val)-smin)*(tmax-tmin))/(smax-smin))+tmin)

def reset_strip():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))
        
def display_img(strip, matrix, iterations=3000000):
    octaves = 4

    span = 144 #(h*w)
    for octave in range(1,octaves):
        for count in range(iterations):
            for i in range(h):
                for j in range(w):
                    led_index = LED_COUNT - int(i*w+j) -1
                    position = led_index/LED_COUNT
        #            blueColor = (float(led_index)/span)
         #           redColor = (float(led_index)/span)
              #      blueColor   = interp(led_index, 0,50,0,255)
                    blueColor   = int(interp(pnoise2(float(i)/span,float(j)/span, octaves=octaves, base=count), 0, 1.0, 50, 255))
                    redColor    = int(interp(pnoise2(float(i+400)/span,float(j+400)/span,octaves=octaves, base=count), 0, 1.0, 50, 255))
                    greenColor  = int(interp(pnoise2(float(i+200)/span,float(j+200)/span,octaves=octaves, base=count), 0, 1.0, 50, 255))
         #           redColor   = interp(pnoise1(((float(led_index))/span, 0, 1.0, 0, 255)))
        #            greenColor = interp(pnoise1(((float(led_index))/span, 0, 1.0, 0, 255)))
       #             print(redColor,blueColor,greenColor)
                    strip.setPixelColor(led_index, Color(redColor,blueColor,greenColor))
                    
            strip.show()
            #time.sleep(.1)
        reset_strip()
        for i in range(octave):
            strip.setPixelColor(i, Color(100,100,100))
        strip.show()

    print("done")
    
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()
    counter = 0

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    
    display_img(strip, img_rgb_matrix)
    #print(array(img))
