import os 
import sys
import cPickle

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *
from stdtrees.tchats import *

from ordertree import *
from orderdata import *

#####################################
AccountResponder = DefaultResponder()
class AccountChat( NWDataChat ):
    def __init__(self):
        NWDataChat.__init__(self, AccountAskTopic, AccountResponder)
######################################
ORDER_NONE 
ORDER_HASID  
ORDER_RECEIVED  
ORDER_INDESIGN 
ORDER_NEEDAPPROVED  
ORDER_BEENAPPROVED  
ORDER_INMANUFCTR  
ORDER_SHIPPED  
ORDER_DELIVERED  
ORDER_ONHOLD  
ochatR = { 
    ORDER_NONE : "But I don't have an order number.\nPlease enter your ORDER #:",
    ORDER_HASID : "Order number {} ... checking status\n",# gets appended to
    ORDER_RECEIVED : "{}",
    ORDER_INDESIGN : "{}",
    ORDER_NEEDAPPROVED  : "{}",
    ORDER_BEENAPPROVED  : "{}",
    ORDER_INMANUFCTR  : "{}",
    ORDER_SHIPPED : "{}",
    ORDER_DELIVERED: "{}",
    ORDER_ONHOLD: "On Hold"
    

    }
ochatRVs = {
    ORDER_NONE : [],
    ORDER_HASID : [MYORDER],
    ORDER_RECEIVED : [MYORDER],
    ORDER_INDESIGN : [MYORDER],
    ORDER_NEEDAPPROVED  : [MYORDER],
    ORDER_BEENAPPROVED  : [MYORDER],
    ORDER_INMANUFCTR  : [MYORDER],
    ORDER_SHIPPED: [MYORDER], # here maybe want a data-time VAR
    ORDER_DELIVERED : [MYORDER],
    ORDER_ONHOLD : [MYORDER]
    }

OrderResponder = NWTopicResponder( ochatR,ochatRVs )
 

class OrderChat( NWDataChat ):
        def __init__(self, orderdata):
            NWDataChat.__init__(self, OrderAskTopic, OrderResponder)   
            self.data = orderdata       
            self.caveat = ''    
            self.stringmode = False


        def Read(self, text):
            if self.stringmode:
                self.stringmode = False
                self.caveat = text
                self.data.setID( text )
                self.responder.stage = ORDER_HASID
                return
            NWDataChat.Read(self,text)

        def loadStage( self ):
            data = self.data


        def update(self):
            self.outtext = ''

            NWDataChat.update(self)
            if self.gof<0.3: #<=0.5?
                 return

            otherGOF = 0
            for reader in self.topic.readers:
                if reader.id=='inputask':
                    continue
                otherGOF = max(otherGOF, reader.GOF)

            for reader in self.topic.readers:
                id = reader.id
              
                if id=='inputask' and reader.GOF>0.8:# and reader.GOF>otherGOF:
                    orderID = reader.getLastValue()
                    orderID = self.data.getValidatedID(orderID)

                    if orderID:
                            # trying to change the order number
                        if reader.GOF>=otherGOF and self.data.hasData() and orderID!=self.data.id:
                            self.caveat = "Wait...could you please start a new conversation to discuss another order."
                            return
                            # or setting the order number
                        elif reader.GOF>otherGOF:
                            self.data.setID( orderID )
                            self.responder.stage = ORDER_HASID
                             
                            # special mode before an orderID is known
                if not self.data.hasData():
                    self.stringmode = True
                    self.responder.stage = ORDER_NONE                 
                    return
     
                t = reader.getLastThing()
                a = reader.getLastAction()
                r = reader.getLastRelation()
                v = reader.getLastValue()
                polarity = reader.nar.polarity

                ############################# 
                # QUERY VENDORS about STATUS  
                ############################# 
                self.data.UpdateFromSource() # currently a dummy funciton

                if self.data.status==ORDER_HASID: # when order exists but has never been updated
                   self.data.status = ORDER_RECEIVED
                   
                # SYNC responder
                status = self.data.status
                self.responder.stage = status
                
                # CAVEATS 
                                
                if t=='what': # details requested
                    self.caveat = self.data.show()
                    return 

                # Begin handling questions, per current state
                if status==ORDER_RECEIVED:
                    if t=='when':
                        self.caveat = "Tomorrrow am"
                    else:
                        self.caveat = "Your order has been placed. It will be in design within 5 minutes"
                elif status==ORDER_INDESIGN:
                    if t=='why' and v=='delay':
                        self.caveat = "I don't know. I'll ask operations to contact you."
                    elif t=='where':
                        self.caveat = "It is being manufactured"
                    else:
                        self.caveat = "The order is not ready"
                elif status==ORDER_RECEIVED:
                    if t=='why' and v=='delay':
                        self.caveat = "I don't know. I'll ask operations to contact you."
                    elif t=='where':
                        self.caveat = "It is being manufactured"
                    else:
                        self.caveat = "The order is not ready"
                elif status==ORDER_SHIPPED:                
                    self.caveat = "It shipped this morning"
                else:
                    self.caveat= 'It is delivered'
 
                  
        def Write( self ):
            outtext = NWDataChat.Write(self)
           
            return outtext 


