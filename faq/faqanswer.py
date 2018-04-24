from narwhal.nwtypes import *
from stdtrees.ask import *
from narwhal.nwchat import *

class FAQBaseData():
    def __init__(self, id, info, phone, contact, vocabLists):
        self.id = id
        self.info = info
        self.phone = phone
        self.contact = contact
        self.vocabLists = vocabLists

class FAQUrl():
    def __init__(self):
        self.address = '' # shown as a link, or displayed
                       # how to login: which *kind* of user name and password
        self.loginType = 'your internal\diXXXXX account and the same password used to log into outlook email' 
        self.recommendedBrowser = 'Chrome'

    def set(self, address, loginType, recBrow):
        self.address = address
        self.loginType = loginType
        self.recommendedBrowser = recBrow

class FAQTopic(NWTopic):
    def __init__(self, id, vocablists):
        # create a tree for all answers
        ANSWERS = KList("answers", "").var()
        vars = MakeVARs(  vocablists )
        ANSWERS.subs(vars)
                                
        # create tree for all the asks
        ASKS = KList("asks", "").var()
        ASKS.sub(QUESTION)    
        ASKS.sub(REQUEST) # later, should add ASKS.sub(DIFF)
                        
        # join them
        ANSWERTREE = KList(id + "_answers", "").var()
        ANSWERTREE.subs( [ASKS, ANSWERS, I_ME] )

        # make a topic out of it
        A = [ 
               NWTopicReader(id+"Q", ANSWERTREE, attribute( QUESTION, ANSWERS, [I_ME] ) ),
               NWTopicReader(id+"R", ANSWERTREE, attribute( REQUEST, ANSWERS, [I_ME]  ) ),
             ]
 
        NWTopic.__init__(self, ANSWERTREE, A )
 
""" 
Instructions include: Each subtopic is defined by a vocabulary list.
The vocabLists should be be non-overlapping and first item in each list 
will be used as the name of the list.
"""
class FAQAnswer():
    def __init__(self, id, vocabLists):
        self.id = id

        self.url = FAQUrl()  
        self.how_to = {}     # how to navigate the web page, or find the info 
                             # to be indexed same as the vocabLists 
        
        self.topic = FAQTopic( id, vocabLists)
  

class FAQAnswerChat( NWDataChat ):
    def __init__(self, faqanswer ):
        NWDataChat.__init__(self, faqanswer.topic, VanillaResponder())
    
    def update(self):
        self.caveat = ''
        if self.gof<0.5:
            return

        reader = self.topic.getBestReader2()
        self.caveat = "I can answer questions about that"
        id = reader.id
        x = 2


