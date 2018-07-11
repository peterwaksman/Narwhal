from narwhal.nwtypes import *
from narwhal.nwchat import *


class UrlInfo():
    def __init__(self):
        self.url = ''  # a link
                       # HOW to login:
        self.user = '' # which *kind* of user name
        self.pswd = '' # which *kind* of password

class QuestionData():
    def __init__(self, treeroot):
        self.tree = treeroot.copy()

        self.generalInfo = 'Chrome browser is recommend'
        self.url = UrlInfo() #points to a web page
        self.how_to = {}     #how to navigate the web page 

        self.contact = 'Lindy Seney'
        self.phoneNumber = '666666' # This really is the IT number!
