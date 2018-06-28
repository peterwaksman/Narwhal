""" 
A "tchat" is a NWDataChat with data in it.

Implementing some basic NWDataChat's: an AboutChat that answers questions and a ConfirmChat
that gets confirmation from the client.
"""

from narwhal.nwutils import *
from narwhal.nwchat import *
from narwhal.nwtypes import *  
from narwhal.nwsegment import *

from stdtrees.ask import *


SENSE_CUTOFF = 0.3

## Build a TChat for basic questions from the client
# final grouping


 
Q = [ 
        NWTopicReader('about', CLIENTASK, about ), 
        NWTopicReader('hello', CLIENTASK, hello ),  
        NWTopicReader('thankyou', CLIENTASK, thankyou ),
    ]  

#######################################################
QueryTopic = NWTopic( CLIENTASK, Q )

######################################################3
QUERYNONE = 0
QUERYHI = 1
QUERYABOUT = 2
QUERYTOPIC = 3 
QUERYTOPIC2 = 4 
QUERYTHANKS = 5

# qchatR[i] is singular qchatRVs[i] is a list, hence the plural
qchatR = { 
    QUERYNONE : "-sigh-",
    QUERYHI : "Hi, Hello, Good morning\nCan I help you?",
    QUERYABOUT: "A chatbot",
    QUERYTOPIC: "Yes I can help you with {} information",
    QUERYTOPIC2: "Yes I can help with {}(s). What do you need?",
    QUERYTHANKS: "You are welcome"
    }
qchatRVs = {
    QUERYNONE : [],
    QUERYHI : [HELLO],
    QUERYABOUT : [YOU],
    QUERYTOPIC : [],
    QUERYTOPIC2 : [],
    QUERYTHANKS : []
    }

QueryResponder = NWTopicResponder( qchatR, qchatRVs )
#########################################

class AboutChat( NWDataChat ):
    def __init__(self ):
        NWDataChat.__init__(self, QueryTopic, QueryResponder)
        self.version = "I am Version 1.0 of a 'dental' chatbot, written by Peter Waksman, circa 2018"
        self.capabilities = "I can order dental products and check the status of orders"
    def update(self):
        NWDataChat.update(self)

        if self.gof<=SENSE_CUTOFF:
            self.responder.stage = QUERYNONE
            self.gof = 0.0 # maybe not a good habit?
            return

        reader = self.topic.getBestReader()
        if reader :
            id = reader.id
            if id=='about':
                if self.gof<= 0.5:
                    self.responder.stage = QUERYNONE
                    self.gof = 0.0 # maybe not a good habit?

                self.responder.stage = QUERYABOUT
                if reader.lastEvent:
                    t = Thing(reader.lastEvent[1])
                else:
                    t=''
                if t=='how':
                    self.responder.extratext = "Good thank you. I finally got my mood swings under control"
                elif t=='can' or t=='does':
                    self.responder.extratext = self.capabilities
                elif t=='where':
                    self.responder.extratext = "I am a program, ghosting around in your machine"
                elif t=='why':
                    self.responder.extratext = "Geez! That's a tough one... I guess cuz it's a win-win"
                else: #if t=='who':
                    self.responder.extratext = self.version
            elif id=='hello':                  
                self.responder.stage = QUERYHI
                self.responder.extratext = self.responder.getStageResponse()
            elif id=='asktopic':
                if self.gof<= 0.5:
                    self.responder.stage = QUERYNONE
                    self.gof = 0.0 # maybe not a good habit?
                    return
                v = reader.getLastValue()
                self.responder.stage = QUERYTOPIC       
                self.responder.extratext = self.responder.getStageResponse().format(v)

            elif id=='requesttopic':
                if self.gof<= 0.5:
                    self.responder.stage = QUERYNONE
                    self.gof = 0.0 # maybe not a good habit?
                    return               
                v = reader.getLastValue()
                #V = reader.getLastValueVAR()

                self.responder.stage = QUERYTOPIC2       
                self.responder.extratext = self.responder.getStageResponse().format(v)

            elif id=='thankyou':
                self.responder.stage = QUERYTHANKS
                self.responder.extratext = self.responder.getStageResponse()
                             
          
    def write(self):
        if self.gof>SENSE_CUTOFF:
            return self.responder.getExtraResponse()  
        else:
            return self.responder.getStageResponse()


