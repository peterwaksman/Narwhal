""" 
IDs


FAQROOT
    FAQPERSON
    FAQTOPICS
        PERSONAL 
            CONTACT
            PHOTO
        EXPENSES
        BENEFITS 


Trying narratives of the form: 
    "I desire to {know/change} about {topic}"

Which I will take to be of the form event(DESIRE, TOPIC, INFO) with
records of the form:
    (topicID, [ info, status ] )

Also narrative of the form:
    "I want to talk to a person"

"""


import collections  # for ordered dictionaryy
from narwhal.nwtypes import KList, event
from stdtrees.ask import *

#TODO: need 'about' , politness, and swear handling


#####################################################################
###################### IDs   ########################################
#####################################################################
#####################################################################

# consts
FAQROOT = 1000
FAQHUMAN = 2000
FAQTOPICS = 3000
#CAPABILITIES = 4000

PERSONAL = FAQTOPICS+100
PERSONALCONTACT = PERSONAL+10
PERSONALPHOTO = PERSONAL+20

EXPENSES = FAQTOPICS+200
BENEFITS = FAQTOPICS+300


FAQID_SEQUENCE = [ 
                'faqroot',
                'faqhuman',
                'faqtopics',

                'personal',
                'personalcontact',
                'personalphoto',

                'expenses',
                'benefits',
                #'capabilities',
                 ]


# VARS
FAQROOTv = KList("faqroot","").var()
FAQHUMANv = KList("faqhuman","human,real human,person,real person, someone,someone real").var()
FAQTOPICSv = KList("faqtopics","").var()

PERSONALv = KList("personal","personal,personal data,personal info,\
                phone _hash_,contact info").var()
PERSONALCONTACTv = KList("personalcontact", "personal contact,personal info,my contact,contact info,my address,my phone").var()
PERSONALPHOTOv = KList("personalphoto","photo, my photo,roster photo,upload * photo").var()

EXPENSESv = KList("expenses","expense,expense report,cost,travel expenses,re emburs,re imburs,reemburs,\
                 reimburs,bill,invoice,receipt").var()

BENEFITSv = KList("benefits","benef,my benef,insurance,401,coverage,health,dental,vision,medical").var()


FaqIDVars = {
            'faqroot':  FAQROOTv,
            'faqhuman': FAQHUMANv,
            'faqtopics':FAQTOPICSv,

            'personal': PERSONALv,
            'personalcontact': PERSONALCONTACTv,
            'personalphoto': PERSONALPHOTOv, 

            'expenses': EXPENSESv,
            'benefits': BENEFITSv,
         #   'capabilities' : CAPABILITIESv,
            }  

        # fix the damn sequence
temp = collections.OrderedDict()
for id in FAQID_SEQUENCE:
    temp[id] = FaqIDVars[id]
FaqIDVars = temp


#####################################################################
###################### MODS  ########################################
#####################################################################
#####################################################################
FAQHUMAN_ = FAQHUMAN+1

# consts (one per id, in this case)
PERSONAL_INFO = PERSONAL+1
PERSONALCONTACT_INFO = PERSONALCONTACT+1
PERSONALPHOTO_INFO = PERSONALPHOTO+1

EXPENSES_INFO = EXPENSES+1
BENEFITS_INFO = BENEFITS+1


#VARs
ABOUTv = KList("about","about").var()
CHANGEv = KList("change","change,edit,modify,report,file").var()
FINDv=KList("find", "find").var()
FINDv.sub(WHERE)
INFOASKv = KList("info", "info").var()
INFOASKv.subs([ABOUTv, CHANGEv, FINDv, QUESTION])

 
# need to be added to the tree
INFOASKv.subs([CONTACTASKv,DESIREv])



FaqMODvars = {
            PERSONAL_INFO : INFOASKv, 
            PERSONALCONTACT_INFO :  INFOASKv,
            PERSONALPHOTO_INFO :  INFOASKv,
            BENEFITS_INFO : INFOASKv,
            EXPENSES_INFO :  INFOASKv,
            FAQHUMAN_     : INFOASKv
           }




faqinfo = event(DESIREv,FAQTOPICSv,INFOASKv)
faqcontact = attribute(INFOASKv,CONTACTASKv,DESIREv)
#faqcontact = event(DESIREv,CONTACTASKv,INFOASKv)

"""
FAQROOT
    FAQPERSON
    FAQTOPICS
        PERSONAL 
            CONTACT
            PHOTO
        EXPENSES
        BENEFITS 
"""
FaqDict = {
                 #  id     : [ENV,   MODS ,  PARTS ,  RELS, var ]
            'faqroot' :  ['', [], ['faqhuman','faqtopics'], None, FAQROOTv],
            'faqhuman' : ['faqroot', [FAQHUMAN_], [], None,FAQHUMANv],
            'faqtopics' : ['faqroot', [], ['personal','expenses','benefits'], None,FAQTOPICSv] ,
            'personal' : ['faqtopics', [PERSONAL_INFO], ['personalcontact','personalphoto'], None,PERSONALv],
            'personalcontact' : ['personal', [PERSONALCONTACT_INFO], [], None, PERSONALCONTACTv],
            'personalphoto' : ['personal', [PERSONALPHOTO_INFO], [], None,PERSONALPHOTOv], 

            'expenses' : ['faqtopics', [EXPENSES_INFO], [], None,EXPENSESv],
            'benefits' : ['faqtopics', [BENEFITS_INFO], [], None,BENEFITSv],
         #   'capabilities' : CAPABILITIESv,
    }
