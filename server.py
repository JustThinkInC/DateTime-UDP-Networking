import datetime
import select
import socket
import sys
import calendar
import locale
import codecs

#how to make socket
#s = socket.socket (socket_family, socket_type, protocol=0)
    
MAGIC_NO = 0x497E
PACKET_TYPE = 0x0002
REQUEST_TYPE = [0x0001, 0x0002]
LANG_CODE = [0x0001, 0x0002, 0x0003]

buff_size = 1000

class DT_response():
    def __init__(self, magicno, packettype, languagecode, text):
        date = datetime.datetime.now()
        self.magicNo = magicno
        self.packetType = packettype
        self.languageCode = languagecode
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.hour = date.hour
        self.minute = date.minute
        self.length = len(text)
        self.text = text
    
    #def __init__(self, packet):
        #def merge(first, second, shift):
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
        #self.text = packet[13:]
        ##check()    
    
    def check(self):
        """Validity Check"""
        pkt =  bytearray([self])
        if len(bytearray([self])) < 13:
            return
        elif self.magicNo != MAGIC_NO:
            return
        elif self.packetType != 0x0002:
            return
        elif self.languageCode in LANG_CODE:
            return
        elif self.year >= 2100:
            return
        elif self.month not in range(1, 12): 
            return
        elif self.day not in range(1, 31):
            return
        elif self.hour not in range(0, 23):
            return
        elif self.minute not in range(0, 59):
            return
        elif len(pkt) != sum(pkt[:11]) + pkt[12]:
            return        
        
        return True
        
        
    def packet(self):
        m_1 = self.magicNo >> 8
        m_2 = self.magicNo & 255
        
        pktype_1 = self.packetType >> 8
        pktype_2 = self.packetType & 255 
        
        lang_1 = self.languageCode >> 8
        lang_2 = self.languageCode & 255
        
        year_1 = self.year >> 8
        year_2 = self.year & 255
        
        array = [m_1, m_2, pktype_1, pktype_2, lang_1, lang_2,
                          year_1, year_2, self.month, self.day, self.hour,
                          self.minute, self.length]
        
        for i in range(len(self.text)):
            array.append(int(bytes(self.text[i], 'utf-8').hex(), 16))
       
        return bytearray(array)
        
    def __repr__(self):
        return self.text

class DT_request():
    def __init__(self, MagicNo, PacketType, RequestType):
        """Initialisiation"""
        self.magicNo = MagicNo
        self.packetType = PacketType
        self.requestType = RequestType
    
    def __init__(self, packet):
        #(first << shift) | second   
        self.magicNo = (packet[0] << 8) | packet[1]
        self.packetType = (packet[2] << 8 ) | packet[3]
        self.requestType = (packet[4] << 8) | packet[5]
        #if not check():
            #print("ERROR PACKET")
            #return
        

    def check(self):
        """Validity Check"""
        if len(self) != 6:
            return False
        elif self.magicNo != MAGIC_NO:
            return False
        elif self.packetType != PKT_TYPE:
            return False
        elif self.requestType not in RQST_TYPE:
            return False
        return True #Correct packet
    
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


def response_text(request_type, language=0x0001):
    #German month names
    month_de = ['Januar', 'Februar', 'Marz', 'April', 'Mai', 'Juni', 'Juli',
                'August', 'September', 'Oktober', 'November', 'Dezember']
    
    #Maori month names
    month_mi = ['Kohitatea', 'Hui-tanguru', 'Poutu-te-rangi', 'Paenga-whawha', 
                'Haratua', 'Pipiri', 'Hongongoi', 'Here-turi-koka', 'Mahuru', 
                'Whiringa-a-nuku', 'Whiringa-a-rangi', 'Hakihea']
    
    #Get date to set time, month, day and year
    date = datetime.datetime.now()
    time = date.strftime('%H:%M')   #hh:mm
    month = date.strftime('%B')     #Full month name in English
    day = date.strftime('%d')       #Day number
    year = date.strftime('%Y')      #Year number in YYYY
    
    
    #Set text based on requested language and date/time
    if request_type is 0x0001:  
        local_string = "Today's date is "
        if language == 0x0002:
            month = month_de[int(date.strftime('%m'))-1]
            local_string = "Ko te ra o tenei ra ko " 
        elif language is 0x0003:
            month = month_de[int(date.strftime('%m'))-1]
            local_string = "Heute ist der "            
            
        text = local_string + "{} {}, {}".format(month, day, year)
    elif request_type is 0x0002:
        local_string = "The current time is "
        if language == 0x0002:
            local_string = "Ko te wa o tenei wa "
        elif language == 0x0003:
            local_string = "Die Uhrzeit ist "            

        text = local_string + time
    
    return text


def start(port1, port2, port3):
    localhost = '127.0.0.1'
    if not (1024 <= port1 <= 64000 and 1024 <= port2 <= 64000 and 1024 <= port3 <= 64000):
        print("Error: port numbers must be between 1024 and 64000")
        return
    
    #Open three UDP/datagram sockets
    #The two letters after underscore are ISO 639-1 codes for language
    #en = English, mi = Maori, de = Deutsch (German)
    s_en = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_mi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_de = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    #Bind sockets to port numbers, on fail give error message
    try:
        s_en.bind((localhost, port1))
        s_mi.bind((localhost, port2))
        s_de.bind((localhost, port3))
        
        #Set as non-blocking
        s_en.setblocking(0)
        s_mi.setblocking(0)
        s_de.setblocking(0)
    except:
        print("An error has occurred during the port binding process")
        return
     
    #Loop infinitely
    while True:
        #Wait for requests to the sockets
        read, write, error = select.select([s_en, s_mi, s_de], [], [])
        for s in read:
            packet, address = s.recvfrom(buff_size)
            pkt = DT_request(packet)       #Create a DT Request packet
            #if not pkt.check():
            #    continue       #go to start of loop
            #TODO: check for error in pkt above

            language = 0x0001 #English
            if s is s_mi:
                language = 0x0002 #German
            elif s is s_de:
                language = 0x0003 #Maori
            text = response_text(pkt.requestType, language)
            response_packet = DT_response(MAGIC_NO, PACKET_TYPE, language, text)
            s.sendto(bytearray(response_packet.packet()), address)
            #print("WORKING")
            
               
                    
        #return #terminate loop, just in case forget to restart shell...
        

def main():
    start(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
start(1025, 1026, 1027)