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
 
from stdtrees.tchats import ConfirmChat
from orderchat import OrderAppChat
#from orderdata import OrderData
 
cvID = '111211311' # conversation id is REQUIRED
cvLoc = "c:\\temp\\" # a location is needed for Load/Save

OChat = OrderAppChat( cvID )



OChat.Load( cvLoc )

#g = OChat.order.responder.getStageResponse()
#print( g ) 
print("HELLO CLIENT. HOW CAN I HELP YOU?\n\n")


while True:
    text = getinput("> ") 

    # backdoors
    if text.lower() == 'q' or text.lower()=='quit' or text.lower()=='exit':
        break
    if text.lower()=='clear':
        OChat.Clear()
 
    OChat.Read(text)
    s = OChat.Write()
    
    print("\n")
    print( s )

    #h = OChat.orderdata.status
    #print("status is " + str(h))


    OChat.Save(cvLoc)
    #x = 2