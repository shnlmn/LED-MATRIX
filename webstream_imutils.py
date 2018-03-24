from __future__ import print_function
import time
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2
import pafy

w = 16 # width of pixel matrix
h = 12 # height of pixel matrix

myvid = pafy.new("https://youtu.be/tKmqyF25WlI")
# myvid = pafy.new("https://youtu.be/gGokmurmJic")
streams = myvid.streams
stream = 0
print(streams[1].title)

def threaded():
    cap = WebcamVideoStream(stream).start()
    fps = FPS().start()
    print("Diplaying image")
    while fps._numFrames < 200:
        frame = cap.read()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xff
        fps.update()
    fps.stop()
    print("[info] elapsed time {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS {:.2f}".format(fps.fps()))
    cv2.destroyAllWindows()
    cap.stop()

def non_threaded():
    cap = cv2.VideoCapture(stream)
    fps = FPS().start()
    print("Diplaying image")
    while fps._numFrames < 200:
       get, frame = cap.read()
       # frame = cv2.resize(frame, (w, h), cv2.INTER_AREA)
       cv2.imshow("Frame", frame)
       key = cv2.waitKey(1) & 0xff
       fps.update()
    fps.stop()
    print("[info] elapsed time {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS {:.2f}".format(fps.fps()))
    cv2.destroyAllWindows()
    cap.release()
# Main program logic follows:

if __name__ == '__main__':
    threaded()
    # non_threaded()
