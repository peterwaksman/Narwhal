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

from faqtree import *
from faqdata import *



class FAQChat( NWDataChat ):
    def __init__(self):
        NWDataChat.__init__(self, FAQTopic, VanillaResponder())
        self.data = AnswerAnswer()
        self.answertoggle = True

    def update(self):
        NWDataChat.update(self) # does nothing but seems like a good practice

        self.caveat = "hm?"

        if self.gof <= 0.49:
            return

        reader = self.topic.getBestReader2()
        if reader.id=="ruhuman":
            self.caveat = "I am a chatbot, from PWAX laboratories"
        elif reader.id=="iwanthuman":
            if reader.nar.polarity or reader.getLastValue()=='bot':
                self.caveat = "OK. Here is a phone number: " + self.data.phoneNumber
            else:
                self.caveat = "You have come to the right place"
        elif reader.id=="ihavequestion":
            self.caveat = "Go ahead and ask, I'll see if I can help"
        elif reader.id=="ineedhelp":
            self.caveat = "I can help with" + self.data.generalInfo
        elif reader.id=="teachme":
            self.caveat = "I wish I could"
        elif reader.id=="about":
            if reader.lastEvent:
                t = Thing(reader.lastEvent[1])
            else:
                t=''
            if t=='how':
                self.caveat = "Good thank you. I finally got my mood swings under control"
            elif t=='can' or t=='does':
                self.caveat = "I can answer questions about: \n" + self.data.generalInfo
                self.caveat += "\nBut please ask your question and I'll try to get the answer"
            elif t=='where':
                self.caveat = "I am a program, ghosting around in your machine"
            elif t=='why':
                self.caveat = "Geez! That's a tough one... I guess cuz it's a win-win"
            else: #if t=='who':
                self.caveat = "A chatbot - software designed to be logical if not personal"
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

