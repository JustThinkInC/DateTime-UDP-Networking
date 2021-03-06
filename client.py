"""Description: Implements a simple UDP client. A request type (date or time)
   followed by the host and port number are taken as arguments from command 
   line. On a valid request, the client sends the request to the port, and waits
   1 second for a response. On a valid response, the received packet is printed.
   Note that the server must be running and using the specified port for the 
   client to work.
   
   Author: George Khella
   Date: August 2018
"""

import select
import socket
import sys
import re
import datetime
from dt_packet import *


def client(dateTime, hostNameIP, port):
    """Takes in a string specifying request ("date" or "time"), 
    an IP address in dotted decimal notation or a host/domain name,
    and a port number. The server must be running already using the specified 
    port to execute correctly. A request packet is then sent to the host/IP.
    If a packet is received within 1 second, a response packet is made from it
    and printed if valid.
    """
    #Check if the request is correct
    if dateTime.lower() not in ["date", "time"]:
        print("First argument must be either 'date' or 'time'")
        return
    try:
        #Check if IP address
        if re.search('[0-9]{3}.[0-9]{1,3}.[0-9]{1,3}', hostNameIP) != None:
            addr = socket.getaddrinfo(hostNameIP, port, proto=socket.IPPROTO_UDP)[0][4]
        #If localhost address
        else:
            addr = (socket.gethostbyname(hostNameIP), port)
    except:
        print("The supplied IP/hostname does not exist.")
        return
    
    #Check the port number is valid    
    if not port in range(1024, 64000):
        print("Error: Port number must be between 1024 and 64 000")
        return 
    
    #Set request type
    request = 0x0001 if dateTime.lower() == "date" else 0x0002 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  #1 second timeout
    
    #Crete DT-Request packet and send it
    dt = DT_request(MAGIC_NO, REQUEST_PACKET_TYPE, request)
    
    #OSError occurs if addr is invalid for use, e.g. 0.0.0.0
    try:
        sock.sendto(bytearray(dt.packet()), addr)
    except OSError:
        print("The supplied address cannot be used.")
        return
    
    #Get response packet and address
    try:
        pkt, addr = sock.recvfrom(BUFF_SIZE)
    except ConnectionError:
        print("The request port is unavailable. Please make sure the server has " 
              + "reserved this port.")
        return
    
    #Construct the response packet and check its validity
    response_packet = DT_response(None, None, None, None, pkt)
    if not response_packet.check():
        return
    
    #Print response packet
    print(response_packet)
    

def main():
    """Takes the command line arguments and passes them to client function"""
    #Check we have right number of arguments
    inp = str(sys.argv)
    if len(inp.split()) < 4:
        print("Usage: <date> or <time> host_ip_address port")  
    else:
        client(sys.argv[1], sys.argv[2], int(sys.argv[3]))

#Start the application
main()