/*
 * Copyright 2013, DENTSPLY Implants, All Rights Reserved.
 * This file contains proprietary information, and may not be viewed, copied,
 * distributed, sold, published, or disseminated without express permission
 * of DENTSPLY Implants.
 */

#pragma warning(disable: 4786)

#include <Utils/common.h> // for ToLower()
#include <Utils/Config.h>

#include <boost/timer.hpp>
#include <boost/algorithm/string/trim.hpp>


#include "Notes.h"


#ifdef _DEBUG
#define new DEBUG_NORMALBLOCK
#endif

using namespace std;

namespace AC {

void clearTokensUsed(std::vector<bool> & tokensUsed)
{
  for(size_t i=0; i<tokensUsed.size(); i++)
    tokensUsed[i] = false;
}

void initTokensUsed(const std::vector<string> & tokens, std::vector<bool> & tokensUsed)
{
  tokensUsed.clear();
  for(size_t i=0; i<tokens.size(); i++)
    tokensUsed.push_back(false);

}

void updateTokensUsed(const std::vector<bool> & src_token_used, std::vector<bool> & dest_token_used)
{
  if( src_token_used.size()!=dest_token_used.size() )
    return;

  for(size_t i=0; i<src_token_used.size(); i++)
    if( src_token_used[i]==true )
      dest_token_used[i] = true;
}

int firstIndexUsed( const std::vector<bool> & token_used, int & numUsed )
{
  numUsed = 0;
  int ret = -1;

  for(size_t i=0; i<token_used.size(); i++)
  {
    if( token_used[i]==true )
    {
      numUsed++;     // count occurances

      if( ret==-1 )  // catch first occurance
        ret = (int)i;
    }
  }
  return ret;
}

int lastIndexUsed( const std::vector<bool> & token_used, int & numUsed )
{
  numUsed = 0;
  int ret = -1;

  for(size_t i=0; i<token_used.size(); i++)
  {
    if( token_used[i]==true )
    {
      numUsed++;     // count occurances
      ret = (int)i;
    }
  }
  return ret;
}



// return enum value if found or -1;
int findWordInTokens( const string & word, const std::vector<string> & tokens, size_t istartTok=0)
{
  size_t found;

  for(size_t i=istartTok; i<tokens.size(); i++)
  {
    string tokenA = tokens[i];
    ToLower( tokenA );
    string tokenL = " " + tokenA + " ";

    found = tokenL.find(word);
//    if( found!=string::npos )
    if( found<2 && found!=string::npos )// can I do that and not break everything?
      return (int)i;
  }  
  return -1;
}

int findWordsInTokens( const std::vector<string> & subwords, const std::vector<string> & tokens, int istartTok=0 )
{
  size_t found;
  size_t N=subwords.size();
  size_t goodcount;
  for(size_t i=istartTok; i<tokens.size(); i++)
  {
    if( i+N>tokens.size() )
      break;

    goodcount = 0;
    for(int j=(int)i; j<(int)(i+N); j++)
    {
      string tokenL = tokens[j];
      ToLower( tokenL );
      found = tokenL.find( subwords[j-i] );
      if( found==string::npos )// mis-match
        continue;
      else if( goodcount<N )
        goodcount++;
      else
        break;
    }
    if( goodcount==N )
      return (int)i;

  }
  return -1;
}

double getValLeftOfMM( const std::vector<string> & tokens, std::vector<bool> & token_used, 
                       int imm , int istartTok=0)
{
  if( imm<0 || imm>(int)tokens.size()-1 || imm<istartTok)
    return NOVAL;


  double val = NOVAL;

  // look for val in same token as mm, eg ".2mm"
  if( 1==sscanf_s( tokens[ imm ].c_str() , "%lf", &val ) )
  {
    token_used[imm] = true;
  }
  else if( 0<imm && 1==sscanf_s( tokens[ imm-1 ].c_str() , "%lf", &val ) )
  {
    token_used[imm-1] = true;
  }

  return val;
}



int Dictionary::findMatchInTokens( const std::vector<string> & tokens, int & itok, int & itok2, int istartTok ) const
{
  std::vector<string> subword;
  size_t numsubs;

  itok = itok2 = -1;
  int iword = -1;
  for(unsigned int w=0; w<_numWords; w++)
  {
    string word = _words[w];

    subword.clear();
    numsubs = Tokenize(word, subword);

    if( numsubs==1 )
    {
      itok = findWordInTokens( word, tokens, istartTok);
      itok2 = itok;
      if( itok>=0 ) // found for some token
      {
        return w;
      }
    }
    else if( numsubs==2 )
    {
      itok = findWordsInTokens( subword, tokens, istartTok );
      if( itok>=0 )
      {
        itok2 = itok + 1;
        return w;
      }
    }
    else // dictionary can have two word entries but not 3 word entries (or use vector of itok)
    {
      return -1; 
    }
  }
  return -1;
}

size_t Dictionary::findInDictionary(const string & token) const
{
  for(size_t i=0; i<_numWords; i++)
  {
    if( token==_words[i] )
      return i;
  }
  return -1;
}
bool Dictionary::foundInDictionary(const std::vector<string> & tokens, std::vector<bool> & token_used )const
{
  int itok=-1,itok2=-1;
  int istartTok = 0;
  while( istartTok<(int)tokens.size() && findMatchInTokens(tokens, itok, itok2, istartTok)>=0 )
  {
    token_used[itok] = token_used[itok2] = true;
    istartTok = itok2+1; // will continue looking from here
    itok = itok2 = -1;
  }

  int numused=0;
  if( firstIndexUsed( token_used, numused )>=0 )
    return true;
  else
    return false;
}



static const string nullString="";
static const Dictionary NullDictionary( &nullString, 0);


//////////HEIGHT SPECIFIC////////////////////


/////////////SYNONYM DICTIONARIES FOR EACH enum and each val of enum
// need a synonym list for each enum value

MARGIN_REFERENCE Ref2Ref(const MHEIGHT_REF & ref )
{
  switch( ref )
  {
  case aMGINGIVA:
    return MGINGIVA;
    break;
  case aMINTERFACE:
    return MINTERFACE;
    break;
  case aMNEIGHBOR:
    return MNEIGHBOR;
    break;
  case aMLINE:
    return MLINE;
    break;
  case aMNOREF:
  default:
    return MNOREFSET;
    break;
  }

}

bool overlay( const MHEIGHT_REF & src, MHEIGHT_REF & dest )
{
  if( dest==aMNOREF || dest==src )
  {
    dest = src;
    return true;
  }
  return false;
}


//MGINGIVA
static const string GingivaD[]=
{
  "gingiva",  // variants: "gingival", "subgingival"
  "subginival",
  "tissue", 
  "gum",      // can be part of gumline
  "supra_g",
  "sub_g",
  "ridge",
  "gm crest"
};
const unsigned int NUM_GINGIVA_WORDS = sizeof( GingivaD ) / sizeof( string ) ;
const Dictionary GingivaDictionary( &GingivaD[0], NUM_GINGIVA_WORDS );


static const string InterfaceD[]=
{
  "interface",
  "fixture",
  "implant",
  "analog"
};
const unsigned int NUM_INTERFACE_WORDS = sizeof( InterfaceD ) / sizeof( string ) ;
const Dictionary InterfaceDictionary( &InterfaceD[0], NUM_INTERFACE_WORDS );

static const string NeighborD[]=
{
  "neighbor",
  "adjacent"
};
const unsigned int NUM_NEIGHBOR_WORDS  = sizeof( NeighborD ) / sizeof( string ) ;
const Dictionary NeighborDictionary( &NeighborD[0], NUM_NEIGHBOR_WORDS );


static const string LineD[]=
{
  "line",
  "mark"
};
const unsigned int NUM_LINE_WORDS = sizeof( LineD ) / sizeof( string ) ;
const Dictionary LineDictionary( &LineD[0], NUM_LINE_WORDS );


const Dictionary & getHeightREFDictionary( MHEIGHT_REF ref )
{
  switch( ref )
  {
  case aMGINGIVA:
    return GingivaDictionary;
    break;
  case aMINTERFACE:
    return InterfaceDictionary;
    break;
  case aMNEIGHBOR:
    return NeighborDictionary;
    break;
  case aMLINE:
    return LineDictionary;
    break;
  default:
    return NullDictionary;
    break;
  }
}



MARGIN_POSITION Rel2Pos(const MHEIGHT_REL & rel)
{
  switch( rel )
  {
  case aMAT:
    return MAT;
    break;
  case aMHI:
  case aMABOVE:
    return MABOVE;
    break;
  case aMLO:
  case aMBELOW:
    return MBELOW;
    break;
  case aMCLOSEST:
    return MCLOSEST;
    break;
  case aMNOREL:
  default:
    return MNOPOS;
    break;
  }
}

bool overlay( const MHEIGHT_REL & src, MHEIGHT_REL & dest )
{
  if( dest==aMNOREL || dest==src)
  {
    dest = src;
    return true;
  }
  return false;
}


static const string AtD[] = 
{
  " at",
  "flush",
  "even with",
  "match"
};
const unsigned int NUM_AT_WORDS = sizeof( AtD ) / sizeof( string ) ;
const Dictionary AtDictionary( &AtD[0], NUM_AT_WORDS );


static const string HiD[] = 
{
  " hi ",
  "high",
  "raise"
};
const unsigned int NUM_HI_WORDS = sizeof( HiD ) / sizeof( string ) ;
const Dictionary HiDictionary( &HiD[0], NUM_HI_WORDS );


static const string LoD[] = 
{
  " lo ",// note space, to avoid ambiguity with "below"
  " low",
  "deep",
  "lower",
  "drop"
};
const unsigned int NUM_LO_WORDS = sizeof( LoD ) / sizeof( string ) ;
const Dictionary LoDictionary( &LoD[0], NUM_LO_WORDS );

static const string AboveD[] = 
{
  "above",
  "supra",
  "supra_g",
  "super",
  "positive"
};
const unsigned int NUM_ABOVE_WORDS = sizeof( AboveD ) / sizeof( string ) ;
const Dictionary AboveDictionary( &AboveD[0], NUM_ABOVE_WORDS );

static const string BelowD[] = 
{
  "below",
  "sub",
  "sub_g",
  "subgingival",
  "subginival"
  "under",
  "depth"
};
const unsigned int NUM_BELOW_WORDS = sizeof( BelowD ) / sizeof( string ) ;
const Dictionary BelowDictionary( &BelowD[0], NUM_BELOW_WORDS );


static const string CloseD[] = 
{
  "close to",
  "close",
  "closest"
};
const unsigned int NUM_CLOSE_WORDS = sizeof( CloseD ) / sizeof( string ) ;
const Dictionary CloseDictionary( &CloseD[0], NUM_CLOSE_WORDS );


const Dictionary & getHeightRELDictionary( MHEIGHT_REL rel )
{
  switch( rel )
  {
  case aMAT:
    return AtDictionary;
    break;
  case aMHI:
    return HiDictionary;
    break;
  case aMLO:
    return LoDictionary;
    break;
  case aMABOVE:
    return AboveDictionary;
    break;
  case aMBELOW:
    return BelowDictionary;
    break;
  case aMCLOSEST:
    return CloseDictionary;
    break;
  default:
    return NullDictionary;
    break;
  }
}

////////////////////////////////


bool overlay( const M_AMT & src, M_AMT & dest )
{
  if( dest==aMNOAMT || dest==src )
  {
    dest = src;
    return true;
  }
  // but you cannot change it, for now
  return false;
}

static const string ValD[] = 
{
  "mm",
  "mn", // misspelling
  "millimeter"
};
const unsigned int NUM_VAL_WORDS = sizeof( ValD ) / sizeof( string ) ;
const Dictionary ValDictionary( &ValD[0], NUM_VAL_WORDS );



static const string JustD[] = 
{
  "just",
  "slightly",
  "may be"
};
const unsigned int NUM_JUST_WORDS = sizeof( JustD ) / sizeof( string ) ;
const Dictionary JustDictionary( &JustD[0], NUM_JUST_WORDS );


static const string AsPossibleD[] = 
{
  "as possible",
  "if possible",
  "as poss"
};
const unsigned int NUM_ASPOSSIBLE_WORDS = sizeof( AsPossibleD ) / sizeof( string ) ;
const Dictionary AsPossibleDictionary( &AsPossibleD[0], NUM_ASPOSSIBLE_WORDS );


const Dictionary & getAMTDictionary( M_AMT amt )
{
  switch( amt )
  {
  case aMVALUE:
    return ValDictionary;
    break;
  case aMJUST:
    return JustDictionary;
    break;
  case aMASPOSSIBLE:
    return AsPossibleDictionary;
    break;
  default:
    return NullDictionary;
    break;
  }
}
 
/////////////////////////////////////////////
bool overlay( const double & srcVal, double & destVal )
{
  // insert val if missing? maybe not
  if( destVal==NOVAL || fabs(destVal-srcVal)<0.0001 )
  {
    destVal = srcVal;
    return true;
  }
  return false;
}


////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////

// generic features named in margin statements
static const string MarginFD[] = 
{
  "margin height",
  "outline",
  "margin",
  "collar",
  "margins",
  "gingival",
  "gingiva",
  "tissue",
  "soft",
  "softtissue",
  "blanch",
  "blanching"
};
const unsigned int NUMMARGINFWORDS = sizeof( MarginFD ) / sizeof(string);
const Dictionary MarginFeatureDictionary( &MarginFD[0], NUMMARGINFWORDS );



bool overlay( const MWIDTH_OPTION & src, MWIDTH_OPTION & dest )
{
  if( dest==aMNOOPTION || dest==src )
  {
    dest = src;
    return true;
  }
  else
    return false;
}



// Each option can refer to a face. eg "no displacment on facial"

////////////////////////////////////////////////////////////
// there will be a dictionary for each of these. For example
static const string fadD[] = 
{
  "anatomical",
  "anatomic",
  "full"
};
const unsigned int NUMFADWORDS = sizeof( fadD ) / sizeof(string);
const Dictionary FullAnatDimD( &fadD[0], NUMFADWORDS );

static const string cstD[] = 
{
  "contour",
};
const unsigned int NUMCSTWORDS = sizeof( cstD ) / sizeof(string);
const Dictionary ContourSoftTissD( &cstD[0], NUMCSTWORDS );


static const string stD[] = 
{
  "support",
  "expand",
  "push",
  "tissue pressure",
  "blanch",
  "blanching"
};
const unsigned int NUMSTWORDS = sizeof( stD ) / sizeof(string);
const Dictionary SupportTissD( &stD[0], NUMSTWORDS );


static const string ntdD[] = 
{
  "displace",
  "displacement",
  "noimpingement",
  "impinge",
  "impingement"
};
const unsigned int NUMNTDWORDS = sizeof( ntdD ) / sizeof(string);
const Dictionary NoTissDiplaceD( &ntdD[0], NUMNTDWORDS );


bool overlay( const MFACE & src, MFACE & dest )
{
  if( dest==aMNOFACE || dest==src )
  {
    dest = src;
    return true;
  }
  return false;
}




static const string FaceD[] = 
{
"all sides"
"all around",
"360", //?
"circumferential",
"around",
"rest",    // as in "...the rest of the margins..."
"other",   // as in "...the other margins...."
"buccal",
"baccal",
"bucc",
"buc",
"buck",
"buccul",
"bucca", 
"bucall",
"B",
"baccal",
"lingual",
"ling",
"B/F",
"B&F",
"buccal/facial",
"f/b",
"b/f"
"facial",
"F",
"labial", // same as facial
"L",
"mesail",
"mesial",
"mes",
"M",
"distal",
"D",
"M/D",
"M&D",
"proximal",
"interproximal",
};
const unsigned int NUMMARGINFACEWORDS = sizeof( FaceD ) / sizeof( string ) ;



static const string AllFaceD[] =
{
"all sides",
"all around",
"360",  
"circumferential",
"around",
"all"
};
const unsigned int NUM_ALLFACE_WORDS = sizeof( AllFaceD ) / sizeof( string ) ;
const Dictionary AllFaceDictionary( &AllFaceD[0], NUM_ALLFACE_WORDS );


static const string OtherFaceD[] =
{
"other",
"rest",  
};
const unsigned int NUM_OTHERFACE_WORDS = sizeof( OtherFaceD ) / sizeof( string ) ;
const Dictionary OtherFaceDictionary( &OtherFaceD[0], NUM_OTHERFACE_WORDS );



static const string BuccalFaceD[] =
{
"baccal",
"buccal",
"bucc",
"buc",
"buck",
"buccul",
"baccal",
"bucca", 
"bucall",
" b ",
"b/f",
"b&f",
"buccal/facial",
"facial",
"labial",
"f/b",
"b/f"
};
const unsigned int NUM_BUCCALFACE_WORDS = sizeof( BuccalFaceD ) / sizeof( string ) ;
const Dictionary BuccalFaceDictionary( &BuccalFaceD[0], NUM_BUCCALFACE_WORDS );

static const string LingualFaceD[] =
{
"lingual",
"ling",
" l ",
"palatinal",
"palatal"
};
const unsigned int NUM_LINGUALFACE_WORDS = sizeof( LingualFaceD ) / sizeof( string ) ;
const Dictionary LingualFaceDictionary( &LingualFaceD[0], NUM_LINGUALFACE_WORDS );


static const string MesialFaceD[] = 
{
"mesail",
"mesial",
"mes",
" m ",
"m/d",
"m&d",
"proximal",
"interproximal",
};
const unsigned int NUM_MESIAL_WORDS = sizeof( MesialFaceD ) / sizeof( string ) ;
const Dictionary MesialFaceDictionary( &MesialFaceD[0], NUM_MESIAL_WORDS );


static const string DistalFaceD[] = 
{
"distal",
" d ",
"m/d",
"m&d",
"proximal",
"interproximal",
};
const unsigned int NUM_DISTAL_WORDS = sizeof( DistalFaceD ) / sizeof( string ) ;
const Dictionary DistalFaceDictionary( &DistalFaceD[0], NUM_DISTAL_WORDS );

// A bit mis-named. THese are phrases that indicate communications occurred separate from the note
// and from the order. So caution is advised.
bool hasWrittenSpec(const std::vector<string> & tokens, std::vector<bool> & token_used)
{
  //--------------------- look for written spec
  ConstantLabel perRx( "per rx", true );
  perRx.readTokens( tokens, token_used );
  ConstantLabel seeRx("see rx", false); // false means extra words are allowed between
  seeRx.readTokens(tokens, token_used );
  ConstantLabel seeWritten("see written", true);
  seeWritten.readTokens(tokens, token_used );
  ConstantLabel asRequested("as requested", true);
  asRequested.readTokens( tokens, token_used );
  ConstantLabel asNoted("as noted", true);
  asNoted.readTokens( tokens, token_used );
  ConstantLabel asnoted("asnoted", true);
  asnoted.readTokens( tokens, token_used );
  ConstantLabel wspec("written spec", true);
  wspec.readTokens( tokens, token_used );
  ConstantLabel rspec("written rx", true);
  rspec.readTokens( tokens, token_used );
  ConstantLabel rnotes("written notes", true);
  rnotes.readTokens( tokens, token_used );
  ConstantLabel rnote("written note", true);
  rnote.readTokens( tokens, token_used );

  ConstantLabel exdoc("ex doc", true);
  exdoc.readTokens(tokens, token_used );
  ConstantLabel extdoc("ext doc");
  extdoc.readTokens(tokens, token_used );

  ConstantLabel docs("docs", true); // too many variations, so let's be paranoid
  docs.readTokens(tokens, token_used );

  ConstantLabel cnote("customer note");
  cnote.readTokens(tokens, token_used );

  ConstantLabel specialInstruction1("special instruction");
  specialInstruction1.readTokens(tokens, token_used);

  ConstantLabel specialInstruction2("special instructions");
  specialInstruction2.readTokens(tokens, token_used);



  return(  rspec._found || wspec._found || perRx._found || seeRx._found 
        || seeWritten._found || asRequested._found || asNoted._found || asnoted._found 
        || rnotes._found || rnote._found 
        || exdoc._found || extdoc._found || docs._found 
        || cnote._found || specialInstruction1._found || specialInstruction2._found);
}


// the face info is "there" whether or not the values are "there"
MFACE getCombinedFaceInfo(const int & iB, const int & iL, const int & iM, const int & iD, const int & iA, const int & iO)
{
  bool b = iB>-1;
  bool l = iL>-1;
  bool m = iM>-1;
  bool d = iD>-1;
  bool a = iA>-1;
  bool o = iO>-1;

  //--- Nothing set. This is interpreted as "all"
  if( !b && !l && !m && !d && !a && !o )
    return aMALL;
  // or "all" was set
  if( !b && !l && !m && !d &&  a && !o )
    return aMALL;

  //--- Single values are set
  if( b && !l && !m && !d && !a && !o )
    return aMBUCCAL;
  if( !b && l && !m && !d && !a && !o )
    return aMLINGUAL;
  if( !b && !l && m && !d && !a && !o )
    return aMMESIAL;
  if( !b && !l && !m && d && !a && !o )
    return aMDISTAL;

  if( !b && !l && !m && !d && !a && o ) // "other" is not handled for now
    return aMNOFACE; // ERROR FOR NOW

  //--- Two are specified
  if( !b && !l && m && d && !a && !o )
    return aMM_D; // returns "mesial/distal", equivalent to "interproximal"

  return aMNOFACE;
}


MFACE getFace(const std::vector<string> & tokens, std::vector<bool> & token_used, bool hasMarginFeature=true)
{
  std::vector<bool> token_usedLing;
  initTokensUsed(tokens,token_usedLing);
  std::vector<bool> token_usedBucc ;
  initTokensUsed(tokens,token_usedBucc);
  std::vector<bool> token_usedMesi ;
  initTokensUsed(tokens,token_usedMesi);
  std::vector<bool> token_usedDist ;
  initTokensUsed(tokens,token_usedDist);
  std::vector<bool> token_usedAll  ;
  initTokensUsed(tokens,token_usedAll);
  std::vector<bool> token_usedOther;
  initTokensUsed(tokens,token_usedOther);

  bool hasBuccal  = BuccalFaceDictionary.foundInDictionary(tokens,  token_usedBucc );
  bool hasLingual = LingualFaceDictionary.foundInDictionary(tokens, token_usedLing );
  bool hasMesial  = MesialFaceDictionary.foundInDictionary(tokens,  token_usedMesi );
  bool hasDistal  = DistalFaceDictionary.foundInDictionary(tokens, token_usedDist );
  bool hasAll     = AllFaceDictionary.foundInDictionary(tokens, token_usedAll );
  bool hasOther   = OtherFaceDictionary.foundInDictionary(tokens, token_usedOther );

    //special case
  ConstantLabel allTheWay("all the way around");
  allTheWay.readTokens(tokens, token_usedAll );


  updateTokensUsed(token_usedBucc, token_used);
  updateTokensUsed(token_usedLing, token_used);
  updateTokensUsed(token_usedMesi, token_used);
  updateTokensUsed(token_usedDist, token_used);
  updateTokensUsed(token_usedAll, token_used);
  updateTokensUsed(token_usedOther, token_used);
 


  int numB=0, numL=0, numM=0, numD=0, numA=0, numO=0;
  // these are -1 if no index was used
  int iB = firstIndexUsed(token_usedBucc, numB);
  int iL = firstIndexUsed(token_usedLing, numL);
  int iM = firstIndexUsed(token_usedMesi, numM);
  int iD = firstIndexUsed(token_usedDist, numD);
  int iA = firstIndexUsed(token_usedAll, numA);
  int iO = firstIndexUsed(token_usedOther, numO);

  if( !hasMarginFeature && (iB==-1 && iL==-1 && iM==-1 && iD==-1 && iA==-1 && iO==-1) )
    return aMNOFACE;
  else
    return getCombinedFaceInfo(iB, iL, iM, iD, iA, iO);
}



///////////////////////////////////////
///MARGIN HEIGHT
double getValTwixtDull(const std::vector<string> & tokens, std::vector<bool> & token_used)
{
  if( token_used.size()<3 )
    return NOVAL;

  double val=NOVAL;
  size_t i;
  for(i=0; i<token_used.size(); i++)
  {
    string tok = tokens[i];

    if( sscanf_s(tok.c_str(), "%lf", &val )>0 )
      break;

  }

  if( i==tokens.size()-1 || i==tokens.size() )
    return NOVAL;
  else if( i>0 ) //so i is not a start/end index
  {
    if( token_used[i-1] && (token_used[i+1] || tokens[i+1]=="|" ) )
    {
      token_used[i] = true;
      return val;
    }
  }
 

  return NOVAL; 

}



void MarginHeightSpec::readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used, int istartTok )
{
  int itok=-1, itok2=-1;
  int iref=-1, irel=-1; // become indices of first occurance of ref or rel

//  clear(); // in case you forgot

  // for each type of enum MHEIGHT_REF, _REL, and _AMT
  // for each value of enum
  // get its dictionary and loop through all its words

  _ref = aMNOREF;
  for( unsigned int ref=0; ref<NUM_MHEIGHT_REFS; ref++)
  {
    const Dictionary & dict = getHeightREFDictionary( (MHEIGHT_REF)ref );

    if( dict.findMatchInTokens(tokens,itok, itok2, istartTok)>=0 ) // found a word (index is return value)
    {
      _ref = (MHEIGHT_REF)ref;
      iref = itok;
      token_used[itok] = true;
      token_used[itok2] = true;
      break;
    }
  }

  int iPrevInfo = iref;
  int iMinPrev = iPrevInfo;

  _rel = aMNOREL;
  for( unsigned int rel=0; rel<NUM_MHEIGHT_RELS; rel++)
  {
    const Dictionary & dict = getHeightRELDictionary( (MHEIGHT_REL)rel);

    if( dict.findMatchInTokens(tokens,itok, itok2, istartTok)>=0 )
    {
      if( iref>=0 )
      {
         if( itok > iPrevInfo+2 || itok2 < iPrevInfo-3 )// relation has to be near the ref(erence)
          continue;
      }

      _rel = (MHEIGHT_REL)rel;
      irel = itok;
      token_used[itok] = true;
      token_used[itok2] = true;
      break;
    }
  }

  iPrevInfo = __max(irel, iref); // reading tokens in and about here.
  iMinPrev = __min(iMinPrev, iPrevInfo);

  _face = getFace(tokens, token_used, _hasMarginFeature);

  int numUsed, tmp;
  tmp = lastIndexUsed(token_used, numUsed);
  if( tmp>iPrevInfo )
    iPrevInfo = tmp;

  iMinPrev = __min(iMinPrev, iPrevInfo);

  _amt = aMNOAMT;
  for( unsigned int amt=0; amt<NUM_M_AMTS; amt++)
  {
    const Dictionary & dict = getAMTDictionary( (M_AMT)amt);

    if( dict.findMatchInTokens(tokens,itok, itok2, istartTok)>=0 )
    {
      if( iPrevInfo>=0 ) // have seen a ref or a rel already
      {
        if( itok > iPrevInfo+3 || itok < iMinPrev-2 )// amount qualifier has to be near previous info
  //      if( itok > iPrevInfo+3 || itok < iPrevInfo-2 )// amount qualifier has to be near previous info
          continue;
      }

      _amt = (M_AMT)amt;
      token_used[itok] = true; // it may not be all of the token
      token_used[itok2] = true;

      if( _amt==aMVALUE )
      {
        _value = getValLeftOfMM( tokens, token_used, itok, istartTok );// may use token[itok-1]
        istartTok = itok+1;

        // sometimes user tosses in an extra "as possible". Do a quick check to mark tokens used
        ConstantLabel asPossible("as possible"); 
        asPossible.readTokens(tokens, token_used );
        ConstantLabel asClose("as close");
        asClose.readTokens(tokens, token_used);

      }
      break;
    }
  }
  if( _amt==aMNOAMT && iref>1 )
  {
    itok = iref-1;
    _value = getValLeftOfMM( tokens, token_used, itok, istartTok );// may use token[itok-1]
    if( _value>NOVAL )
    {
      _amt = aMVALUE;
      token_used[iref-1] = true;
    }
  }

  _hasWrittenSpec = hasWrittenSpec(tokens, token_used  );

  // implicit reference
  if( _amt==aMASPOSSIBLE && _ref==aMNOREF )
  {
    if( _rel==aMLO || _rel==aMBELOW )
    {
      _ref = aMINTERFACE;
      _rel = aMCLOSEST;
    }
    if( _rel==aMHI || _rel==aMABOVE )
    {
      _ref = aMGINGIVA;
    }
  }

  // height statements for occlusal clearance can look like implicit gingiva statements (NOT!)
  // SO HERE WE LOOK TO MAKE SURE IT IS NOT A CLEARANCE STATEMENT.
  vector<unsigned int> indexUsed;
  string clrS, occS;
  unsigned int nfields = semscanf( tokens, indexUsed, "%clearance %occlusal", &clrS, &occS );

  // implicit references are risky. This is where you do or don't take a risk.
  if( _rel!=aMNOREL && _rel!=aMAT )
  {
    if( occS!="" )
    {
      clear();
      return;
    }
    if( _ref==aMNOREF )
      _ref = aMGINGIVA; // implicit
  }

  if( _ref==aMGINGIVA && (_rel==aMABOVE || _rel==aMBELOW) && _amt==aMNOAMT && _value<0 )
  {
    double val = getValTwixtDull(tokens, token_used);
    if( 0<=val && val<=2.5 )
    {
      _value = val;
      _amt = aMVALUE;
    }
  }
}

