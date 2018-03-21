import socket
import threading
import sys
import time

host = '127.0.0.1'
port = 5555
interrupt =[]

s = socket.socket()
s.bind((host, port))
s.listen(5)

count= 0

def listen():
    while True:
        c, addr = s.accept()
        print("Received connection from "+str(c)+':'+str(addr))
        interrupt.append(c.recv(1024).decode('utf-8'))
        if not interrupt[0]:
            break
    c.close()

if __name__ == "__main__":
    t = threading.Thread(target=listen)
    t.start()
    while 1:
        while len(interrupt) == 0:
            sys.stdout.write("Counting: {} \r".format(count))
            sys.stdout.flush()
            time.sleep(.5)
            count += 1
        print(interrupt[0], "INTERRUPTION")
        time.sleep(2)
        interrupt = []