class OrderAppChat( TChat ):
    def __init__(self, id):
        self.id = id #CONVERSATION ID. NOT ORDER ID

        self.appResponder = DefaultAppResponder()      

        self.orderdata = OrderData()
        self.orderchat   = OrderChat(self.orderdata)

        self.accountchat = AccountChat()
        self.aboutchat  = AboutChat()

        self.outtext = ''

        self.currentChat = self # can switch to self.dental, or to ...

    def Clear(self):
        self.orderdata = OrderData()
        self.orderchat   = OrderChat(self.orderdata)
        self.outtext = ''
        self.currentChat = self # can switch to self.dental, or to ...


    def SetReceived(self):
        self.orderdata.status = ORDER_RECEIVED
    def SetInDesign(self):
        self.orderdata.status = ORDER_INDESIGN
    def SetNeedApprove(self):
        self.orderdata.status = ORDER_NEEDAPPROVED
    def SetApproved(self):
        self.orderdata.status = ORDER_BEENAPPROVED
    def SetInManufacturing(self):
        self.orderdata.status = ORDER_INMANUFCTR
    def SetOnHold(self):
        self.orderdata.status = ORDER_ONHOLD
    def SetShipped(self):
        self.orderdata.status = ORDER_SHIPPED
    def SetDelivered(self):
        self.orderdata.status = ORDER_DELIVERED

    def Save(self, cvLoc):
        fname = cvLoc + self.id + ".txt"
        f = open(fname,'w')
        cPickle.dump( self.orderdata, f ) 
        f.close()

    def Load(self, cvLoc):
        fname = cvLoc + self.id  + ".txt"
        # if file does not exist, create it
        # The order data is constructed by default
        if not os.path.isfile(fname) : 
            f = open(fname,'w')
            f.close()
            return

        f = open(fname, 'r' )
        try:
            self.orderdata = cPickle.load( f )
        except: # if corrupt
            f = open(fname,'w') # re-create the file
            f.close()
            return

        self.orderchat.data = self.orderdata # needs to be reset each time
        self.orderchat.responder.stage = self.orderchat.data.status
        f.close()
    
    def GetID(self):
        return self.orderchat.data.id    

    def Read(self, text):
        self.outtext = ''

        # always be on the lookout for polite banter. Cannot defer that to sub-chats.
        self.aboutchat.Read(text)  
        if self.aboutchat.gof >= 0.5:
          self.appResponder.stage = APP_HELLO 
          v = self.aboutchat.Write()
          self.outtext += self.appResponder.getStageResponse().format(v)
          self.currentChat = self
          return

        # Enable sub-chat

        if self.currentChat != self:
            #TODO: remove assumption that the currentChat is the orderchat

            # a distraction from the achitecture
            wasstringmode = self.currentChat.stringmode

            self.currentChat.Read(text) 
            g = self.currentChat.gof
            if g >= 0.5: # use '>' ?
                self.gof = g
                self.outtext = self.currentChat.Write()

                ### A kind of hack: the 'readers' may not have been cleared since 
                # before the order number was entered, so go ahead and answer the 
                # question now, if you can
                if wasstringmode:
                    self.currentChat.update()
                    self.outtext += self.currentChat.Write()
                return

            else:
                self.currentChat = self
      
        self.orderchat.Read(text)
        self.accountchat.Read(text)
 
        v = ''

        if self.accountchat.gof> 0.5:
           self.appResponder.stage = APP_ACCOUNT

        elif self.orderchat.gof > 0.3:
           self.appResponder.stage = APP_TOPIC

           self.currentChat = self.orderchat
           v = self.orderchat.Write()

        else:
            self.appResponder.stage = APP_HUH

        t = self.appResponder.getStageResponse()
        self.outtext += self.appResponder.getStageResponse().format(v)

    def Write(self):
        return self.outtext
    
 