/*
 * Copyright 2013, DENTSPLY Implants, All Rights Reserved.
 * This file contains proprietary information, and may not be viewed, copied,
 * distributed, sold, published, or disseminated without express permission
 * of DENTSPLY Implants.
 */

#include <vector>
#include <Math/point3.h>
#include <Math/vector3.h>
#include <Lib/GLTools/Obj3D.h>
#include <assert.h>
#include <Vad/globals.h>
#include <Data/Preference.h>

#include <AtlasData/MarginHeightOption.h>

#ifndef _autonotes_h_
#define _autonotes_h_

using namespace std;

namespace AC {
///////////////// PARSING //////////////////////////////////
const char STDSEPARATOR='|' ;  //Used to flag separate phrases, replacing other separators in the text 
const string sSTDSEPARATOR = " " + string(&STDSEPARATOR) + " "; // a string version with extra spaces



size_t Tokenize(const string & text, std::vector<string> & tokens );
void splitToken( const string & tok, const string & subtok, string & lefttok, string & righttok );
size_t DelimTokenize( const string & text, std::vector<string> & tokens, const char *delim);


void CleanParse( const string & noteIn, string & noteOut );

void replaceENTER(string & text);


class PhraseSplitter
{
public:
  PhraseSplitter( const vector<string> & tokens ) 
          : _tokens(tokens)
  {
    _split = 0; 
    _prevsplit = 0;
  }

  vector<string>  getNextPhrase();

  void updateTokenUsed( const vector<bool> & subtoken_used, vector<bool> &token_used );

private:
  const vector<string> & _tokens;
  unsigned int _split, _prevsplit;
  vector<string > phraseTokens;
};    


////////////////////////////////////////////////////
#ifdef HADONCE
enum UNITTYPE
{
  NOUNIT,
  OTHER, // could be used for shades, serial numbers, other stuff 
  UNIT,
  TOOTH, 
  MMs, //s to avoid ambiguity with AC::MM
  DEGREE,
  PERCENT,
  PHONEDATE
};
const unsigned int NUMUNITTYPES = 7;
#endif



////////////////////////////////////////////////////////////////////////
//////////////// semscanf() related ////////////////////////////////////
////////////////////////////////////////////////////////////////////////

const double NOVAL=-FLT_MAX;
const double DEFAULTVAL=-FLT_MAX/2.0;
// use these for printouts
const double NOVALNAME=-99.99;
const double DEFAULTVALNAME=-88.88;
string getValName( double val ); // for printout of these names or standard double vals
string bool2Str( const bool b );


// for now we can process a single tooth number. The result.tooth
// has these allowed values otherwise.
const int NOTOOTHSET=-1;
const int MULTITOOTH=-2;

// replace words with "dull"
void maskTokens(  vector<string> & token, vector<bool> token_used );

void maskPreDullTokens(  vector<string> & token, vector<bool> token_used );

// insert used tokens from src into dest...vects must be of same size().
void updateTokensUsed(const std::vector<bool> & src_token_used, std::vector<bool> & dest_token_used);


              // returns number of format-specified arguments
              // uses the global dictionary list to sanity check the args
bool countArgs(const char * format, unsigned int & argCount, unsigned int & tokenCount);


              // returns with a dictionary pointer and its number of words.
              // false if no such dictionary exists (add new dictionaries as needed)
bool getDictionary( string name, const string * & dictionary, unsigned int & NumWords );

              // the workhorse for extracting words from text and putting results into arguments
              // returns the count of fields found. Input arguments need to be initialized
              // and if not all fields are found, those corresponding args are left at their initial value
              // returns with vector of used token indices
unsigned int semscanf( const std::vector<string> & token, std::vector<unsigned int> & usedIndex, const char * format, ...);


              // here pass pointer to an unsigned int vector for each format argument
              // false if dictionary args are illegal
bool semscanfALL( const std::vector<string> & token, vector<unsigned int> & allUsedIndices, const char * format, ... );


////////////////////////////////////////////////////////////////////////
//////////////// WorldLabel classes ////////////////////////////////////
////////////////////////////////////////////////////////////////////////

const unsigned int MAXFORMAT =100;            // count of chars in format     

class WorldLabel
{
public:
  WorldLabel(){_found=false;};

  WorldLabel(const char * format)
  { 
    for(unsigned int j=0; j<MAXFORMAT; j++)
    {
      _format[j] = format[j];
      if( format[j]==0 )
        break;
    }
    _found=false;
  }
  
