import select
import socket
import sys
import re

MAGIC_NO = 0x497E
PKT_TYPE = 0x0001
RQST_TYPE = [0x0001, 0x0002]
buff_size = 100
#how to make socket
#s = socket.socket (socket_family, socket_type, protocol=0)

class DT_response():
    #def __init__(self, magicno, packettype, languagecode, text):
        #date = datetime.datetime.now()
        #self.magicNo = magicno
        #self.packetType = packettype
        #self.languageCode = languagecode
        #self.year = datetime.year
        #self.month = date.month
        #self.day = date.day
        #self.hour = date.hour
        #self.minute = date.minute
        #self.length = date.length
        #self.text = text
        
    def __init__(self, packet):
        def merge(first, second, shift):
            return (first << shift) | second   
        #packet = packet.split(b' ')
        self.magicNo = merge(packet[0], packet[1], 8)
        self.packetType = merge(packet[2], packet[3], 8)
        self.languageCode = merge(packet[4], packet[5], 8)
        self.year = merge(packet[6], packet[7], 8)
        self.month = packet[8]
        self.day = packet[9]
        self.hour = packet[10]
        self.minute = packet[11]
        self.length = packet[12]
        self.text = packet[13:]
        #check()
    
    def check(self):
        """Validity Check"""
        
        if self.magicNo != MAGIC_NO:
            print(1, self.magicNo)
            return 
        elif self.packetType != PACKET_TYPE:
            print(2)
            return 
        elif self.languageCode not in [0x0001, 0x0002, 0x0003]:
            print(3)
            return 
        elif self.year >= 2100:
            print(4)
            return 
        elif self.length < len(self.text):
            print(5)
            return 
    
        return True
        
    def __str__(self):
        return str(self.text.decode('utf-8'))
    
class DT_request():
    def __init__(self, MagicNo, PacketType, RequestType):
        """Initialisiation"""
        self.magicNo = MagicNo
        self.packetType = PacketType
        self.requestType = RequestType

    def check(self):
        """Validity Check"""
        if len(bytearray([self])) != 6:
            return
        elif self.magicNo != MAGIC_NO:
            return
        elif self.packetType != PKT_TYPE:
            return
        elif self.requestType not in RQST_TYPE:
            return
    
    def packet(self):
        """Create packet for bytearray"""
        #Split MagicNo fields to 2 bytes
        m_1 = self.magicNo >> 8
        m_2 = self.magicNo & 255
        #Split packettype to 2 bytes
        pktype_1 = self.packetType >> 8
        pktype_2 = self.packetType & 255        
        #Split requesttype to 2 bytes
        rqst_1 = self.requestType >> 8
        rqst_2 = self.requestType & 255 
        
        #Return packet in list format
        return [m_1, m_2, pktype_1, pktype_2, rqst_1, rqst_2] 


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
    dt = DT_request(MAGIC_NO, PKT_TYPE, request)
    sock.sendto(bytearray(dt.packet()), addr[0][4])
    
    #Get response packet
    pkt, addr = sock.recvfrom(buff_size)
    #print(pkt.split())
    #TODO: Check response packet validity
    response_packet = DT_response(pkt)
    #if not response_packet.check():
     #   return
    
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