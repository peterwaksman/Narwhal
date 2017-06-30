""" ask.py is a place to define the vocabulary of questions

And anything else you can think of. Grouped as I see fit but you
can re-arrange it or sub divide it if you like.

"""
from narwhal.nwtypes import * #KList, attribute
from narwhal.nwchat import NWChatnode, strAPOLOGY
from narwhal import nwutils as nwu
from narwhal import nwvault as nwv




# in spoken language this can be an inflection 
kQUESTION = " ? , ask # about, question, question about , questions about , problem , problem with, need to know , want to know, want to find out, help with , info, information, infomation " 

kWHO = " who , who are" #asking for a person
kHOW = " how # much|often, not sure how , do I " #asking for instructions
kWHEN = " when , how long , how long until , how long will it take " #asking for a time
kWHERE = " where , where from , where to , where are " #asking for a place

kWHAT = " what , are you, to find out, finding out, what are, status , check , to check , verify ,\
 ask about, ask if, to ask about , information " #asking for information

kWHY = " why " #asking for a story
kDOES = " do you , does it , can it " #asking about possibility
kCAN = " can I , may I , will you , can you " # asking permission for an action
kAMOUNT = " how much , how often , how well , how many " #asking for a quantity


QUESTION = KList( "ask" , kQUESTION ).var()

WHO = KList( "who", kWHO ).var()
HOW = KList( "how", kHOW ).var()
WHEN = KList( "when", kWHEN ).var()
WHERE = KList( "where", kWHERE ).var()
WHAT = KList( "what",kWHAT ).var()
WHY = KList( "why", kWHY ).var()
DOES = KList( "does", kDOES ).var()
CAN = KList( "can", kCAN ).var()
AMOUNT = KList("amount", kAMOUNT ).var() 

QUESTION.sub(WHO)
QUESTION.sub(HOW) 
QUESTION.sub(WHEN)
QUESTION.sub(WHERE) 
QUESTION.sub(WHAT)  
QUESTION.sub(WHY) 
QUESTION.sub(DOES) 
QUESTION.sub(CAN) 
QUESTION.sub(AMOUNT)


########################################
########################################
kREQUEST = ' please , use , build , ask for , sell me , fabricate , produce , provide ,\
 provide me , make #an , make me , to make , my|the|an $ order , to order ,\
 want , want to , want you to, need ,need to , need you to, give me ,  '
REQUEST = KList( "request", kREQUEST ).var()

#########################################
# not really quantities but what the heck

kYOU = ' you , dentsply, person '
YOU =  KList( "you", kYOU ).var()
#########################################
kYES = ' yes , ok , y , done , no problem'
YES = KList("YES",kYES).var()
kNO = ' no # problem , n , not '
NO = KList("NO",kNO).var()

#YES_NO = KList("YES",kYES).var() | KList("NO",kNO).var()
YES_NO = KList("yesno", "yesno" ).var()
YES_NO.sub(YES)
YES_NO.sub(NO)

""" 
YES_NO could be handled several different ways:
 - as a nar based on a var with polarity. In this case slot Events will
   not be useful because the last const is not a VAR name but a token
 - as a nar based on a var parent (yesno) with two children ( yes and no)
   In that case the name of the child found would be available instead of the
   lastConst. 
 - as an two valued "unknown", tested using recordSlotEvents(), and readable
 from the lastConst. However there are too many spellings to check for that 
 too work well.
 
 I guess you cannot have your cake (two alternate values) and eat it too 
 (have the value equal what was typed). So I do the first option. 
"""
yesno = attribute([YOU], YES_NO )

class YesNoChat( NWChatnode ):
    def __init__(self, parent, responder, lbool):
        self.yes = True

        NWChatnode.__init__(self, YES_NO , [ yesno ])
        self.parent = parent
        self.responder = responder
        self.lbool = lbool # a list of answers
        x = 2

    def getContext(self):
        return "YES/NO"

    def read(self,segment,tokens):

        self.readAll( segment, tokens) 
 
        self.ibest = self.bestFitI() 

        ibest = self.ibest # onely one nar, so -1 or 0

        eventrecord = nwv.recordSlotEvents(yesno, segment)
        val = None
        for event in eventrecord :
            val = nwv.Value( event[1] ) # phew!

        if ibest<0:
            self.response = strAPOLOGY
            val = ''
            self.yes = None
        else:   
            if val=='YES':
               polarity = True
            else:
                polarity = False

            #polarity = self.nreaders[0].nar.polarity # see above comment
            self.yes = polarity
            self.parent.lastConst = val
            self.response = '' #haven't thought of a reason to use this

        self.restoreParentControl()

        #self.parent.lastConst = nwu.Value( self.lastConst )


        if self.yes==True or self.yes==False: 
            self.lbool.append( self.yes )

        return ibest



def OK(parent, responder, lbool):
    Y = YesNoChat(parent,responder, lbool)
    responder.node = Y


######################################
######################################
kUNDO = " undo, no , not that, no that's not right, no that is not right, wrong,\
cancel, cancel that, not right, not what I want, redo, redo that"
UNDO = KList( "undo", kUNDO ).var()