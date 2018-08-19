
import collections  # for ordered dictionaryy


from narwhal.nwtypes import KList
from stdtrees.geometry import *
from stdtrees.quantities import INTx

from mouthCONSTS import *


#########################################################################
######################### context ID VARs ###############################
#########################################################################

ORDERv = KList("order", " my order , my * order , order , the order  , an order , case , a case , the case ").var()
MOUTHv = KList("mouth","mouth, casts").var()
ARCHv = KList("arch", "arch, upper, lower").var()
SITEv = KList("site", "site, unit, tooth, _hash_ ").var()
MULTISITEv = KList("multisite","multisite").var()
ABUTMENTv  = KList("abutment", "abutment, abut, abutmen").var()
MARGINv = KList("margin",  "shoulder $ margin, collar, outline, contour").var()  
COREv = KList("core", "core # file, post").var()  
BASEv = KList("base",  "base, between interface and margin,support tissue").var()  
EPSv =KList("eps", "eps, esp, ets,profile,emergence,emergense,emmergence,emergance,emergency,profile,profiling").var()      
CROWNv = KList("crown", "crown").var()


#########################################################################
###################### Context modifier VARs ############################ 
#########################################################################

SCREW = KList("screw","screw").var()
CEMENT = KList("cement","cement").var()
RETENTION = KList("retention", "retention, retained").var()
RETENTION.subs([SCREW,CEMENT])

# retention--------------------------------------
# best not to have overlap
CROWN_RETENTIONv = KList("crownretention", "retention, retained").var()
CROWN_RETENTIONv.subs([SCREW,CEMENT])
ABUTMENT_RETENTIONv =KList("abtretention", "retention, retained").var()
ABUTMENT_RETENTIONv.subs([SCREW,CEMENT])

# Crown type ----------------------------
TEMP = KList("temp", "temp, temp crown, temporary, temporary crown").var()
FULL = KList("full", " full, full crown,full contoured, full contoured crown,\
regular, regular crown, normal, normal crown, standard, standard crown").var()
JANUSCROWN = KList("janus", "janus # abutment, janus crown" ).var()
CUTBACK = KList("cutback", "cutback, cut back, cutback crown, cut back crown").var()
CROWN_TYPEv = KList("crowntype", "crowntype").var()
CROWN_TYPEv.subs([TEMP, FULL, JANUSCROWN, CUTBACK])

# Crown material -------------------------
PFM = KList("pfm","pfm").var()
EMAX = KList("emax","emax").var()
PORCELAIN = KList("porcelain","porc").var()
CROWN_MATERIALv = KList("crownmaterial","").var()
CROWN_MATERIALv.subs([PFM, EMAX, PORCELAIN])

# EPS_TYPE --------------------------------
STRAIGHT = KList("straight", "off , straight, striaght, srtaight").var()
CONCAVE = KList("concave", "concave, convave").var()
CONVEX = KList("convex", "convex").var()
ANKYLOS  = KList("ankylos", "ankylos, golf, tee , option _hash_ 5").var()
EPS_TYPEv = KList("epstype", "").var()
EPS_TYPEv.subs([STRAIGHT, CONCAVE, CONVEX, ANKYLOS])
  
# PRESSURE -------------------------------
PRESSURE =  KList("pressure", "press, presure, blanch, blaching, push, push on,\
                   expand,pressure,compression, displace,displacement,\
                   diplace, impinge, impingement").var()  
BASE_PRESSUREv = PRESSURE.copy()

# CORE_THICKNESS ----------------------------------------------      
THICK = KList("thick", "thick, fat, big, wide").var()
THIN = KList("thin", "thin, narrow").var()
NORMAL = KList("normal", "normal").var()
COREWIDTH = KList("corewidth","corewidth").var()
COREWIDTH.sub(THICK)
COREWIDTH.sub(THIN)
COREWIDTH.sub(NORMAL)

CORE_THICKNESSv = COREWIDTH.copy()

# CORE_TAPER ------------------------------
TAPER = KList("taper","taper").var()
CORE_TAPERv = TAPER.copy()