bool MarginHeightSpec::isComplete(bool hasMarginFeature) 
{
  //get rigid for now
  if( !hasMarginFeature && (_ref==aMNOREF || _rel==aMNOREL || _amt==aMNOAMT || _face==aMNOFACE) )
    return false;

  // no reference but it is a margin statement
  if( hasMarginFeature && _ref==aMNOREF )
  {
    if( _amt==aMJUST || _amt==aMASPOSSIBLE )
    {
      _ref;
    }
  }

/*KILL THE REST?*/

  ///////////clean up some implicit cases
  if( _ref==aMNOREF ) // sometimes the reference is implicit
  {
    if( _rel!=aMNOREL && _amt!=aMNOAMT )
      _ref = aMGINGIVA;

    if( (_rel==aMLO||_rel==aMBELOW) && _amt==aMASPOSSIBLE && hasMarginFeature )
    {
      _ref = aMINTERFACE;
      _value = DEFAULTVAL;
      return true;
    }
    else if( (_rel==aMHI||_rel==aMABOVE) && _amt==aMASPOSSIBLE && hasMarginFeature )
    {
      _ref = aMGINGIVA;
      _value = DEFAULTVAL;
      return true;
    }
  }

  // This is a place to troll for lost opportunities.
/*
  if( _amt==aMNOAMT && (_rel!=aMNOREL) )
  {
    if( _ref==aMNOREF )
      _ref = aMGINGIVA;
    if( _rel==aMAT )
      _amt = aMJUST;
    else if( (_rel!=aMLO ) && (_rel!=aMHI) )
    {
      _amt = aMJUST; // have a relation and now _ref is set. No amount means "just"???
      if( _value==NOVAL )
        _value = 0.0;
    }
  }
*/

  if( _ref>aMNOREF && (_rel==aMCLOSEST || _rel==aMAT ) && _amt==aMNOAMT)
  {
    _amt = aMJUST;
    _value = 0.0;
  }

  if( _ref==aMNOREF || _rel==aMNOREL || _amt==aMNOAMT )
    return false;

  if( _amt==aMVALUE && _value==NOVAL )
    return false;

  return true;
}

