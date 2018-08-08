import select
import socket
import sys

MAGIC_NO = 0x497E
PKT_TYPE = 0x0001
RQST_TYPE = [0x0001, 0x0002]
#how to make socket
#s = socket.socket (socket_family, socket_type, protocol=0)
    
class DT_request():
    def __init__(self, MagicNo, PacketType, RequestType):
        """Initialisiation"""
        self.magicNo = MagicNo
        self.packetType = PacketType
        self.requestType = RequestType

    def check(self):
        """Validity Check"""
        if self.magicNo != MAGIC_NO:
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
        addr = socket.getaddrinfo(hostNameIP, 00000, proto=socket.IPPROTO_UDP)
        #addr = socket.gethostbyname(hostNameIP)
        #print(addr)
    except:
        print("The IP/hostname supplied does not exit")
        return
    #TODO: get address by localhost if ip failed
    if not (1024 <= port <= 64000):
        print("Error: Port number must be between 1024 and 64000")
        return 
    request = 0x0001 if dateTime.lower() == "date" else 0x0002 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    #Crete DT-Request packet and send it
    dt = DT_request(MAGIC_NO, PKT_TYPE, request)
    sock.sendto(bytearray(dt.packet()), addr[0][4])
    #TODO: Get response in 1sec or exit
    select.select([], sock, [])
    #TODO: Check response packet validity
    
    #TODO: Print response packet
    

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
start("date", '127.0.0.1', 1027)