# CORE_TILT-------------------------------
TILT = KList("tilt","tilt, angulate, angle towards").var()
CORE_TILTv = TILT.copy() 

# CORE_CLEARANCE ---------------------------
CLEARANCE = KList("clearance", "offset, distance, clearance, clearance, clerance,clearence, room, space , reduction, from ").var()
CORE_CLEARANCEv = CLEARANCE.copy()


# ABUTMENT_MATERIAL ---------------------
ZR = KList("zirconia"," zircomium, zirconia, zr , zi , z ").var()
TI = KList("titanium"," titanium, titania, ti , t ").var()
GOLDTI = KList("goldTi", "gold, gold hue").var()
ABTMATERIAL = KList("abtmaterial", "").var()
ABTMATERIAL.subs([ZR, TI, GOLDTI])

ABUTMENT_MATERIALv =ABTMATERIAL.copy()

# ABUTMENT_TYPE -----------------------------------
HEALING = KList("healingabut","healing abutment, healing").var()
SMOOTH = KList("smoothabut", "smooth abutment").var()
JANUSABT = KList("janusabut","janus # crown").var()
STOCK= KList( "stockabut", "stock").var()
ABTTYPE = KList("abutmenttype", "").var()
ABTTYPE.subs([HEALING, SMOOTH, JANUSABT, STOCK])

ABUTMENT_TYPEv = ABTTYPE.copy()

# SITE_TOOTHTYPE ---------------------------------
PREPPED = KList("prepped", "prep, prepared").var()
MISSING = KList("missing", "missing").var()
PONTIC = KList("pontic", "pontic").var()
REGULAR = KList("regular", "regular").var()
TOOTHTYPE = KList("toothtype","").var()
TOOTHTYPE.subs([PREPPED, MISSING, PONTIC, REGULAR] )

SITE_TOOTHTYPEv = TOOTHTYPE.copy()

# SITE_TOOTHNUM -----------------------------------
#(tolerate duplicate of "tooth" here and in 'site'; or else rely on 'site' being in context when "tooth 3"
# processed as desired because all MODs are explored and...)
TOOTH = KList("tooth", " tooth , _hash_ ").var()
SITE_TOOTHNUMv = TOOTH.copy()
SITE_TOOTHNUMv.sub(INTx)

# SITE_TOOTHGROUP --------------------
############# TOOTHGROUP ##################
INCISOR= KList("incisor",  "incisor, central, lateral").var()
CENTRAL = KList("central","central").var()
LATERAL = KList("lateral","lateral").var()
CANINE= KList( "canine", "canine, eye tooth, eye teeth").var()
ANTERIOR= KList("anterior",  "anterior, ant").var()
ANTERIOR.subs( [INCISOR, CENTRAL, LATERAL, CANINE] )

MOLAR= KList( "molar", "molar").var()
PREMOLAR= KList("premolar", "premolar, pre-molar, primolar,\
                 bicuspid, bi-cuspid, bi-suspid").var()
POSTERIOR= KList( "posterior", "posterior, post").var()
POSTERIOR.subs([MOLAR, PREMOLAR])

TOOTHGROUP = KList("toothgroup","").var()
TOOTHGROUP.subs( [ANTERIOR, POSTERIOR] )
 
SITE_TOOTHGROUPv = TOOTHGROUP.copy()



# REF_FEATURE -----------------------------
SOFTTISSUE = KList("softtissue", "soft tissue, softtissue, support tissue, tissue").var()
GUM= KList("gum", "gingiva, gingival, gigival , subgingival, subginival, gum, supra_g,sub_g,ridge, gm crest, \
    supra-gingival, supra-ging, supra_g,\
    sub-gingival, sub-ginival, sub_g, subgingival, subginival, crest, ridge").var()
INTERFACE= KList("interface","interface, fixture, implant, analog, anolog").var()
OPPOSING= KList( "opp", "opp").var()
ADJACENT = KList("adjacent","adjacent, adjacent tooth, adjacent teeth, adjecent, neighbor, \
            neighboring tooth, neighboring teeth, surrounding").var()
