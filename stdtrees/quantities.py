"""
quantities.py lists numbers in various forms, as VARs

This defines QUANTITY and its children ZERO through THIRTYTWO
For other ints, like negatives or > 32, make up your own names.

It is a chore to write out these numbers and you could do it automatically
for most of them. 

"""

from narwhal.nwtypes import KList

# NOTE INCOMPLETE. ONLY #7 is correct

kZERO = ' none , zero , 0 '
kONE  = ' tooth|number|_hash_ $ one , an , a , tooth|number|_hash_ $ 1 ' #introduces a small bug, since 'a'  is also DULL
kTWO = ' tooth|number|_hash_ $ two , couple , _tooth|number|_hash_ $ 2 '
kTHREE = ' tooth|number|_hash_ $ three , tooth|number|_hash_ $ 3 '
kFOUR  = ' tooth|number|_hash_ $ four , tooth|number|_hash_ $ 4 '
kFIVE = ' tooth|number|_hash_ $ five , tooth|number|_hash_ $ 5 '
kSIX  = ' tooth|number|_hash_ $ six , tooth|number|_hash_ $ 6 '
kSEVEN = ' tooth|number|_hash_ $ seven , tooth|number|_hash_ $ 7 ' 
kEIGHT = ' tooth|number|_hash_ $ eight , tooth|number|_hash_ $ 8 '
kNINE = ' tooth|number|_hash_ $ nine , tooth|number|_hash_ $ 9 '
kTEN  = ' tooth|number|_hash_ $ ten , tooth|number|_hash_ $ 10 '
kELEVEN = ' tooth|number|_hash_ $ eleven , tooth|number|_hash_ $ 11 '
kTWELVE = ' tooth|number|_hash_ $ twelve , tooth|number|_hash_ $ 12 '
kTHIRTEEN = ' tooth|number|_hash_ $ thirteen , tooth|number|_hash_ $ 13 '
kFOURTEEN = ' tooth|number|_hash_ $ fourteen, tooth|number|_hash_ $ 14 '
kFIFTEEN = ' tooth|number|_hash_ $ fifteen , tooth|number|_hash_ $ 15 '
kSIXTEEN = ' tooth|number|_hash_ $ sixteen, tooth|number|_hash_ $ 16 '
kSEVENTEEN = ' tooth|number|_hash_ $ seventeen , tooth|number|_hash_ $ 17 '
kEIGHTEEN = ' tooth|number|_hash_ $ eighteen , tooth|number|_hash_ $ 18 '
kNINETEEN = ' tooth|number|_hash_ $ nineteen , tooth|number|_hash_ $ 19 '
kTWENTY = ' twenty # one|two|three|four|five|six|seven|eight|nine, tooth|number|_hash_ $ 20 '
kTWENTYONE = ' twenty one , tooth|number|_hash_ $ 21 '
kTWENTYTWO = ' twenty two , tooth|number|_hash_ $ 22 '
kTWENTYTHREE = ' twenty three , tooth|number|_hash_ $ 23 '
kTWENTYFOUR = ' twenty four , tooth|number|_hash_ $ 24 '
kTWENTYFIVE = ' twenty five , tooth|number|_hash_ $ 25 '
kTWENTYSIX = ' twenty six , tooth|number|_hash_ $ 26 '
kTWENTYSEVEN = ' twenty seven , tooth|number|_hash_ $ 27 '
kTWENTYEIGHT = ' twenty eight , tooth|number|_hash_ $ 28 '
kTWENTYNINE = ' twenty nine , tooth|number|_hash_ $ 29 '
kTHIRTY = ' thirty # one|two, tooth|number|_hash_ $ 30 '
kTHIRTYONE = ' thirty one , tooth|number|_hash_ $ 31 '
kTHIRTYTWO = ' thirty two , tooth|number|_hash_ $ 32 '

kQUANTITY = ' quantity '
QUANTITY = KList( "quantity", kQUANTITY).var()


