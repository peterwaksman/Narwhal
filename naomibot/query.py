""" 
query.py handles questions from the user
In case a response is needed, it is stored in the MetaQuery object.

Reads with these NARs:
    askABTMaterial
    about  
    orderinfo  
    productinfo  
    account 
    hi

"""

import sys
import os 
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwutils import *
#from narwhal.nwchat import *

from stdtrees.quantities import *
from stdtrees.ask import *
from nbtree import *


QUERYNONE = 0
QUERYHI = 1
QUERYABOUT = 2
QUERYACCOUNT = 3
QUERYPRODUCT = 4
QUERYORDER = 5
QUERYMATERIAL = 6

def queryStr( q ):
    if q==QUERYNONE:
        return "none"
    elif q==QUERYABOUT:
        return "ABOUT?"
    elif q== QUERYACCOUNT:
        return "ACCOUNT?"
    elif q== QUERYPRODUCT:
        return "PRODUCT?"
    elif q== QUERYORDER:
        return "ORDER?" 
    elif q== QUERYMATERIAL:
        return "MATERIAL?"
    else: 
        return ''

""" 
The MetaQuery handles questions and answers (other than yes/no)
Its updateX() include a response that may or may not be used
"""

class MetaQuery:
    def __init__(self):
        self.question = QUERYNONE
        self.response = ''
        self.action = []
 
    def str(self):
        return queryStr( self.question )

    def updateHi(self, h):
        if h and h.GOF>=0.5:
            self.question = QUERYHI
            self.response += "Hi, hello, good morning.\n"
            return True
        else:
            return False

    def updateAbout(self, a):
        if a and a.GOF>0.6:
            self.question = QUERYABOUT
            lc = a.lastConst()
            T = Thing( lc )  
            V = Value( lc )
            if len(V)>0:
                self.response += "Yes we make " + V + "s\n"
            elif len(T)==0:
                self.response += "Please give me a little more information.\n" 
            elif T=='how':
                self.response += "Good, thank you. I finally got my mood swings under control.\n"
            else:
                self.response += "I am the Atlantis Chatbot, hoping to help you order a custom abutment.\n"
            return True
        else:
            return False    

    def updateAccount( self, a ):
        if a and a.GOF>0.6:
            self.question = QUERYACCOUNT
            self.response += "For questions about your account please call Customer Service at 1-844-848-0137\n" 
            return True
        else:
            return False

    def updateProductInfo(self, p):
        if p and p.GOF>0.6:
            self.question = QUERYPRODUCT
            val = Value(p.lastConst())
            self.response += "\n[HERE SUMMARY about " +val + "].\n[HERE LINK]\n[HERE recommend]\n"
            self.action.append( { 'INFO':val } )
            return True
        else:
            return False    
        
    def updateOrderInfo(self,o, order):
        if o and o.GOF>0.6:
            self.question = QUERYORDER
            self.response = order + "\n"
            self.response += "\nIf you want to know about a past order: PLEASE ENTER A REFERENCE # [under construction here]\n"
            return True
        else:
            return False
            
    def updateMaterialInfo(self,a , normal=True ):
        if not a:
            return False

        if a.GOF>=0.6 or (not normal and a.GOF>=0.25):
            self.question = QUERYMATERIAL
            self.response +=  "\n[Ti versus Zr: HERE SUMMARY, RECOMMEND, LINK]\n"
            self.action.append( { 'INFO':"Ti versus Zr" } )

            return True
        else:
            return False