  virtual void readTokens( const std::vector<string> & token , std::vector<bool> & token_used)=0;

  virtual void clear(){ _found = false; }
  virtual void setFound() { _found = true; }

  char _format[MAXFORMAT];
  bool _found;
};


class OccClearanceLabel : public WorldLabel
{
public:
  OccClearanceLabel();

  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used);
  double _clearance;

  void clear(){ WorldLabel::clear(); _clearance=NOVAL; } 
};



enum EPS_SHAPE
{
  EPSNOTSET=0,
  EPSON,
  EPSOFF,
  EPSSTRAIGHT,
  EPSCONCAVE,
  EPSCONVEX
};

// accessor
EPS_SHAPE getEPSSHAPE( const string & shapeString );
string getEPSShapeString( const EPS_SHAPE & shape );


class MarginInfo;

class EPSLabel : public WorldLabel
{
public:
  EPSLabel();
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used );
  string _profShape;
  void clear(){ WorldLabel::clear(); _profShape=""; } 
  bool setFromMarginInfo(const MarginInfo & minfo); // true only if minfo is a MWIDTH with _profile set
};

// for any fixed pattern of constants
class ConstantLabel : public WorldLabel
{
public:
              // format must contain constants and no format specifiers  
              // set isRigid=false to allow extra tokens between specified format constants   
  ConstantLabel(const char * format, bool isRigid=true); 
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used);

  void clear(){ WorldLabel::clear(); } // do not clear constructor arguments

private:
  std::vector<string> _ftokens;
  bool _isRigid;
};


// look for a string within a fixed pattern of other words, use "?" to indicate blank
class BlankLabel: public WorldLabel
{
public:
    BlankLabel(const char *format); // accepts strings of the form "X ? Y" where X and Y are arbitrart
    void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used);
    void clear() { _ifound=-1; _foundString=""; }

    std::vector<string> _ftok;     // tokenized format
    string _foundString;
    size_t _ifound; // token index if found in tokens[]

};

// Spots "Later order" at start of note. _found flag is not used in CaseWorld::Decision()
// Instead we expect the content of the note to be analyzed generically.
// The purpose of this label is to raise alarms as needed
class LaterOrderLabel : public WorldLabel
{
public:
  LaterOrderLabel();
  void readTokens(const std::vector<string> & tokens, std::vector<bool> & token_used);
  bool _reScanned;
  bool _hasCannedText;
  bool _hasExtraText;
  bool _badFormat;

  void clear() { WorldLabel::clear(); _reScanned=false; _hasCannedText=false; _hasExtraText=false; _badFormat=false;}

  void setSafe(){ _reScanned = _hasCannedText = _hasExtraText = _badFormat = false; }
  void setSEMOUnsafe() { _hasExtraText = true; _hasCannedText = true;}
};

class ForeignLaterOrder : public WorldLabel
{
public:
  ForeignLaterOrder();
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used);
  bool hasDregs()const { return _hasDregs; }
private:
  ConstantLabel _swedishLO; //senare bestalling
  ConstantLabel _germanLO;  //nachbestellung
  ConstantLabel _frenchLO;  // commande ulterieur
  ConstantLabel _dutchLO;  // commande ulterieur
  ConstantLabel _englishLO; // must be used BEFORE regular LaterOrderLabel
  ConstantLabel _italianLO; // must be used BEFORE regular LaterOrderLabel
//HOPELESS  ConstantLabel _japaneseLO; // must be used BEFORE regular LaterOrderLabel
  void clear() { WorldLabel::clear(); _swedishLO.clear(); _germanLO.clear(); _frenchLO.clear(); _englishLO.clear(); _italianLO.clear();}

  bool _hasDregs; //"extra" or "canned"
};



class OptionNLabel : public WorldLabel
{
public:
  int _optionNumber;
  OptionNLabel();
  // need to handle possible modifiers and misspellings  
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used);
  void clear() { WorldLabel::clear(); _optionNumber=0; }
  bool processable() const;
};

class SoftTissueLabel : public WorldLabel
{
public:
  SoftTissueLabel();
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used);
  void clear() { WorldLabel::clear();
                _stIS.clear(); //se
                _stON.clear(); //se
                _stMODEL.clear();  
                _stCONTOUR.clear();
                _stHAS.clear();  //
                _FOLLOWst.clear(); 
                _CONTOURst.clear();
                _OFst.clear();
               }

