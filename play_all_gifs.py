from numpy import *
from PIL import Image
from PIL import GifImagePlugin
from noise import pnoise1
import os
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
LED_COUNT      = 144    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

speed = .05 # frame time for gif animation
w = 12 # width of pixel matrix
h = 12 # height of pixel matrix
img_rgb_matrix = [[[] for x in range(h)] for y in range(w)] # construct matrix to hold rgb vals

def display_img(strip, matrix):
    for i in range(h):
        for j in range(w):
            led_index = (w*h)- 1 - int(i*w+j)
            color = matrix[j][i]
            strip.setPixelColor(led_index, Color(*color))
    strip.show()

def sample_image(img):
    for i in range(h):                               #iterate through rows
            for j in range(w):                           # iterate through columns
                img_x = j
                if i%2 == 0:
                    img_x = (w-1)-j
                img_rgb_matrix[j][i] = img.getpixel((img_x,i))   # load matrix with rgb values
    return(img_rgb_matrix)

def retrieve_gif_frame(img, palette, ind):
    img.seek(ind)
    img.putpalette(palette)
    new_im = Image.new("RGBA", img.size)
    new_im.paste(img)
    new_im = new_im.resize((w,h), Image.ANTIALIAS)
    new_im = new_im.rotate(-90)
    
    return(new_im)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()
    counter = 0
    is_gif = False # Test to see if image is animated
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
       
    gif_files = os.listdir("images/")
    gif_files = list(filter(lambda i: i[-3:] == "gif", gif_files))
    gif_count = 0
    
    images_loaded = [[]]*len(gif_files)
    for ind, file in enumerate(gif_files):
        
        print("Loading image: "+file)
        img = Image.open("images/"+file)
        gif_stills = [[]]*img.n_frames
        gif_palette = img.getpalette()

        for i in range(img.n_frames):
            gif_stills[i] = retrieve_gif_frame(img, gif_palette, i)

        images_loaded[ind] = gif_stills 

    print("Loading complete")
    while 1:
        
        current_gif = images_loaded[gif_count]
        print("Now Playing: "+gif_files[gif_count]) 
        gif_count += 1
        if gif_count > len(images_loaded)-1:
            gif_count = 0
        timer = time.time()

        while time.time()-timer < 60:
            if counter <= len(current_gif)-2:
                counter += 1
            else:
               counter = 0
            img_rgb_matrix = sample_image(current_gif[counter])
            #print(gif_stills[counter])
            display_img(strip, img_rgb_matrix)
            time.sleep(speed)
