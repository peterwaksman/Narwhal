from narwhal.nwtypes import *
from narwhal.nwchat import *

from stdtrees.quantities import *
from stdtrees.geometry import * 
 
"""


MISCELLANEOUS= KList(
    FUTURE = KList("future", "will be").var()
    DR= KList("dr", "doctor").var()
    BOW= KList(  "face bow, bow, facebow"
    ARTICULATOR = KList(

    DOCS= KList( "document"
        RX= KList( "Rx, document, paper,written, external doc"
        DRAWING= KList( "draw, diagram"
    PREFERENCE= KList(
    VENEER= KList(
    SECTION= KList(  
    PIN= KList(  
    SLEEVE= KList(
    STUMP = = KList("stump","stump, stub",
    BONE = KList("bone",  
    OPTION= KList( "option, opt"
    PLACEMENT= KList(
    CHANNEL= KList(
    MASTICATION= KList(
    HOLE= KList(
    TELESCOPE= KList(
    SHOWING = KList("showing"
    CONICAL = KList("conical, conicity"

PERIDENTAL
    MYORDER = nwt.KList( "myorder", ' my order , my * order , order , the order  , an order , case , a case , the case ').var()
    ACCOUNT = nwt.KList( "account", ' account , payment , amount due , cost , pay , finance' ).var()

DENTAL= KList( 
    CAST= KList(  "cast, study, study model, provisional, diagnostic"
    SCAN = KList("scan", "scan").var()
    JAW= KList(  " jaw" 
        UPPER " upper , maxil"
        LOWER " lower, mandib" 
    BITE= KList( "bite"
        PROTR= KList( "protrusive"
        RETRO= KList( "retro"
        CROSSBITE = KList("cross bite, cross-bite, crossbite"
        CLASS_I= KList( "class i"
        CLASS_II= KList( "class ii"
        CLASS_III= KList( "class iii"
        OPENBITE= KList( "open # the"
        CLOSEDBITE= KList( "closed, close # the"
   
        DIASTEMA= KList( "diastema, diestema, diastama"
        GAP= KList(

 
       CONDITION
            PREP= KList(  "prep"
            PONTIC= KList(  "pontic"
            MISSING= KList(   "missing, absent"
            REGULAR= KList(    


    PRODUCT= KList( 
        STOCK= KList( "stock"

        PART= KList( " unit, part "
        CAP= KList( "cap, healing cap, healing abutment, healingabut"               
        ABUTMENT= KList(
 
        CROWN= KList( "crown"
        COREFILE
        SUPERSTRUCT = KList("superstructure"
            BRIDGE "bridge, brigde"
            CONUS "conus"
        KIT "kit, procedure pack"
        BOX
        SCREW
        GUIDE "guide" 
            DRILL "drill guide"
            INSERT "insertion guide"
            SURG "surgical guide"
"""


#----------------SIDE --------------
ALL = KList( "all",  "all sides, all around, 360, circumferential, all the way around, around, other values").var()
REMAINING= KList( "remainder", "remainder, rest of, other").var() # as in "the rest of the margins
BF= KList("bf",  " b/f, f/b, buccal/facial, b&f").var()
BUCCAL= KList("buccal", " b , buccal, baccal, buc, buck, bucca").var()
FACIAL= KList( "facial"," f , facial").var()
BF.sub(BUCCAL)
BF.sub(FACIAL)

MD= KList("md", " m/d , d/m , mesial/distal, distal/mesial, m&d, proximal, interproximal").var()
MESIAL= KList( "mesial", " m , mesial , mesail , mes , meaisl , mesial").var()
DISTAL= KList("distal",  " d , distal , dist , distall ").var()
MD.sub(MESIAL)
MD.sub(DISTAL)

LABIAL= KList("labial",  "labial").var()
LINGUAL= KList("lingual",  "lingual, ling, lin, l ").var()

#PALATAL= KList( "palatal", "palat").var()

SIDE = KList("side","").var() 
SIDE.sub(ALL)
SIDE.sub(REMAINING)
SIDE.sub(BF)
SIDE.sub(MD)
SIDE.sub(LABIAL)
SIDE.sub(LINGUAL)
 

############# TOOTHGROUP ##################

TOOTHGROUP = KList("toothgroup","").var()
ANTERIOR= KList("anterior",  "anterior, ant").var()
INCISOR= KList("incisor",  "incisor, central, lateral").var()
CENTRAL = KList("central","central").var()
LATERAL = KList("lateral","lateral").var()
CANINE= KList( "canine", "canine, eye tooth, eye teeth").var()
ANTERIOR.sub(INCISOR)
ANTERIOR.sub(CENTRAL)
ANTERIOR.sub(LATERAL)
ANTERIOR.sub(CANINE)

