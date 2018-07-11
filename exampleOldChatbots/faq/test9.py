#!/usr/bin/env python
"""
Basic example. To test your TChat directly.

"""
import sys
import os 
from time import gmtime, strftime

ver = sys.version.split('.')
majorV = ver[0]
if int(majorV)>2 :
    getinput = input
else:
    getinput = raw_input


this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)
 

from dsdata import *

from faqchat import FAQAppChat 
from faqabout import FAQAboutChat
from faqanswer import *
from stdtrees.tchats import *

OChat = FAQAboutChat(HRBASEDATA.info,HRBASEDATA.phone, HRBASEDATA.contact)

#OChat = FAQAppChat( HRBASEDATA, HRAnswerChats )

#OChat = ConnectionsChat()

print("HELLO CLIENT. CAN I HELP YOU?\n\n")

#Start listening
while True:
    print("\n")

    text = getinput("> ") 

    # backdoors
    if text.lower() == 'q' or text.lower()=='quit' or text.lower()=='exit':
        break
   

    ############
    # READ/WRITE
    ############
    OChat.Read(text)
    s = OChat.Write()
    
    print( s )

    x = 2


 