MARK = KList("mark", "mark, line").var()
CEJ = KList("cej", "cej, cement enamel junction").var()
CONTRALATERAL = KList("contralateral", "contralateral").var()
REFFEATURE = KList("reffeature","").var()
REFFEATURE.subs( [SOFTTISSUE, GUM, INTERFACE, OPPOSING, ADJACENT, MARK, CEJ, CONTRALATERAL] )

REF_FEATUREv = REFFEATURE.copy()

# MDFL ----------------------------------------
ALL = KList( "all",  "all sides, all around, 360, circumferential, around, other values").var()
REMAINING= KList( "remainder", "remainder, rest of, other").var() # as in "the rest of the margins
BUCCAL= KList("buccal", " b , buccal, baccal, buc, buck, bucca").var()
FACIAL= KList( "facial"," f , facial").var()
BF= KList("bf",  " b/f, f/b, buccal/facial, b&f").var()
BF.subs([BUCCAL, FACIAL] )
 
MESIAL= KList( "mesial", " m , mesial , mesail , mes , meaisl , mesial").var()
DISTAL= KList("distal",  " d , distal , dist , distall ").var()
MD= KList("md", " m/d , d/m , mesial/distal, distal/mesial, m&d, proximal, interproximal").var()
MD.subs([MESIAL ,DISTAL])

LABIAL= KList("labial",  "labial").var()
LINGUAL= KList("lingual",  "lingual, ling, lin, l ").var()
PALATAL= KList( "palatal", "palat").var()
SIDE = KList("side","").var() 
SIDE.subs( [ALL, REMAINING, BF, MD, LABIAL, LINGUAL, PALATAL] )

MDFLv =  SIDE.copy()

# OCCL ---------------------------------
OCCLUSAL= KList("occlusal",  "occ").var()
INCISAL= KList( "incisal", "incisal, inc").var()
OCCLv = KList("occ","").var()
OCCLv.subs([OCCLUSAL, INCISAL])

# ORDER_LATER ------------------------------------
ORDER_LATERv = KList("laterorder", "later order").var()


# sucks that I need this to init the orderedDicts
# THIS IS THE MASTER LIST FOR ITEM SEQUENCE
MOUTHID_SEQUENCE = [ 
                'order' ,
#                'mouth',
                'arch',
                'site' ,
                'multisite', 
                'abutment' , 
                'margin' ,
                'core'  ,
                'base' ,
                'eps' ,
                'crown',
            ]

###########################################################
# Lookup ID VAR from its id string

MouthIDvar = {
        'order' : ORDERv ,
 #       'mouth' : MOUTHv , 
        'arch' : ARCHv ,
        'site'  : SITEv ,
        'multisite' : MULTISITEv ,
        'abutment'  : ABUTMENTv ,
        'margin' : MARGINv ,
        'core'  : COREv ,
        'base' : BASEv ,
        'eps' : EPSv ,
        'crown'  : CROWNv ,
        }  


        # fix the damn sequence
temp = collections.OrderedDict()
for id in MOUTHID_SEQUENCE:
    temp[id] = MouthIDvar[id]
MouthIDVar = temp

