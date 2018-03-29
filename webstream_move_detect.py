from __future__ import print_function
import time
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2
import websocket
import numpy as np
import pafy

w = 16 # width of pixel matrix
h = 12 # height of pixel matrix
host = "ws://192.168.254.81:5555"

def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

stream = 0
vector1d = 0
new_pos = 0
max_pixels = 640*480

def threaded():
    kernel = np.ones((5,5), np.uint8)
    global vector1d
    global new_pos
    cap = WebcamVideoStream(stream).start()
    fgbg = cv2.createBackgroundSubtractorMOG2()
    print("Diplaying image")

    while True:
        frame = cap.read()
        fgmask = fgbg.apply(frame)
        erosion = cv2.erode(fgmask, kernel, iterations = 1)
        avg_white = np.argwhere(erosion == 255).tolist()
        old_pos = new_pos

        try:
            if avg_white[0] and len(avg_white)>100:
                ws = websocket.create_connection(host)
                new_pos = np.mean([x[1] for x in avg_white])
                vector1d = old_pos-new_pos
                print(old_pos, new_pos)
                send_text = "y_drift:{}".format(20*np.interp(vector1d, [-200,200], [-1,1]))
                print(send_text)
                ws.send(send_text)
        except:
            pass
        #frame = adjust_gamma(frame, .2)
        cv2.imshow("Frame", frame)
        cv2.imshow("fg", erosion)
        key = cv2.waitKey(1) & 0xff
        if key == 27:
            break
    cv2.destroyAllWindows()
    cap.stop()


if __name__ == '__main__':
    threaded()
