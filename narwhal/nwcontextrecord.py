
""" 
Context Record is going to be another tree structure

"""
# Detail status
EMPTYDETAIL=0 # never written or copied 
SOFTDETAIL=1  # when copied to programmatically, as an assumption
HARDDETAIL=2  # when written to, because of the incoming text

def strStatus(status):
    if status==EMPTYDETAIL:
        return 'E'
    elif status==SOFTDETAIL:
        return 'S'
    else:
        return 'H'


class ContextRecord():
    def __init__(self, id = '', contextMods = []):
        self.id = id

        self.block = False # could call this anything

        # details are indexed by mods of the context
        self.details = {}
        for m in contextMods:
            self.details[ m ] = ['' , EMPTYDETAIL]

        self.children = []

 
    def str(self, ntabs=0):
        pre = ''
        for i in range(0,ntabs):
            pre += "\t"

        out = pre

        if self.block:        
            out += "~" 
                        # id
        out += self.id + ":"

                        # details (mod values)
        M = self.details
        
        out += '('
        for mod in M:
            out += '['
            out +=  M[mod][0] + ',' + strStatus(M[mod][1])
            out += "]"

            if mod<len(M)-1:
                out += ','
            
        out += ')\n'

        for c in self.children:
            out += c.str(ntabs+1) #+ '\n' # use record.str()
            if False and c != self.children[ len(self.children)-1 ]:
                out += '\n'
        return out 
 

    def merge(self, other, applyBlock=False):
        if self.id!=other.id:
            print("OOPS!")
            return

        temp = ContextRecord(self.id )

        # unless applying the block to self, test compatibility
        if (not applyBlock) and (other.block != self.block):
            return False
          
        for mod in other.details:
            temp.details[mod] = self.details[mod][:]

            val    = temp.details[mod][0]
            status = temp.details[mod][1]
            oval   = other.details[mod][0]
            ostatus= other.details[mod][1]        

            if status==HARDDETAIL: 
                if val != oval and oval:
                #if val != oval: # cannot change a hard detail
                    return False
                else:
                    continue
            # now status is SOFT or EMPTY
            elif ostatus==SOFTDETAIL or ostatus==HARDDETAIL:
                temp.details[mod][0] = oval  # can overwrite  
                temp.details[mod][1] = ostatus
       
        for d in temp.details:
            self.details[d] = temp.details[d][:] # children and id are unchanged.
            #self.details[d][1] = temp.details[d][1] # children and id are unchanged.
            x = 2

        if applyBlock:
            self.block = other.block
        return True

    def copyDetails( self, other):
        if self.id!=other.id:
            print("OOPS!")
            return
        for d in other.details:
            self.details[d] = other.details[d][:]
            x = 2

    def copy(self, makesoft=False):
        other = ContextRecord( self.id)
        #other.block = self.block
        other.details = {}
        for d in self.details:
            detail = self.details[ d ][:]    # copy the list
            if makesoft and detail[1]==HARDDETAIL:
                detail[1] = SOFTDETAIL      # soften
            other.details[d] = detail[:]     # store here
        return other

    def harden( self ):
        for d in self.details:
            if self.details[d][0]: # the mod has a value
                self.details[d][1] = HARDDETAIL

        for child in self.children:
            child.harden() 

 
# used as a placeholder for RELS handlers
def nullRel():
    return None



                     
                