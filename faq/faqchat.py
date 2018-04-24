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

from faqabout import *
from faqanswer import *

class FAQAppChat(TChat):
    def __init__(self, basedata, subchats = None):

        self.basedata = basedata
        self.about = FAQAboutChat( basedata.info, basedata.phone, basedata.contact )
        self.answer = FAQAnswerChat( FAQAnswer(basedata.id, basedata.vocabLists) )
        self.subchats = subchats

        self.currentAnswer = self.answer

    def findAnswerChat(self, val):
        if not self.subchats:
            return None
        return self.subchats.get(val)

    def Read(self, text):
        about = self.about #for readability
        #answer = self.answer 
        answer = self.currentAnswer 
        answer.topic.clearReaders()

        about.caveat = ''
        answer.caveat = ''

        if about.questionPending:
            answer.Read(text)
            if answer.gof>0.5:
                self.caveat = answer.Write()
            else:
                about.Read(text) 
                if about.gof>0.5:
                    self.caveat = about.Write()
                else:
                    self.caveat = "I am sorry, I don't know about that"
            about.questionPending = False
        else:
            about.Read(text)
            if about.questionPending: #handle question this time?
                answer.Read(text)
                if answer.gof>0.5:
                    about.caveat = ''
                    self.caveat = answer.Write()
                elif about.gof>0.5:
                    answer.caveat = ''
                    self.caveat = about.Write()
                else:
                    self.caveat = "I am sorry, I don't know about that"
            else:
                self.caveat = about.Write()
             

        C = self.update()
        if C:
            self.currentAnswer = C


    def update(self):
        C = None
        if self.answer==self.currentAnswer and self.answer.gof>0.65:
            reader = self.answer.topic.getBestReader2()
            v = reader.getLastValue()
            C = self.findAnswerChat(v)
        elif self.answer.gof>=0.65:
            C = self.answer
  
        return C
        
    def Write(self):
        s = self.caveat
        return s

             
#---------------------------------
FAQGREET = 0
FAQASK = 1
FAQASKDETAIL = 2

faqResponse = {
    FAQGREET : "ok",
    FAQASK: "I {}",
    FAQASKDETAIL : "please clarify {}"
    }

faqResponseV = {
    FAQGREET : [],
    FAQASK: [],
    FAQASKDETAIL :[],
    }

faqResponder = NWTopicResponder(bResponse, bResponseV)


class FAQChat(NWDataChat):
    def __init__(self, topic):
        NWDataChat.__init__(self, topic, faqResponder)

    def Read(self, text):
        NWDataChat.Read(self,text)

    def update(self):
        x = 2