POSTERIOR= KList( "posterior", "posterior, post").var()
MOLAR= KList( "molar", "molar").var()
PREMOLAR= KList("premolar", "premolar, pre-molar, primolar,\
                 bicuspid, bi-cuspid, bi-suspid").var()
POSTERIOR.sub(MOLAR)
POSTERIOR.sub(PREMOLAR)

TOOTHGROUP.sub(ANTERIOR)
TOOTHGROUP.sub(POSTERIOR)

############### REFFEATURE ######################
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
REFFEATURE.sub(SOFTTISSUE)
REFFEATURE.sub(GUM)
REFFEATURE.sub(INTERFACE)
REFFEATURE.sub(OPPOSING)
REFFEATURE.sub(ADJACENT)
REFFEATURE.sub(MARK)
REFFEATURE.sub(CEJ)
REFFEATURE.sub(CONTRALATERAL)
# useful subset (excludes OPPOSING, and CONTRALATERAL)
MREF = KList("marginreference", "").var() 
MREF.sub(SOFTTISSUE)
MREF.sub(GUM)
MREF.sub(INTERFACE)
MREF.sub(ADJACENT)
MREF.sub(MARK)
MREF.sub(CEJ)

#----------------------------------------------------
kCROWN = 'temporary|temp|janus|cutback|regular|normal|standard $ crown'
CROWN = KList( "crown", kCROWN).var()

CROWNTYPE = KList("crowntype", "crowntype").var()
TEMP = KList("temp", "temp, temp crown, temporary, temporary crown").var()
FULL = KList("full", " full, full crown,full contoured, full contoured crown,\
regular, regular crown, normal, normal crown, standard, standard crown").var()
JANUSCROWN = KList("janus", "janus # abutment, janus crown" ).var()
CUTBACK = KList("cutback", "cutback, cut back, cutback crown, cut back crown").var()
CROWNTYPE.sub( TEMP )
CROWNTYPE.sub( FULL )
CROWNTYPE.sub( JANUSCROWN )
CROWNTYPE.sub( CUTBACK )

#--------CROWN SURFACE
OCCLUSAL= KList("occlusal",  "occ").var()
INCISAL= KList( "incisal", "incisal, inc").var()
SURFACE = KList("surface","").var()
SURFACE.sub(OCCLUSAL)
SURFACE.sub(INCISAL)
#---------------CROWNFEATURE
HOLE= KList("hole","hole, screw hole, screwhole").var()
WALL = KList("wall", "wall").var()
#CUSPS
#FOSSA
#VESTIBULE
#CINGULUM
CROWNFEATURE = KList("crownfeature","").var()
CROWNFEATURE.sub(HOLE)
CROWNFEATURE.sub(WALL)

CROWN.sub(CROWNTYPE)
CROWN.sub(CROWNFEATURE)
CROWN.sub(SURFACE)


#------------------ABTFEATURE-----------
MARGIN = KList("margin", "shoulder $ margin, collar, outline").var()
BASE = KList("base", "base, between interface and margin").var()      
CORE = KList("core","core # file, post").var()
SHOULDER = KList("shoulder","shoulder, sholder, shoulder * margin, chamfer, chamf, \
                   champfer, champ, flar, flair" ).var()   
BEVEL = KList("bevel", "bevel, occlusal bevel").var()
GROOVE = KList("groove", "groove, retention groove, retentive groove").var()
ABTFEATURE = KList("abtfeature", "").var()
ABTFEATURE.sub(MARGIN)
ABTFEATURE.sub(BASE)
ABTFEATURE.sub(CORE)
ABTFEATURE.sub(SHOULDER)
ABTFEATURE.sub(BEVEL)
ABTFEATURE.sub(GROOVE)

#------------------ABTMATERIAL-------------------
ZR = KList("zirconia"," zircomium, zirconia, zr , zi , z ").var()
TI = KList("titanium"," titanium, titania, ti , t ").var()
GOLDTI = KList("goldTi", "gold, gold hue").var()
ABTMATERIAL = KList("abtmaterial", "").var()
ABTMATERIAL.sub(ZR)
ABTMATERIAL.sub(TI)
ABTMATERIAL.sub(GOLDTI)

#-------------------------------------
    # BASE values
EPS = KList("eps", "eps, esp, ets, profile, emergence, emergense, emergency, emmergence").var()      
PRESSURE =  KList("pressure", "press, presure, blanch, blaching, push, push on, support, \
                   expand,tissue pressure,compression, displace,displacement,\
                   diplace, impinge, impingement").var()        
    # 'value' values:
