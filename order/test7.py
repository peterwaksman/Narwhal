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
from orderchat import OrderDentalAppChat
#from orderdata import OrderData
 
cvID = '111211311' # conversation id is REQUIRED
cvLoc = "c:\\temp\\" # a location is needed for Load/Save

OChat = OrderDentalAppChat( cvID )
# load previous state
OChat.Load( cvLoc )
# check for an order ID
s = OChat.GetID()
#Greet:
if s:
    print("I can help you with order " + s)
else:
    print("HELLO CLIENT. HOW MAY I HELP YOU?\n\n")

#Start listening
while True:
    print("\n")

    text = getinput("> ") 

    # backdoors
    if text.lower() == 'q' or text.lower()=='quit' or text.lower()=='exit':
        break
    if text.lower()=='clear':
        OChat.Clear()
        OChat.Save(cvLoc)
        continue
    if text.lower()=='ship':
        OChat.SetShipped()
        OChat.Save(cvLoc)
        continue
    if text.lower()=='deliver':
        OChat.SetDelivered()
        OChat.Save(cvLoc)
        continue
    if text.lower()=='design':
        OChat.SetInDesign()
        OChat.Save(cvLoc)

    ############
    # READ/WRITE
    ############
    OChat.Read(text)
    s = OChat.Write()
    
    print( s )

    OChat.Save(cvLoc)
    x = 2


 