private:
  ConstantLabel _stIS; //senare bestalling
  ConstantLabel _stON; //senare bestalling
  ConstantLabel _stMODEL;  //nachbestellung
  ConstantLabel _stCONTOUR;  //nachbestellung
  ConstantLabel _stHAS;  // commande ulterieur
  ConstantLabel _FOLLOWst; // must be used BEFORE regular LaterOrderLabel
  ConstantLabel _CONTOURst; // must be used BEFORE regular LaterOrderLabel
  ConstantLabel _OFst;
};

// for "large abutment" or "over size abutment" or "oversize abutment"
class BigAbutment : public ConstantLabel
{
public:
  BigAbutment();
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used);
};

class PathOfInsertion : public ConstantLabel
{
public:
  PathOfInsertion();
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used);
};

// for "#13 will be a molar" type patterns
// this class name is pronounced ToothWillBe....Label
class ToothWillBeLabel : public ConstantLabel
{
public:
  ToothWillBeLabel();
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used);
  void clear() { _tooth=NOTOOTHSET; _property=""; }
  int _tooth;
  string _property;
};

//////////////////////////////////// MARGIN //////////////////////////////
// false if no margin info found
enum MARGIN_INFO_TYPE
{
  MNOTYPE=0,
  MDEFAULT,   // has a little info but not much
  MHEIGHT,
  MWIDTH,
  MSHOULDER
  // EPS???
  // Option 5 ???
};

enum MARGIN_POSITION
{
  MNOPOS=0,
  MAT,
  MCLOSEST, // for "as possible"
  MABOVE,
  MBELOW
};
const unsigned int NUM_MARGIN_POSITIONS=5;

enum MARGIN_REFERENCE
{
  MNOREFSET=0,
  MGINGIVA,
  MINTERFACE,
  MNEIGHBOR,
  MLINE
};

enum MARGIN_FACE
{
  MNOFACE=0,
  MALL,
  MBUCCAL, // also called facial and labial
  MLINGUAL, 
  MMESIAL,
  MDISTAL,
  MM_D,   // also called interproximal and proximal
};


class MarginInfo
{
public:
  MarginInfo( );

  bool SafetyOK();

  MARGIN_INFO_TYPE _type;
  bool _hasWrittenSpec;

      // for height
  MARGIN_REFERENCE _reference;
  MARGIN_POSITION  _position;
  double _all, _B, _L, _M, _D; // absolute offset measured from MARGIN_REF

      // for width
  EPS_SHAPE        _profile;
  double           _push;
  AC::Preference::MarginWidthOption _opt;//note this value is offset from MWIDTH_OPTION

  bool isComplete() const; // true if fields are correctly/consistently filled. So it is "read safe"
  void report() const;
  bool hasData() const; 
  string details(const char * delim);
  string DetailsHeader(const char * delim);

};

bool examineMarginInfo( const std::vector<string> & tokens, std::vector<bool> & token_used, 
                        MarginInfo & minfo, const bool & foundAlready);



/////////////////////////////////////////////////////

// very low level utilities
bool isInteger(const string & in);
bool isInteger(const char & inC);


////////////////////////////////////////////////////////////////////////
//////////////// Dictionary related ////////////////////////////////////
////////////////////////////////////////////////////////////////////////

// This is a more "modern" version of dictionary. The "main data object" below is a legacy
// For example, this "Dictionary" allows entries with two words.
class Dictionary
{
public:
  Dictionary( const string * pWords, unsigned int numWords ){ _words=pWords; _numWords=numWords;}
  const string * _words;
  unsigned int _numWords;

  bool foundInDictionary(const std::vector<string> & tokens, std::vector<bool> & token_used) const;

  size_t  findInDictionary( const string & token ) const ; // return -1 or index in _words[]

  // Returns index of word. itok is index of token. If word is in two parts, second part has index itok2
  // The token can be larger than word. Complete token does not need to be matched
  int findMatchInTokens( const std::vector<string> & tokens, int & itok, int & itok2 , int istartTok=0) const;
};





// main data object, is a map of dictionares
struct DictionaryInfo
{
  void clear()
  {
    dictionary.clear();
    numWords=0; 
    isUnit=false;
  }

  DictionaryInfo(){ clear(); }

  std::vector<string> dictionary;
  unsigned int numWords;
  bool  isUnit; // true for unit dictionaries (including string valued unit types, like profile types