"""
I guess every modifier constant specifies a VAR but also specifies a slot
in the data to be filled with (sometime without) that VAR and other VARs.
This creates an awkwardness when the same underlying VAR (eg RETENTION) is used
for two different slots: (abutment retention and crown retention). You could resolve
this by using the same VAR for both but what to call it? Currently I am duplicating 
the VAR. 

It also is awkward to have other VARs needed to fill one slot but that is the design.
"""
# lookup mod var from its
MouthMODvars = {
    ORDER_LATER         : ORDER_LATERv  ,
    MDFL                : MDFLv , 
    OCCL                : OCCLv,
    REF_RELATION        : RELATION , # defined in GEOMETRY
    REF_AMOUNT          : RELAMOUNT, 
    MARGIN_DEPTH        : RELAMOUNT, 
    REF_FEATURE         : REF_FEATUREv ,

    SITE_TOOTHNUM       : SITE_TOOTHNUMv , 
    SITE_TOOTHTYPE      : SITE_TOOTHTYPEv  ,
    SITE_TOOTHGROUP     : SITE_TOOTHGROUPv  ,

    ABUTMENT_MATERIAL   : ABUTMENT_MATERIALv  ,
    ABUTMENT_TYPE       : ABUTMENT_TYPEv  ,
    ABUTMENT_RETENTION  : ABUTMENT_RETENTIONv ,
    CORE_TILT           : CORE_TILTv  ,
    CORE_THICKNESS      : CORE_THICKNESSv  ,
    CORE_TAPER          : CORE_TAPERv  ,
    CORE_CLEARANCE      : CORE_CLEARANCEv  ,
    CORE_MATCH          : MATCH, # in geometry

    BASE_PRESSURE       : BASE_PRESSUREv  ,
 
    EPS_TYPE            : EPS_TYPEv ,

    CROWN_MATERIAL      : CROWN_MATERIALv ,
    CROWN_TYPE          : CROWN_TYPEv  ,
    CROWN_RETENTION     : CROWN_RETENTIONv , 

    }
 

 #########################################################
 #########################################################
""" Mouth Contexts (not all implemented)
 'order'
    #'mouth' 
        'arch' 
        'site'   
            'abutment'  
                'margin'  
                'core'  
                'base' 
                    'eps'  
            'crown'  
            'neighbor'

        'multisite'  
            'superstructure',
            'guide',
            'kit', # NAH this is an mod of 'order'

Dental products are defined within the (sub)context of mouth where they apply. 
For now, a context will have different vocabulary lists associated to its identity 
and its modifiers. 

"""

""" DICTIONARY 
I am going to initialize this with a dictionary of entries
  id : [ env, mods, parts, rels, var ]
"""

MouthDict = {   
              #  id     : [ENV,   MODS ,  PARTS ,  RELS, var ]
                'order' : [ '', [ORDER_LATER], ['multisite','arch','site'], None, ORDERv],
                                
                #'mouth' : [ 'order', 
                #           [], 
                #           ['site', 'multisite', 'arch'], 
                #           None, MOUTHv]  ,

                'multisite' : ['order', [], [], None, MULTISITEv ], # 'superstructure','guide','kit'
                'arch' : ['order', [], [], None, ARCHv ],      #'upper','lower','cast','scan'

                'site'  : [ 'order', 
                           [ SITE_TOOTHNUM, SITE_TOOTHTYPE, SITE_TOOTHGROUP], 
                           ['abutment', 'crown'] ,  #'neighbor'], 
                           None, SITEv] ,

                'abutment' : [ 'site',
                              [ABUTMENT_MATERIAL, ABUTMENT_TYPE, ABUTMENT_RETENTION],
                              [ 'margin', 'core', 'base' ],
                              None, ABUTMENTv] ,
                                            
                                        # only MARGIN_DEPTH (REF_AMOUNT+1)
                                        # has a handler
                'margin' : [ 'abutment',
                            [ MDFL, REF_FEATURE, REF_RELATION, MARGIN_DEPTH ],
                            [],
                            None, MARGINv],
                'core' : [ 'abutment',
                           [ CORE_TILT, CORE_THICKNESS, CORE_TAPER, CORE_CLEARANCE, CORE_MATCH],
                           [],
                           None, COREv],
                'base' : [ 'abutment',[BASE_PRESSURE], ['eps'],None, BASEv],
                'eps' : [ 'base', [EPS_TYPE], [], None, EPSv],             

                'crown' : [ 'site', 
                            [CROWN_MATERIAL, CROWN_TYPE, CROWN_RETENTION], #CROWN_OCCLUSION
                            [],
                            None, CROWNv] ,
               }


        # fix the damn sequence
for id in MOUTHID_SEQUENCE:
    temp[id] = MouthDict[id]
MouthDict = temp

        