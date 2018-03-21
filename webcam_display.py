import pickle
from numpy import *
from PIL import Image
from PIL import GifImagePlugin
from noise import pnoise1
import os
import time
import cv2
import socket

import argparse
import signal
import sys


def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)
host = 'localhost'
port = 5050
isock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isock.bind((host, port))
try:
   isock.listen(1)
   conn, addr = isock.accept()
   recv_val = []
   while True:
       dim = conn.recv(1024)
       if not dim:
           break
       else:
           recv_val.append(dim)
except:
    print("Could not establish connection: ")
recv_val = pickle.loads(recv_val[0])
print(recv_val)
w = recv_val[0] # width of pixel matrix
h = recv_val[1] # height of pixel matrix
img_rgb_matrix = [[[] for x in range(h)] for y in range(w)] # construct matrix to hold rgb vals

# LED strip configuration:
LED_COUNT      = w*h      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
def get_connection():
    try:
       sock.listen(1)
       conn, addr = sock.accept()
       recv_vals = []
       while True:
           dim = conn.recv(1024)
           if not dim:
               break
           else:
               recv_vals.append(dim)
    except:
        print("Could not establish connection: ")
    return(pickle.loads(recv_vals[0]))

def display_img(strip):
    print("Diplaying image")
    while True:
        vals = get_connection()
        
        for i in range(h):
            for j in range(w):
                led_index = w*h-1
                color = vals[i,j]
                strip.setPixelColor(led_index, Color(*color))
        strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    print("at least it ran")
    display_img(strip)
    #print(array(img)))