bool MarginHeightSpec::Overlay( const MarginHeightSpec & hspec)
{
  if( hspec._amt!=aMNOAMT && _amt!=aMNOAMT )
    if( hspec._amt!=_amt ) // cannot change _amt
      return false;
  if( hspec._face==_face) // cannot repeat faces
    return false;   

  // allow filling in implicity ref and rel
  overlay( hspec._ref, _ref );
  overlay( hspec._rel, _rel );
  return true;
}


double MarginHeightSpec::convertToOffset( )
{
  switch( _amt )
  {
  case aMVALUE:
  case aMJUST:
    return _value;
    break;
  case aMASPOSSIBLE:
    if( _ref==aMINTERFACE && (_rel==aMHI || _rel==aMABOVE) ) 
    {
      // "hi as possible above interface" a strange possibility
      _ref = aMGINGIVA;
      _rel = aMCLOSEST;
      return 0.0;
    }
    else if( _ref==aMINTERFACE && (_rel==aMLO || _rel==aMBELOW ) )
    {
      // even stranger, below interface is not possible
      _rel = aMCLOSEST;
      return DEFAULTVAL;
    }
    else if( (_ref==aMGINGIVA || _ref==aMNEIGHBOR || _ref==aMLINE) && (_rel==aMLO || _rel==aMBELOW) )
    {
      // low as possible below gum
      _ref = aMINTERFACE;
      _rel = aMCLOSEST;
      return 0.0;
    }
    else if( (_ref==aMGINGIVA || _ref==aMNEIGHBOR || _ref==aMLINE) && (_rel==aMHI || _rel==aMABOVE) )
    {
      // hi as as possible above gum
      _ref = aMGINGIVA;
      _rel = aMABOVE;
      return 0.0;
    }
    else
    {
      return DEFAULTVAL; // punt for now!
    }
    break;
  case aMNOAMT:
  default:
    return DEFAULTVAL;
    break;
  }
}

