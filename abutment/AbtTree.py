import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *
from stdtrees.quantities import FLOATx

"""
The parts of the abutment and surrounding features, their inter relations.

ABUTMENTSAYS
  MARGIN
  EPS
  FEATURE
    GINGIVA
    INTERFACE
    ADJACENT
    OPPOSING
  RELATION
    AT
    ABOVE (for now, verbs that 'move up' are subsumed in this)
    BELOW
    CLOSEST
  RELAMOUNT
    FLOATx
    JUST 
    ASPOSS
  UNITS
    MM
    DEGREE
  WIDTHTYPE
    NODISPLACE
    FULLANATOM
    CONTOURTIS
    SUPPORTTIS
  PROFILE
    STRAIGHT
    CONVEX
    CONCAVE
    ANKYLOS
  CLEARANCE
"""

##### ACTIONS
# going for narrative: make [margin] subgingival [by this amount]
# (put margin in:) RELATION to REF by AMT
# doAction = attribute( MAKE, [AMT], REF )
MAKE = KList("make", "make, make it, turn, turn it, put, put it, I want").var()
MOVE = KList("move", "move").var()

ACTION = KList("action", "do, act").var()
ACTION.sub(MAKE)
ACTION.sub(MOVE)

######################### RELATIONS
AT = KList("at", "at").var()
            # include verbs that could move to being separate ACTIONs
ABOVE = KList("above", "above, sup, raise, move * up").var()
BELOW = KList("below", "below, sub, lower, move * down").var()
CLOSEST = KList("closest", "close, close to, as close, close to").var()

RELATION = KList("relation", "relative, relation").var()
RELATION.sub(AT)
RELATION.sub(ABOVE)
RELATION.sub(BELOW)
RELATION.sub(CLOSEST)

################### FEATURES
kGINGIVA = "gingiva,ginival, subG, supraG, tissue, gum, supra_g, sub_g, ridge, crest, gm crest"
GINGIVA = KList("gingiva", kGINGIVA).var()
INTERFACE = KList("interface", "interface, fixture, implant ,analog").var()
ADJACENT = KList("adjacent", "adjacent, neighbor, neighboring, neighbour, surrounding").var()
OPPOSING = KList("opposing", "opposing, opp").var()

FEATURE = KList("feature", "feature").var()
FEATURE.sub(GINGIVA)
FEATURE.sub(INTERFACE)
FEATURE.sub(ADJACENT)
FEATURE.sub(OPPOSING)

################## AMOUNTS
JUST = KList("just", "just, slightlye").var()
ASPOSS = KList("possible", "possible, as possible, as * as possible, as much as possible").var()
RELAMOUNT = KList("amount", "amount").var()
RELAMOUNT.sub(JUST)
RELAMOUNT.sub(ASPOSS)
RELAMOUNT.sub(FLOATx)

################### EPSSHAPE
STRAIGHT = KList("straight", "straight, striaght,srtaight").var()
CONCAVE = KList("concave", "concave,convave,concavity").var()
CONVEX = KList("convex", "convex").var()
ANKYLOS = KList("ankylos", "ankylos, golf").var()
EPSSHAPE = KList("epsshape","eps shape").var()
EPSSHAPE.sub(STRAIGHT)
EPSSHAPE.sub(CONCAVE)
EPSSHAPE.sub(CONVEX)
EPSSHAPE.sub(ANKYLOS) 
############################### CORETHINKNESS
THICK = KList("thick", "thick, fat, big, wide").var()
THIN = KList("thin", "thin, narrow").var()
NORMAL = KList("normal", "normal").var()
COREWIDTH = KList("corwidth","corewidth").var()
COREWIDTH.sub(THICK)
COREWIDTH.sub(THIN)
COREWIDTH.sub(NORMAL)


####################### entities
MARGIN = KList("margin", "margin, contour").var()
EPS = KList("eps", "eps, esp, emergence,emergense,emergance,emergency,profile,profiling, base").var()
CORE = KList("core","core").var()
######################################

ABUTMENTSAYS = KList("abutment", "abutment, unit").var()
ABUTMENTSAYS.sub(ACTION)
ABUTMENTSAYS.sub(RELATION)
ABUTMENTSAYS.sub(FEATURE)
ABUTMENTSAYS.sub(RELAMOUNT)
ABUTMENTSAYS.sub(EPSSHAPE)
ABUTMENTSAYS.sub(COREWIDTH)
ABUTMENTSAYS.sub(MARGIN)
ABUTMENTSAYS.sub(EPS)
ABUTMENTSAYS.sub(CORE)


# (make margin) [.2] sub gingival
makeRelation = attribute( FEATURE, [RELAMOUNT], RELATION )
# move (margin) to relation with feature
doHeightAction = event( FEATURE, RELATION, ACTION )
# make emergence convex
doEPSAction = attribute ( [EPS], EPSSHAPE, MAKE )

doCoreAction = attribute ( [CORE], COREWIDTH, MAKE )
# LATER requestCoreAction = attribute( CORE, REQUEST, COREWIDTH  )

################## READERS
A = [ 
      NWTopicReader("relationReader", ABUTMENTSAYS, makeRelation ),
      NWTopicReader( "heightReader", ABUTMENTSAYS, doHeightAction ),
      NWTopicReader( "epsReader", ABUTMENTSAYS, doEPSAction ),
      NWTopicReader( "coreReader", ABUTMENTSAYS, doCoreAction )
    ]

AbutmentTopic = NWTopic( ABUTMENTSAYS, A ) 


