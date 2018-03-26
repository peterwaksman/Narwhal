"""
nwfind.py implements matching keywords to tokens in a window of text.

THE FOLLOWING DOCUMENTS HOW TO BUILD A TREE. NOTE VERY SPECIAL CAUTION
IS NEEDED WITH SPACES BEFORE AND AFTER SYNONYMS IN A KEYWORD LIST.

A KList uses a comma separate string of synonyms. Thus if 'abc' occurs
in the list it will match "abc" in the text. For example 'tee' matches
"teeth" or "tee". But ' tee' only matches "tee" but could match "stee". 
Thus unless you want to deliberately take advantage of this ambiguity,
put spaces around your synonyms. I use ' par' for all the versions of
"parallel" and ' opp' for versions of "opposing".

Matching keywords from a KList also uses special symbols to help disambiguate, 
in terms of what comes before or after the match in the text.  
 
Thus an entry like this from a KList:
    abc # X
means text with "abc X" will not match. Hence abc followed by X is excluded.
 
Similarly, this notation excludes being preceded by X:
    X $ abc
means text with "X abc" will not be matched by that item from the KList.
 
In both those cases, "abc" matches otheries, if not followed by "X".

EG "tooth numbers" might be a pattern you want to match, separately from "tooth" or 
"numbers" occurring alone. Those patterns are 
tooth numbers    - to match "tooth numbers"
tooth # numbers  - to match "tooth" alone
tooth $ numbers  - to match "numbers" alone
 
In this context we also use the '|' character as an "or", so that an entry
like the following excludes several things at once:
    abc # X|Y|Z
So text with any of X, Y, or Z after abc will not be a match for this
item of the KList. You can use '|'  with the '$' and can put as many
un-quoted substrings in the exlusion as you like.
[NOTE: this is a different use of the'|' character than when or'ing VARs]
 
Also you are supposed to ignore wildcards so
    abc * def
means match by searcing forward from abc allowing one word in between
[could be more complicated] before def.
 
By the way, space before or after a keyword, means its ending (at the space)
must match the ending of the token. Without the space, different beginnings
or endings are allowed in matching a substring of the token.

Obviously it could all be greatly improved if keywords implemented regular expressions
and matchTOK() knew how to handle it. What is important for Narhwal is to keep track
of the place in the text where the match occurs. Each pattern must be centered on a
particular token index 'itok'.
"""

from narwhal.nwutils import *

#useful sometimes, eg for printouts
def TOKS(text):
    tokens = text.split(' ')
    return tokens

    # T = numTokens. It is assume ifound is list of indices from
    # in [0, T)


#related to int unknowns
def asInt(token):
    """ true if token is digits, optionally preceeded with a '+' or '-' """
    if len(token)<1 :
        return ''
    if token[0]=='-' or token[0]=='+':
        tmp = token[1:]
        if tmp.isdigit():
            if token[0] == '-':
                return token # preserve the minus
            else:
                return tmp   # strip off the plus
        return ''
    elif token.isdigit():
        return token
    else:
        return ''

# assume utoken has no sign prefix
def isdigitFL(token):
    pcount = 0 #count periods
    for i in range( len(token) ) :
        if token[i]=='.':
            pcount += 1
        elif not token[i].isdigit():
            return False
    if pcount==1:
        return True
    else:
        return False


def asFloat(token):
        """ Same as asInt() except we allow one decimal before the
        last digit """
        if len(token)<1 :
            return ''
        if token[0]=='-' or token[0]=='+':
            tmp = token[1:]
            if isdigitFL(tmp):
                if token[0] == '-':#if it begins with a minus
                    return token   # preserve the minus  
                else:
                    return tmp     # strip off the plus
        elif isdigitFL(token):
            return token
        else:
            return ''

def kwordLen(kword):
    if len(kword) < 1:
        return 0

    kpart = kword.split("#")
    if len(kpart) > 1:
        return 1

    kpart = kword.split('*')
    if len(kpart) > 1:
        return 2
    return 1



