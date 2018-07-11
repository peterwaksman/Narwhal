import os     
import sys

# add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *

ORDER_NONE = 0
ORDER_HASID = 1 #order placed
ORDER_RECEIVED = 2 #materials and data received
ORDER_INDESIGN = 3 
ORDER_NEEDAPPROVED = 4 
ORDER_BEENAPPROVED = 5 
ORDER_INMANUFCTR = 6
ORDER_SHIPPED =  7
ORDER_DELIVERED = 8 
ORDER_ONHOLD =  9

# string for reporting in the order data
orderStage = {  
                ORDER_NONE : "none",
                ORDER_HASID : "HasID",  
                ORDER_RECEIVED: "Received",  
                ORDER_INDESIGN: "InDesign",
                ORDER_NEEDAPPROVED: "AwaitsApproval",
                ORDER_BEENAPPROVED: "Approved",
                ORDER_INMANUFCTR: "InManufacturing",
                ORDER_SHIPPED: "Shipped",
                ORDER_DELIVERED : "Delivered",
                ORDER_ONHOLD: "OnHold"
              }

class OrderData():
    def __init__(self):
        self.id = ""
        self.status = ORDER_NONE

    def UpdateFromSource(self):
        if self.status>=ORDER_HASID:
            x = 2 # call vendor APIs 
        else:
            x = 3 # nothing to update

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
        if text and text[0]=='#':
            self.id = text[1:]
        else:
            self.id = text
        #if self.status<=ORDER_HASID:
        self.status = ORDER_HASID # changing the id resets the chatbot

    def getValidatedID( self, oid ):
        if oid =='_query_':
            return ''
        else: # for now
            return oid

    def show(self):
        s = "\nOrder: " + self.id + "\n"
        s += "Status: " + orderStage[ self.status ] + "\n"
        status = self.status
        if status<ORDER_SHIPPED:
            s += "Ship by: Tomorrow am\n"
        else:
            s += "Ship by: [done]\n"

        if status >= ORDER_SHIPPED:
            s += "UPS id: 8802"
        else:
            s += "UPS id: -n/a-"

        return s