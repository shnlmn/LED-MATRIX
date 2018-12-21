from numpy import *
import numpy as np
from imutils.video import FileVideoStream
from imutils.video import FPS 
import os
import time
import cv2
import socket
import sys
import pafy

def load_video(video):
    #myvid = pafy.new(args['video'])

    streams = myvid.streams
    stream = streams[1].url
    print(streams[1].title)
    cap = FileVideoStream(stream).start()
    time.sleep(1)
#cap = cv2.VideoCapture(stream)
# while True:
#     ret, frame = cap.read()
# 
# #    cv2.imshow('frame', frame)
#     k = cv2.waitKey(100) & 0xff
#     if k == 27:
#         break
# 
# cap.release()
# cv2.destroyAllWindows()
def display_img(strip):
    print("Diplaying image")
    while cap.more():
        frame = cap.read()
        frame = cv2.resize(frame, (w, h), cv2.INTER_LINEAR)
        vals = frame.tolist()
        for j in range(h):
            for i in range(w):
                ind_i, ind_j = i,j
                if i%2 != 0:
                    ind_j = h-j-1
                led_index = ind_i * h + ind_j + 1
                color = vals[j][i]
                #print(led_index)
                #print("Color: {}".format(color))
                if type(color) == int:
                    color = [color]*3
                strip.setPixelColor(led_index, Color(*color))
            strip.show()

def play():
    print("PLAYING YOUTUBE VIDS BRO!!!!!")

# Main program logic follows:
if __name__ == '__main__':
    pass
