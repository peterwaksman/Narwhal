"""
nwfind.py implements matching keywords to tokens in a window of text.

Matching keywords from a KList uses special symbols to help disambiguate, 
in terms of what comes before or after the match in the text. This is 
primitive type of , built-in regular expression matching.
 
Thus an entry like this from a KList:
    abc # X
means text with "abc X" will not be matched by that item from the KList.
Hence abc followed by X is excluded.
 
Similarly, this notation excludes being preceded by X:
    X $ abc
means text with "X abc" will not be matched by that item from the KList
 
In both those cases, "abc", without the X, DOES match

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
NOTE: this is a different use of the'|' character than when or'ing VARs
 
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
def findInText(klist, tokens, itok, ifound):
    ret = ''
    for kword in klist.list:
        if kword == ' __d__ ':
            a = asInt(tokens[itok])
            if len(a)>0 :
                ifound.append(itok)
            return a
        elif kword == ' __fl__ ':
            a = asFloat(tokens[itok])
            if len(a)>0:
                ifound.append(itok)
            return a
        # look for this kword at itok position in tokens
        # and return with ifound storing itok and any
        # adjacent indices used during the matching
        if matchTOK(kword, itok, ifound, tokens):
            ret = tokens[itok]
            x = 2
            # NOTE this return value is ignored on the client side
    return ret

###############################################################
###############################################################
