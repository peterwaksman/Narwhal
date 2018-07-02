
from narwhal.nwtypes import *
from narwhal.nwchat import *

from stdtrees.geometry import *

from mouthCONSTS import *
from mouthVARS import *

def nullRel():
    return None



class LaterOrderReader( NWTopicReader ):
    lateOnar = attribute( ORDERv, ORDER_LATERv )
    def __init__(self, treeroot):
        NWTopicReader.__init__(self, "lateOreader", treeroot, lateOnar)
         
def LaterOrderRead( segment, tree, tokens ):
    reader = LaterOrderReader( tree )
    reader.readSegment( segment, tokens)


# lookup mod handler from its
MouthHandlers = {
    ORDER_LATER         : LaterOrderRead,
    MDFL                : nullRel,
    OCCL                : nullRel,
    REF_FEATURE         : nullRel,
    REF_RELATION        : nullRel, 
    REF_AMOUNT          : nullRel, 
 
    SITE_TOOTHNUM       : nullRel,
    SITE_TOOTHTYPE      : nullRel,
    SITE_TOOTHGROUP     : nullRel,

    ABUTMENT_MATERIAL   : nullRel,
    ABUTMENT_TYPE       : nullRel,
    ABUTMENT_RETENTION  : nullRel, 
    CORE_TILT           : nullRel, 
    CORE_THICKNESS      : nullRel,
    CORE_TAPER          : nullRel,
    CORE_CLEARANCE      : nullRel,
    CORE_MATCH          : nullRel,

    BASE_PRESSURE       : nullRel,
 
    EPS_TYPE            : nullRel,

    CROWN_MATERIAL      : nullRel,
    CROWN_TYPE          : nullRel,
    CROWN_RETENTION     : nullRel,
    }
 