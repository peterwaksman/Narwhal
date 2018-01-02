""" ask.py is a place to define the vocabulary of questions

And anything else you can think of. Grouped as I see fit but you
can re-arrange it or sub divide it if you like.

"""
from narwhal.nwtypes import * #KList, attribute
from narwhal.nwchat import strAPOLOGY
from narwhal import nwutils as nwu
from narwhal import nwvault as nwv
from narwhal.nwcontext import *


# in spoken language this can be an inflection 
kQUESTION = " ? , ask # about, question, question about , questions about , problem , problem with, need to know , want to know, want to find out, help with , info, information, infomation " 

kWHO = " who , who are" #asking for a person
kHOW = " how # did|much|often, not sure how , do I " #asking for instructions
kWHEN = " when , how long , how long until , how long will it take " #asking for a time
kWHERE = " where , where from , where to , where are " #asking for a place

kWHAT = " what , what about , how|where $ are , show, show me, to find out, finding out, what is, what's, what are, status , check , to check , verify ,\
 ask about, ask if, to ask about , information, tell me about " #asking for information

kWHY = " why " #asking for a story
kDOES = " do you , does it , can it " #asking about possibility
kCAN = " can I , may I , will , can " # asking permission for an action
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
  
QUESTION.sub(WHY) 
QUESTION.sub(DOES) 
QUESTION.sub(CAN) 
QUESTION.sub(AMOUNT)
QUESTION.sub(DIFF)
QUESTION.sub(WHAT)

########################################
########################################
kREQUEST = ' you get, pls , please , use , build , ask for , sell me , fabricate , produce , provide ,\
 provide me ,make sure, make #an , make me , to make , my|the|an $ order , to order ,\
 want , want to , want you to, need ,need to , need you to, give me ,add,'

kUNREQUEST = "remove, unselect, deselect"

kUNDO = "undo, undo that, not that, no that's not right, no that is not right, wrong,\
cancel, cancel that, not right, not what I want, redo, redo that"

kUNREQUEST += kUNDO

REQUEST = KList( "request", kREQUEST ).var() | KList("remove", kUNREQUEST ).var()


#########################################
# not really quantities but what the heck

kYOU = ' you # get, dentsply, person , your '
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

yesno = attribute([YOU], YES_NO )


######################################
######################################

kHELLO = ' hi , hello , greeting'
HELLO = KList("hello", kHELLO).var()


######################################
######################################


THANKS = KList("thanks", "thanks, thx, thank you").var()

#######################################
#######################################
ACTION   = KList("actions", "").var()
# subs:
SEND     = KList("send", "send, resubmit, submit , ship " ).var()
HOLD     = KList( "hold", " hold, wait").var()
DO       = KList("do", " place , show , mimic, mirror, copy, match,\
        soften, seat, connect, extract, mill, mold, mould, lap, fill, \
        trim, scoop, allow, fit, adjust, reverse, sculpt, flare the, can, get").var()
REDO     =  KList("redo", "remake, redo").var()
NOTDO    = KList("notdo", "leave, ignore")
AUTOMATE = KList( "automate","automate").var()
MOVE     = KList("move","move, bring, tilt, lean, pull, push, close the,\
             open the, expand, extend, toward").var()
MAKE     = KList("make", "make # contact, make it, turn, turn it").var()
ANGULATE = KList("angle",  "angle, angulate, align").var()    
CANTILEVER= KList("cantilever", "cantilever").var()  
ROTATE   = KList("rotate", "rotate, rot ").var()
CONTACT = KList("contact", "contact, make contact").var()

ACTION.sub(ACTION)
ACTION.sub(SEND)
ACTION.sub(HOLD)
ACTION.sub(DO)
ACTION.sub(REDO)
ACTION.sub(NOTDO)
ACTION.sub(AUTOMATE)
ACTION.sub(MOVE)
ACTION.sub(MAKE)
ACTION.sub(ANGULATE)
ACTION.sub(CANTILEVER )
ACTION.sub(ROTATE)
ACTION.sub(CONTACT)
################################### 
###################################