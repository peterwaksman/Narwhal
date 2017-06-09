""" ask.py is a place to define the vocabulary of questions

And anything else you can think of. Grouped as I see fit but you
can re-arrange it or sub divide it if you like.

"""
from narwhal.nwtypes import KList
from narwhal.nwchat import NWChatnode


# in spoken language this can be an inflection 
kQUESTION = " ? , ask # about, question, question about , questions about , problem , problem with, need to know , want to know, help with , information " 

kWHO = " who , who are" #asking for a person
kHOW = " how # much|often, not sure how , do I " #asking for instructions
kWHEN = " when , how long , how long until , how long will it take " #asking for a time
kWHERE = " where , where from , where to , where are " #asking for a place

kWHAT = " what , what are, status , check , to check , verify ,\
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
kREQUEST = ' please , use , build , sell me , fabricate , produce , provide ,\
 provide me , make , make me , to make , my|the|an $ order , to order ,\
 want , want to , want you to, need ,need to , need you to, give me ,  '
REQUEST = KList( "request", kREQUEST ).var()

#########################################
# not really quantities but what the heck

kYOU = ' you , dentsply '
YOU =  KList( "you", kYOU ).var()
#########################################
kYES = ' yes , ok '
YES = KList("YES",kYES).var()
kNO = ' no '
NO = KList("NO",kNO).var()
YES_NO = KList("YES",kYES).var() | KList("NO",kNO).var()
yesno = YES_NO.nar()

#YESCONTEXT = 0
#NOCONTEXT = 1
#class YesNoChat( NWChatnode ):
#    def __init__(self):
#        self.yes = True
#        yesno = YES_NO.nar()
#        A = [ yesno ]
#        NWChatnode.__init__(self, YES_NO , A)

#    def getContext(self):
#        if self.yes:
#            return "YES"
#        else:
#            return  "NO"

#    def read(self, segment, tokens ):
#        readAll(self,segment,tokens)