  // dictionary is filled when reading from static array
  void loadFromArray( const string DArray[], const unsigned int numwords );
  // dictionary is filled when reading data from file
  void loadFromFile(const string & filepath, string & dictName);

  bool loadAdtList();

};

const DictionaryInfo NODICTIONARY;
extern std::map< string , DictionaryInfo > DICTIONARY;
void MapAllDictionaries( ); // initializes the global DICTIONARY
bool getDictionaryInfo( const string & dictionary, DictionaryInfo & info );
int findInDictionary( const string token, const DictionaryInfo & info );
bool findInDictionary( const string & nameD, const string & token);
int findSubInfoInDictionary( const string token, const DictionaryInfo & info );
int findSubInDictionary( const string dname, const string token, string & subtok ); 


class DictionaryUsage
{
public:
  
  // any ctor will work that initializes the same variables.
  DictionaryUsage(  const string dictName  )
    : _header( dictName+" Words:" )
  {
    getDictionaryInfo(dictName, _info);
    _Dictionary = _info.dictionary;
    _NumWords = _info.numWords;
    for(unsigned int i=0; i<_NumWords; i++)
      _used.push_back(false);
  };

  string word( unsigned int n){ if(n<_NumWords) return _Dictionary[n]; else return "";}

  void clear()
  {
    for(unsigned int i=0; i<_NumWords; i++)
      _used[i] = false;
  };

  unsigned int numWordsFound()
  {
    unsigned int count = 0;
    for(unsigned int i=0; i<_NumWords; i++)
      count += (unsigned int)_used[i]; // adds 1 or 0
    return count;
  }

  void ReportMyWords( const std::vector<string> & tokens, std::vector<bool> & tok_used  );

  std::vector<bool>_used;

  std::vector<string> _Dictionary;
  DictionaryInfo _info;
  unsigned int _NumWords;
  string _header;
};


////////////////////////////////////////////////////////////////////////
//////////////// NotesWorld related classes ////////////////////////////
////////////////////////////////////////////////////////////////////////
class CaseWorld;
class MarginInfo; // too big to be a single WorldLabel
class Preference;

// This is supposed to be a reporting tool. Responsible for output format
struct DecisionResult
{
  bool isReadSafe; // means all design fields from note have been consumed by WorldLabels
                   // So no design info is lost by reading DecisionResult.
  bool isComm;
  bool isBox;
  bool isShipping;
  bool isHistory;
  bool isADT;
  bool isDesign;
  bool isAlarm;

  // summarizing the state of the subsequent world labels
  bool hasOccC;
  bool hasOpt5;
  bool hasOpt6;
  bool hasEPS;
  bool hasMarginInfo;


  // come from world labels
  int  tooth;
  MarginInfo  minfo;
  double      OccClearanceVal;
  EPS_SHAPE   EPSshape;  


  // these fields are not summarized (yet) in decision.Report() or other
  bool hasLaterOrder;
  bool hasLaterOrderWithExtraText;
  bool hasLaterOrderWithCannedText;   // "canned" means autogenerated
  bool hasLaterOrderWithRescan;
  bool hasLaterOrderBadFormat;

  DecisionResult()
  { 
    isReadSafe = false;

    isComm=false;
    isBox=false;
    isShipping=false;
    isHistory=false;
    isADT=false;
    isDesign=false;
    isAlarm = false;

    // labels
    OccClearanceVal = NOVAL;
    EPSshape        = EPSNOTSET;

    // label summary
    hasOccC = false;
    hasOpt5 = false;
    hasOpt6 = false;
    hasEPS = false;
    hasMarginInfo = false;

    hasLaterOrder = false;
    hasLaterOrderWithExtraText = false;
    hasLaterOrderWithCannedText = false;
    hasLaterOrderWithRescan = false;
    hasLaterOrderBadFormat = false;

    tooth = NOTOOTHSET;
  }

  void Block()
  {
    isAlarm = true;
  }
      
  bool hasInfo( ) const 
  {
    return (isComm || isBox || isShipping || isHistory || isADT || isDesign || isAlarm );
  }

  void Report(const string & inputNote, const CaseWorld & world);

  string SummaryHeader(const char * delim );
  string Summary(const char * delim);

  string DetailsHeader( const char * delim);
  string DesignDetails(const char * delim);

  std::string fillPreference(Preference& pref, size_t_int tooth) const;

  /// fill margin height info from the results of note reading
  std::string fillMarginHeightPreference(Preference& pref, const MarginInfo& minfo) const;

