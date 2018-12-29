from numpy import *
from PIL import Image
from PIL import GifImagePlugin
from noise import pnoise1
import os
import asyncio
import time
from neopixel import *
import argparse
import signal
import sys
import config

class GifPlayer:

    def __init__(self, strip, config):
        self.strip = strip
        self.speed = .03  # frame time for gif animation
        self.w = config['w']
        self.h = config['h']
        self.img_rgb_matrix = [[[] for x in range(self.h)] for y in range(self.w)]
        print(strip)
    def opt_parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true',
                            help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
            signal.signal(signal.SIGINT, signal_handler)


    def display_img(self):
        for i in range(self.h):
            for j in range(self.w):
                led_index = (self.w*self.h) - 1 - int(i*self.w+j)
                color = self.img_rgb_matrix[j][i]
#                print(led_index,color[0:3])  
                self.strip.setPixelColor(led_index, Color(*color))
        self.strip.show()


    def sample_image(self, img):
        for i in range(self.h):  # iterate through rows
            for j in range(self.w):                           # iterate through columns
                img_x = j
                if i % 2 == 0:
                    img_x = (self.w-1)-j
                self.img_rgb_matrix[j][i] = img.getpixel(
                    (img_x, i))   # load matrix with rgb values
        #return(img_rgb_matrix)
        return

    def pick_gif(self):

        #for k,v in seld_config.items():
        #    print(type(v), v)

        print("Loading GIF list...")
        gif_files = os.listdir(os.getcwd()+"/images/")

        gif_files = list(filter(lambda i: i[-3:] == "gif", gif_files))
        gif_count = 0
   
        gif_number = int(input("Select gif to display (type number):"))
        file = gif_files[gif_number]
        
        print("Loading image: "+file)
        img = Image.open(os.getcwd()+"/images/"+file)
        gif_stills = [[]]*img.n_frames
        print("gif frames: ", len(gif_stills))
        for i in range(img.n_frames):
            gif_stills[i] = self.retrieve_gif_frame(img, i)
        
        return gif_stills

    def retrieve_gif_frame(self, img, ind):
        img.seek(ind)
        palette = img.getpalette()
        img.putpalette(palette)
        new_im = Image.new("RGBA", img.size)
        new_im.paste(img)
        new_im = new_im.resize((self.w, self.h), Image.ANTIALIAS)
        new_im = new_im.rotate(-90)

        return(new_im)

    def play(self):

        counter = 0
        gif_stills = pick_gif()

        print("Loading complete")
        while 1:

            if counter <= len(gif_stills)-2:
                counter += 1
            else:
                counter = 0
            self.sample_image(gif_stills[counter])
            # print(gif_stills[counter])
            self.display_img()
            time.sleep(self.speed)

# Main pyogram logic follows:
if __name__ == '__main__':

    def read_config():

        matrix_configs = config.read_sections()
        return matrix_configs

    def load_config(type):

        # load fixture details from config
        fixture = config.load(args.profile)
        h = fixture["h"] # height of pixel matrix
        w = fixture["w"]  # width of pixel matrix
        print("LED COLOR MATRIX CONTROLLER")

    # READ CONFIGURATION LIST 
    config_list = read_config()

    for i,section in enumerate(config_list,1):
        print("{}: {}".format(i, section))
    
    # PROMPT USER FOR SELECTION
    config_select = int(input("Select LED matrix configuration:"))
    seld_config = config.load(config_list[config_select-1])
    
    # SET STRIP TO CONFIG
    strip = Adafruit_NeoPixel(seld_config['LED_COUNT'],
                              seld_config['LED_PIN'], 
                              seld_config['LED_FREQ_HZ'],
                              seld_config['LED_DMA'],
                              seld_config['LED_INVERT'],
                              seld_config['LED_BRIGHTNESS'],
                              seld_config['LED_CHANNEL'],
                              seld_config['LED_STRIP'])
    strip.begin()
    #strip = Adafruit_NeoPixel(25, 18, 800000, 10, False, 255, 0, ws.WS2811_STRIP_GBR)
    player = GifPlayer(strip, seld_config)
    player.play()