MarginInfo MarginHeightSpec::convertToMarginInfo()
{
  MarginInfo minfo;
  minfo._type = MHEIGHT;

  // reference and relation need to convert to a single offset from a "position"
  switch( _face )
  {
  case aMBUCCAL:
    minfo._B = convertToOffset();
  case aMLINGUAL: 
    minfo._L = convertToOffset();
    break;
  case aMMESIAL:
    minfo._M = convertToOffset();
    break;
  case aMDISTAL:
    minfo._D = convertToOffset();
    break;
  case aMM_D: 
    minfo._M = minfo._D = convertToOffset();
    break;
  case aMNOFACE:
  case aMALL:
    minfo._all = convertToOffset();
  default:
    break;
  }

  // set these at the end. The might be changed during the convertToOffset().
  minfo._reference = Ref2Ref( _ref );
  minfo._position = Rel2Pos( _rel );

  minfo._hasWrittenSpec = _hasWrittenSpec;
  
  return minfo;
}
//////////////////////MARGIN WIDTH //////////////////
/////////////////////////////////////////////////////
const Dictionary & getWidthOptionDictionary( MWIDTH_OPTION opt )
{
  switch( opt )
  {
  case aFULL_ANATOMICAL_DIMENSIONS:
    return FullAnatDimD;
    break;
  case aCONTOUR_SOFT_TISSUE:
    return ContourSoftTissD;
    break;
  case aSUPPORT_TISSUE:
    return SupportTissD;
    break;
  case aNO_TISSUE_DISPLACEMENT:
    return NoTissDiplaceD;
    break;
  default:
    return NullDictionary;
    break;
  }
}

