"""Description: This module holds the DT-Response & DT-Request classes. Global constants
   are also included as well as a merge_bits function for merging two binary
   numbers. Each class has an __init__, init_from_packet, check and packet
   method. The response class also includes a __str__ method which returns
   a string containing every field in the packet.
   
   Author: George Khella
"""

import datetime

MAGIC_NO = 0x497E
REQUEST_PACKET_TYPE = 0x0001
REQUEST_TYPE = [0x0001, 0x0002]
LANG_CODE = [0x0001, 0x0002, 0x0003]
RESPONSE_PACKET_TYPE = 0x0002
BUFF_SIZE = 1024

def merge_bits(first, second, shift):
    """Merge two binary numbers into one"""
    return (first << shift) | second     


class DT_response():
    """DT Response packet class. This is the packet containing the requested
    date/time in the requested language"""
    def init_from_packet(self, packet):
        """Takes a bytearray as input and constructs the packet from it"""  
        #Incorrect packet length
        if len(packet) < 13:
            return
        self.magicNo = merge_bits(packet[0], packet[1], 8)
        self.packetType = merge_bits(packet[2], packet[3], 8)
        self.languageCode = merge_bits(packet[4], packet[5], 8)
        self.year = merge_bits(packet[6], packet[7], 8)
        self.month = packet[8]
        self.day = packet[9]
        self.hour = packet[10]
        self.minute = packet[11]
        self.length = packet[12]
        self.text = packet[13:].decode('utf-8')     #Convert to string
        
        
    def __init__(self, magicno=None, packettype=None, languagecode=None, text=None, packet=None):
        """Construct response packet. If the function receives a packet, 
        the init_from_packet() function is used instead"""
        
        #Check if a packet is given
        if packet:
            self.init_from_packet(packet)
            return
        
        #Construct the packet contents
        date = datetime.datetime.now()      #Get the date
        
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
    

    def packet(self):
        """Construct the packet structure to send"""
        #Split the 16 bit fields into two 8-bit fields
        m_1 = self.magicNo >> 8
        m_2 = self.magicNo & 255
        
        pktype_1 = self.packetType >> 8
        pktype_2 = self.packetType & 255 
        
        lang_1 = self.languageCode >> 8
        lang_2 = self.languageCode & 255
        
        year_1 = self.year >> 8
        year_2 = self.year & 255
        
        #Create a packet array with each field size as 1 byte
        packet_array = [m_1, m_2, pktype_1, pktype_2, lang_1, lang_2,
                          year_1, year_2, self.month, self.day, self.hour,
                          self.minute, self.length]
        
        #Convert the text into hex and append it to packet_array
        for i in range(len(self.text)):
            packet_array.append(int(bytes(self.text[i], 'utf-8').hex(), 16))
       
        #Create the bytearray to return
        packet_bytearray = bytearray(packet_array)
        
        return packet_bytearray    
    
    
    def check(self):
        """Validity Check, returns True on valid packet"""
        #Create packet format for easier checking         
        packet = self.packet()
        
        if len(packet) < 13:
            return False
        elif self.magicNo != MAGIC_NO:
            return False
        elif self.packetType != RESPONSE_PACKET_TYPE:
            return False
        elif self.languageCode not in LANG_CODE:
            return False
        elif self.year >= 2100:
            return False
        elif self.month not in range(1, 12):
            return False
        elif self.day not in range(1, 31):
            return False
        elif self.hour not in range(0, 23):
            return False
        elif self.minute not in range(0, 59):
            return False
        elif len(packet) != 13 + self.length:
            return False  
        
        return True
        
        
    def __str__(self):
        """Returns every part of the packet as a string""" 
        return "{}\n {}\n {}\n {}\n {}\n {}\n {}\n {}\n {}\n {}\n".format(
            self.magicNo, self.packetType, self.languageCode, self.year,
            self.month, self.day, self.hour, self.minute, self.length, self.text)
    
    
    
class DT_request():
    """The DT-Request packet class."""
    
    def init_from_packet(self, packet):
        """Takes bytearray as input and constructs packet from it"""
        #Exit on invalid packet
        if len(packet) < 6:
            return
        
        self.magicNo = merge_bits(packet[0], packet[1], 8)   
        self.packetType = merge_bits(packet[2], packet[3], 8) 
        self.requestType = merge_bits(packet[4], packet[5], 8)
 
    
    def __init__(self, MagicNo=None, PacketType=None, RequestType=None, packet=None):
        """Initialisiation"""
        if packet:
            self.init_from_packet(packet)
            return
        self.magicNo = MagicNo
        self.packetType = PacketType
        self.requestType = RequestType

    
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
    

    def check(self):
        """Validity Check"""
        packet = self.packet()
        if len(packet) != 6:
            return False
        elif self.magicNo != MAGIC_NO:
            return False
        elif self.packetType != REQUEST_PACKET_TYPE:
            return False
        elif self.requestType not in REQUEST_TYPE:
            return False
        
        return True