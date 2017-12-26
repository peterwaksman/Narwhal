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
kONE  = ' tooth|number|_hash_ $ one , tooth|number|_hash_ $ 1 ' #introduces a small bug, since 'a'  is also DULL
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

It is safe to say that I wouldn't need to define these "unknowns" if I 
had the time to name all the numbers I might encounter. :)
"""

kINT = " __d__ "
INTx = KList('int', kINT).var()
# See the connection to the asInt() method in nwutils.pw

kFLOAT = " __fl__ "
FLOATx = KList('float', kFLOAT).var()
# See the connection to the asFloat() method in nwutils.pw

"""
I realize that my handling of this is inconsistent. I cannot look 
look for a generic variable string. But I can allow prefix and 
suffix matching with the remainder generic and variable. Also, sadly, 
only lower case letters are handled.

To match things with a prefix, use something like this:
PARTNO = KList("STR_[YOUR LISTNAME HERE]", "__prfx__[YOUR PREFIX HERE]").var()
example:
P = KList("STR_parts","__prfx__ABC_.var()
matches anything of the form ABCxxxxxx and the whole token is returned from findInText()

Make sure to include STR_ as the beginning of the list name; and
__prfx__ as the beginning of the list entry. Your list can include more
than one entry.


Similarly, to match things with a suffix, use something like this:
PARTNO = KList("STR_[YOUR LISTNAME HERE]", "__sufx__[YOUR SUFFIX HERE]").var()

Usage is defined in this comment, and supported in:
       nwtypes.VAR.isUnknown() 
       nwfind.findInText() [not tested yet but let's be optimistic]

It would be good to implement a convention where, if the KList name begins with "REGEX_"
and a kword in its list begins with __regex__ then what follows is a regular expression to be matched.
So the entries of the VARs klist are regular expressions. The isUnknown() could
check for "REGEX_" in the list name and the findInText() could do a regular expression 
match when it detects __regex__ at the  beginning of a kword. 
So KList("REGEX_[your listname]","__regex__*").var() will match anything. 

"""


#------------------
UNITS= KList("unittype","").var()
MM = KList( "mm", "mm, mn, millimeter").var()
IN = KList( "in"," in , inch").var() # god forbid!
DEGREE= KList( "degree","deg, degree").var()
UNITS.sub(MM)
UNITS.sub(IN)
UNITS.sub(DEGREE)

##################### PUT TOGETHER FOR EXTERNAL SIMPLICITY
GEN_QUANTITY = KList("allquantities", "").var()
GEN_QUANTITY.sub(QUANTITY)
GEN_QUANTITY.sub(TOOTH)
GEN_QUANTITY.sub(INTx)
GEN_QUANTITY.sub(FLOATx)
GEN_QUANTITY.sub(UNITS)
