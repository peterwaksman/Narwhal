""" 
CONSTANTS
These predefined constants will be used for context IDs and and modifier IDs.
 
Contexts will come with a VAR for ID vocabulary, which can be elaborated by VARs for
ID vocabs of its sub contexts. 

Context modifiers will come with a tree of vocabularies incorporated as a VAR tree

In principle, although there are vocabularies and VARs coming from outside of the
context, every context specific vocab and VAR is either an ID or a modifier and 
there should be a constant for each one of them.
"""


########################## context CONSTANTS ###################################
# note these are set up to have plenty of headroom, for insertion of context specific
# modifier constants (below) 

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

#ORDER = 500
ORDER_LATER = ORDER+10

#MOUTH = 1000
MDFL = MOUTH+10 #direction: mesial, distal, facial, lingual
OCCL = MOUTH+11

REF_FEATURE = MOUTH+20 #reference feature: gum, neighbor, opposing
REF_RELATION = MOUTH+30 #above, below, closest, ...
REF_AMOUNT = MOUTH+40  #"2 mm" or "as much as possible"


#SITE = 2000
SITE_TOOTHNUM = SITE+1
SITE_TOOTHTYPE = SITE+2
SITE_TOOTHGROUP = SITE+3

#ABUTMENT = SITE + 100
ABUTMENT_MATERIAL = ABUTMENT+1
ABUTMENT_TYPE = ABUTMENT+2
ABUTMENT_RETENTION = ABUTMENT+3

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

