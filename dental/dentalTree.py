from narwhal.nwtypes import *
from narwhal.nwchat import *

from stdtrees.quantities import *
from stdtrees.geometry import * 
from stdtrees.ask import * 
from stdtrees.tchats import CLIENTASK
 
"""
Mostly words can be divided into ones that describe features of a patient's
mouth versus ones that describe parts that go in the mouth. Some words, 
like "fossa" or "cusp" can apply to existing structures in a mouth or corresponding 
features on the parts. So those are stored willy nilly.
"""


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

#----------------------------------------------------
#------------------MOUTH TREE ---------------------
#----------------------------------------------------
#----------------------------------------------------

############# SIDE (TOOTHSURFACE)##################
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
REFFEATURE.subs( [SOFTTISSUE, GUM, INTERFACE, OPPOSING, ADJACENT, MARK, CEJ, CONTRALATERAL] )
# useful subset (excludes OPPOSING, and CONTRALATERAL)
MREF = KList("marginreference", "").var() 
MREF.subs([SOFTTISSUE, GUM, INTERFACE, ADJACENT, MARK, CEJ])

MOUTH = KList("mouth", "").var()
MOUTH.subs([TOOTHGROUP, REFFEATURE, SIDE])

#----------------------------------------------------
#------------------PRODUCT TREE ---------------------
#----------------------------------------------------
#----------------------------------------------------
TEMP = KList("temp", "temp, temp crown, temporary, temporary crown").var()
FULL = KList("full", " full, full crown,full contoured, full contoured crown,\
regular, regular crown, normal, normal crown, standard, standard crown").var()
JANUSCROWN = KList("janus", "janus # abutment, janus crown" ).var()
CUTBACK = KList("cutback", "cutback, cut back, cutback crown, cut back crown").var()
CROWNTYPE = KList("crowntype", "crowntype").var()
CROWNTYPE.subs([TEMP, FULL, JANUSCROWN, CUTBACK])
 
#--------CROWN SURFACE
OCCLUSAL= KList("occlusal",  "occ").var()
INCISAL= KList( "incisal", "incisal, inc").var()
SURFACE = KList("surface","").var()
SURFACE.subs([OCCLUSAL, INCISAL])
 
#------------------CROWNMATERIAL
PFM = KList("pfm","pfm").var()
EMAX = KList("emax","emax").var()
PORCELAIN = KList("porcelain","porc").var()
CROWNMATERIAL = KList("crownmaterial","").var()
CROWNMATERIAL.subs([PFM, EMAX, PORCELAIN])
 
#---------------CROWNFEATURE
HOLE= KList("hole","hole, screw hole, screwhole").var()
WALL = KList("wall", "wall").var()
#CUSPS
#FOSSA
#VESTIBULE
#CINGULUM
CROWNFEATURE = KList("crownfeature","").var()
CROWNFEATURE.subs([HOLE, WALL])
 
kCROWN = 'temporary|temp|janus|cutback|regular|normal|standard $ crown'
CROWN = KList( "crown", kCROWN).var()
CROWN.subs([CROWNTYPE, CROWNFEATURE, SURFACE, CROWNMATERIAL])
 

#------------------ABTFEATURE-----------
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
EPSTYPE = KList("epstype", "").var()
EPSTYPE.subs([STRAIGHT, CONCAVE, CONVEX, ANKYLOS])
 
#-----------------------------
BASE = KList("base", "base, between interface and margin").var()     
BASE.subs([EPS, PRESSURE, EPSTYPE ])
 
#------------------------------
MARGIN = KList("margin", "margin, collar, outline").var()
CORE = KList("core","core # file, post").var()
SHOULDER = KList("shoulder","shoulder, sholder, chamfer, chamf, \
                   champfer, champ, flar, flair" ).var()   
BEVEL = KList("bevel", "bevel, occlusal bevel").var()
GROOVE = KList("groove", "groove, retention groove, retentive groove").var()
ABTFEATURE = KList("abtfeature", "").var()
ABTFEATURE.subs([BASE , MARGIN, CORE, SHOULDER, BEVEL, GROOVE])

 #------------------ABTMATERIAL-------------------
ZR = KList("zirconia"," zircomium, zirconia, zr , zi , z ").var()
TI = KList("titanium"," titanium, titania, ti , t ").var()
GOLDTI = KList("goldTi", "gold, gold hue").var()
ABTMATERIAL = KList("abtmaterial", "").var()
ABTMATERIAL.subs([ZR, TI, GOLDTI])
 
#-------------------------------------

ABTTYPE = KList("abttype", "").var()
HEALING = KList("healingabut","healing abutment").var()
SMOOTH = KList("smoothabut", "smooth abutment").var()
JANUSABT = KList("janusabut","janus # crown").var()
STOCK= KList( "stock", "stock").var()
ABTTYPE.subs([HEALING, SMOOTH, JANUSABT, STOCK])
 
