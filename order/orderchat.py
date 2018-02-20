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

ochatR = { 
    ORDER_NONE : "I don't have an order number.\nPlease enter your ORDER #:",
    ORDER_HASID : "Order number {} ... checking status\n",# gets appended to
    ORDER_UPDATED : "{}",
    ORDER_READY: "It is ready for you."
    }
ochatRVs = {
    ORDER_NONE : [],
    ORDER_HASID : [MYORDER],
    ORDER_UPDATED : [MYORDER],
    ORDER_READY : [MYORDER]
    }

OrderResponder = NWTopicResponder( ochatR,ochatRVs )
 

class OrderChat( NWDataChat ):
        def __init__(self, orderdata):
            NWDataChat.__init__(self, OrderAskTopic, OrderResponder)   
            self.data = orderdata       
            self.caveat = ''   # for out-of-bounds warning 
            self.stringmode = False


        def Read(self, text):
            if self.stringmode:
                self.caveat = text
                self.responder.stage = ORDER_HASID
                self.stringmode = False
                self.data.id = text
                self.data.status = ORDER_HASID
                return
            NWDataChat.Read(self,text)

        def update(self):
            NWDataChat.update(self)
            if self.gof==0:
                #self.responder.stage = AQU  
                return

            data = self.data #for convenience
            for reader in self.topic.readers:
                id = reader.id
                if not id=='orderinfo': #necessary dependency?
                    return

                if not self.data.hasData():
                    self.stringmode = True
                    self.responder.stage = ORDER_NONE                 
                    return

                self.outtext = ''

                t = reader.getLastThing()
                a = reader.getLastAction()
                r = reader.getLastRelation()
                v = reader.getLastValue()
                polarity = reader.nar.polarity

                         # here get the status
                if t=='what':
                    self.caveat = self.data.show()
                else:
                    self.caveat = "NOT READY"
                if self.gof>= 0.3 :
                   self.responder.stage = ORDER_UPDATED
                   self.data.status = ORDER_UPDATED
  
                  
        def Write( self ):
            outtext = NWDataChat.Write(self)
           
            return outtext 


class OrderAppChat( TChat ):
    def __init__(self, id):
        self.id = id #conversation ID  

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
        self.orderdata = cPickle.load( f )
        self.orderchat.data = self.orderdata # needs renewal

        f.close()
        

    def Read(self, text):
        self.outtext = ''

        # this allows me to spawn a sub-chat
        if self.currentChat != self:
            wasstringmode = self.currentChat.stringmode # save
            self.currentChat.Read(text) 
            g = self.currentChat.gof
            if g >= 0.5: # use '>' ?
                self.gof = g
                self.outtext = self.currentChat.Write()

                ### A kind of hack: the readers may not have been cleared since 
                # before the order number was entered, so go ahead and answer the 
                # question now, if they can
                if wasstringmode:
                    self.currentChat.update()
                    self.outtext += self.currentChat.Write()
                return

            else:
                self.currentChat = self
              

        self.aboutchat.Read(text)  
        self.orderchat.Read(text)
        self.accountchat.Read(text)
 
        v = ''

        if self.accountchat.gof> 0.5:
           self.appResponder.stage = APP_ACCOUNT

        elif self.aboutchat.gof >= 0.5:
          self.appResponder.stage = APP_HELLO 
          v = self.aboutchat.Write()

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
    
 