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

    STOCK= KList( "stock"
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

MEASUREMENTUNIT= KList(
     LINEAR= KList(
        MM= KList( "mm, mn, millimeter"
        IN= KList( "in, inch" # god forbid!
     ANGULAR= KList(
        DEGREE= KList( "deg, degree"
        ANGLE= KList( "angle, angulation" # overlaps with the verb
        AXIS = KList("axis", axes, axial"



ACTIONS = KList( 
    SEND= KList( "send, resubmit, submit"
    SHIP = KLIst("ship"
    HOLD= KList( "hold, remake, redo"
    DO= KList( " place , show , mimic, mirror, copy, match, ignore, remake, redo, \
            soften, seat, connect, extract, mill, mold, mould, lap, fill, \
            trim, scoop, allow, fit, adjust, reverse, sculpt, flare the, can, get"
    NOTDO= KList( "leave, ignore"
    AUTOMATE= KList( "automate"
    MOVE= KList( "move, make, bring, tilt, lean, pull, push, close the, open the, expand, extend, toward"
    ANGULATE= KList(  "angle, align"    
    CANTILEVER= KList(  
    ROTATE = KLst(


PERIDENTAL
    MYORDER = nwt.KList( "myorder", ' my order , my * order , order , the order  , an order , case , a case , the case ').var()
    ACCOUNT = nwt.KList( "account", ' account , payment , amount due , much , cost ' ).var()

DENTAL= KList( 
    CAST= KList(  "cast, study, study model, provisional, diagnostic"
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
   
    TOOTHGROUPFEATURE
        DIASTEMA= KList( "diastema, diestema, diastama"
        GAP= KList(

    TOOTHSITE
        TOOTH  # borrowed from quantities

        TOOTHGROUP = KList(  "tooth"
            ANTERIOR= KList(  "anterior"
            POSTERIOR= KList(  "posterior"
            MOLAR= KList(  "molar"
            PREMOLAR= KList(  "premolar, pre-molar, primolar, bicuspid, bi-cuspid, bi-suspid"
            INCISOR= KList(  "incisor, central, lateral"
                CENTRAL
                LATERAL
            CANINE= KList(  "canine, eye tooth, eye teeth"

       CONDITION
            PREP= KList(  "prep"
            PONTIC= KList(  "pontic"
            MISSING= KList(   "missing, absent"
            REGULAR= KList(    

        SIDE = KList( 
            ALL= KList(  "all sides, all around, 360, circumferential, around, other values",
            REMAINING= KList(  "rest, other, other values" # as in "the rest of the margins
            BF= KList(  "b/f, f/b, buccal/facial, b&f"
                BUCCAL= KList(  " b , buccal, baccal, buc, buck, bucca, "
                FACIAL= KList(  "f , facial"
                LABIAL= KList(  " labial"
                LINGUAL= KList(  "lingual, ling, lin, l"
                PALATAL= KList(  "palat"
            MD= KList(  "m/d", d/m, mesial/distal, distal/mesial, m&d, proximal, interproximal"
                MESIAL= KList(  "m , mesial , mesail , mes , meaisl , mesial"
                DISTAL= KList(  " d , distal , dist, distall "
            OCCLUSAL= KList(  "occ"
            INCISAL= KList(  "incisal, inc"

        FEATURE= KList(
            FOSSA= KList( "fossa"
            CUSP= KList( "cusp"
            EMBRASURE= KList( "embrasure, vestibule"
            CINGULUM= KList( "cingulum"
            ROOT= KList( "root"
            WALL= KList( "wall"

        REFFEATURE= KList(                   
            SOFTTISSUE= KList( "soft tissue, softtissue, support tissue"   
            SULCUS= KList( "sulcus"
            GUM= KList( "gingiva, gingival, subgingival, subginival, gum, supra_g,sub_g,ridge, gm crest, \
                    supra-gingival, supra-ging, supra_g,\
                    sub-gingival, sub-ginival, sub_g, subgingival, subginival, crest, ridge"
            OPPOSING= KList( "opp"
            ADJACENT= KList( "adjacent, adjacent tooth, adjacent teeth, adjecent, neighbor, \
                            neighboring tooth, neighboring teeth, surrounding"
            INTERFACE= KList(   "interface, fixture, implant, analog, anolog"
            MARK "mark, line"     
            CEJ= KList(  "cej, cement enamel junction"          
            CONTRALATERAL

        CROWN (maybe no indent?)
            CROWNMATERIAL
                PFM= KList( "pfm"
                EMAX= KList( "emax"
                GOLD
            CROWNTYPE= KList(
                FULL= KList( "anatomical, anatomic, full, full contour, anotomical",
                CUTBACK= KList( "cutback, cut back, cutback"
                TEMP= KList( "temp, temporary"
                JANUS= KList( "janus"
            RETENTION= KList( "retained"
                SCREWR= KList( "screwretention, screw retained"
                CEMENTR= KList( "cementretnetion, cement retained"
 
        ABUTMENT (no indent?)
            ABTMATERIAL
                ZR= KList( "zirconia, zirconium, zr"
                TI= KList( "titanium, ti, titania"
                GOLDTI = KList("goldhue","gold, gold hue").var()
            ABTTYPE
                HEALING
                SMOOTH
                
            ABTFEATURE
                MARGIN "margin, collar, outline, height"
                BASE "base, between interface and margin"
                    EPS "eps, esp, ets, profile, emergence, emergense, emergency, emmergence"
                        STRAIGHT "straight, straight eps, striaght, srtaight, off"
                        CONCAVE "concave, convave"
                        CONVEX "convex"
                        ANKYLOS  "ankylos, golf, tee"
                    PRESSURE  "press, presure, blanch, blaching, push, push on, support, expand,\
                                compression, displace,displacement, diplace, impinge, impingement"               
                CORE "core # file, post"
                SHOULDER "shoulder, sholder, chamfer, chamf, champfer, champ, flar, flair"    
                BEVEL "bevel, occlusal bevel"
                GROOVE "groove, retention groove, retentive groove"


    PRODUCT= KList( 
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

################ SIDE ####

SIDE = KList("side","").var()
ALL = KList( "all",  "all sides, all around, 360, circumferential, around, other values").var()
REMAINING= KList( "remainder", "remainder, rest of, other, other values").var() # as in "the rest of the margins
BF= KList("bf",  "b/f, f/b, buccal/facial, b&f").var()
BUCCAL= KList("buccal", " b , buccal, baccal, buc, buck, bucca").var()
FACIAL= KList( "facial","f , facial").var()
BF.sub(BUCCAL)
BF.sub(FACIAL)

MD= KList("md", "m/d, d/m, mesial/distal, distal/mesial, m&d, proximal, interproximal").var()
MESIAL= KList( "mesial", "m , mesial , mesail , mes , meaisl , mesial").var()
DISTAL= KList("d",  " d , distal , dist, distall ").var()
MD.sub(MESIAL)
MD.sub(DISTAL)

LABIAL= KList("labial",  " labial").var()
LINGUAL= KList("lingual",  "lingual, ling, lin, l").var()
PALATAL= KList( "palatal", "palat").var()
OCCLUSAL= KList("occlusal",  "occ").var()
INCISAL= KList( "incisal", "incisal, inc").var()
OPPOSING=KList("opposing", "opp").var()

SIDE.sub(ALL)
SIDE.sub(REMAINING)
SIDE.sub(BF)
SIDE.sub(MD)
SIDE.sub(LABIAL)
SIDE.sub(LINGUAL)
SIDE.sub(PALATAL)
SIDE.sub(OCCLUSAL)
SIDE.sub(INCISAL)
SIDE.sub(ALL)
SIDE.sub(OPPOSING)

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
GUM= KList("gum", "gingiva, gingival, subgingival, subginival, gum, supra_g,sub_g,ridge, gm crest, \
    supra-gingival, supra-ging, supra_g,\
    sub-gingival, sub-ginival, sub_g, subgingival, subginival, crest, ridge").var()
INTERFACE= KList("interface","interface, fixture, implant, analog, anolog").var()
OPPOSING= KList( "opp", "opp").var()
ADJACENT = KList("adjacent","adjacent, adjacent tooth, adjacent teeth, adjecent, neighbor, \
            neighboring tooth, neighboring teeth, surrounding").var()
MARK = KList("mark", "mark, line").var()
CEJ = KList("cej", "cej, cement enamel junction").var()
CONTRALATERAL = KList("contralateral", "contralateral").var()
#-------------------------------------
REFFEATURE = KList("reffeature","").var()
REFFEATURE.sub(SOFTTISSUE)
REFFEATURE.sub(GUM)
REFFEATURE.sub(INTERFACE)
REFFEATURE.sub(OPPOSING)
REFFEATURE.sub(ADJACENT)
REFFEATURE.sub(MARK)
REFFEATURE.sub(CEJ)
REFFEATURE.sub(CONTRALATERAL)
#------------------------------------
ABTFEATURE = KList("abtfeature", "").var()
MARGIN = KList("margin", "margin, collar, outline").var()
BASE = KList("base", "base, between interface and margin").var()      
CORE = KList("core","core # file, post").var()
SHOULDER = KList("shoulder","shoulder, sholder, chamfer, chamf, \
                   champfer, champ, flar, flair" ).var()   
BEVEL = KList("bevel", "bevel, occlusal bevel").var()
GROOVE = KList("groove", "groove, retention groove, retentive groove").var()
ABTFEATURE.sub(MARGIN)
ABTFEATURE.sub(BASE)
ABTFEATURE.sub(MARGIN)
ABTFEATURE.sub(CORE)
ABTFEATURE.sub(SHOULDER)
ABTFEATURE.sub(BEVEL)
ABTFEATURE.sub(GROOVE)
#-------------------------------------
ABTMATERIAL = KList("material", " material ").var() #1st is the name, 2nd is a list
ZIRC = KList("zirconia"," zircomium, zirconia, zr , zi , z ").var()
TITN = KList("titanium"," titanium, titania, ti , t ").var()
GOLDTI = KList("goldTi", "gold, gold hue").var()
ABTMATERIAL.sub(ZIRC)
ABTMATERIAL.sub(TITN)
ABTMATERIAL.sub(GOLDTI)
#-------------------------------------
    # BASE values
EPS = KList("eps", "eps, esp, ets, profile, emergence, emergense, emergency, emmergence").var()      
PRESSURE =  KList("pressure", "press, presure, blanch, blaching, push, push on, support, \
                   expand,tissue pressure,compression, displace,displacement,\
                   diplace, impinge, impingement").var()        
    # value values:
STRAIGHT = KList("off", "off, straight, striaght, srtaight").var()
CONCAVE = KList("concave", "concave, convave").var()
CONVEX = KList("convex", "convex").var()
ANKYLOS  = KList("ankylos", "ankylos, golf, tee, option _hash_ 5").var()
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

# FINAL DENTAL TREE----------------------
TOOTHSITE = KList("dentaltree", "").var()
TOOTHSITE.sub(TOOTHGROUP)
TOOTHSITE.sub(REFFEATURE)
TOOTHSITE.sub(SIDE)
TOOTHSITE.sub(ABTFEATURE)
TOOTHSITE.sub(ABTMATERIAL)

# ADD THE INCLUDED TREES
TOOTHSITE.sub(GEN_QUANTITY)
TOOTHSITE.sub(GEN_GEOMETRY)
#------------------------------


 # NARs and readers for the BASE topic
epsNAR = attribute( EPS, EPSTYPE ) # an easy one
tisspressNAR = attribute( PRESSURE, FLOATx, [MM] )
tisspressNAR2 = attribute( PRESSURE, STRENGTH, [SOFTTISSUE] )

B = [
        NWTopicReader("epsReader", TOOTHSITE , epsNAR ),
        NWTopicReader("tpReader", TOOTHSITE , tisspressNAR ),
        NWTopicReader("tpReader2", TOOTHSITE , tisspressNAR2 )
    ]
BaseTopic = NWTopic( TOOTHSITE, B ) 