#---------------------------------------
ABUTMENT = KList("abutment", "abutment, abut, unit, abutmen").var()
ABUTMENT.subs([ABTFEATURE, ABTMATERIAL, ABTTYPE])
 
#-------------- retention --------------------
SCREW = KList("screw","screw").var()
CEMENT = KList("cement","cement").var()
RETENTION = KList("retention", "retention, retained").var()
RETENTION.subs([SCREW,CEMENT])

#-----------------SINGLE UNIT-------------
PERTOOTH = KList("pertooth","unit").var()
PERTOOTH.subs([ABUTMENT, CROWN, RETENTION])


               
#----------------MULTIUNIT---------------
BAR = KList( "bar", " bar ").var()
BRIDGE = KList( "bridge", " bridge ").var()
SUPERSTRUCTURE = KList( "superstructure", "superstructure").var()
GUIDE = KList("guide", "guide, seating guide, drill guide").var()
IMPLANT = KList("implant", "implant").var()
KIT = KList("kit","kit").var()
BOX = KList("box"," box , pack, package").var()
MULTIUNIT = KList("multiunit", "").var()
MULTIUNIT.subs([BAR, BRIDGE, SUPERSTRUCTURE, GUIDE, IMPLANT, KIT, BOX])
 
# Dental products are made up of "per tooth" products, "per tooth group" products
# "per jaw (maxilla or mandible)) products", "generic consumable", ...
PRODUCT= KList("product","product").var()
PRODUCT.subs([PERTOOTH, MULTIUNIT])
 
#-----------------------a separate version of the variables (not used currently)---
MATERIAL = KList("material","").var()
MATERIAL.subs([ABTMATERIAL, CROWNMATERIAL])
 
# FINAL DENTAL TREE--------------------
DENTAL= KList("dental","").var()
DENTAL.subs([MOUTH, PRODUCT])
 
# FINAL VOCAB--------------------
# add the vocabulary used in NAR definition and reading                  
DTREE = KList("dtree","").var()
DTREE.subs([DENTAL, GEN_QUANTITY, GEN_GEOMETRY, CLIENTASK])
 
###########################################
###########################################

#------------------------------

# BASE topic
# "make base convex" or "convex EPS please"
epsNAR = attribute( BASE, EPSTYPE ) # an easy one 
# ".2mm tissue pressure"
tisspressNAR = attribute( PRESSURE, FLOATx, [MM] )
# "light tissue pressure"
tisspressNAR2 = attribute( PRESSURE, STRENGTH, [SOFTTISSUE] )

B = [
        NWTopicReader("epsReader", DTREE , epsNAR ),
        NWTopicReader("tpReader",  DTREE , tisspressNAR ),
        NWTopicReader("tpReader2", DTREE , tisspressNAR2 )
    ]

BaseTopic = NWTopic( DTREE, B ) 

#-----------------------------------------------
 # MARGIN topic
 # "put margin .2mm below gingiva", or ".2 mm below" or "below gingiva"
#marginNAR = relation( [SIDE], [REFFEATURE], LO_HI , [FLOATx] )
marginNAR = relation( [SIDE], [MREF], RELATION , [FLOATx] )
toothfeatureNAR = attribute( ABTFEATURE, [INTx], [TOOTH]) # will often score .5

M = [
        NWTopicReader("margR", DTREE, marginNAR),
        NWTopicReader("toothfeatureR", DTREE, toothfeatureNAR)
    ]

MarginTopic = NWTopic( DTREE, M)

#-------------------------------------------------------
toothNAR = attribute( [TOOTH], INTx) # will often score .5

T = [
        NWTopicReader("toothnumR", DTREE, toothNAR),
    ]

ToothTopic = NWTopic( DTREE, T)

#------------------------------------------------------
MYORDER = KList( "order", ' my order , my * order , order , the order  , an order , case , a case , the case ').var()
MYACCOUNT = KList( "account", ' account , payment , amount due , cost , pay , finance' ).var()
 
#--------------------------------------------------
# questions and requests involving dental info.
dentalAsk = attribute(QUESTION, DENTAL)
dentalRequest = attribute(REQUEST, DENTAL)
DentalAgendaReaders = [ 
                      NWTopicReader("dask",DTREE, dentalAsk),
                      NWTopicReader("dreq",DTREE, dentalRequest)
                    ]

## Sub readers, become separate topics
DentalQ = [ NWTopicReader("dask",DTREE, dentalAsk) ]
DentalQuestionTopic = NWTopic( DTREE, DentalQ )

DentalR = [  NWTopicReader("dask",DTREE, dentalAsk) ]
DentalRTopic = NWTopic( DTREE, DentalR )
