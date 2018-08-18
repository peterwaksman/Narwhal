
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

def GenAttributeRead( segment, tree, tokens, id, mod, MODS):
    OBJ = MouthIDvar[ id ]
    MODv = MouthMODvars[mod]
    nar = attribute( OBJ, MODv)
    reader = NWTopicReader("genAttribReader", tree, nar)

    reader.readSegment( segment, tokens)
    Vault = reader.getVault()

    R = []
    for V in Vault:
        t = Thing( V.lastConst )
        v = Value( V.lastConst )
        record = ContextRecord(id, MODS)
        record.details[mod][0] = v
        record.details[mod][1] = HARDDETAIL     
        R.append(record)
    return R
 
    x = 2


def ToothNumberRead( segment, tree, tokens, id, mod, MODS):
    getToothNumber = attribute([TOOTH],  INTx)
    reader = NWTopicReader("toothNumberReader", tree, getToothNumber)
    reader.readSegment( segment, tokens)

    L = len( reader.eventrecord)
    if L==0 or reader.GOF<0.66:
        return [ ContextRecord(id, MODS) ] # empty record

    R = []
    for event in reader.eventrecord:
        t = Thing( event[1] )
        v = Value( event[1] )
        record = ContextRecord(id, MODS)
        record.details[mod][0] = v
        record.details[mod][1] = HARDDETAIL     
        R.append(record)
    return R
        
def MarginDepthRead( segment, tree, tokens, id, mod, MODS):
    marginDepth =  relation( [MDFLv], REF_FEATUREv, RELATION, [RELAMOUNT])
    reader = NWTopicReader("marginDepthReader", tree, marginDepth)
    reader.readSegment( segment, tokens)
    L = len(reader.eventrecord)
    if L==0 :
        return [ ContextRecord(id, MODS) ] # empty record
     
    # note: you could also use reader.reader.vault entries
    # but it is not needed for NARs of order 1, like relation()
    R = []
    for event in reader.eventrecord:
        t = Thing( event[1] )
        a = Action( event[1] )
        r = Relation( event[1] )
        v = Value( event[1] )
        record = ContextRecord(id, MODS)

        if t:
            record.details[MDFL][0] = t
            record.details[MDFL][1] = HARDDETAIL     
        if a:
            record.details[MARGIN_DEPTH][0] = a
            record.details[MARGIN_DEPTH][1] = HARDDETAIL
        if r:
            record.details[REF_RELATION][0] = r
            record.details[REF_RELATION][1] = HARDDETAIL
        if v:
            record.details[REF_FEATURE][0] = v
            record.details[REF_FEATURE][1] = HARDDETAIL   
                     
        R.append(record)
  
    return R

# lookup mod handler from its
MouthHandlers = {
    ORDER_LATER         : GenAttributeRead,
    MDFL                : nullRel,
    OCCL                : nullRel,

    REF_FEATURE         : nullRel,  
    REF_RELATION        : nullRel,  
    REF_AMOUNT          : nullRel, 
    MARGIN_DEPTH        : MarginDepthRead,
 
    SITE_TOOTHNUM       : ToothNumberRead,
    SITE_TOOTHTYPE      : nullRel,
    SITE_TOOTHGROUP     : nullRel,

    ABUTMENT_MATERIAL   : GenAttributeRead,
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
    CROWN_TYPE          : GenAttributeRead,
    CROWN_RETENTION     : nullRel,
    }
 