//////////////////////////////////
///////////// MARGIN WIDTH /////////

bool MarginWidthSpec::isConsistent()
{
/*  if( _opt>aMNOOPTION && _amt>aMNOAMT )
  {
    return false;
  }
?????*/

  if( _profile==EPSNOTSET )
  {
    switch( _opt )
    {
    case aFULL_ANATOMICAL_DIMENSIONS:
      if( _push>DEFAULTVAL )
        return false;
      else
        return true;
      break;
    case aNO_TISSUE_DISPLACEMENT:
       if( _push==DEFAULTVAL || (0.0<=_push && _push<0.1 ))
        return true;
      else
        return false;
        break;
    case aSUPPORT_TISSUE: 
    case aCONTOUR_SOFT_TISSUE:
      if( _push==DEFAULTVAL )
        return true;
      else if(0.1<=_push && _push<0.6 )
      {
        _opt = aSUPPORT_TISSUE; //forced consistency
        return true;
      }
      else if(0.6<=_push && _push<2.001 )
      {
        _opt = aCONTOUR_SOFT_TISSUE;
        return true;
      }
      else
        return false;
        break;
    case aMNOOPTION:
    default:
      if( 1 )//_push==NOVAL  )
        return false;
      else
        return true; // but it will probably should not be "complete" with a value and no clear option
    }
  }
  else // EPS is set
  {
      return true;
  }
}


bool MarginWidthSpec::isComplete(bool hasMarginFeature)
{
  if( _profile!=EPSNOTSET)
   {
     //do error checking somewhere else!
      return true;
  }
  if( _face==aMNOFACE )
    return false; // it should have been set to aMALL if it did not occur in text and no other error

  return isConsistent();
}



