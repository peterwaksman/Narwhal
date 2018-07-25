
from narwhal.nwtypes import *
from narwhal.nwchat import *
from narwhal.nwcontextrecord import *

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

This file begins with handler definitions, which are put in a table at the end
    
"""

# this hard codes the object (OBJ) and attribute (MOD) dictionaries

def GenAttributeRead( segment, tree, tokens, record, mod):
    OBJ = MouthIDvar[ record.id ]
    MOD = MouthMODvars[mod]
    nar = attribute( OBJ, MOD)
    reader = NWTopicReader("genAttribReader", tree, nar)
    reader.readSegment( segment, tokens)
    L = len( reader.eventrecord)
    if L>0 and reader.eventGOF==1:
        event = reader.eventrecord[L-1]
        t = Thing( event[1] )
        v = Value( event[1] )
        record.details[mod][0] = v
        record.details[mod][1] = HARDDETAIL           

    x = 2


def ToothNumberRead( segment, tree, tokens, record, mod):
    getToothNumber = attribute([TOOTH],  INTx)
    reader = NWTopicReader("toothNumberReader", tree, getToothNumber)
    reader.readSegment( segment, tokens)

    L = len( reader.eventrecord)
    if L==0 or reader.GOF<0.66:
        return

    event = reader.eventrecord[L-1]
    t = Thing( event[1] )
    v = Value( event[1] )
    record.details[mod][0] = v
    record.details[mod][1] = HARDDETAIL           





# lookup mod handler from its
MouthHandlers = {
    ORDER_LATER         : GenAttributeRead,
    MDFL                : nullRel,
    OCCL                : nullRel,
    REF_FEATURE         : nullRel,
    REF_RELATION        : nullRel, 
    REF_AMOUNT          : nullRel, 
 
    SITE_TOOTHNUM       : ToothNumberRead,
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
 
    EPS_TYPE            : GenAttributeRead,

    CROWN_MATERIAL      : nullRel,
    CROWN_TYPE          : nullRel,
    CROWN_RETENTION     : nullRel,
    }
 
