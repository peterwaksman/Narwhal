""" ask.py is a place to define the vocabulary of questions

And anything else you can think of. Grouped as I see fit but you
can re-arrange it or sub divide it if you like.

"""
from narwhal.nwtypes import KList, attribute
from narwhal.nwchat import NWChatnode, strAPOLOGY
from narwhal import nwutils as nwu



# in spoken language this can be an inflection 
kQUESTION = " ? , ask # about, question, question about , questions about , problem , problem with, need to know , want to know, want to find out, help with , info, information, infomation " 

kWHO = " who , who are" #asking for a person
kHOW = " how # much|often, not sure how , do I " #asking for instructions
kWHEN = " when , how long , how long until , how long will it take " #asking for a time
kWHERE = " where , where from , where to , where are " #asking for a place

kWHAT = " what , to find out, finding out, what are, status , check , to check , verify ,\
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
 provide me , make , make me , to make , my|the|an $ order , to order ,\
 want , want to , want you to, need ,need to , need you to, give me ,  '
REQUEST = KList( "request", kREQUEST ).var()

#########################################
# not really quantities but what the heck

kYOU = ' you , dentsply '
YOU =  KList( "you", kYOU ).var()
#########################################
kYES = ' yes , ok , y , done'
YES = KList("YES",kYES).var()
kNO = ' no , n , not '
NO = KList("NO",kNO).var()
YES_NO = KList("YES",kYES).var() | KList("NO",kNO).var()


class YesNoChat( NWChatnode ):
    def __init__(self, parent, responder):
        self.yes = True

        yesno = attribute([YOU], YES_NO )

        NWChatnode.__init__(self, YES_NO , [ yesno ])
        self.parent = parent
        self.responder = responder
        x = 2

    def getContext(self):
        if self.yes:
            return "YES"
        else:
            return  "NO"

    def read(self,segment,tokens):

        self.readAll( segment, tokens) 
 
        self.ibest = self.bestFitI() 

        ibest = self.ibest # onely one nar, so -1 or 0

        if ibest<0:
            self.response = strAPOLOGY
            val = ''
            self.yes = None
        else:   
            val = nwu.Value( self.lastConst )
            if val=='no':
                self.yes = False
            else:
                self.yes = True 

            self.response = '' #haven't thought of a reason to use this

        self.restoreParentControl()

        # so paent can capture the yes/no on the next iteration
        self.parent.lastConst = val

        return ibest



def OK(parent, responder):
    Y = YesNoChat(parent,responder)
    responder.node = Y

