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


"""
FAQTREE for words we expect to encounter in general

ANSWERTREE for filling questiondata and responding to 
specific questions.

Let's start with the grand plan of an FAQTREE 
"""

HUMAN = KList("human","human, person , real person").var()
ROBOT = KList("bot"," bot , chat bot, chatbot, robot, ai , language assistant").var()
VOICE = KList("voice","").var()
VOICE.subs([HUMAN , ROBOT ])

HELP = KList("help","help, instruction, direction, guidance, how to").var()

SWEAR = KList("swear","fuck, shit, cunt, ass , suck").var()

FAQTREE = KList("faqtree","").var()
FAQTREE.subs([VOICE, HELP, SWEAR]) 
FAQTREE.subs( [QUESTION, REQUEST, YOU, I_ME, HELLO , YES_NO, THANKS ] )

ruhuman = attribute(QUESTION, YOU, VOICE )
iwanthuman = attribute(REQUEST, VOICE )
ihavequestion = attribute(I_ME, QUESTION )
ineedhelp = attribute(I_ME, HELP, [REQUEST])
teachme = attribute(QUESTION, HELP)
swear = attribute( YOU, SWEAR)


H = [ 
     NWTopicReader("ruhuman", FAQTREE, ruhuman),
     NWTopicReader("iwanthuman", FAQTREE, iwanthuman) ,
     NWTopicReader("ihavequestion", FAQTREE, ihavequestion) ,
     NWTopicReader("ineedhelp", FAQTREE, ineedhelp) ,
     NWTopicReader("teachme", FAQTREE, teachme) ,
     NWTopicReader("about", FAQTREE, about ), 
     NWTopicReader("hello", FAQTREE, hello ),  
     NWTopicReader("thankyou", FAQTREE, thankyou ),
     NWTopicReader("cuss", FAQTREE, swear ),
    ]


FAQTopic = NWTopic( FAQTREE, H )


#------------------------------------------------------
kCONNECTIONS = "connections, personal data, job information, job listings, careers, org chart"
CONNECTIONS = KList("connections",kCONNECTIONS).var() 

kLMS =  "learning, training, required training, compliance training, corporate training, corporate compliance training"
LMS = KList("lms", kLMS).var()
       
FAQANSWERS = KList("faqanswers","").var()
FAQANSWERS.subs( [CONNECTIONS, LMS] )