ZERO = KList("0", kZERO ).var()
ONE = KList( "1", kONE ).var()
TWO = KList( "2", kTWO ).var()
THREE = KList( "3", kTHREE ).var()
FOUR = KList( "4", kFOUR ).var()
FIVE = KList( "5", kFIVE ).var()
SIX = KList( "6", kSIX ).var()
SEVEN = KList( "7", kSEVEN ).var()
EIGHT = KList( "8", kEIGHT ).var()
NINE = KList( "9", kNINE  ).var()
TEN = KList( "10", kTEN  ).var()
ELEVEN = KList( "11", kELEVEN  ).var()
TWELVE = KList( "12", kTWELVE ).var()
THIRTEEN = KList( "13", kTHIRTEEN  ).var()
FOURTEEN = KList( "14", kFOURTEEN ).var()
FIFTEEN = KList( "15", kFIFTEEN  ).var()
SIXTEEN = KList( "16", kSIXTEEN  ).var()
SEVENTEEN = KList( "17", kSEVENTEEN ).var()
EIGHTEEN = KList( "18", kEIGHTEEN  ).var()
NINETEEN = KList( "19", kNINETEEN  ).var()
TWENTY = KList("20",  kTWENTY  ).var()
TWENTYONE = KList("21",  kTWENTYONE ).var()
TWENTYTWO =  KList( "22", kTWENTYTWO ).var()
TWENTYTHREE = KList("23",  kTWENTYTHREE  ).var()
TWENTYFOUR = KList("24",  kTWENTYFOUR ).var()
TWENTYFIVE= KList("25",  kTWENTYFIVE ).var()
TWENTYSIX= KList("26",  kTWENTYSIX  ).var()
TWENTYSEVEN = KList("27",  kTWENTYSEVEN  ).var()
TWENTYEIGHT = KList("28",  kTWENTYEIGHT  ).var()
TWENTYNINE = KList("29",  kTWENTYNINE  ).var()
THIRTY = KList("30",  kTHIRTY  ).var()
THIRTYONE = KList("31",  kTHIRTYONE  ).var()
THIRTYTWO = KList("32",  kTHIRTYTWO  ).var()


kQUANTITY = ' quantity '
QUANTITY = KList( "quantity", kQUANTITY).var()
QUANTITY.sub(ZERO)
QUANTITY.sub(ONE)
QUANTITY.sub(TWO)
QUANTITY.sub(THREE)
QUANTITY.sub(FOUR)
QUANTITY.sub(FIVE)
QUANTITY.sub(SIX)
QUANTITY.sub(SEVEN)
QUANTITY.sub(EIGHT)
QUANTITY.sub(NINE)
QUANTITY.sub(TEN)
QUANTITY.sub(ELEVEN)
QUANTITY.sub(TWELVE)
QUANTITY.sub( THIRTEEN )
QUANTITY.sub(FOURTEEN)
QUANTITY.sub(FIFTEEN)
QUANTITY.sub(SIXTEEN)
QUANTITY.sub(SEVENTEEN)
QUANTITY.sub(EIGHTEEN)
QUANTITY.sub(NINETEEN)
QUANTITY.sub(TWENTY)
QUANTITY.sub(TWENTYONE)
QUANTITY.sub(TWENTYTWO)
QUANTITY.sub(TWENTYTHREE)
QUANTITY.sub(TWENTYFOUR)
QUANTITY.sub(TWENTYFIVE)
QUANTITY.sub(TWENTYSIX)
QUANTITY.sub(TWENTYSEVEN)
QUANTITY.sub(TWENTYEIGHT)
QUANTITY.sub(TWENTYNINE)
QUANTITY.sub(THIRTY)
QUANTITY.sub(THIRTYONE)
QUANTITY.sub(THIRTYTWO)

kTOOTH = " tooth , _hash_ "
TOOTH = KList("tooth",kTOOTH).var()


############################################
""" introduces unknowns, in this case: unknown int
VARs are usually "variable" with range limited to 
sepecific sub VARs. Here we deal with knowns to be
read from the input.

I am using 'x' to indicate "unknown"
"""

kINT = " __d__ "
INTx = KList("int", kINT).var()
# See the connection to the asInt() method in nwutils.pw

kFLOAT = " __fl__ "
FLOATx = KList("float", kFLOAT).var()
# See the connection to the asFloat() method in nwutils.pw

