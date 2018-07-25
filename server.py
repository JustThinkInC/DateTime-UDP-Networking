import selectors
import socket
import sys

#how to make socket
#s = socket.socket (socket_family, socket_type, protocol=0)
    
def DT_response():
    pass


def start(port1, port2, port3):
    if not (1024 <= port1 <= 64000 and 1024 <= port2 <= 64000 and 1024 <= port3 <= 64000):
        print("Error: port numbers must be between 1024 and 64000")
        return
    #open three UDP/datagram sockets
    s_en = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_mi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_de = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #bind them to port numbers, on fail give error message
     
    sel = selectors.DefaultSelector()
    #infinite loop...
    while True:
        break
        
    
start(1025, 1026, 1027)