import selectors
import socket
import sys

#how to make socket
#s = socket.socket (socket_family, socket_type, protocol=0)
    
def DT_request():
    pass


def start(dateTime, hostNameIP, port):
    if dateTime.lower() not in ["date", "time"]:
        print("First argument must be either 'date' or 'time'")
        return
    elif 1: #TODO: broken hostNameIP
        pass
    elif not (1024<=port<=64000):
        print("Error: Port number must be between 1024 and 64000")
        return 
        
    
start(1025, 1026, 1027)