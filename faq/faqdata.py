from faqtree import FAQTREE

class faqURl():
    def __init__(self):
        self.address = '' # shown as a link, or displayed
                       # how to login: which *kind* of user name and password
        self.loginType = 'your internal\diXXXXX account and the same password used to log into outlook email' 
        self.recommendedBrowser = 'Chrome'

    def set(self, address, loginType, recBrow):
        self.address = address
        self.loginType = loginType
        self.recommendedBrowser = recBrow

class Answer():
    def __init__(self, treeroot):
        self.tree = treeroot.copy()

        self.url = faqURl()  

        self.generalInfo = ''
        self.contact     = ''
        self.phoneNumber = '' 

        self.how_to = {}     #how to navigate the web page 

#-----------------------------------------------
class AnswerAnswer( Answer ):
    def __init__(self):
        Answer.__init__(self, FAQTREE )

        self.url.set('https://connected.dentsply.com/adfs/ls/idpinitiatedsignon.aspx',
                    'your internal\diXXXXX account and the same password used to log into outlook email', 
                    'Chrome')
        
        self.generalInfo = "\n\
  *Connections and Learning (pesonal data, job data, org charts, careers, Corporate Training)\n\
  *Employee Photo\n\
  *Benefits (health, dental, vision, ...)\n\
  *IT (technical support)\n\
  *Employment Verification\n\
  *Databasic (Expense Reports)\n\
  *BCD Travel (Concur, ie Business Travel Arrangements)\n\
  *Time and Attendance (US ONLY)(ADP Enterprise eTime, ie Vacation, Jury Duty, etc Requests)\n\
  *iPay (US ONLY)(Pay Statements, W-2's - Option to go paperless)\n\
  *Policies and General Info\n\n"

        self.contact     = 'Lindy Seney'
        self.phoneNumber = '-' 
 

    # to address questions about Connections subjects
class ConnectionsAnswer( Answer ):
    def __init__(self):
        Answer.__init__(self, FAQTREE )

        self.url.set('https://connected.dentsply.com/adfs/ls/idpinitiatedsignon.aspx',
                    'your internal\diXXXXX account and the same password used to log into outlook email', 
                    'Chrome')
        
        self.generalInfo = 'Goals, Performance, Learning, Careers, Company Info, Personal Info'
        self.contact     = 'Lindy Seney'
        self.phoneNumber = '-' 
 