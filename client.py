import select
import socket
import sys
import re
import datetime
from dt_packet import *

#MAGIC_NO = 0x497E
#PKT_TYPE = 0x0001
#RQST_TYPE = [0x0001, 0x0002]
#LANG_CODE = [0x0001, 0x0002, 0x0003]
buff_size = 100
#how to make socket
#s = socket.socket (socket_family, socket_type, protocol=0)


#class DT_response():
    #def init_from_packet(self, packet):
        #"""Takes a bytearray as input and constructs the packet from it"""
        
        #def merge(first, second, shift):
            #"""Merge two binary numbers into one"""
            #return (first << shift) | second        
        
        #self.magicNo = merge(packet[0], packet[1], 8)
        #self.packetType = merge(packet[2], packet[3], 8)
        #self.languageCode = merge(packet[4], packet[5], 8)
        #self.year = merge(packet[6], packet[7], 8)
        #self.month = packet[8]
        #self.day = packet[9]
        #self.hour = packet[10]
        #self.minute = packet[11]
        #self.length = packet[12]
        #self.text = packet[13:].decode('utf-8')     #Convert to string
        
        
    #def __init__(self, magicno=None, packettype=None, languagecode=None, text=None, packet=None):
        #"""Construct response packet. If the function receives a packet, 
        #the init_from_packet() function is used instead"""
        
        ##Check if a packet is given
        #if packet:
            #self.init_from_packet(packet)
            #return
        
        ##Construct the packet contents
        #date = datetime.datetime.now()      #Get the date
        
        #self.magicNo = magicno
        #self.packetType = packettype
        #self.languageCode = languagecode
        #self.year = date.year
        #self.month = date.month
        #self.day = date.day
        #self.hour = date.hour
        #self.minute = date.minute
        #self.length = len(text)
        #self.text = text
    

    #def packet(self):
        #"""Construct the packet structure to send"""
        ##Split the 16 bit fields into two 8-bit fields
        #m_1 = self.magicNo >> 8
        #m_2 = self.magicNo & 255
        
        #pktype_1 = self.packetType >> 8
        #pktype_2 = self.packetType & 255 
        
        #lang_1 = self.languageCode >> 8
        #lang_2 = self.languageCode & 255
        
        #year_1 = self.year >> 8
        #year_2 = self.year & 255
        
        ##Create a packet array with each field size as 1 byte
        #packet_array = [m_1, m_2, pktype_1, pktype_2, lang_1, lang_2,
                          #year_1, year_2, self.month, self.day, self.hour,
                          #self.minute, self.length]
        
        ##Convert the text into hex and append it to packet_array
        #for i in range(len(self.text)):
            #packet_array.append(int(bytes(self.text[i], 'utf-8').hex(), 16))
       
        ##Create the bytearray to return
        #packet_bytearray = bytearray(packet_array)
        
        #return packet_bytearray    
    
    
    #def check(self):
        #"""Validity Check"""
        ##self.languageCode = format(16, str(self.languageCode) +'b')
        ##print(self.languageCode)        
        #packet = self.packet()
        #if len(packet) < 13:
            #print(1)
            #return
        #elif self.magicNo != MAGIC_NO:
            #print(2)
            #return
        #elif self.packetType != 0x0002:
            #print(3)
            #return
        #elif self.languageCode not in LANG_CODE:
            #print(4)
            #return
        #elif self.year >= 2100:
            #print(5)
            #return
        #elif self.month not in range(1, 12): 
            #print(6)
            #return
        #elif self.day not in range(1, 31):
            #print(7)
            #return
        #elif self.hour not in range(0, 23):
            #print(8)
            #return
        #elif self.minute not in range(0, 59):
            #print(9)
            #return
        #elif len(packet) != 13 + self.length:
            #print(10)
            #return        
        
        #return True
        
        
    #def __str__(self):
        #"""Returns the text field of the packet""" 
        #return self.text
    
    
    
#class DT_request():
    #def __init__(self, MagicNo, PacketType, RequestType):
        #"""Initialisiation"""
        #self.magicNo = MagicNo
        #self.packetType = PacketType
        #self.requestType = RequestType

    #def check(self):
        #"""Validity Check"""
        #if len(bytearray([self])) != 6:
            #return
        #elif self.magicNo != MAGIC_NO:
            #return
        #elif self.packetType != PKT_TYPE:
            #return
        #elif self.requestType not in RQST_TYPE:
            #return
    
    #def packet(self):
        #"""Create packet for bytearray"""
        ##Split MagicNo fields to 2 bytes
        #m_1 = self.magicNo >> 8
        #m_2 = self.magicNo & 255
        ##Split packettype to 2 bytes
        #pktype_1 = self.packetType >> 8
        #pktype_2 = self.packetType & 255        
        ##Split requesttype to 2 bytes
        #rqst_1 = self.requestType >> 8
        #rqst_2 = self.requestType & 255 
        
        ##Return packet in list format
        #return [m_1, m_2, pktype_1, pktype_2, rqst_1, rqst_2] 


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