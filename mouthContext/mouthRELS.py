
from narwhal.nwtypes import *
from narwhal.nwchat import *
from narwhal.nwcontext import nullRel

from stdtrees.geometry import *

from mouthVARS import *


""" 
MouthHandlers are loaded into the entries of the MouthDict during
construction of the ContextManager. The reason for delayed load
is to avoid circular dependencies with mouthVARS while keeping these
handlers in their own file.

Need a temp tree made from ContextManager.tree and (id,mod) tree in MODvars 
caution: read() should either work with a copy of self.tree, or should not
clear the tree in PrepareSegment   
    
"""


class LaterOrderReader( NWTopicReader ):
    def __init__(self, treeroot):
        LOnar = attribute( ORDERv, ORDER_LATERv )
        NWTopicReader.__init__(self, "lateOreader", treeroot, LOnar)
         
def LaterOrderRead( segment, tree, tokens ):
    reader = LaterOrderReader( tree )
    reader.readSegment( segment, tokens)
    x = 2


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
 