"""
quantities.py lists numbers in various forms, as VARs
"""

from narwhal.nwtypes import KList

kZERO = ' none , zero , 0 '
kONE  = ' one , an, a , 1 '
kTWO = ' two , 2 '
kTHREE = ' three , 3 '
kFOUR  = ' four , 4 '
kFIVE = ' five , 5 '
kSIX  = ' six , 6 '
kSEVEN = ' seven , 7 '
kEIGHT = ' eight , 8 '
kNINE = ' nine , 9 '
kTEN  = ' ten , 10 '
kELEVEN = ' eleven , 11 '
kTWELVE = ' twelve , 12 '
kTHIRTEEN = ' thirteen , 13 '
kFOURTEEN = ' fourteen, 14 '
kFIFTEEN = ' fifteen , 15 '
kSIXTEEN = ' sixteen, 16 '
kSEVENTEEN = ' seventeen , 17 '
kEIGHTEEN = ' eighteen , 18 '
kNINETEEN = ' nineteen , 19 '
kTWENTY = ' twenty # one|two|three|four|five|six|seven|eight|nine, 20 '
kTWENTYONE = ' twenty one , 21 '
kTWENTYTWO = ' twenty two , 22 '
kTWENTYTHREE = ' twenty three , 23 '
kTWENTYFOUR = ' twenty four , 24 '
kTWENTYFIVE = ' twenty five , 25 '
kTWENTYSIX = ' twenty six , 26 '
kTWENTYSEVEN = ' twenty seven , 27 '
kTWENTYEIGHT = ' twenty eight , 28 '
kTWENTYNINE = ' twenty nine , 29 '
kTHIRTY = ' thirty # one|two, 30 '
kTHIRTYONE = ' thirty one , 31 '
kTHIRTYTWO = ' thirty two , 32 '

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

def getValue( kname ):
    return int(kname)
    