void MarginWidthSpec::readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used, int istartTok )
{
  int itok=-1, itok2=-1;

  bool bAmtAsValue=false;

  clear(); // in case you forgot

  // for each value of MWITDH_OPTION
  // get its dictionary and loop through all its words

  _opt = aMNOOPTION;
  for( unsigned int opt=0; opt<NUM_MWITDH_OPTIONS; opt++)
  {
    const Dictionary & dict = getWidthOptionDictionary( (MWIDTH_OPTION)opt);

    if( dict.findMatchInTokens(tokens,itok, itok2, istartTok)>=0 ) // found a word (index is return value)
    {
      _opt = (MWIDTH_OPTION)opt;
      token_used[itok] = true;
      token_used[itok2] = true;
      if( _opt==aSUPPORT_TISSUE )
      {
        const Dictionary vdict=ValDictionary;
        if( vdict.findMatchInTokens(tokens, itok, itok2,istartTok)>=0 )
        {
          _push = getValLeftOfMM( tokens, token_used, itok, istartTok );// may use token[itok-1]
          bAmtAsValue = true;
        }
      }
      else if( _opt==aNO_TISSUE_DISPLACEMENT )
      {
        bAmtAsValue = true;
        _push = 0.0;
      }


      break;
    }
  }

  // second chance to set _push
  _amt = aMNOAMT;
  for( unsigned int amt=0; amt<NUM_M_AMTS; amt++)
  {
    const Dictionary & dict = getAMTDictionary( (M_AMT)amt);

    if( dict.findMatchInTokens(tokens,itok, itok2, istartTok)>=0 )
    {
      _amt = (M_AMT)amt;
      token_used[itok] = true; // it may not be all of the token
      token_used[itok2] = true;
      if( _amt==aMVALUE )
      {
        _push = getValLeftOfMM( tokens, token_used, itok, istartTok );// may use token[itok-1]
        token_used[itok] = true;
      }
      break;
    }
  }
  if( _amt==aMNOAMT && bAmtAsValue ) // implied value
    _amt = aMVALUE;
  else if( _amt!=aMVALUE && bAmtAsValue ) // or _amt contradicts value
  {
    clear(); // keep going but limp along with a fresh beginning here
    return;
  }

  // Got EPS?
  EPSLabel eps; // this guy knows how to find it
  std::vector<bool>tmpUsed = token_used;
  clearTokensUsed(tmpUsed);
  eps.readTokens(tokens,tmpUsed);
  if( eps._found )
  {
    _profile = getEPSSHAPE( eps._profShape );
    updateTokensUsed( tmpUsed, token_used );
  }
  //else we use the _push value and forget about EPS

  if( _opt==aMNOOPTION && _amt==aMVALUE && _push>=0.0 )// implicit "option"
  {
    ConstantLabel wid("width");
    wid.readTokens(tokens, token_used );
    if( wid._found )
    {
      if( _push<0.1 )
        _opt = aNO_TISSUE_DISPLACEMENT;
      else if( _push<2.0 )
        _opt = aSUPPORT_TISSUE;
    }
  }

  _face = getFace(tokens, token_used);
  if( _face!=aMALL && _face!=aMNOFACE )// i.e. a face is specified. Currently this is not allowed in automation
  {
    clear();
    return;
  }

  if( _opt==aSUPPORT_TISSUE && _amt==aMJUST && _push<0 )
  {
    _push = 0.0;
    ConstantLabel slight("slightly");
    slight.readTokens(tokens, token_used);
    if( slight._found )
      _push = 0.1;
  }


  _hasWrittenSpec = hasWrittenSpec(tokens, token_used );
}


bool MarginWidthSpec::Overlay( const MarginWidthSpec & wspec)
{ 
  if( wspec._amt!=aMNOAMT && _amt!=aMNOAMT )
    if( wspec._amt!=_amt ) // cannot change _amt
      return false;
  if( wspec._face==_face) // cannot repeat faces
    return false;   

  // allow filling in missing opt and _amt
  overlay( wspec._opt, _opt );
  overlay( wspec._amt, _amt );
  return true;
}


MarginInfo MarginWidthSpec::convertToMarginInfo()
{
  MarginInfo minfo;
  minfo._type = MWIDTH;

  // separate value per tooth "face" is not supported
  minfo._push = _push;
  minfo._profile = _profile;

  // options are simple 1-1 translation (x -> x-1)
  switch(_opt )
  {
  case aFULL_ANATOMICAL_DIMENSIONS:
    minfo._opt = AC::Preference::FULL_ANATOMICAL_DIMENSIONS;
    break;
  case aCONTOUR_SOFT_TISSUE:
    minfo._opt = AC::Preference::CONTOUR_SOFT_TISSUE;
    break;
  case aSUPPORT_TISSUE:
    minfo._opt = AC::Preference::ANATOMICAL_SUPPORT_TISSUE;
     break;
  case aNO_TISSUE_DISPLACEMENT:
    minfo._opt = AC::Preference::NO_TISSUE_DISPLACEMENT;
  case aMNOOPTION: // BUT WE COOK UP SOMETHING IN THIS CASE (HOW ABOUT USING PUSH?)
  default:
    minfo._opt = AC::Preference::INVALID_WIDTH_OPTION;
    minfo._profile = _profile;
    break;
  }

   minfo._hasWrittenSpec = _hasWrittenSpec;
  
  return minfo;
}


////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
bool getMarginSpec(std::vector<string> & tokens, 
                   std::vector<bool> & token_used_H,
                   std::vector<bool> & token_used_W,
                   MarginHeightSpec & Hspec, MarginWidthSpec &Wspec)
{
  Hspec.clear();
  Wspec.clear();

  //------------------ look for generic margin terms
  bool hasMarginFeature; 
  std::vector<bool> token_usedM = token_used_H;//just to get the size
  clearTokensUsed(token_usedM);                //start fresh anyway
  hasMarginFeature = MarginFeatureDictionary.foundInDictionary(tokens, token_usedM );
  Hspec._hasMarginFeature = hasMarginFeature; //avoids passing as an arg (since this was an afterthought)

  BlankLabel asXas("as ? to implant as possible");
  asXas.readTokens(tokens, token_used_H );

  if( asXas._foundString=="low" || asXas._foundString=="close" )
    hasMarginFeature=true;

  if( hasMarginFeature )
  {
    updateTokensUsed( token_usedM, token_used_H );
    updateTokensUsed( token_usedM, token_used_W );
  }

  //------------------------READ HEIGHT INFO-----------
  std::vector<bool> token_usedH = token_used_H;
  Hspec.readTokens( tokens, token_usedH);
  bool hComplete = Hspec.isComplete(hasMarginFeature); // (will re-check this later)
  // if hComplete, worry about grabbing the same tokens during width reading
  // so here the policy is that height get's first crack at them
  if( hComplete )
  {
    updateTokensUsed( token_usedH, token_used_H );
    maskTokens(tokens,token_used_H);   
  }


  //------------------------READ WIDTH INFO-----------
  std::vector<bool> token_usedW = token_used_W;
  Wspec.readTokens( tokens, token_usedW );
  bool wComplete = Wspec.isComplete(hasMarginFeature); // (will re-check this later)
  if( wComplete )
  {
    updateTokensUsed(token_usedW, token_used_W);
    maskTokens( tokens, token_used_W);
  }

  return hasMarginFeature;
}



