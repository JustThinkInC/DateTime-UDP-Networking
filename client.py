import select
import socket
import sys
import re
import datetime
from dt_packet import *


def start(dateTime, hostNameIP, port):
    if dateTime.lower() not in ["date", "time"]:
        print("First argument must be either 'date' or 'time'")
        return
    try:
        #Check if IP address
        if re.search('[0-9]{3}.[0-9]{1,3}.[0-9]{1,3}', hostNameIP) != None:
            addr = socket.getaddrinfo(hostNameIP, port, proto=socket.IPPROTO_UDP)
        #If localhost address
        else:
            addr = socket.gethostbyname(hostNameIP)
    except:
        print("The IP/hostname supplied does not exit")
        return
        
    if not (1024 <= port <= 64000):
        print("Error: Port number must be between 1024 and 64000")
        return 
    request = 0x0001 if dateTime.lower() == "date" else 0x0002 #set the request type
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  #1 second timeout
    
    #Crete DT-Request packet and send it
    dt = DT_request(MAGIC_NO, REQUEST_PACKET_TYPE, request)
    sock.sendto(bytearray(dt.packet()), addr[0][4])
    
    #Get response packet
    pkt, addr = sock.recvfrom(buff_size)
    #print(pkt.split())
    #TODO: Check response packet validity
    response_packet = DT_response(None, None, None, None, pkt)
    if not response_packet.check():
        return
    
    #TODO: Print response packet
    print(response_packet)
    
    return
    

def main():
    dateTime = None
    hostNameIP = None
    port = None
    inp = str(sys.argv)
    if len(inp.split()) < 4:
        print("Usage: <date> or <time> host_ip_address port")  
    else:
        start(sys.argv[1], sys.argv[2], int(sys.argv[3]))

#main()
start("date", '127.0.0.1', 1025)