STRAIGHT = KList("off", "off, straight, striaght, srtaight").var()
CONCAVE = KList("concave", "concave, convave").var()
CONVEX = KList("convex", "convex").var()
ANKYLOS  = KList("ankylos", "ankylos, golf, tee , option _hash_ 5").var()
#------------------------------------
EPSTYPE = KList("epstype", "").var()
EPSTYPE.sub(STRAIGHT)
EPSTYPE.sub(CONCAVE)
EPSTYPE.sub(CONVEX)
EPSTYPE.sub(ANKYLOS)
#-----------------------------
BASE.sub(EPS)
BASE.sub(EPSTYPE)
BASE.sub(PRESSURE)
#------------------------------

ABTTYPE = KList("abttype", "").var()
HEALING = KList("healingabut","healing abutment").var()
SMOOTH = KList("smoothabut", "smooth abutment").var()
JANUSABT = KList("janusabut","janus # crown").var()
STOCK= KList( "stock", "stock").var()

ABTTYPE.sub(HEALING)
ABTTYPE.sub(SMOOTH)
ABTTYPE.sub(JANUSABT)
ABTTYPE.sub(STOCK)

ABUTMENT = KList("abutment", "abutment, abut").var()
ABUTMENT.sub(ABTFEATURE)
ABUTMENT.sub(ABTMATERIAL)
ABUTMENT.sub(ABTTYPE)

#---------------------------------------
PERTOOTH = KList("pertooth","unit").var()
PERTOOTH.sub(ABUTMENT)
PERTOOTH.sub(CROWN)

#--------------------
PRODUCT= KList("product","").var()
PRODUCT.sub(PERTOOTH)

# ----------------------
MOUTH = KList("mouth", "").var()
MOUTH.sub(TOOTHGROUP)
MOUTH.sub(REFFEATURE) # eg gingiva
MOUTH.sub(SIDE)       # eg mesial

#FINAL DENTAL TREE---------------------------------------
DENTAL = KList("dental","").var()
DENTAL.sub(MOUTH)
DENTAL.sub(PRODUCT)

# ADD THE INCLUDED TREES
ALLWORDS = DENTAL.copy()
ALLWORDS.sub(GEN_QUANTITY)
ALLWORDS.sub(GEN_GEOMETRY)
#------------------------------
toothNAR = attribute( [TOOTH], INTx) # will often score .5
toothfeatureNAR = attribute( ABTFEATURE, [INTx], [TOOTH]) # will often score .5

#--------------------------------------

 # BASE topic
# "make base convex" or "convex EPS please"
epsNAR = attribute( BASE, EPSTYPE ) # an easy one 
# ".2mm tissue pressure"
tisspressNAR = attribute( PRESSURE, FLOATx, [MM] )
# "light tissue pressure"
tisspressNAR2 = attribute( PRESSURE, STRENGTH, [SOFTTISSUE] )

B = [
        NWTopicReader("epsReader", ALLWORDS , epsNAR ),
        NWTopicReader("tpReader",  ALLWORDS , tisspressNAR ),
        NWTopicReader("tpReader2", ALLWORDS , tisspressNAR2 ),
        NWTopicReader("toothfeatureR", ALLWORDS, toothfeatureNAR)
    ]
BaseTopic = NWTopic( MOUTH, B ) 

#-----------------------------------------------
 # MARGIN topic
 # "put margin .2mm below gingiva", or ".2 mm below" or "below gingiva"
#marginNAR = relation( [SIDE], [REFFEATURE], LO_HI , [FLOATx] )
marginNAR = relation( [SIDE], [MREF], RELATION , [FLOATx] )

M = [
        NWTopicReader("margR", ALLWORDS, marginNAR),
        NWTopicReader("toothfeatureR", ALLWORDS, toothfeatureNAR)
    ]

MarginTopic = NWTopic( ALLWORDS, M)

#-------------------------------------------------------

#T = [
#        NWTopicReader("toothnumR", TOOTHSITE, toothNAR),
#    ]

#ToothTopic = NWTopic( ALLWORDS, T)

#------------------------------------------------------
MYORDER = KList( "order", ' my order , my * order , order , the order  , an order , case , a case , the case ').var()
MYACCOUNT = KList( "account", ' account , payment , amount due , cost , pay , finance' ).var()
#-------------------------------------
TOPIC = KList( "topic", "" ).var()  
#TOPIC.sub(ALLWORDS)
#TOPIC.sub(PERTOOTH)
#TOPIC.sub(MYORDER)
#TOPIC.sub(MYACCOUNT)

 



