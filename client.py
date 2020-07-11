import pickle
import socket
import sys

port: int = 8484

server_address = ('localhost', port)
print(sys.stderr, 'connecting to %s port %s' % server_address)
sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_obj.connect(server_address)
while True:
    try:
        msg = sock_obj.recv(100000)
        print(pickle.loads(msg))
        msg = b""
    finally:
        print("completed")