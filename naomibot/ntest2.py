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

#from projectoxford.speech  import SpeechClient
#sc = SpeechClient("520d49e98f34457aa01c669fbfd23f9d", gender='Male', locale='en-US')
#print = sc.print
#input = sc.input


this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from nbchat import NBChat 


NB = NBChat()

print("HELLO ABUTMENT CUSTOMER. HOW CAN I HELP YOU?\n\n")



while True:
    text = getinput("> ") 

    # backdoors
    if text.lower() == 'q' or text.lower()=='quit':
        break

    if text.lower() == 'clearbot':
        print("restart") 
        NB.clear()
        continue
    NB.read(text)
    s = NB.respondNext()
    
    print("\n")
    print( s )


    x = NB.getOrder() 
    x = 2



