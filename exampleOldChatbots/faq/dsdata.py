import os     
import sys

# add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *
from stdtrees.ask import *

#from faqtree import *
from faqanswer import *


#-----------------------------------------------
#------------- particular ----------------------
#-----------------------------------------------

kCONX = "connections, personal data, job data, job , org charts, career"
kLMS = "lms, learning, training, compliance, regulatory"
kPHOTO = "photo" 
kBENEF  = "benefits, medical, health, dental, vision, life,\
 beneficiaries, spousal, spouse, wife, husband, child, disablility, \
 health advocate, insurance, accident, event, qualifying event, pain, sick" 
kIT  = " it, tech support, technical support, computer" 
kEMPLOY = "employment" 
kEXPENS = "expenses, travel expenses, databasics" 
kTRAVEL  = "travel" 
kTIME   = "time" 
kPOLICY = "policies"
 
HRVocab = [
     kCONX, 
     kLMS,
     kPHOTO,
     kBENEF,
     kIT,
     kEMPLOY,
     kEXPENS,
     kTRAVEL,
     kTIME,
     kPOLICY
    ]

HRPHONE = "-"
HRGENINFO = "\n\
  *Connections (personal data, job data, org charts, careers)\n\
  *Learning (Corporate Training)\n\
  *Employee Photo\n\
  *Benefits (medical, health, dental, vision, life, beneficiaries, spousal, spouse, wife, husband, child, disablility)\n\
  *IT (technical support)\n\
  *Employment Verification\n\
  *Databasic (Expense Reports)\n\
  *BCD Travel (Concur, ie Business Travel Arrangements)\n\
  *Time and Attendance (US ONLY)(ADP Enterprise eTime, ie Vacation, Jury Duty, etc Requests)\n\
  *iPay (US ONLY)(Pay Statements, W-2's - Option to go paperless)\n\
  *Policies and General Info\n\n"

HRBASEDATA = FAQBaseData( "HR", HRGENINFO, HRPHONE, "Lyndy Seney", HRVocab)



kCONX2 = "goals, performance, learning, careers, company info, personal" 

CONXBASEDATA = FAQBaseData("CONX", kCONX , "-", "Lindy Seney", [kCONX, kCONX2] )

class ConnectionsAnswer( FAQAnswer ):
    def __init__(self ):
        FAQAnswer.__init__(self, CONXBASEDATA.id, CONXBASEDATA.vocabLists )
        self.url.set('https://connected.dentsply.com/adfs/ls/idpinitiatedsignon.aspx',
                    'your internal\diXXXXX account and the same password used to log into outlook email', 
                    'Chrome') 

CNXChat = FAQAnswerChat( ConnectionsAnswer() )


class ConnectionsChat( FAQAnswerChat ):
    def __init__(self ):
        FAQAnswerChat.__init__(self, ConnectionsAnswer() )
        x = 2

    def update(self):
        x = 2
CNXChat = ConnectionsChat( )



#-------------------------------------------------------
kLMS = " lms , learning, training, compliance, corporate training, courses"

LMSBASEDATA = FAQBaseData("LMS", kLMS, "-", "Katie Bianchi" , [kLMS] )
class LMSAnswer( FAQAnswer ):
    def __init__(self ):
        FAQAnswer.__init__(self, LMSBASEDATA.id, LMSBASEDATA.vocabLists )
        self.url.set('https://connected.dentsply.com/adfs/ls/idpinitiatedsignon.aspx',
                    'your internal\diXXXXX account and the same password used to log into outlook email', 
                    'Chrome') 
LMSChat = FAQAnswerChat( LMSAnswer() )

HRAnswerChats = {
                    'cnx' : CNXChat,
                    'lms' : LMSChat,
                }