  /// fill margin width info (including EPS shape) from the results of note reading
  std::string fillMarginWidthPreference(Preference& pref, const MarginInfo& minfo) const;

  /// fill eps shape info from the results of note reading
  std::string fillEPSPreference(Preference& pref, EPS_SHAPE epsShape) const;

};

////////////////////////////////////////////////////////////////////////////////////////////////

// These "worlds" are roughly parallel to dictionaries but these are the MEANINGS
// wheras the dictionaries are the TEXT which needs to be converted to meaning
// But the first one (NotesWorld) is a "parent" meta world, with text-to-meaning relations
class NotesWorld
{
public:
  NotesWorld() { _wordCount = 0; };

  virtual void clear() { _wordCount = 0; };

  unsigned int _wordCount; // counts words used relavant to this world
};

class ADTWorld : public NotesWorld { ; };
class PoliteWorld : public NotesWorld { ; };
class CommWorld : public NotesWorld { ; };
class BoxWorld : public NotesWorld { ; };
class ShippingWorld : public NotesWorld 
{ 
public:
  ShippingWorld() { _imperativeCount = 0; };
  unsigned int _imperativeCount;
};
class HistoryWorld : public NotesWorld { ; };
class SiteWorld : public NotesWorld { ; };
class AbutmentWorld : public NotesWorld { ; };

class DesignWorld : public NotesWorld 
{ 
public:  
  DesignWorld(){ NotesWorld::clear();_intCount=0; _decimalCount=0; _unitsCount = 0; _weakCount=0; _alarmCount=0;
                 _materialsCount=0; _hasRx = false;};

  void clear() { NotesWorld::clear();
                 _intCount=0; _decimalCount=0; _unitsCount = 0; _weakCount=0; _alarmCount=0; 
                 _materialsCount=0; 
                 _abutment.clear(); _site.clear(); _minfoV.clear(); _tooth=NOTOOTHSET; _hasRx = false;
                 _occL.clear();
                 _epsL.clear();
                 _optN.clear();
                 _laterOrderL.clear();
                 _bigAbutment.clear();
                 _POI.clear();
                 _toothWillBe.clear();
               };

  AbutmentWorld _abutment;
  SiteWorld     _site; 
  unsigned int _intCount;
  unsigned int _decimalCount;
  unsigned int _unitsCount; // needs eliminate when unit dictionarty has better usage
  unsigned int  _weakCount;
  unsigned int  _alarmCount;
  unsigned int _materialsCount;

  //Design World Labels
  bool hasKnownLabels();
  bool hasKnownLabelsProcessed();

  OccClearanceLabel _occL;
  EPSLabel          _epsL;
  OptionNLabel      _optN;
  LaterOrderLabel   _laterOrderL;
  BigAbutment       _bigAbutment;
  PathOfInsertion   _POI;
  ToothWillBeLabel  _toothWillBe;
  bool              _hasRx;

  vector< MarginInfo > _minfoV; // it is a vector cuz it can be read in a bit at a time

  int _tooth;

};

// A container class for the other "Worlds"
// This also contains hanlding of the note (DoIt() ) and of results
// Note that there is only English dictionary.
class CaseWorld : public NotesWorld
{
public:
  CaseWorld() {
    MapAllDictionaries();
    clear();
  }

  void clear();

  // a high level interface
  DecisionResult readNote( const string & note, const size_t_int & caseno );


  // clears then fills the dictionary counts
  void DoIt(const string & noteIn, const std::vector<int> & teeth );
  // applies logic to the word counts
  DecisionResult Decision();


  enum { CURRENT, REMAKE, LATER, FUTURE };

  // Worlds
  PoliteWorld    _polite;
  CommWorld      _comm;
  BoxWorld       _box;
  ShippingWorld  _shipping;
  HistoryWorld   _history;
  DesignWorld    _design;
  ADTWorld       _adt;

// TEMP. TO MOVE TO PARSER
  bool _hasEquals;
  bool _hasAtSymbol;
  bool _hasSpecialAlarm;

  bool _haveSafetyDoubt;

}; 

///////////////////////////////////////////////////
/// NEW MARGIN IMPLEMENTATION //////////////////////
///////////////////////////////////////////////////
enum MHEIGHT_REF
{
  aMNOREF=0,
  aMGINGIVA,  // the default, if not mentioned at all
  aMINTERFACE,
  aMNEIGHBOR,
  aMLINE
};
const unsigned int NUM_MHEIGHT_REFS=5;

