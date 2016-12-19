#this file is for the Noise application with VAR tree like this:
##EXPERIENCE( experienceD )
##  PROBLEM( problemD )
##  SOUND( soundD )
##    NOISE( noiseD | quietD )
##    INTENSITY( loudD | softD )
##    SOURCE( peopleD + equipmentD + ... + oceanD )
##  LOC( locationD )
##    ROOM( roomD )
##    HOTEL( hotelD )
##    PROX( nearD | farD )
##  INSULATION()
##    MATERIAL( windowD + wallD )
##    STATE( openD | closedD )
##    TRANSPARENCY( letInD | keepOutD )
##  TOD( timeofdayD )
##  AFFECT( stressD | relaxD )


from nwtypes import *


kOTHERTOPICS = "tourist,boulangerie,flight,write,located,neighborhood,feeling, far ,looked,trip, deal,carpet,decor,big,inn,days,month,usd,sauna,mention,stay ,dinner,smell,speak,cheap,gym,remodeled,buffet,decorations,refurbished,seal out,view,safe,apart from,otherwise,central,cost , clean, tidy,towel,sheets, bed, neat";


# KEYWORDS SHOULD BE IN LOWER CASE

########### FOR ANOTHER DAY#############
kSUPER    = "very pleased,soothing,a gem, love ,home away from home,\
                          homely,wow,wonderful,bliss,happy,superb,gorgeous,spotless,\
                          immaculate,phenomenal,fantastic,perfect,relax,excellent,\
                          spectacular,peaceful,lovely,beautiful,amazing,impressive,\
                          impressed,heaven,magical,fabulous,serene,paradise,special,\
                          cozy,oasis" 
kHORRIBLE = "unacceptable,filthy,dump,mildew,lousy,awful,horrible,\
                          horrid,poison,gross, ick,ss icky,disgusting, hairs,yuck,\
                          ugh ,unhelpful,unpleasant,dissappoint,disappoint,\
                          terrible,bugs,spider"



############################ SOUND EXPERIENCE WORD LISTS #####################################
NONRESPONSIVE = "grumpy,abrupt,aloof,non responsive,clueless,did nothing,"
NONRESPONSIVE += " nothing was done,no one followed up,ineffective,disorganized,"
NONRESPONSIVE += "no apology,disinterested,ignored,barely polite,unresponsive "

RESPONSIVE = "very helpful,attentive,taking the trouble,positive,apologetic,"
RESPONSIVE += "accomodat,worked hard,welcoming"

kSLEEPPOSITIVES = "undisrupted,undisturb,sleep, rest # of "

kSLEEPNEGATIVES = "wake # up,awake,woke,awoke,waken,woken, disturb, disrupt,stirred,bother,sleepless"

kTIMEOFDAY = " am ,pm ,all night, nights ,throughout the night,early, late ,all hours,"
kTIMEOFDAY += "morning,each morning,half the night,at night,middle of the night,every night,"
kTIMEOFDAY += "sunday night,monday night,tuesday night,wednesday night,thursday night,"
kTIMEOFDAY += "friday night,saturday night,midnight,evening,"
kTIMEOFDAY += " 1 am, 1 pm, 2 am, 2 pm, 3 am, 3 pm, 4 am, 4 pm, 5 am, 5 pm, 6 am, 6 pm, 7 am, 7 pm,"
kTIMEOFDAY += "8 am,8 pm, 9 am, 9 pm, 10 am, 10 pm, 11 am, 11 pm, 12 am, 12 pm"



kNOISEWORDS = "street sound, noise, nosie,noise level,rampage,noisy,hear # about,"
kNOISEWORDS += "heard # of|from|how|great,blaring, loud ,deafening,deafning,racket # club,"
kNOISEWORDS += "moan ,shout # out, crying,scream,slamming,slammed, barking ,yelling,talking # with|to,"
kNOISEWORDS += "whistling,snoring,roaring,knocking,swearing,footstep,flush,spoken, word spoken"

kQUIETWORDS = "soft,low volume,tranquil,good sleep,silent,quiet,"
kQUIETWORDS += "isolation, rested,soundly,oasis,peace,serene,frogs,birds, waves"

