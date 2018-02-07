""" 
A "tchat" is a NWTopicChat with data in it.

Implementing some basic NWTopicChat's: an AboutChat that answers questions and a ConfirmChat
that gets confirmation from the client.
"""

from narwhal.nwutils import *
from narwhal.nwchat import *
from narwhal.nwtypes import *  
from narwhal.nwcontext import *

from stdtrees.ask import *


SENSE_CUTOFF = 0.3

## Build a TChat for basic questions from the client
# final grouping

################# VARS NARS AND CLIENTASK TREE ################
###VARS
CLIENTASK = KList( "clientask", ' i , me , we ').var()
CLIENTASK.sub(QUESTION) 
CLIENTASK.sub(REQUEST) 
CLIENTASK.sub(YOU)  
CLIENTASK.sub(HELLO)
CLIENTASK.sub(YES_NO) #this ensures YES_NO is used when the CLIENTASK tree is used.
CLIENTASK.sub(THANKS)

#TOPIC = KList( "topic", "" ).var() # use TOPIC.sub() elsewhere
#CLIENTASK.sub(TOPIC)

###NARS
about = attribute(QUESTION,YOU)
hello = attribute(HELLO,HELLO) 
# have yesno defined in ask.py
#asktopic = attribute(QUESTION, TOPIC )
#requesttopic = attribute(REQUEST, TOPIC )
thankyou = attribute(THANKS, YOU)
 

 
Q = [ 
        NWTopicReader('about', CLIENTASK, about ), 
        NWTopicReader('hello', CLIENTASK, hello ),  
        #NWTopicReader('asktopic', CLIENTASK, asktopic ),
        #NWTopicReader('requesttopic', CLIENTASK, requesttopic ),
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

class AboutChat( NWTopicChat ):
    def __init__(self ):
        NWTopicChat.__init__(self, QueryTopic, QueryResponder)

    def update(self):
        NWTopicChat.update(self)

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
                t = Thing(reader.lastEvent[1])
                if t=='how':
                    self.responder.extratext = "Good thank you. I finally got my mood swings under control"
                elif t=='can' or t=='does':
                    self.responder.extratext = "I can help you order dental products and services"
                elif t=='where':
                    self.responder.extratext = "I am a program, ghosting around in your machine"
                else: #if t=='who':
                    self.responder.extratext = "I am Version 1.0 of a 'dental' chatbot,\n written by Peter Waksman"
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

class ConfirmChat( NWTopicChat ):
    def __init__(self ):
        NWTopicChat.__init__(self, ConfirmTopic, ConfirmResponder)
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
        NWTopicChat.Read(self, text)

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

        NWTopicChat.update(self)
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
                        


        



    

   