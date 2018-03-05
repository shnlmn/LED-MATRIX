import socket
import threading
import sys
def Main():
	host = '127.0.0.1'
	port = 5555

	s = socket.socket()
	s.connect((host, port))
	message = sys.argv[1]
	s.send(message.encode("utf-8"))
	s.close()

if __name__ == "__main__":
	Main()