def matchTOK(kword, itok, ifound, tokens):
    """
    Args: the space-tokenized text into the method, along with the index of one token
    The keyword is an item from a KList's self.list (or a substring)
    Per above, the keyword can encode alternatives

    here we match an entry from a keyword list to a space-delimeted token
    after putting the space back into the token

    I have convinced myself that the use of indexed arrays of tokens is helpful
    when text matching involves not just one token but the other tokens on either
    side. The client is also interested in which indices are involved as they
    will want to know the number of words between matches. So itok is useful
    """
    if itok > len(tokens) - 1:
        return False

    if len(kword) < 1:
        return False

    # look for complex kwords
    kpart = kword.split('#')
    if len(kpart) > 1:
        return matchWordToToken_pound(kpart, itok, ifound, tokens)

    kpart = kword.split('*')
    if len(kpart) > 1:
        return matchWordToToken_star(kpart, itok, ifound, tokens)

    kpart = kword.split('$')
    if len(kpart) > 1:
        return matchWordToToken_dollar(kpart, itok, ifound, tokens)

    # -------------SPACES ARE HARD
    # First, there is a tendency to create '' entries.
    # Next, mult-part tokens should not start or end with space(s).
    # they get stripped away here. You must RE-PAD the
    # subparts of the keyword, or else they are falsely detected inside
    # of non-matching words, like "each" inside "reached".
    prekpart = kword.split(' ')
    kpart = []
    for part in prekpart:
        if len(part) > 0:
            kpart.append(part)

    if len(kpart) > 1:  # multi-part token, using spaces
        tmp = []
        dtok = 0  # to count forward from itok
        for part in kpart:
            j = ' ' + part + ' '  # RE-PAD
            if not matchTOK(j, itok + dtok, tmp, tokens):
                break
            dtok += 1

        if dtok < len(kpart):  # break occurred before end of loop
            return False
        else:
            ifound.extend(tmp)
            return True

    # Or len(kpart)==1
    # We revert to original kword that could have spaces at start or end
    # (just for readability, not used below).

    # MAIN TOKEN MATCH
    # tokens[i] cannot include spaces, since they were split from text
    # using ' '. But keywords can, so pad tok to allow this matching. No
    # harm if the keyword starts/ends without space, this allows
    # matching to words with ' ' terminations. We also allow the token
    # to be preceded by a comma or a period, in case someone is
    # parsing larger units than sentences. It should be up to them to
    # eliminate punctuation before this.
    tok = " " + tokens[itok] + " "
    if tok.find(kword) >= 0:
        ifound.append(itok)
        # print( "APPEND to ifound with itok="+str(itok)+" and kword="+kword")
        return True

    tok = "," + tokens[itok] + " "  # for token glued to a comma
    if tok.find(kword) >= 0:
        ifound.append(itok)
        return True

    tok = "." + tokens[itok] + " "   # for token glued to a period
    if tok.find(kword) >= 0:
        ifound.append(itok)
        return True

    return False

# if this gives a match, it consumes one token


def matchWordToToken_pound(kpart, itok, ifound, tokens):
    if len(kpart) != 2:
        return False

    # for |-separated exclusions
    word = kpart[0]

    exclude = kpart[1].split('|')  # list of words to exclude
    for exc in exclude:
        tmp = []
        if matchTOK(exc, itok + 1, tmp, tokens):  # no change to ifound
            return False

    return matchTOK(kpart[0], itok, ifound, tokens)

# if this gives a match, it consumes one token


def matchWordToToken_dollar(kpart, itok, ifound, tokens):
    if len(kpart) != 2:
        return False

    if itok == 0:
        return matchTOK(kpart[1], itok, ifound, tokens)

    # prev = tokens[itok-1]
    exclude = kpart[0].split('|')  # list of words to exclude
    for exc in exclude:
        tmp = []
        if matchTOK(exc, itok - 1, tmp, tokens):  # no change to ifound
            return False

    return matchTOK(kpart[1], itok, ifound, tokens)

# this may consume 2 tokens


def matchWordToToken_star(kpart, itok, ifound, tokens):
    if len(kpart) != 2:
        return False

    tmp = ifound

    a = matchTOK(kpart[0], itok, tmp, tokens)
    b = matchTOK(kpart[1], itok + 2, tmp, tokens)
    c = matchTOK(kpart[1], itok + 3, tmp, tokens)

    if a and b:
        ifound = tmp
        return True
    elif a and c:
        ifound = tmp
        return True
    else:
        return False


# ------------------------------------------------

def findInText(klist, tokens, rawtokens, itok, ifound):
    ret = ''
    tok = tokens[itok]
    for kword in klist.list:
        h = kword[:8]
        if kword == ' __d__ ': # spaces for no particular reason
            a = asInt(tok)
            if len(a)>0 :
                ifound.append(itok)
            return a
        elif kword == ' __fl__ ':
            a = asFloat(tok)
            if len(a)>0:
                ifound.append(itok)
            return a
        elif kword[:8]=='__prfx__': #no spaces dammit!
            # NEEDS DEBUGGING
            m = kword[8:] # the body of the keyword IS the prefix
                          # match it to prefix of token
            if m==tok:
                ifound.append(itok)
                #return tok
                return rawtokens[itok]
            else:
                return '' # prevents finding by matchTOK below
        elif kword[:8]=='__sufx__':
            L = len(tokens)
            m = kword[8:] # the body of the keyword IS the suffix
                          # match it to suffix of token
            if m==tok or m==tok + ' ':
                ifound.append(itok)
                if itok < L-1:
                    ifound.append(itok+1)  
                    #return tokens[itok+1]   
                    return rawtokens[itok+1]
            elif itok<L-2:
                s = tok + " " + tokens[itok+1]
                if m==s or m==s+ ' ':
                    ifound.append(itok) 
                    ifound.append(itok+1) 
                    ifound.append(itok+2) 
                    #return tokens[itok+2]
                    return rawtokens[itok+2]
                else:
                    return ''     
            else:
                return ''           

        # look for this kword at itok position in tokens
        # and return with ifound storing itok and any
        # adjacent indices used during the matching
        if matchTOK(kword, itok, ifound, tokens):
            ret = tok
            x = 2
            # NOTE this return value is ignored on the client side
            # [No it isn't, it's length is used]
    return ret
###############################################################
###############################################################
