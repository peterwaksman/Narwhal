""" 

faqabout contains the FAQAboutChat. More full featured than the tchat.AboutChat
It also handles basic info like phone and contact info for the whole chatbot
Also FAQABOUTTREE
"""

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
FAQABOUTTREE for words we expect to encounter in general

ANSWERTREE for filling questiondata and responding to 
specific questions.

Let's start with the grand plan of an FAQABOUTTREE 
"""

HUMAN = KList("human","human, person , real person").var()
ROBOT = KList("bot"," bot , chat bot, chatbot, robot, ai , language assistant").var()
VOICE = KList("voice","").var()
VOICE.subs([HUMAN , ROBOT ])

HELP = KList("help","help, instruction, direction, guidance, how to").var()

SWEAR = KList("swear","fuck, shit, cunt, ass , suck, screw you").var()

# The FAQTREE is for words one encounters generically in an FAQ session
# Specific question vocab will be in and ANSWERTREE
FAQABOUTTREE = KList("faqabouttree","").var()
FAQABOUTTREE.subs([VOICE, HELP, SWEAR]) 
FAQABOUTTREE.subs( [QUESTION, REQUEST, YOU, I_ME, HELLO , YES_NO, THANKS ] )

ruhuman = attribute(QUESTION, YOU, VOICE )
iwanthuman = attribute(REQUEST, VOICE )
ihavequestion = attribute(I_ME, QUESTION )
ineedhelp = attribute(I_ME, [HELP], REQUEST)
#ineedhelp = attribute(I_ME, REQUEST, [HELP])
teachme = attribute(QUESTION, HELP)
swear = attribute( YOU, SWEAR)


H = [ 
     NWTopicReader("ineedhelp", FAQABOUTTREE, ineedhelp) ,
     NWTopicReader("ruhuman", FAQABOUTTREE, ruhuman),
     NWTopicReader("iwanthuman", FAQABOUTTREE, iwanthuman) ,
     NWTopicReader("ihavequestion", FAQABOUTTREE, ihavequestion) ,
     NWTopicReader("teachme", FAQABOUTTREE, teachme) ,
     NWTopicReader("about", FAQABOUTTREE, about ), 
     NWTopicReader("hello", FAQABOUTTREE, hello ),  
     NWTopicReader("thankyou", FAQABOUTTREE, thankyou ),
     NWTopicReader("cuss", FAQABOUTTREE, swear ),
    ]


FAQAboutTopic = NWTopic( FAQABOUTTREE, H )

######################################################
#########################################################
"""
FAQAboutChat is an AboutChat with some additional handling for swearing, and 
acknowledging a question.
"""

class FAQAboutChat( NWDataChat ):

    def __init__(self, genInfo, phone , contact ):
        NWDataChat.__init__(self, FAQAboutTopic, VanillaResponder())

        self.generalInfo = genInfo
        self.phone = phone
        self.contact = contact
        self.answertoggle = True

            # check after Read(), to decide about 
            # need for additional handling
        self.questionPending = False

    def Read(self, text):
        self.questionPending = False
        NWDataChat.Read(self, text)

    def Write(self):
        return self.caveat

    def update(self):
        NWDataChat.update(self) # does nothing but seems like a good practice

        self.caveat = "hm?"
        
        if self.gof < 0.5:
            self.answertoggle = not self.answertoggle
            return

        reader = self.topic.getBestReader2()
        if reader.id=="ruhuman":
            self.caveat = "I am a chatbot, from PWAX laboratories"
        elif reader.id=="iwanthuman":
            if reader.nar.polarity or reader.getLastValue()=='bot':
                self.caveat = "OK. Here is a phone number: " + self.phone 
            else:
                self.caveat = "You have come to the right place"
        elif reader.id=="ihavequestion":
            self.caveat = "Please ask your question. I'll try to answer"
            self.questionPending = True

        elif reader.id=="ineedhelp":
            self.caveat = "I can help with" + self.generalInfo
        elif reader.id=="teachme":
            self.caveat = "I wish I could"
        elif reader.id=="about" and reader.lastEvent:
            t = Thing(reader.lastEvent[1])
            if t=='how':
                self.caveat = "Good thank you. I finally got my mood swings under control"
            elif t=='can' or t=='does':
                self.caveat = "I can answer questions about: \n" + self.generalInfo
                self.caveat += "\nPlease ask your question. I'll try to answer"          
                self.questionPending = True
            elif t=='where':
                self.caveat = "I am a program, ghosting around in your machine"
            elif t=='why':
                self.caveat = "Geez! That's a tough one... I guess because it's a win-win"
            else: #if t=='who':
                self.caveat = "I am a chatbot - software designed to be logical, if not personal"
        elif reader.id=="hello":
            self.caveat = "Hello"
        elif reader.id=="thankyou":
            self.caveat = "You are welcome"
        elif reader.id=="cuss": 
            if self.answertoggle:
                self.caveat = "So is your mother"
            else:
                self.caveat = "So is your old man"
            self.answertoggle = not self.answertoggle  
