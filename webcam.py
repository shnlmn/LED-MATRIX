import socket
import pickle
import cv2
import time
import numpy as np


host = '10.0.0.41'
port = 5050
buff_size = 1024
image_size =(5,5)


def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

# def send_size():
#     data = pickle.dumps(image_size)
#     isock.sendall(data)
#     print("init sent")

cap = cv2.VideoCapture(0)
while True:
    isock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    isock.connect((host, port))
    ret, frame = cap.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = adjust_gamma(frame, gamma=0.5)
    frame = cv2.GaussianBlur(frame, (21,21), 0)
    cv2.imshow('frame', frame)

    #
    frame = cv2.resize(frame, image_size, cv2.INTER_AREA)
    # # print(frame)
    frame = pickle.dumps(frame.tolist())
    isock.sendall(frame)
    # isock.close()
    # time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord('g'):
        break
