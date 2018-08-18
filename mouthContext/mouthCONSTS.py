""" 
CONSTANTS
These predefined constants will be used to name context IDs and modifier IDs.
(The IDs themselves are strings).
 
In principle, although there are names coming from outside of the
context, every context specific entity should have a defined constant.
"""


########################## context CONSTANTS ###################################
# note these are set up to have plenty of headroom, for insertion of context specific
# modifier constants (below) 

# These are the topics (su contexgts) within the dental order conversational context
ORDER    = 500
MOUTH    = 1000
ARCH     = 2000
SITE     = 3000
MULTISITE = 4000

ABUTMENT = SITE + 100
MARGIN   = ABUTMENT+10 
CORE     = ABUTMENT+20
BASE     = ABUTMENT + 30
EPS      = BASE+1 # straight, concave, ...
 
CROWN = SITE + 200
 
 
########################### modifier CONSTANTS ################
# (note convention of underbar "_" use to relate a modifier name to
# a context ID name: SITE_TOOTHNUM is a 'toothnum' modifier of the 'site'
# context. The convention is dropped for MDFL and OCCL because they
# name modifiers related to several different contexts.

#ORDER = 500
ORDER_LATER = ORDER+10

#MOUTH = 1000
MDFL = MOUTH+10 #direction: mesial, distal, facial, lingual
OCCL = MOUTH+11

REF_FEATURE = MOUTH+30 #reference feature: gum, neighbor, opposing
REF_RELATION = MOUTH+20 #above, below, closest, ...
REF_AMOUNT = MOUTH+40  #"2 mm" or "as much as possible"

# NOTE these general concepts are used in margin setting, so 
# at least one of them needs a version unique to margins, because
# the handler function needs to be unique to margins.
MARGIN_DEPTH = REF_AMOUNT+1




#SITE = 2000
SITE_TOOTHNUM = SITE+1  # tooth number
SITE_TOOTHTYPE = SITE+2 # prepped, regular, missing
SITE_TOOTHGROUP = SITE+3 # molar, anterior, canine, central, ...

#ABUTMENT = SITE + 100
ABUTMENT_MATERIAL = ABUTMENT+1
ABUTMENT_TYPE = ABUTMENT+2
ABUTMENT_RETENTION = ABUTMENT+3 # cement, screw

#CORE = ABUTMENT+50
CORE_TILT = CORE+1
CORE_THICKNESS = CORE+2
CORE_TAPER = CORE+3
CORE_CLEARANCE = CORE+4
CORE_MATCH = CORE+5

#BASE = ABUTMENT + 100
BASE_PRESSURE = BASE+1 # width info
#EPS = BASE+10 # straight, concave, ...
EPS_TYPE = EPS+1

#CROWN = SITE + 200
CROWN_MATERIAL = CROWN+1
CROWN_TYPE = CROWN+2
CROWN_RETENTION = CROWN+3

