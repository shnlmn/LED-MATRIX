from __future__ import print_function
import time
import numpy as np
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import time
import cv2
import socket
from neopixel import *
import sys
import pafy

w = 16 # width of pixel matrix
h = 12 # height of pixel matrix
img_rgb_matrix = [[[] for x in range(h)] for y in range(w)] # construct matrix to hold rgb vals

# LED strip configuration:
LED_COUNT      = w*h      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10   # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_BGR # Strip type and colour ordering

stream = 0
print("getting webcam")

# hsv hue sat value
lower_red = np.array([150,150,50])
upper_red = np.array([180,255,150])

def threaded(strip):
    cap = WebcamVideoStream(stream).start()
    print("Diplaying image")
    while True: 
        frame = cap.read()
        frame = cv2.resize(frame, (w, h), cv2.INTER_AREA)
        display(frame, strip)
    cv2.destroyAllWindows()
    cap.stop()

def non_threaded(strip):
    cap = cv2.VideoCapture(stream)
    print("Diplaying image")
    while True: 
       get, frame = cap.read()
       frame = cv2.resize(frame, (w, h), cv2.INTER_AREA)
       display(frame, strip)
       key = cv2.waitKey(1) & 0xff
    cv2.destroyAllWindows()
    cap.release()
   
def filter_color(frame):
# Filter Color
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask = mask)
    return(res)
    
def display(frame, strip):
    frame = filter_color(frame)
    frame = frame.tolist()
    for j in range(h):
        for i in range(w):
            ind_i, ind_j = i,j
            if i%2 != 0:
                ind_j = h-j-1
            led_index = ind_i * h + ind_j + 1
            color = frame[j][i]
            #print(led_index)
            #print("Color: {}".format(color))
            if type(color) == int:
                color = [color]*3
            strip.setPixelColor(led_index, Color(*color))
        strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    threaded(strip)
    #non_threaded(strip)
