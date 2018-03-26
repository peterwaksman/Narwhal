""" 
Atlantis chat specific VAR trees
    CLIENTSAYS
        QUESTION
        HELLO
        ACCOUNT 
        MYORDER 
        PRODUCT
            ABUTMENT    
            CROWN
            BAR
            BRIDGE
            SUPERSTRUCTURE
            KIT

    ORDERSAYS  
        REQUEST 
        INTx 
        FLOATx 
        TOOTH 
        YES_NO 
        ABTMATERIAL
        CROWNTYPE
        PRODUCT
            ABUTMENT    
            CROWN
            BAR
            BRIDGE
            SUPERSTRUCTURE
            KIT


Also incuded, for now, are the NARs and their
grouping into the chattopics.
"""
import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal import nwtypes as nwt
from narwhal.nwchat import NWTopicReader, NWTopic


from stdtrees.quantities import *  
from stdtrees.ask import *  
 

###############################################################################
###############################################################################
############################# NARS   ##########################################
###############################################################################

kABUTMENT = ' abutment, unit, abutmen'
ABUTMENT = nwt.KList( "abutment", kABUTMENT).var()
 
#kCROWN = ' crown, cut back , full contour , janus, janus crown, temp crown, temporary crown'
kCROWN = 'temporary|temp|janus|cutback|regular|normal|standard $ crown'
CROWN = nwt.KList( "crown", kCROWN).var()

kBAR = ' bar'
BAR = nwt.KList( "bar", kBAR).var()

kBRIDGE = ' bridge,'
BRIDGE = nwt.KList( "bridge", kBRIDGE).var()

kSUPERSTRUCTURE = ' superstructure '
SUPERSTRUCTURE = nwt.KList( "superstructure", kSUPERSTRUCTURE).var()

kGUIDE = ' guide, seating guide, drill guide' # note terminations
GUIDE = nwt.KList("guide", kGUIDE).var()

kIMPLANT = ' implant'
IMPLANT = nwt.KList("implant", kIMPLANT).var()

kKIT = ' kit'
KIT = nwt.KList("kit",kKIT).var()

kBOX = ' box , package '
BOX = nwt.KList("box",kBOX).var()

# grouping them
kPRODUCT = ' product, part'
PRODUCT = nwt.KList( "product", kPRODUCT).var()

#UNIT = nwt.KList("unit", ' unit' ).var()
#UNIT.sub(ABUTMENT)
#UNIT.sub(CROWN)
#PRODUCT.sub(UNIT)
PRODUCT.sub(ABUTMENT)
PRODUCT.sub(CROWN)
PRODUCT.sub(BAR)
PRODUCT.sub(BRIDGE)
PRODUCT.sub(SUPERSTRUCTURE)
PRODUCT.sub(GUIDE)
PRODUCT.sub(IMPLANT)
PRODUCT.sub(KIT)
PRODUCT.sub(BOX)

# slightly meta (separate 'case' from 'order'?):
kMYORDER = ' my order , my * order , order , the order  , an order , case , a case , the case '
MYORDER = nwt.KList( "myorder", kMYORDER).var()

kACCOUNT = ' account , payment , amount due , much , cost '
ACCOUNT = nwt.KList( "account", kACCOUNT ).var()

# final grouping
kCLIENTSAYS = ' i , me '
CLIENTSAYS = nwt.KList( "clientsays", kCLIENTSAYS).var()

CLIENTSAYS.sub(HELLO)
CLIENTSAYS.sub(MYORDER)
CLIENTSAYS.sub(PRODUCT)
CLIENTSAYS.sub(ACCOUNT)
# Avoid  making PRODUCT a sub() of MYORDER. It  
# confuses questions about orders and about products)
CLIENTSAYS.sub(QUESTION)   
CLIENTSAYS.sub(YOU)
CLIENTSAYS.sub(YES_NO)
CLIENTSAYS.sub(QUANTITY) 

#CLIENTSAYS.sub(INTx)
#CLIENTSAYS.sub(BOTH)

 
# material dictionary for abutments
ABTMATERIAL = nwt.KList("material", " material ").var() #1st is the name, 2nd is a list
ZIRC = nwt.KList("zirconia"," zircomium, zirconia, zr , zi , z ").var()
TITN = nwt.KList("titanium"," titanium, titania, ti , t ").var()
GOLDTI = nwt.KList("goldTi", "gold, gold hue").var()
ABTMATERIAL.sub(ZIRC)
ABTMATERIAL.sub(TITN)
ABTMATERIAL.sub(GOLDTI)
#########experiment


 

