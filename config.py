import configparser
import os
import sys
from neopixel import *

devices = {
        "SK6812_STRIP_RGBW":ws.SK6812_STRIP_RGBW,
        "SK6812_STRIP_RGBW":ws.SK6812_STRIP_RBGW,
        "SK6812_STRIP_GRBW":ws.SK6812_STRIP_GRBW,
        "SK6812_STRIP_GBRW":ws.SK6812_STRIP_GBRW,
        "SK6812_STRIP_BRGW":ws.SK6812_STRIP_BRGW,
        "SK6812_STRIP_BGRW":ws.SK6812_STRIP_BGRW,
        "SK6812_SHIFT_WMASK":ws.SK6812_SHIFT_WMASK,

# 3 color R, G and B ordering
        "WS2811_STRIP_RGB":ws.WS2811_STRIP_RGB,
        "WS2811_STRIP_RBG":ws.WS2811_STRIP_RBG,
        "WS2811_STRIP_GRB":ws.WS2811_STRIP_GRB,
        "WS2811_STRIP_GBR":ws.WS2811_STRIP_GBR,
        "WS2811_STRIP_BRG":ws.WS2811_STRIP_BRG,
        "WS2811_STRIP_BGR":ws.WS2811_STRIP_BGR,

# predefined fixed LED types

        "SK6812_STRIP":ws.WS2811_STRIP_GRB,
        "SK6812W_STRIP":ws.SK6812_STRIP_GRBW
}

filename = os.path.join(os.path.dirname(__file__), "config.ini")
print(os.path.dirname(__file__))
print(filename)

config = configparser.RawConfigParser()
config.read(filename)

def read_sections():

    return config.sections() 


def load(fixture):
    fixturevars = {
            "w":config.getint(fixture, 'w'),
            "h":config.getint(fixture, 'h'),
            "LED_COUNT":config.getint(fixture, 'w')*config.getint(fixture, 'h'),
            "LED_PIN":config.getint(fixture, 'LED_PIN'),
            "LED_FREQ_HZ":config.getint(fixture, 'LED_FREQ_HZ'),
            "LED_DMA":config.getint(fixture, 'LED_DMA'),
            "LED_BRIGHTNESS":config.getint(fixture, 'LED_BRIGHTNESS'),
            "LED_INVERT":config.getboolean(fixture, 'LED_INVERT'),
            "LED_CHANNEL":config.getint(fixture, 'LED_CHANNEL'),
            "LED_STRIP":devices[config.get(fixture, 'LED_STRIP')]
            }
    return(fixturevars)
# Only store values that are supposed to be changes
def store():
	config.set(fixture, 'brightness', brightness)
	with open(filename, 'wb') as configfile:
   		config.write(configfile)

if __name__ == "__main__":
    print(load('5x5'))
