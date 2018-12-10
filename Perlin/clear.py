import config
import argparse
import time
from neopixel import *

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(25):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

if __name__ == "__main__":

#   def opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    parser.add_argument('profile', type=str, help='profile name from config.json')
    args = parser.parse_args()
    if not args.profile:
        print("no profile")
    fixture = config.load(args.profile)
    strip = Adafruit_NeoPixel(fixture["LED_COUNT"], fixture["LED_PIN"], fixture["LED_FREQ_HZ"], fixture["LED_DMA"], fixture["LED_INVERT"], fixture["LED_BRIGHTNESS"], fixture["LED_CHANNEL"], ws.WS2811_STRIP_RGB)
    strip.begin()
    colorWipe(strip, Color(0,0,0), 10)