kPEOPLESOURCES="kitchen,maids,steps # from|away,people,fisherman,fishermen,our $ group,"
kPEOPLESOURCES += "other guest,other guests,neighbors,neighbours,kids,teenagers,"
kPEOPLESOURCES += "shower,couples,neighbors,dogs,hustle,bustle,squeak,"


kPARTYSOURCES="stadium,party,function,wedding,drunk,club,mcdonalds,music,"
kPARTYSOURCES += " bar ,hofbrau,piano player,singer,partied,revellers"

kEQUIPMENTSOURCES=" ac , a/c ,air con,air-con,a/c,aircon,air conditioner,air conditioning,"
kEQUIPMENTSOURCES += "tv,air shaft,drains,hvac,central heating,lift,elevator, fan ,"
kEQUIPMENTSOURCES += " ice ,ventilation,clanking,clattering,rumbling"

kTRAFFICSOURCES="truck,traffic,busy,busy street,shopping, street, main , market , road noise,highway,diesel,"
kTRAFFICSOURCES+= "road, alley, city , downtown , center, centre , garage , engine , tram,deliveries"


kCONSTRUCTIONSOURCES="banging,pounding,construction,remodelling,remodeling,maintenance,machinery,hammering" 

kOASISSOURCES="ocean"

kNOISELOCSROOM="that, it ,our floor, room # for,my room,our room,outside,window,balcony door,next to,door ,next door,"
kNOISELOCSROOM+="my door,outside my door,adjacent room,next suite,"
kNOISELOCSROOM+="next room,neighboring roof,above,below,hallway,hall,corridor,"
kNOISELOCSROOM+="bathroom,walls"

kNOISELOCSHOTEL="hotel, high $ floor,building,area, section,location,quiet hotel,"
kNOISELOCSHOTEL+="lobby,patio,neighborhood,pool"
 



#-------------OTHER LISTS FROM THE OLD NOISE APP--------
SLOWSPEED = "slow,we|I $ spent,wait # staff,waiting # to|staff,took time,took * minutes,takes time"
FASTSPEED = "ready,immediate,convenient,easy,speedy,prompt,quick,quickly,smooth,efficient, fast ,within minutes,no time"
TIMEUNITS = "0,1,2,3,4,5,6,7,8,9,minutes,hour, mins "  

PROFFESIONAL = "infromative,well run,hard-working,assist,out of their way,out of the way,always remember,"
PROFFESIONAL += "helpful,gracious,polite,sensitive,accommodating,professional, eager,knowledgeable,"
PROFFESIONAL += "courteous,attentive,attentive to,attention,apology,apologized,apologetic,competent,"
PROFFESIONAL += "know how,no problem,made sure,make sure,making sure,ensure,taking the trouble,care of,"
PROFFESIONAL += "positive,accomodat,worked hard,bent over backwards"

UNPROFFESIONAL = "complain, exception ,lost a bag,spotty,sketchy,hit or miss,grumpy,abrupt,aloof,"
UNPROFFESIONAL += "non responsive,clueless,no one came,did nothing,nothing was done,ineffective,"
UNPROFFESIONAL += "disorganized,no apology,disinterested,ignored,barely polite,unresponsive,"
UNPROFFESIONAL += "not experienced,inexperienced,over enthusiastic,failed,refused,forgot # her|him"

############################################################################
#------------- KLists
# add to this list
# note: expericence shoule be made as the | of two KList VARs
# For example "was bad" belongs in a negative KList
kEXPERIENCE = "experience,we found,I found,we did find"
experienceD = KList("experience", kEXPERIENCE)  

kPROBLEM = "problem,issue,drawback,not for you"
problemD = KList("problem", kPROBLEM)

kSOUND = "sound"
soundD = KList("sound", kSOUND)

noiseD = KList("noise", kNOISEWORDS)
quietD = KList("quiet", kQUIETWORDS)

kLOUD = "very noisy,loud,very loud, a bit of, a bit,bad" #people hate to criticize and use understatement
loudD = KList("loud", kLOUD)
kSOFT = "soft, low # volume|tide, down ,very quiet" #I'm too lazy to implement "keep the noise down"
softD = KList("soft", kSOFT)

