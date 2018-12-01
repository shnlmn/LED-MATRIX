from noise import pnoise3
import pygame
from numpy import *
import numpy as np
from imutils.video import WebcamVideoStream
import os
import time
import cv2
import socket
import math
#from neopixel import *
import config

w = config.w
h = config.h
x_res = config.w
y_res = config.h
stream = 0
vector1d = 0
new_pos = 0
max_pixels = 640*480
img_rgb_matrix = [[[] for x in range(config.w)] for y in range(config.h)]

mag = 10 # magnification/scale of perlin field
octaves = 2
timing = 0.001
min_bright = 0
max_bright = 255
x_drift = 0
y_drift = 0
x_stretch = 1
y_stretch = 1
red_offset = 1000
green_offset = 100
count = 0
span = w*h


def interp(val, smin=0.0, smax=100.0, tmin=0.0, tmax=1.0, power=1):
    return((((abs(val)-smin)*(tmax-tmin))/(smax-smin))+tmin)

def update_matrix(counter, pos):
    for i in range(h):
        for j in range(w):
            y_dir, x_dir = i * mag + 1 + (counter * y_drift), j * mag + 1 + (counter * x_drift)
            x_dir += interp(pos, 0, 640, 0, (mag * 16 * 2))
            blueColor   = int(interp(pnoise3(
                                  float(y_dir)/span,
                                  float(x_dir)/span,
                                  float(counter),
                                  octaves=octaves),
                              0, 1.0, 50, 255))

            redColor    = int(interp(pnoise3(
                              float(y_dir+400)/span,
                              float(x_dir+400)/span,
                              float(counter),
                              octaves=octaves),
                              0, 1.0, 50, 255))

            greenColor  = int(interp(pnoise3(
                              float(y_dir+200)/span,
                              float(x_dir+200)/span,
                              float(counter),
                              octaves=octaves),
                              0, 1.0, 50, 255))
            img_rgb_matrix[i][j] = pygame.Color(redColor,blueColor,greenColor)

def display_img():
    global vector1d
    global new_pos
    global count
    update_matrix(count,0)
    kernel = np.ones((4,4), np.uint8)
    cap = WebcamVideoStream(stream).start()
    fgbg = cv2.createBackgroundSubtractorMOG2()

    pygame.init()
    screen = pygame.display.set_mode((800,600))
    running = True
    screen.fill((0,0,0))

    cell_width  = screen.get_width()/x_res
    cell_height = screen.get_height()/y_res

    while running:
        frame = cap.read()
        fgmask = fgbg.apply(frame)
        erosion = cv2.erode(fgmask, kernel, iterations=1)
        avg_white = np.argwhere(erosion==255).tolist()
        old_pos = new_pos
        update_matrix(count, new_pos)
        # count += timing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        try:
            if avg_white[0] and len(avg_white)>100:
                new_pos = np.mean([x[1] for x in avg_white])
                print(new_pos)
        except:
            pass

        for v in range(y_res):
            for u in range(x_res):
                # color.hsva = (v*u*(360/(y_res*x_res)), 50, 50, 50)
                pygame.draw.rect(screen, img_rgb_matrix[v][u], (u*cell_width, v*cell_height, math.ceil(cell_width),math.ceil(cell_height)))
                #pygame.draw.rect(screen, color, (u*cell_width, v*cell_height, math.ceil(cell_width),math.ceil(cell_height)))

        pygame.display.flip()

        cv2.imshow("Frame", frame)
        cv2.imshow("fg", erosion)
        key = cv2.waitKey(1) & 0xff
        if key == 27:
            break
    cv2.destroyAllWindows()
    cap.stop()

if __name__=="__main__":
    # Create NeoPixel object with appropriate configuration.
#    strip = Adafruit_NeoPixel(config.LED_COUNT, config.LED_PIN, config.LED_FREQ_HZ, config.LED_DMA, config.LED_INVERT, config.LED_BRIGHTNESS, config.LED_CHANNEL, config.LED_STRIP)
    # Intialize the library (must be called once before other functions).
#    strip.begin()
    print("at least it ran")
    display_img()
    #print(array(img)))
