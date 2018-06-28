import os 
import sys

ver = sys.version.split('.')
majorV = ver[0]
if int(majorV)>2 :
    getinput = input
else:
    getinput = raw_input


# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwcontrol import *
from narwhal.nwsegment import *
from stdtrees.geometry import *
from narwhal.nwcontext import *

from mouthCONSTS import *
from mouthVARS import *


A = ContextManager(MouthDict, MouthMODvars, 'order')

s = A.getMODTree("margin")

while True:
    text = getinput("enter text:> ") 

    # backdoors
    if text.lower() == 'q' or text.lower()=='quit' or text.lower()=='exit':
        break
 

    A.read(text)

