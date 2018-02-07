import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *
from stdtrees.tchats import *
 
from dentalTree import *  
from dentalData import *

from abtSketch2 import AbutmentSketch

SENSE_CUTOFF = 0.3

BaseResponder = DefaultResponder() #NWTopicResponder(aResponse, aResponseV)

###################################################
class BaseChat( NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, BaseTopic, BaseResponder)
        
        self.data = None       
        self.caveat = ''   # for out-of-bounds warning 

    def SetData( self, data):
        if isinstance(data, AllAbutments):
            self.data = data.base
        else:
            self.data = data #??

    def update(self):
        NWTopicChat.update(self)
        if self.gof==0:
            self.responder.stage = AQU  
            return

        self.responder.stage = AOK  

        data = self.data #for readablity

        for reader in self.topic.readers:
            id = reader.id

            t = reader.getLastThing()
            a = reader.getLastAction()
            r = reader.getLastRelation()
            v = reader.getLastValue()
            T = reader.getLastThingVAR()
            A = reader.getLastActionVAR()
            R = reader.getLastRelationVAR()
            V = reader.getLastValueVAR()
           
            polarity = reader.nar.polarity

            if id=='epsReader' and reader.GOF>=0.75:
                data[0].eps.value = v
                self.responder.stage = AOK
                self.caveat = 'setting emergence profile ' + v
      
            elif id=='tpReader' and reader.GOF>=0.66: 
                data[0].pressure.value = float(v)
                self.responder.stage = AOK
                self.caveat = 'setting tissue pressure to ' + v 

            elif id=='tpReader2' and reader.GOF>=0.66: 
                if v=='weak' or (polarity==False and v=='strong' ):
                    data[0].pressure.value = 0.1
                    self.responder.stage = AOK
                    h = str( 0.1 )
                    self.caveat = 'setting tissue pressure to ' + h
                    x=2
            #TODO, handle tooth numbers when id=='toothfeatureR' has data
 
    def write(self):
        s = self.responder.getStageResponse().format(self.caveat)
        return s

################################################

class MarginChat( NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, MarginTopic , DefaultResponder())
        
        # don't implement data ownership
        self.data     = None
         
    def Read(self, text):
        NWTopicChat.Read(self,text)
                # implement a policy for 0.5
        if self.gof==0.5:
            self.gof = 0 # so many implicits, when down to .5 you got nothin

        # assumes the data is an AllAbutments
    def SetData(self, data):
        if isinstance(data, AllAbutments):
            self.data = data.margin
        else:
            self.data = data # a reference, not a copy

    def fillData(self, Vault, TVault):
                        
       # margin = self.data[toothno]  # allows toothno== 
        toothno = 0
        it = 0 # wants to be index in TVault 
        if it<len(TVault):
            c = Value( TVault[ it ].lastConst )
            if c.isdigit():
                toothno = int( Value( TVault[ it ].lastConst ) )
            it += 1

        outtext = ''
        rel = ''
        ref = ''
        margin = MarginData()
        spec = MarginSpec()

        for v in Vault:
            lc = v.lastConst

            side = Thing(lc)


            r = Relation(lc) # stores the relation
            f = Value(lc) # stores the reference feature
            
            if len(r)>0:
                rel = r
            if len(f)>0:
                ref = f

            if len(r)*len(f)==0 and side=='': # yu need something
                return outtext

            amount = Action(lc)
            if amount and float(amount):
                a = float(amount)
            elif r=='at':
                a = 0.0
            else:
                a = 2.0 # or use customer pref


            if len(r)*len(f)==0 and spec.hasData():
                spec.value = a
            else:
                spec = MarginSpec(rel,ref,a)

            isset = False
            if side=='mesial' or side=='md': # code is probably simpler using 'MD'    
                margin.M = spec
                isset = True
                outtext += ' mes margin '
            if side=='distal' or side=='md':
                margin.D = spec
                isset = True
                outtext += ' dist margin '

            if side=='facial' or side=='bf' or side=='labial':
                margin.F = spec
                isset = True
                outtext += ' bf margin '

            if side == 'lingual':
                margin.L = spec
                isset = True
                outtext += ' ling margin '

            if side=='remainder':
                print(" NOT IMPLEMENTED, use init values as signal?")
                isset = True
                outtext += ' others at '

            if not isset or side=='all':
                margin.M = spec
                margin.D = spec
                margin.F = spec
                margin.L = spec         
                outtext += ' (M,D,F,L) margins on tooth#' + str(toothno) + ' '
             
            outtext += str(a) + ' ' + rel + ' ' + ref + '\n'

            self.data[toothno] = margin

            if toothno>0:
                self.data[0] = margin # save latest

            if it<len(TVault):           
                toothno = int(Value( TVault[ it ].lastConst ))
                it += 1

        return outtext

    def update(self):
        NWTopicChat.update(self)
        if self.gof==0:
            self.responder.stage = AQU  
            return
        
        self.responder.stage = AOK              

                # margin reader, side surface reader  
        mReader = self.topic.readers[0]
        if mReader.GOF==0:
            self.responder.stage = AQU  
            return

        mtReader = self.topic.readers[1]
         
        polarity = mReader.nar.polarity # assume it is same for both nars
              
        side = mReader.getLastThing()
        amount = mReader.getLastAction()
        rel = mReader.getLastRelation()
        ref = mReader.getLastValue()     
        V = mReader.reader.vault._vault   


        feature = mtReader.getLastThing()      
        W = mtReader.reader.vault._vault   

        if side=='' and amount=='' and ref=='':
            self.responder.stage = AQU              
            self.caveat = ''
            return
         
        # feature can be missing but not set to something else
        if feature != 'margin' and feature != '':
        #if feature != 'tooth' and feature != '':
            self.responder.stage = AQU              
            self.caveat = ''
            return

        c = self.fillData(V,W)
        self.caveat = c

    def write(self):
        return self.responder.getStageResponse().format(self.caveat)


 