bool getMarginSpecs(const std::vector<string> & tokens, std::vector<bool> & INtoken_used,
                    std::vector<MarginHeightSpec> & H,
                    std::vector<MarginWidthSpec> & W )
{
  H.clear();
  W.clear();

  // use private version of tokens. At end, if all went well, the get moved back into the INtoken_used
  std::vector<bool> token_used;
  initTokensUsed( tokens, token_used );


  PhraseSplitter burse(tokens);
  std::vector<string> subtokens = burse.getNextPhrase();

  // clean "used" array
  std::vector<bool> subtoken_used_H;
  std::vector<bool> subtoken_used_W;
  while(subtokens.size()>0) 
  {
    subtoken_used_H.clear();
    subtoken_used_W.clear();
    for(unsigned int i=0; i<subtokens.size(); i++)
    {
      subtoken_used_H.push_back(false);
      subtoken_used_W.push_back(false);
    }

    MarginHeightSpec hspec;
    MarginWidthSpec  wspec;
     

    bool hasMarginFeature = getMarginSpec(subtokens, subtoken_used_H, subtoken_used_W , hspec, wspec);

    bool hComplete = hspec.isComplete(hasMarginFeature);
    bool wComplete = wspec.isComplete(hasMarginFeature);

    if( hComplete )
      burse.updateTokenUsed( subtoken_used_H, token_used );
    if( wComplete )
      burse.updateTokenUsed( subtoken_used_W, token_used );

    ///////// ERROR CONDITIONS (temporary?) //////////////
    // allow width and eps but mixed width/height is too risky
    if( hComplete && wComplete && wspec._profile==EPSNOTSET ) // error out
    {
      H.clear();
      W.clear();
      return false;
    }
    // this case is not supported in VAD
    if( 0 )//wComplete && wspec._face>aMALL )
    {
      W.clear();
      return false;
    }

    // archive Hspec info
    if( hComplete )
    {
      H.push_back(hspec);
    }
    else if( H.size()>0 ) // already had a complete spec
    {
      // maybe partial info can be overlaid on prior spec?
      hspec.Overlay( H[ H.size()-1 ] );
      hComplete = hspec.isComplete(hasMarginFeature);
      if( hComplete )
      {
        H.push_back(hspec);
        burse.updateTokenUsed( subtoken_used_H, token_used );// really! they were used
      }
    }

    // SEPARATE EPS FROM OTHER INFO
    MarginWidthSpec epsTmp;
    if( wspec._profile!=EPSNOTSET ) // have an eps statement mixed in
    {
      epsTmp._profile = wspec._profile; 
      wspec._profile = EPSNOTSET;
      wComplete = false;
    }

    if( wComplete )
    {
      W.push_back(wspec);
    }
    else if( W.size()>0 )
    {
      wspec.Overlay( W[ W.size()-1] );
      wComplete = wspec.isComplete(hasMarginFeature);
      if( wComplete )
      {
        W.push_back(wspec);
        burse.updateTokenUsed( subtoken_used_W, token_used );// really! they were used
      }
    }

    if( epsTmp.isComplete(hasMarginFeature) )// put eps at the end (earlier messes up Overlay)
    {
      W.push_back(epsTmp);
      updateTokensUsed( subtoken_used_W, token_used);
    }

    // continue the loop
    subtokens = burse.getNextPhrase();
  }

  // finalize the token usage
  updateTokensUsed(token_used, INtoken_used);
 
return true;
}
/////////////////////////////////////////////////////////////////////
MARGIN_POSITION RelToPos( const MHEIGHT_REL & rel )
{
  switch( rel )
  {
  case aMNOREL:
    return MNOPOS;
    break;
  case aMAT:
    return MAT;
    break;
  case aMHI:
  case aMABOVE:
    return MABOVE;
    break;
  case aMLO:
  case aMBELOW:
    return MBELOW;
    break;
  case aMCLOSEST:
    return MCLOSEST;
    break;
  default:
    return MNOPOS;
    break;
  }
}

// awkward since these constants cannot be manipulated properly (use as return type?)
Preference::MarginWidthOption Opt2Pref(const MWIDTH_OPTION & opt)
{
  // options are simple 1-1 translation (x -> x-1)
  switch( opt )
  {
  case aFULL_ANATOMICAL_DIMENSIONS:
    return AC::Preference::FULL_ANATOMICAL_DIMENSIONS;
    break;
  case aCONTOUR_SOFT_TISSUE:
    return AC::Preference::CONTOUR_SOFT_TISSUE;
    break;
  case aSUPPORT_TISSUE:
    return AC::Preference::ANATOMICAL_SUPPORT_TISSUE;
     break;
  case aNO_TISSUE_DISPLACEMENT:
    return AC::Preference::NO_TISSUE_DISPLACEMENT;
  case aMNOOPTION: 
  default:
    return AC::Preference::INVALID_WIDTH_OPTION;
    break;
  }
}


bool collapseMarginWidthInfo(const std::vector<MarginWidthSpec> & W, MarginInfo & minfo )
{
  if( W.size()==0 )
    return false;

  minfo._type = MWIDTH;

  for(size_t i=0; i<W.size(); i++)
  {
    MarginWidthSpec w = W[i];
    if( w._hasWrittenSpec )// can be set true but not set false
      minfo._hasWrittenSpec;

    double push = w._push;
    EPS_SHAPE profile = w._profile;

    if( push>NOVAL && profile!=EPSNOTSET )//should not have both
      return false;

    if( minfo._push==NOVAL )
      minfo._push = push;
    else if( minfo._push!=push )// cannot be changed
      return false;
    else if( minfo._profile==EPSNOTSET )
      minfo._profile = profile;
    else if( minfo._profile!=profile )// cannot be changed
      return false;

    Preference::MarginWidthOption opt = Opt2Pref( w._opt );
    if( opt==Preference::INVALID_WIDTH_OPTION )
      return false;

    if( minfo._opt==Preference::INVALID_WIDTH_OPTION )
      minfo._opt = opt;
    else if( minfo._opt!=opt ) // cannot be changed
      return false;
  }

  return minfo.isComplete();

}

bool collapseMarginHeightInfo(const std::vector<MarginHeightSpec> & H, MarginInfo & minfo )
{
  if( H.size()==0 )
    return false;

  MARGIN_REFERENCE mref=MNOREFSET;
  MARGIN_POSITION  mpos=MNOPOS;

  minfo._type = MHEIGHT;

  M_AMT lastamt = aMNOAMT;

  for(size_t i=0; i<H.size(); i++)
  {
    MarginHeightSpec h = H[i];
    if( h._hasWrittenSpec )// can be set true but not set false
      minfo._hasWrittenSpec = true;


    mref = (MARGIN_REFERENCE)h._ref;
    if( minfo._reference==MNOREFSET )// can be set one time
      minfo._reference = mref;
    else if( minfo._reference!=mref )// but not changed
      return false;
    
    mpos = Rel2Pos( h._rel );
    if( minfo._position==MNOPOS )
      minfo._position = mpos;
    else if( minfo._position!=mpos )
      return false;

    double value = NOVAL;
    M_AMT amt = h._amt;
    if( i==0 )
      lastamt = amt; 
    else if( amt!=lastamt )// not allowed to change amt type (eg mesial .1mm and others as close to interface as possible_
      return false;
  
    if( h._amt==aMNOAMT )
      return false;
    else if( h._amt==aMJUST || h._amt==aMASPOSSIBLE )
      value = 0.0;
    else
      value = h._value;


    MFACE face = h._face;

    double all = minfo._all;
    double buc = minfo._B;
    double lng = minfo._L;
    double mes = minfo._M;
    double dst = minfo._D;
    // nothing is set
    switch( face )
    {
    case aMALL:
      if( all==NOVAL )
        minfo._all = value;
      else if( all!=value ) // cannot reset _all
        return false;
      break;
    case aMBUCCAL:
      if( all>NOVAL ) // no reset to all allowed
        return false;
      else if( buc>NOVAL && fabs(buc-value)>0.001 ) // no reset of value allowed
        return false;
      else
        minfo._B = value;
      break;
    case aMLINGUAL:
      if( all>NOVAL ) // no reset to all allowed
        return false;
      else if( lng>NOVAL && fabs(lng-value)>0.001 ) // no reset of value allowed
        return false;
      else
        minfo._L = value;
      break;
    case aMMESIAL:
      if( all>NOVAL ) // no reset to all allowed
        return false;
      else if( mes>NOVAL && fabs(mes-value)>0.001 ) // no reset of value allowed
        return false;
      else
        minfo._M = value;
      break;
    case aMDISTAL:
      if( all>NOVAL ) // no reset to all allowed
        return false;
      else if( dst>NOVAL && fabs(dst-value)>0.001 ) // no reset of value allowed
        return false;
      else
        minfo._D = value;
      break;
    case aMM_D:
      if( all>NOVAL )// cannot already be set
        return false;
      else if( mes>NOVAL || dst>NOVAL )// if already set
        return false;
      else 
        minfo._M = minfo._D = value;
      break;
    case aMNOFACE:
      if( h._amt!=aMNOAMT && h._ref!=aMNOREF && h._rel!=aMNOREL )
      {
        h._face = aMALL;
        if( all==NOVAL )
          minfo._all = value;
        else if( all!=value ) // cannot reset _all
          return false;
      }
      else
        return false;
      break;
    default:
      return false; 
      break;
    }// ends setting of margin height offset
  }

  return minfo.isComplete();
}



