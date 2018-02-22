import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *

ORDER_NONE = 0
ORDER_HASID = 1
ORDER_UPDATED = 2
ORDER_READY = 3
orderStage = {  
                ORDER_NONE : "none",
                ORDER_HASID : "hasid", 
                ORDER_UPDATED: "not ready",
                ORDER_READY : "ready"
              }

class OrderData():
    def __init__(self):
        self.id = ""
        self.status = ORDER_NONE
    def hasData(self):
        if len(self.id)>0 and self.status>ORDER_NONE :
            return True
        else:
            return False
    def __eq__(self,other):
        if self.id==other.id and self.status==other.status :
            return True
        else:
            return False
    def setID( self, text ):
        self.id = text
        self.status = ORDER_HASID

    def show(self):
        s = "\nOrder: " + self.id + "\n"
        s += "Status: " + orderStage[ self.status ] + "\n"
        s += "Ship by: tomorrow am\n"
        s += "UPS id: -n/a-"

        return s