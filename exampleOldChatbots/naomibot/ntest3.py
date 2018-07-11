#!/usr/bin/env python
"""
Basic example. 
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

print("HELLO CLIENT. HOW CAN I HELP YOU?\n\n")

from stdtrees.tchats import *
NB = AboutChat()
#NB = ConfirmChat()
#NB.Confirm("serial#")
#print NB.Write()


while True:
    text = getinput("> ") 

    # backdoors
    if text.lower() == 'q' or text.lower()=='quit' or text.lower()=='exit':
        break
 
    NB.Read(text)
    s = NB.Write()
    
    print("\n")
    print( s )

 