peopleD = KList("people", kPEOPLESOURCES)
partyD  = KList("party", kPARTYSOURCES)
equipmentD = KList("equip", kEQUIPMENTSOURCES)
trafficD = KList("traffic", kTRAFFICSOURCES)
constructionD = KList("constr", kCONSTRUCTIONSOURCES)
oasisD = KList("oasis", kOASISSOURCES)
## unfotunately, to work around a bug:
nsourceD = KList("nsource", kPEOPLESOURCES + kPARTYSOURCES + kEQUIPMENTSOURCES + kTRAFFICSOURCES + kCONSTRUCTIONSOURCES)
qsourceD = KList("oasis",kOASISSOURCES)




roomD = KList("room", kNOISELOCSROOM)
hotelD = KList("hotel", kNOISELOCSHOTEL)
 


kNEAR = "nowhere $ near , near to ,in the heart of, over , on the ,on our,being on, right on ,overlooked,overlooks, close to,next door"
nearD = KList("near", kNEAR)
kFAR  = " far , far from,farthest from, away from,nowhere near"
farD = KList("far",kFAR)

kINSULATION = "insulation,filter,isolated from, away from , deaden,soundproof,glazed,"
kINSULATION += "glazing,sound deadening,sound proof,sound prof,sound insulation,insulate,"
insulationD = KList("insul", kINSULATION)

kWINDOW = " window, balcony "
windowD = KList("window", kWINDOW)
kWALL = "wall,my|next $ door,floor"
wallD = KList("wall", kWALL)

kOPEN = "open, thin , paper thin"
openD = KList("open", kOPEN)
kCLOSED = "closed,thick "
closedD = KList("closed", kCLOSED)

kLETIN = "let in, still hear, heard through, came in, lets in, lets * in, let * in, came through, through , coming through, carries"
letinD = KList("letin", kLETIN)

kKEEPOUT  = "keep out,keep * out,the $ block, filter,cut down on,far away enough,"
kKEEPOUT += "far away from,shut out,cut out,block,keep out,kept out,drown out,"
kKEEPOUT += "escape from"
keepoutD = KList("keepout", kKEEPOUT)

timeofdayD = KList("tod", kTIMEOFDAY)

relaxD = KList("relax", kSLEEPPOSITIVES)
stressD = KList("stress", kSLEEPNEGATIVES)

############################################################################
############################################################################
############################################################################

#-----------define the VARs from the KeyLists
EXPERIENCE = experienceD.var()
PROBLEM = problemD.var()
SOUND = soundD.var()

NOISE = noiseD.var()|quietD.var()

INTENSITY = loudD.var()|softD.var()


SOURCE = nsourceD.var() | qsourceD.var()
 
#SOURCE = (peopleD.var() + partyD.var() + equipmentD.var()+ trafficD.var() + constructionD.var()) | oasisD.var()


LOC = KList("loc","").var() #VAR()  
ROOM = roomD.var()  
HOTEL =  hotelD.var()

PROX =  nearD.var()|farD.var()  # typically an adjective val
INSULATION = insulationD.var() 
BARRIER = windowD.var() + wallD.var() 
STATE = openD.var()|closedD.var()
LETINOUT = letinD.var()|keepoutD.var() # typically a verb
TOD = timeofdayD .var() 
AFFECT = stressD.var()|relaxD.var() 

#--------------define the tree built from these VARs
EXPERIENCE.sub(PROBLEM)
EXPERIENCE.sub(SOUND)
EXPERIENCE.sub(LOC)
EXPERIENCE.sub(PROX)
EXPERIENCE.sub(INSULATION)
EXPERIENCE.sub(TOD)
EXPERIENCE.sub(AFFECT)

#PROBLEM
#
SOUND.sub(NOISE)
SOUND.sub(INTENSITY)
SOUND.sub(SOURCE)
#
LOC.sub(ROOM)
LOC.sub(HOTEL)
#LOC.sub(PROX) moved up
#
INSULATION.sub(BARRIER)
INSULATION.sub(STATE)
INSULATION.sub(LETINOUT)
#
# TOD - no children
#
# AFFECT - no children
 
  
# Some NARs
#                       sound->me :: me_/affect
#                       sound_/intensity_/source_/timeOfDay (use implicits)
#                       problem_/sound
#                       (barrier_/state)-letInOut->sound
#                       location _nearfar_/ source
#                       X_/Y :: sound

