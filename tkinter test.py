import Tkinter

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
LED_COUNT      = 144    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 25     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

def interp(val, smin=0.0, smax=100.0, tmin=0.0, tmax=1.0):
    return((((abs(val)-smin)*(tmax-tmin))/(smax-smin))+tmin)

def reset_strip():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(255,255,255))

def color_lerp(color1, color2, pos):
    returnColor = [[]]*3
    for ind in range(len(returnColor)):
        returnColor[ind] = int(color1[ind] + (color2[ind]-color1[ind])*pos)
    return returnColor

def update_strand(pos, color):
    reset_strip()
    strip.setPixelColor(pos, Color(color[0], color[1], color[2]))
    strip.show()   
    
    
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()
    counter = 0
    
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    colorA = (0, 0, 0)  # color when y is min
    colorB = (0, 255, 0)   # color when y is max

    while 1:
        p = Tkinter.Tk()
        x, y = p.winfo_pointerxy()
        update_strand(interp(x, 0, 1920, 0, 144), color_lerp(colorA, colorB, interp(y, 0, 1200, 0, 1.0)))
