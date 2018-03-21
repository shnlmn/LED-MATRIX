import socket
import pickle
import cv2


host = 'localhost'
port = 5050

image_size =(10,10)

def send_size():
    data = pickle.dumps(image_size)
    isock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    isock.connect((host, port))
    isock.sendall(data)
    isock.close()
    print("init sent")

if __name__=="__main__":
    send_size()
#    while True:
#        ret, frame = cap.read()
#        frame = cv2.resize(frame, image_size, cv2.INTER_CUBIC)
