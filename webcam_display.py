import pickle
from numpy import *
from PIL import Image
from PIL import GifImagePlugin
from noise import pnoise1
import os
import time
import cv2
import socket
from neopixel import *
import argparse
import signal
import sys


def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)
host = '10.0.0.41'
port = 5050
#try:
#   isock.listen(1)
#   conn, addr = isock.accept()
#   recv_val = []
#   while True:
#       dim = conn.recv(1024)
#       if not dim:
#           break
#       else:
#           recv_val.append(dim)
#except:
#    print("Could not establish connection: ")
#recv_val = pickle.loads(recv_val[0])
#print(recv_val)
w = 5 # width of pixel matrix
h = 5 # height of pixel matrix
img_rgb_matrix = [[[] for x in range(h)] for y in range(w)] # construct matrix to hold rgb vals

# LED strip configuration:
LED_COUNT      = w*h      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GBR   # Strip type and colour ordering

isock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
isock.bind((host, port))
isock.listen(1)
def get_connection(conn):
#    try:
#       recv_vals = []
#       while True:
#           dim = conn.recv(1024)
#           if not dim:
#               break
#           else:
#               recv_vals.append(dim)
#    except Exception as e:
#        print("Could not establish connection: "+str(e))
    recv_vals = []
#    isock.close()
    recv_vals.append(conn.recv(1024))
    return(pickle.loads(recv_vals[0]))

def display_img(strip):
    print("Diplaying image")
    while True:
        conn, addr = isock.accept()
        vals = get_connection(conn)
        for i in range(h):
            for j in range(w):
                led_index = i*h+j
                if i%2 != 0:
                    j = w-j-1
                color = vals[i][j]
                #print(led_index)
                #print("Color: {}".format(color))
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