CLIENTSAYS.sub(ABTMATERIAL)

CROWNTYPE = nwt.KList("crowntype", "crowntype").var()
TEMP = nwt.KList("temp", "temp, temp crown, temporary, temporary crown").var()
FULL = nwt.KList("full", " full, full crown,full contoured, full contoured crown,\
regular, regular crown, normal, normal crown, standard, standard crown").var()
JANUS = nwt.KList("janus", "janus, janus crown" ).var()
CUTBACK = nwt.KList("cutback", "cutback, cut back, cutback crown, cut back crown").var()
CROWNTYPE.sub( TEMP )
CROWNTYPE.sub( FULL )
CROWNTYPE.sub( JANUS )
CROWNTYPE.sub( CUTBACK )



##############################################
ORDERSAYS = nwt.KList("ordersays","").var()
ORDERSAYS.sub(INTx)
ORDERSAYS.sub(FLOATx)
ORDERSAYS.sub(TOOTH)
ORDERSAYS.sub(YES_NO)
ORDERSAYS.sub(ABTMATERIAL)
ORDERSAYS.sub(REQUEST)
ORDERSAYS.sub(PRODUCT) #OK to share with another tree (CLIENTSAYS)
ORDERSAYS.sub(CROWNTYPE)

ORDERSAYS.sub(BOTH)

####################### SCANNERSAYS ###################
""" 
SCANNER
    NONE
    LABSCANNED
        THREESHAPE
        DENTALWINGS
        ...
    INTRAORAL
        ITERO
        SIRONA_X5
        ...
"""

# basic scanner and it subcategories
kSCANNER = ''#'scanner'
SCANNERSAYS = nwt.KList("scannersays", kSCANNER ).var()
kINTRAORAL =' io , ios , intraoral, intra-oral, intra oral, inter oral, inter-oral, interoral '
INTRAORAL = nwt.KList("intraoral", kINTRAORAL ).var()
kLABSCANNED = 'labscanned'
LABSCANNED = nwt.KList("labscanned", kLABSCANNED ).var()
kNOSCANNER = ' none, no scanner '
NOSCANNER = nwt.KList("noscanner", kNOSCANNER).var()
#group into tree
SCANNERSAYS.sub(NOSCANNER)
SCANNERSAYS.sub(INTRAORAL)
SCANNERSAYS.sub(LABSCANNED)



# specific scanners (labscaned)
k3SHAPE = '3shape # trios'
THREESHAPE = nwt.KList("3shape", k3SHAPE).var()
kLAVASYSTEM = 'lavasystem, 3m espe lava'
LAVASYSTEM = nwt.KList("lavasystem", kLAVASYSTEM).var()
kDENTALWINGS = 'dentalwings, dental wings'
DENTALWINGS = nwt.KList("dentalwings", kDENTALWINGS).var()
kDWOSCANST = 'dwoscanst, lava scan, dwos'
DWOSCANST = nwt.KList("dwoscanst", kDWOSCANST).var()
kSIMPLANT = ' simplant '
SIMPLANT = nwt.KList("simplant", kSIMPLANT).var()
kLYRA = 'lyra, lyra scanner' 
LYRA = nwt.KList("lyra", kLYRA).var()
kISUSSOFT = 'isussoft ' 
ISUSSOFT = nwt.KList("isussoft", kISUSSOFT).var()
kTRIOS = '3shape trios, trios ' #dismbiguate TRIOS io and TRIOS Labscanned ?
TRIOS = nwt.KList("trios", kTRIOS).var()
kEXOCAD = 'exocad'
EXOCAD = nwt.KList("exocad", kEXOCAD).var()
 
# group as labscanned (in house?) scanners
LABSCANNED.sub(THREESHAPE)  
LABSCANNED.sub(LAVASYSTEM)
LABSCANNED.sub(DENTALWINGS)
LABSCANNED.sub(DWOSCANST)
LABSCANNED.sub(SIMPLANT)
LABSCANNED.sub(LYRA) 
LABSCANNED.sub(ISUSSOFT)
LABSCANNED.sub(TRIOS)
LABSCANNED.sub(EXOCAD)


# specific scanner (intra oral)
kITERO = ' itero '
ITERO = nwt.KList("itero", kITERO).var()

