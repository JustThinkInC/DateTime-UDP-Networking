"""Description: This implements a simple UDP server. Three ports are taken as
   command line arguments. First port is for English, second Maori, third German.
   If a valid request is received, the server responds with a date-time (DT)
   packet in the appropriate language for the respective port.
   
   Author: George Khella
"""

import datetime
import select
import socket
import sys
import calendar
import locale
import codecs
from dt_packet import *


def response_text(request_type, language=0x0001):
    """Takes in the request type and language to form the response text"""
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


def server(port1, port2, port3):
    """Takes in 3 ports, first is English, second is Maori, third is German.
    Three UDP sockets are then bound to the ports, waits for a packet on any 
    socket. Upon receiving a packet, if it's valid, creates a response packet
    and sends it to the appropriate port."""
    host = '0.0.0.0'
    #Check port range is valid
    if (port1 not in range(1024, 64000) and port2 not in range(1024, 64000)
        and port3 not in range(1024, 64000)):
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
        s_en.bind((host, port1))
        s_mi.bind((host, port2))
        s_de.bind((host, port3))
        
        #Set as non-blocking
        s_en.setblocking(0)
        s_mi.setblocking(0)
        s_de.setblocking(0)
    except:
        print("An error has occurred during the port binding process")
        return
     
    while True:
        #Wait for requests to the sockets
        read, write, error = select.select([s_en, s_mi, s_de], [], [])
        for s in read:
            packet, address = s.recvfrom(BUFF_SIZE)
            #Create a DT Request packet
            pkt = DT_request(None, None, None, packet)       
            if not pkt.check():
                continue        #Go to start of loop

            language = 0x0001   #English
            if s is s_mi:
                language = 0x0002 #German
            elif s is s_de:
                language = 0x0003 #Maori
            text = response_text(pkt.requestType, language)
            response_packet = DT_response(MAGIC_NO, RESPONSE_PACKET_TYPE, language, text)
            s.sendto(bytearray(response_packet.packet()), address)

        

def main():
    """Takes the command line arguements and passes them to server"""
    #Check for a correct number of arguments
    if len(str(sys.argv).split()) < 4:
        print("Usage: <port1> <port2> <port3>")
    else:
        server(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

main()