// attempt to combine info from multiple Hspec and Wspec into a single MarginInfo object
// return false if not possible
bool collapseMarginInfo(const std::vector<MarginHeightSpec> & H, const std::vector<MarginWidthSpec> & W, 
                        MarginInfo & Minfo)
{
  MarginInfo minfo; // start with fresh empty instance

  if( H.size()==0 && W.size()==0 )
  {
    Minfo = minfo;// empties it
    return false;
  }

  // currently MarginInfo cannot mix width and height
  // A note with both is risky anyway
  if( H.size()>0 && W.size()>1 )
  {
    Minfo = minfo;
    return false;
  }
  if( H.size()>0 && W.size()==1 )
    if( W[0]._profile==EPSNOTSET )// eps set is OK but otherwise...
      return false;


  // all of these Hspec are supposed to be complete
  if( H.size()>0 )
  {
    if( collapseMarginHeightInfo(H,minfo) )
    {
      if( W.size()==1 ) //EPS SET CASE
      {
        minfo._profile = W[0]._profile;
      }
      Minfo = minfo;
      return true;
    }
    else
    {
      return false;
    }
  }

  if( W.size()>0 )
  {
    if( collapseMarginWidthInfo(W,minfo) )
    {
      Minfo = minfo;
      return true;
    }
    else
    {
      return false;
    }
  }
  return false;
}

////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


/////////////////////////////////////////////////////////////////////////
/////////////////////////////// MarginInfo //////////////////////////////
/////////////////////////////////////////////////////////////////////////

string reportMarginInfoType( const MARGIN_INFO_TYPE & type)  
{
  switch( type )
  {
  case MDEFAULT:
    return "DEFAULT";
    break;
  case MHEIGHT:
    return "HEIGHT";
    break;
  case MWIDTH:
    return "WIDTH";
    break;
  case MSHOULDER:
    return "SHOULDER";
    break;
  default:
    return "none";
    break;
  }
}
string reportMarginInfoReference( const MARGIN_REFERENCE & ref )  
{
  switch( ref )
  {
  case MGINGIVA:
    return "GINGIVA";
    break;
  case MINTERFACE:
    return "INTERFACE";
    break;
  case MNEIGHBOR:
    return "NEIGHBOR";
    break;
  case MLINE:
    return "LINE";
    break;
  default:
    return "none";
    break;
  }
}

string reportMarginInfoPosition( const MARGIN_POSITION & pos )  
{
  switch(pos)
  {
  case MAT:
    return "AT";
    break;
  case MCLOSEST:
    return "CLOSEST";
    break;
  case MABOVE:
    return "ABOVE";
    break;
  case MBELOW:
    return "BELOW";
    break;
  default:
    return "none";
    break;
  }
};

string reportMarginVal( double val )  
{
  if( val==NOVAL )
    return " ";

  if( val==DEFAULTVAL )
    return "*";

  char foo[10];
  sprintf_s(  &foo[0], 10, "%.2lf", val );

  string bar( foo ); 

  return bar;
}

MarginInfo::MarginInfo()
{
  _type = MNOTYPE;
  _hasWrittenSpec = false;

      // for height
  _reference = MNOREFSET;
  _position  = MNOPOS;
  _all = _B = _L = _M = _D = NOVAL;

  // for width
  _profile   = EPSNOTSET;
  _push      = NOVAL;
  _opt       = AC::Preference::INVALID_WIDTH_OPTION; //used in the new version
}

bool MarginInfo::isComplete() const
{
  if( _type==MHEIGHT )// need a reference, a position, and some kind of value
  {
    if( _reference==MNOREFSET )
      return false;

    if( _position==MNOPOS )
      return false;

    if( _all==NOVAL && _B==NOVAL && _L==NOVAL && _M==NOVAL && _D==NOVAL )
      return false;

    return true;
  }
  
  if( _type==MWIDTH )  // need a profile shape and optional _push
  {
    if( _profile==EPSNOTSET && _push==NOVAL)
      return false;
    return true;
  }
  
  return false; // for now, all other types are considered incomplete
}


void MarginInfo::report() const
{
  cout << "********** Margin **************";
  if( _type==MHEIGHT )
  {
    cout << "\n " << reportMarginInfoType(_type) 
          << " "   << reportMarginInfoPosition(_position) 
          << " "   << reportMarginInfoReference( _reference );

    cout << "\n " 
          << "all="<<reportMarginVal( _all)
          << " B=" <<reportMarginVal(_B)
          << " L=" <<reportMarginVal(_L)
          << " M=" <<reportMarginVal(_M)
          << " D=" <<reportMarginVal(_D);
  }
  else if( _type==MWIDTH )
  {
    cout << "\n " << reportMarginInfoType(_type);
    if( NOVAL==_push )
      cout  << " "   << getEPSShapeString( _profile );
    else
      cout << " push=" << _push;
  }


//  if( _hasWrittenSpec )
//    cout<< "\n (has rx)";

  cout << "\n";
  cout << "\n";
}


bool MarginInfo::hasData() const
{
  if( _type==MNOTYPE ) // simple-minded check. If this was set it means there is some data.
    return false;
  else
    return true;
}

string getValName( double val )
{
  char text[1000];
  sprintf_s( text, "%.2lf", NOVALNAME );
  string novalname( text );

  sprintf_s( text, "%.2lf", DEFAULTVALNAME );
  string defaultvalname( text );

  string valName;
  if( val==NOVAL )
    valName = novalname;
  else if( val==DEFAULTVAL )
    valName = defaultvalname;
  else
  {
    sprintf_s(text, "%.2lf", val );
    valName = string( text );
  }
  return valName;
}


string MarginInfo::DetailsHeader(const char * delim)
{
  string DEL(delim);
  string header = "TYPE" + DEL + "MREF" + DEL + "MPOS" + DEL 
              + "ALL " + DEL + "B   " + DEL + "L   " + DEL + "M   " + DEL + "D   " + DEL 
              + "PROF" + DEL + "PUSH" + DEL + "RX  ";
                 
  return header;    
}

string MarginInfo::details(const char * delim)
{
  string DEL(delim);
  string foo;

  foo = I2Str( (int)_type ) + DEL
      + I2Str( (int)_reference ) + DEL
      + I2Str( (int)_position ) + DEL
      + getValName(_all ) + DEL
      + getValName( _B ) + DEL
      + getValName( _L ) + DEL
      + getValName( _M ) + DEL
      + getValName( _D ) + DEL
      + I2Str((int)_profile) + DEL
      + getValName( _push )  + DEL
      + bool2Str( _hasWrittenSpec );

#ifdef HAVE
  MARGIN_INFO_TYPE _type;
  bool _hasWrittenSpec;

      // for height
  MARGIN_REFERENCE _reference;
  MARGIN_POSITION  _position;
  double _all, _B, _L, _M, _D; // absolute offset measured from MARGIN_REF

      // for width
  EPS_SHAPE        _profile;
  double           _push;

  bool isComplete(); // true if fields are correctly/consistently filled. So it is "read safe"
  void report() const;
  bool hasData() const; 
  string details(const char * delim);

};
#endif


  return foo;
}

bool MarginInfo::SafetyOK()
{
  double TOOFAR=2.51;// simple mm limit on height,depth,pressure. Larger values will me marked not safe

  if( _hasWrittenSpec )
    return false;
  if( _all>TOOFAR || _B>TOOFAR || _L>TOOFAR || _M>TOOFAR || _D>TOOFAR )
    return false;
  if( _push>TOOFAR )
    return false;

  if( _reference==aMINTERFACE && _position==MBELOW )
    return false;

  if( _reference==aMINTERFACE && _all==NOVAL )// do not support setting only one face at interface
    return false;

  return true;
} 


} // end namespace AC

