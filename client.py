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
        print("The IP/hostname supplied does not exit")
        return
    
    #Check the port number is valid    
    if not port in range(1024, 64000):
        print("Error: Port number must be between 1024 and 64000")
        return 
    
    #Set request type
    request = 0x0001 if dateTime.lower() == "date" else 0x0002 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  #1 second timeout
    
    #Crete DT-Request packet and send it
    dt = DT_request(MAGIC_NO, REQUEST_PACKET_TYPE, request)
    sock.sendto(bytearray(dt.packet()), addr)
    
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
    
    return
    

def main():
    dateTime = None
    hostNameIP = None
    port = None
    inp = str(sys.argv)
    if len(inp.split()) < 4:
        print("Usage: <date> or <time> host_ip_address port")  
    else:
        client(sys.argv[1], sys.argv[2], int(sys.argv[3]))

main()
#client("date", '127.0.0.1', 1025)