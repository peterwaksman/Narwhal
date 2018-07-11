import os 
import sys

from PIL import ImageTk, Image

"""
bouncy is a chatbot intended to move a colored "bouncing" ball around
the screen to demonstrate simple scene editing and navigation commands.

The BouncyTopic uses the (single) doAction() narrative with the BOUNCYSAYS tree.

The BouncyResponder is devoted to agreeing, asking for clarification, or exaplining
its inability.
"""


# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *
#from stdtrees.quantities import *  
#from stdtrees.ask import *  

from bouncytree import *  
from bouncyscene import *

SENSE_CUTOFF = 0.3

BOK = 0 # agree
BNOK = 1 # apologize but "no"
BQU = 2 # ask clarifaction


bResponse = {
    BOK : "ok",
    BNOK: "I {}",
    BQU : "please clarify {}"
    }

bResponseV = {
    BOK : [],
    BNOK : [],
    BQU : []
    }

BouncyResponder = NWTopicResponder(bResponse, bResponseV)


###################################################

class BouncyChat( NWDataChat ):
    def __init__(self, bdata):
        NWDataChat.__init__(self, BouncyTopic, BouncyResponder)
        # get yourself 2 instances of empty scene data
        self.data = BouncySceneData()
        self.data.copy(bdata) 
        self.prevdata = BouncySceneData()
        self.prevdata.copy(bdata)  
        self.caveat = ''   # for out-of-bounds warning 

    def Read(self, text):
        self.caveat = ''
        self.prevdata.copy(self.data) # keep copy
        NWDataChat.Read(self, text)


    def update(self):
        NWDataChat.update(self)
        if self.gof==0:
            self.responder.stage = BQU  
            return

        reader = self.topic.getBestReader()
  
        t = reader.getLastThing()
        a = reader.getLastAction()
        v = reader.getLastValue()
        T = reader.getLastThingVAR()
        A = reader.getLastActionVAR()
        V = reader.getLastValueVAR()

        data = self.data
        polarity = reader.nar.polarity

        if A<=DISPLAY:           
            if T<=BALL:
                data.balldisplay = polarity
            elif T<=SCALE:
                data.scaledisplay = polarity
        elif A<=ZOOM:
            if polarity==True:
                if data.zoom==MAXZOOM:
                    self.caveat = 'cannot zoom in further (but good luck with that)'
                else:
                    data.zoom = min( MAXZOOM, data.zoom*2 )  
                    x = 2                                   
            elif polarity==False:
                if data.zoom==MINZOOM:
                    self.caveat = 'cannot zoom out further' 
                else:
                    data.zoom = max( MINZOOM, data.zoom/2)  
                    x = 2                    
        elif A<=MAKE:
            if T<=BALL:
                if V<=COLOR:
                    data.ballcolor = v
                    x = 2
                elif V<=SIZE:
                    if not polarity:
                        if data.ballsize==BIGRAD:
                            self.caveat = 'cannot get any bigger'
                        data.ballsize = BIGRAD                    
                    else:
                        if data.ballsize==SMALLRAD:
                            self.caveat = 'cannot get any smaller'
                        data.ballsize = SMALLRAD
                else:
                    x = 2
            elif T<=SCALE:
                self.caveat = 'cannot change color or size of the scale, try zooming in or out'
        
        elif A<=MOVE:
            if T<=BALL:
                if v=='right' and polarity:
                    data.ballxy[0] = data.ballxy[0]+TICWIDTH
                elif v=='right' and not polarity:
                    data.ballxy[0] = data.ballxy[0]-TICWIDTH
                else:
                    self.caveat = 'left or right?'
            
                x = 2
        x = 2


    def write(self):
        if self.caveat:
            return self.caveat
        else:
            return self.responder.getStageResponse()