/////////////////////////////////////////////////////
enum MHEIGHT_REL
{
  aMNOREL=0,
  aMAT,    
  aMHI,    
  aMLO,
  aMABOVE,
  aMCLOSEST,
  aMBELOW
};
const unsigned int NUM_MHEIGHT_RELS=7;

/////////////////////////////////////////////////
enum M_AMT
{
  aMNOAMT=0,
  aMVALUE,
  aMJUST,    
  aMASPOSSIBLE,
};

const unsigned int NUM_M_AMTS=4;

// ATTN!!!!! these are offset by -1 from usual values
// eg SUPPORT_TISSUE=(aSUPPORT_TISSUE- 1)
enum MWIDTH_OPTION
{
  aMNOOPTION=0,
  aFULL_ANATOMICAL_DIMENSIONS,   //"fad"
  aCONTOUR_SOFT_TISSUE,          //"cst"
  aSUPPORT_TISSUE,               //"st"
  aNO_TISSUE_DISPLACEMENT        //"ntd" 
};
const unsigned int NUM_MWITDH_OPTIONS=5;

///////////////////////////////
enum MFACE
{
  aMNOFACE=0,
  aMALL,
  aMBUCCAL, // also called facial and labial
  aMLINGUAL, 
  aMMESIAL,
  aMDISTAL,
  aMM_D,   // also called interproximal and proximal
};
const unsigned int NUM_MFACE=7;

////////////////// MARGIN HEIGHT ///////////
////////////////////////////////////////////
class MarginHeightSpec 
{
public:
  MarginHeightSpec(){ clear(); }
  void clear() { _ref = aMNOREF; _rel=aMNOREL; _amt=aMNOAMT; _value=NOVAL; _face =aMNOFACE; _hasWrittenSpec=false; _hasMarginFeature=true;};
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used, int istartTok=0 );
  bool Overlay( const MarginHeightSpec & hspec);
  bool isComplete(bool hasMarginFeature);

  // interfaces to MarginInfo class
  MarginInfo convertToMarginInfo();
  double convertToOffset();

  MHEIGHT_REF _ref;
  MHEIGHT_REL _rel;
  M_AMT _amt;
  double _value;

  MFACE _face;

  bool _hasWrittenSpec;
  bool _hasMarginFeature;
};

//////////////////////////////////
///////////// MARGIN WIDTH /////////
class MarginWidthSpec
{
public:
  MarginWidthSpec(){ clear(); }
  void clear(){ _opt = aMNOOPTION; _amt=aMNOAMT; _push=NOVAL; _face = aMNOFACE; _hasWrittenSpec=false; _profile=EPSNOTSET;};
  void readTokens( const std::vector<string> & tokens, std::vector<bool> & token_used, int startTok=0 );
  bool isComplete(bool hasMarginFeature);
  bool isConsistent();
  bool Overlay( const MarginWidthSpec & wspec);

  // interfaces to MarginInfo class
  MarginInfo convertToMarginInfo();
//  double convertToOffset();

  MWIDTH_OPTION _opt;
  M_AMT _amt;
  double _push;
  EPS_SHAPE _profile;

  MFACE _face;

  bool _hasWrittenSpec;

};
////////////////////////
// interface methods
bool getMarginSpecs(const std::vector<string> & tokens, std::vector<bool> & INtoken_used,
                    std::vector<MarginHeightSpec> & H,
                    std::vector<MarginWidthSpec> & W );

bool collapseMarginInfo(const std::vector<MarginHeightSpec> & H, const std::vector<MarginWidthSpec> & W, 
                        MarginInfo & Minfo);

bool hasWrittenSpec(const std::vector<string> & tokens, std::vector<bool> & token_used);


////////////////////////////////////
// need this for use in VAD
string getCustomerNoteFromCase( size_t_int caseno );

string getProductionNoteFromCase( size_t_int caseno );

void getAllToothNumbers( const size_t_int & caseno, std::vector<int> & tooth);

string getCustomerCountryCode( const size_t_int & caseno );

size_t USTooth2EUTooth( const size_t toothNumber );
void replaceEUToothNumbers( const string noteIn, string & noteOut, std::vector<int> caseteeth );
bool isSafePossibility(const std::vector<string> & tokens, std::vector<bool> & tokenUsed);




} // end namespace AC

#endif // _autonotes_h_