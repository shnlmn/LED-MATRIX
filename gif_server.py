from numpy import *
from PIL import Image
from PIL import GifImagePlugin
from noise import pnoise1
import os
import time
from neopixel import *
import asyncio
import websockets
import argparse
import signal
import sys

gif_parser = argparse.ArgumentParser()
gif_parser.add_argument("filename", help="Name of file in images/ directory.")
args = gif_parser.parse_args()

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
LED_COUNT      = 192    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering
counter = 0
speed = .05 # frame time for gif animation
w = 12 # width of pixel matrix
h = 16  # height of pixel matrix
img_rgb_matrix = [[[] for x in range(h)] for y in range(w)] # construct matrix to hold rgb vals

async def listen(websocket, path):
    received = await websocket.recv()
    await choose_gif(received)

async def display_img(strip, matrix):
    for i in range(h):
        for j in range(w):
            led_index = (w*h)- 1 - int(i*w+j)
            color = matrix[j][i]
            strip.setPixelColor(led_index, Color(*color))
    strip.show()

async def sample_image(img):
    for i in range(h):                               #iterate through rows
            for j in range(w):                           # iterate through columns
                img_x = j
                if i%2 == 0:
                    img_x = (w-1)-j
                img_rgb_matrix[j][i] = img.getpixel((img_x,i))   # load matrix with rgb values
    return(img_rgb_matrix)

async def retrieve_gif_frame(img, ind):
    img.seek(ind)
    palette = img.getpalette()
    img.putpalette(palette)
    new_im = Image.new("RGBA", img.size)
    new_im.paste(img)
    new_im = new_im.rotate(-90)
    new_im = new_im.resize((w,h), Image.ANTIALIAS)
    return(new_im)

async def choose_gif(path):

    img = "images/"+path
    global gif_stills
    print("Loading image: "+img)
    img = Image.open(img)
    #gif_palette = img.getpalette()
    gif_stills = [[]]*img.n_frames
    for i in range(img.n_frames):
        gif_stills[i] = await retrieve_gif_frame(img, i)

    print("Loading complete")
    await play_gif(gif_stills)

async def play_gif(gif):
    while 1:
        global gif_stills
        global counter 
        await asyncio.sleep(0)
        if counter <= len(gif_stills)-2:
            counter += 1
        else:
           counter = 0
        img_rgb_matrix = await sample_image(gif_stills[counter])
        #print(gif_stills[counter])
        await display_img(strip, img_rgb_matrix)
        time.sleep(speed)

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    start_server = websockets.serve(listen, '192.168.254.81', 5555)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(start_server, choose_gif(sys.argv[1])))
#    print('Serving on {}.'.format(
    print(start_server)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()