kLYRA_IOS = 'lyra ios, lyra intra-oral, lyra intra oral, lyra introral' 
LYRA_IOS = nwt.KList("lyra_ios", kLYRA_IOS).var()
kSIR_OMNI= 'omni , sirona omni, sirona_omnicam ios'
SIR_OMNI = nwt.KList("sirona_omni", kSIR_OMNI).var()
kSIR_BLUE = 'sirona_bluecam_ios, sirona bluecam, sirona blucam ios'
SIR_BLUE = nwt.KList("sirona", kSIR_BLUE).var()
kSIR_X5 = 'sirona_x5, sirona x5, sirona x3 ios'  
SIR_X5 = nwt.KList("sirona_x5", kSIR_X5).var()
kIMETRIC = ' imetric ' 
IMETRIC = nwt.KList("imetric", kIMETRIC).var()
# group as intra oral scanners
INTRAORAL.sub(ITERO) 
INTRAORAL.sub(LYRA_IOS)
INTRAORAL.sub(SIR_OMNI)
INTRAORAL.sub(SIR_BLUE)
INTRAORAL.sub(SIR_X5)
INTRAORAL.sub(IMETRIC)


###############################################################################
###############################################################################
############################# NARS   ##########################################
###############################################################################

# NARs using CLIENTSAYS  #

askABTMaterial = nwt.attribute(QUESTION, ABTMATERIAL )
about = nwt.attribute(QUESTION,[PRODUCT],YOU)
orderinfo = nwt.attribute(QUESTION, MYORDER)
productinfo = nwt.attribute(QUESTION,PRODUCT)
account =  nwt.attribute(QUESTION, ACCOUNT)
hi = nwt.attribute(HELLO,HELLO) 

 
N = [ 
        NWTopicReader('askmaterial', CLIENTSAYS, askABTMaterial),
        NWTopicReader('about', CLIENTSAYS, about ), 
        NWTopicReader('orderinfo', CLIENTSAYS, orderinfo ),
        NWTopicReader('productinfo', CLIENTSAYS, productinfo ),
        NWTopicReader('account', CLIENTSAYS, account ),
        NWTopicReader('hi', CLIENTSAYS, hi ),  
    ]  


###########NARS using ORDERSAYS #
makeorder = nwt.attribute(REQUEST,[TOOTH],PRODUCT)
getToothNumber = nwt.attribute([TOOTH],  INTx)
getCaseNumber  = nwt.attribute([MYORDER],INTx )     
getMarginDepth = nwt.attribute([TOOTH],  FLOATx)
getABTMaterial = nwt.attribute( [TOOTH],[INTx], ABTMATERIAL )
getCrownPerTooth = nwt.attribute( [TOOTH], [INTx], CROWNTYPE)
getCrownXPerTooth = nwt.attribute( [TOOTH], [INTx], CROWN)
 

M = [
        NWTopicReader('toothno', ORDERSAYS, getToothNumber),
        NWTopicReader('makeorder', ORDERSAYS, makeorder),
        NWTopicReader('caseno', ORDERSAYS, getCaseNumber),
        NWTopicReader('margin', ORDERSAYS, getMarginDepth),
        NWTopicReader('getmaterial', ORDERSAYS, getABTMaterial),
        NWTopicReader('getcrowntooth', ORDERSAYS, getCrownPerTooth),
        NWTopicReader('getcrownXtooth', ORDERSAYS, getCrownXPerTooth),
    ]

############ A NAR using YES_NO  #

Y = [ 
        NWTopicReader('yesno', YES_NO, yesno )
    ]


########### A NAR using SCANNER
getScanner = nwt.attribute(SCANNERSAYS,SCANNERSAYS) 
# the max gof score of 0.5 becomes meaningful in "getscanner" context

S = [
        NWTopicReader('scantype', SCANNERSAYS, getScanner )
    ]

#############
ClientTopic = NWTopic(CLIENTSAYS, N)
OrderTopic = NWTopic(ORDERSAYS, M)
YesNoTopic = NWTopic(YES_NO,Y)
ScannerTopic = NWTopic(SCANNERSAYS, S)


#chattopics = [ClientTopic, OrderTopic]
#chattopics = [ClientTopic,OrderTopic, YesNoTopic]
chattopics = [ClientTopic, OrderTopic, YesNoTopic, ScannerTopic ]