class DentalChat(  NWTopicChat ):
    def __init__(self):
 
        # root piece of data
        self.sites = ToothSites()

        # supposed to display the tooth sites, but for now
        self.sketch = AbutmentSketch()

        # language UI for abutments
        self.abutmentChat = MarginChat() + BaseChat()
        self.abutmentChat.SetData(self.sites.abutments)

    
    def Read(self, text):
        self.abutmentChat.Read(text)
        self.gof = self.abutmentChat.gof

        if self.gof>0.3:
            self.draw()
        x = 2

    def Write(self):
        s = self.abutmentChat.Write()
        return s

    def draw(self):
        self.sites.updateSketch( self.sketch )


"""
Handle questions. 
"""
class DentalQuestionChat( NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, DentalQuestionTopic , DefaultResponder())
    def Read(self, text):
        NWTopicChat.Read(self, text)    
        self.update() 
          
    def update(self):
        NWTopicChat.update(self)
        if self.gof==0:
            self.responder.stage = AQU  
            return
        
        subject = self.topic.readers[0].getLastValue()

        # either we think subject is incompletely specified - so ask for clarification  
        # or
        # the subject is  specified and we have a good answer.

        x = 2


#######################################################
# Nars for getting the agenda


 
#######################################################
ACTREE = KList("acctree","").var()
ACTREE.sub(CLIENTASK)
ACTREE.sub(MYACCOUNT)
accountAsk = attribute(QUESTION, MYACCOUNT)
AccountAgendaReaders = [
                        NWTopicReader("account", ACTREE, accountAsk)
                     ]

#################################################
APP_HUH = 0
APP_HELLO = 1
APP_DENTAL = 2
APP_ACCOUNT = 3 
# qchatR[i] is singular qchatRVs[i] is a list, hence the plural
appR = { 
    APP_HUH :  "hmm?",
    APP_HELLO : "{}",
    APP_DENTAL : "I can help you with that...\n{}",
    APP_ACCOUNT : "For account info phone (978)xxx-xxxx"
    }
appRVs = {
    APP_HUH :  [],
    APP_HELLO : [],
    APP_DENTAL : [],
    APP_ACCOUNT : []
    }

##################################################
"""
For now an "agenda" can be supported either with an NWTopicReader 
without response mechanisms - which is informational, or an
agenda can be supported by a TChat
"""
##################################################

"""
 Agendas are:
        Unknown (hun...what?)
        Social (hello)
        Account question (call...)
        Dental question or request (I can help with that...)

Why have a separate agenda for determining dental, why not just get right to it?
Answer is: because setting a dental context is separate and can be included in a
statement but needs some acknowledgement, because it sets the context of discussion.
"""
class AppChat( TChat ):
    def __init__(self):
        TChat.__init__(self)

        self.appResponder = NWTopicResponder( appR, appRVs )

                # includes questions and requests
        self.dentalAgenda = NWTopic( DTREE, DentalAgendaReaders ) 

        self.accountAgenda = NWTopic(ACTREE, AccountAgendaReaders)

        self.about = AboutChat()
        self.dental = DentalChat()
        self.dentalQ = DentalQuestionChat()

        self.outtext = ''

        self.currentChat = self # can switch to self.dental, or to ...

    def Read(self, text):
        # this allows me to spawn a sub-chat
        if self.currentChat != self:
            self.currentChat.Read(text) 

            # The sub-chat can retain control by manipulating its gof
            # But otherwise, control returns to 'self', and reading is done below
            g = self.currentChat.gof
            if g >= 0.5: # use '>' ?
                self.gof = g
                self.outtext = self.currentChat.Write()
                return
            else:
                self.currentChat = self
              


        self.dentalAgenda.read(text)
        self.accountAgenda.read(text)
        self.about.Read(text)  
 
        v = ''

        if self.accountAgenda.maxGOF > 0.5:
           self.appResponder.stage = APP_ACCOUNT

        elif self.about.gof >= 0.5:
          self.appResponder.stage = APP_HELLO 
          v = self.about.Write()

        elif self.dentalAgenda.maxGOF > 0.3:
           self.appResponder.stage = APP_DENTAL

           self.dental.Read(text)
           self.dentalQ.Read(text)
           if self.dental.gof > self.dentalQ.gof:
               dchat = self.dental           
           else:
               dchat = self.dentalQ 

           self.currentChat = dchat
           v = dchat.Write()

        else:
            self.appResponder.stage = APP_HUH

        self.outtext = self.appResponder.getStageResponse().format(v)

    def Write(self):
        return self.outtext
    
 