#############################################    
###########   ConfirmChat   #################  
#############################################  
#############################################   

# ConfirmTopic
Y = [ NWTopicReader('yesno', YES_NO, yesno ) ]
ConfirmTopic = NWTopic( YES_NO, Y )
#ConfirmResponder
CONFIRM0 = 0 #not waiting
CONFIRM1 = 1 #asking client for string
CONFIRM2 = 2 #waiting for answer
CONFIRM3 = 3 #got yes/no from client
CONFIRM4 = 4 # got gobbletygook from client

confR = { 
        CONFIRM0 : "-inactive-",
        CONFIRM1 : "Please enter a {}",# eg serial#
        CONFIRM2 : "You entered {}. Is this correct?",
        CONFIRM3 : "Client confirms {} is {}",  #eg .format(serial#,yes_no)
        CONFIRM4 : "Cient does not confirm"
        }
confRVs = {
    CONFIRM0 : [],  
    CONFIRM1 : [],
    CONFIRM2 : [],
    CONFIRM3 : [],
    CONFIRM4 : []
    }
ConfirmResponder = NWTopicResponder( confR, confRVs )

class ConfirmChat( NWDataChat ):
    def __init__(self ):
        NWDataChat.__init__(self, ConfirmTopic, ConfirmResponder)
        self.confirm = NULL_VAR #or set to YES or NO
        self.label = ''  # name of value to confirm
        self.value = '' # value to confirm 
        self.rawtext = '' # for when value is a raw text without processing
        self.isYes = None #0 = no, 1=yes, 
        self.responder.stage = CONFIRM0
    
    def getReader(self): # there is only one
        return self.topic.readers[0]

    def Read(self, text):
        self.rawtext = text
        NWDataChat.Read(self, text)

    def Confirm(self, label):
        self.label = label
        self.responder.stage = CONFIRM1
        
 

    def updateYesNo(self):
        yn = self.getReader()# there is only one
         
        if not yn:
            return None
        if not yn.eventrecord:
            return None
        
        # extact the yes or no - quite a hassle
        isYes = None
        event = yn.eventrecord[0]
        if event[0]>=0.5:
            if Value(event[1])=='YES':
                self.isYes= True
            elif Value(event[1])=='NO':
                self.isYes = False
        else:
            self.isYes = None

    def update(self):
        if self.responder.stage == CONFIRM0:
            return
        if self.responder.stage == CONFIRM4 or self.responder.stage ==CONFIRM3:
            self.responder.stage = CONFIRM0

        NWDataChat.update(self)
        if self.responder.stage == CONFIRM1:
            self.responder.stage = CONFIRM2
            self.value = self.rawtext # this may be temporary

        elif self.responder.stage == CONFIRM2:
            temp = self.value
            self.responder.stage = CONFIRM4    
            self.value = ''
            if self.gof>=0.5:
                self.updateYesNo()            
                if self.isYes != None:
                    if self.isYes:
                        self.value = temp
                        self.responder.stage = CONFIRM3
                
    def write(self):
        if self.responder.stage==CONFIRM1:
            return self.responder.getStageResponse().format(self.label)
        elif self.responder.stage==CONFIRM2:
            return self.responder.getStageResponse().format( self.rawtext)
        elif self.responder.stage==CONFIRM3:
            return self.responder.getStageResponse().format( self.label, self.value)
        else:
            return self.responder.getStageResponse()
                        


        



    

   