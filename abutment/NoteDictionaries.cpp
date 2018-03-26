/*
 * Copyright 2013, DENTSPLY Implants, All Rights Reserved.
 * This file contains proprietary information, and may not be viewed, copied,
 * distributed, sold, published, or disseminated without express permission
 * of DENTSPLY Implants.
 */

#pragma warning(disable: 4786)

#include <Utils/common.h> // for ToLower()
#include <Utils/DataPaths.h>
#include <Utils/Config.h>
#include <Utils/utils.h>  // for getAdtList()
#include "Notes.h"


#ifdef _DEBUG
#define new DEBUG_NORMALBLOCK
#endif

using namespace std;

#define TEXTCAST "cast" // weird. This string gives the compiler a hard time.

/*
DICTIONARIES: must be defined as follows, then must be added to MapAllDictionaries() to be
manipulated programmatically in semscanf( )
*/

namespace AC {

/////////////////////////////////////////////
// SINGLE CONCEPT dicitionaries
/////////////////////////////////////////////

//--------------------- UNIT DICTIONARIES
static const string mmD[] = 
{
"mm",
"mn", // misspelling
"millimeter"
};
const unsigned int NUMMMWORDS = sizeof( mmD ) / sizeof( string ) ;

static const string degreeD[] = 
{
"degree",
"degrees",
"°"
};
const unsigned int NUMDEGREEWORDS = sizeof( degreeD ) / sizeof( string ) ;

// descriptors of profile shapes (see enum EPS_SHAPE)
static const string profValD[] = 
{
"on", //handled as part of 2-word constant labels
"off",
"straight",
"striaght",
"srtaight",
"concave",
"convave",
"concavity",
"convex",
"ankylos",
"golf"
};
const unsigned int NUMPROFVALWORDS = sizeof( profValD ) / sizeof( string ) ;

EPS_SHAPE getEPSSHAPE( const string & shapeString )
{
  if( shapeString=="on" )
  {
    return EPSON;
  }
  else if( shapeString=="off" )
  {
    return EPSOFF;
  }
  else if( shapeString=="straight" || shapeString=="srtaight" || shapeString=="striaght")
  {
    return EPSSTRAIGHT;
  }
  else if( shapeString=="concave" || shapeString=="golf" || shapeString=="convave" || shapeString=="concavity")
  {
    return EPSCONCAVE;
  }
  else if( shapeString=="convex" )
  {
    return EPSCONVEX;
  }
  else if( shapeString=="ankylos" )
  {
    return EPSCONCAVE;
  }
  else
  {
    return EPSNOTSET;
  }
}

string getEPSShapeString( const EPS_SHAPE & shape )
{
  if( shape==EPSON )
    return "on";
  else if( shape==EPSOFF )
    return "off";
  else if( shape==EPSSTRAIGHT )
    return "straight";
  else if( shape==EPSCONCAVE )
    return "concave";
  else if( shape==EPSCONVEX )
    return "convex";
  else // shape==EPSNOTSET or othe
    return "";
}




//------------------ SINGLE WORD DICTIONARIES (synonym lists)

static const string clearanceD[] = 
{
"clearance",
"clerance",
"clearence",
"clearnce",
"room",
"height",
//"from", "from opposing",
"space"
};
const unsigned int NUMCLEARANCEWORDS = sizeof( clearanceD ) / sizeof( string ) ;


static const string occlusalD[] = 
{
"occlusion",
"occlusal",
"occlusial",
"occ",
"occl",
"opposing",
"opposer",
"incisal",
"opp"
};
const unsigned int NUMOCCLUSALWORDS = sizeof( occlusalD ) / sizeof( string ) ;


static const string epsD[] = 
{
"eps",
"esp",
"ets",
"emergence",
"emergense",
"emergance",
"emmergence",
"emergency",
"profile",
"profiling"
};
const unsigned int NUMEPSWORDS = sizeof( epsD ) / sizeof(string);


static const string negationD[] = 
{
"no",
"not",
"nothing",
"don't",
"avoid"
};
const unsigned int NUMNEGATIONWORDS = sizeof( negationD ) / sizeof(string);

static const string optionD[] = 
{
"option",
"opption",
"potion",
"position", //?
"opt",
"type"
};
const unsigned int NUMOPTIONWORDS = sizeof( optionD ) / sizeof(string);

static const string fiveD[] = 
{
"5",
"#5",
"five"
};
const unsigned int NUMFIVEWORDS = sizeof( fiveD ) / sizeof(string);

static const string sixD[] = 
{
"6",
"#6",
"six"
};
const unsigned int NUMSIXWORDS = sizeof( sixD ) / sizeof(string);

static const string optionNumberD[] = 
{
"5",
"#5",
"five",
"6",
"#6",
"six"
};
const unsigned int NUMOPNUMWORDS = sizeof( optionNumberD ) / sizeof(string);


/////////////////////////////////////////////////////////////

bool getDictionary( string name, const string * & dictionary, unsigned int & NumWords )
{
  NumWords = 0;
  if( name=="mmD" )
  {
    dictionary  = &mmD[0];
    NumWords = NUMMMWORDS;
    return true;
  }
  else if( name=="degreeD" )
  {
    dictionary  = &degreeD[0];
    NumWords = NUMDEGREEWORDS;
    return true;
  }
  else if( name=="clearanceD" )
  {
    dictionary  = &clearanceD[0];
    NumWords = NUMCLEARANCEWORDS;
    return true;
  }
  else if( name=="occlusalD" )
  {
    dictionary  = &occlusalD[0];
    NumWords = NUMOCCLUSALWORDS;
    return true;
  }

  return false;
}

//////////////////////////////////////////////////////////////////////////
// TOPIC DICTIONARIES (not that well defined, functional rather than pure)
//////////////////////////////////////////////////////////////////////////
static const string MaterialsDictionary[] =  
{
"metal",
"titanium",
"ti",
"zirconium",
"zirconia",
"zr",
"zirc",
"ceramic",
"Emax",
"pfm",
"pfm'",
"porcelain",
"porcelian",
"porc",
"cement",
"screw",
"access",
"fgc",  // full gold crown
"gold"
};

const unsigned int NUMMATERIALSWORDS = sizeof( MaterialsDictionary ) / sizeof( string ) ;


static const string DullDictionary[] =
{
"unit",         // these are convenient to maske
"can",       
"only",
"s",
"is",
"was",
"also",
"a",
"help",
"to", 
"the",
"etc",
"ATTN",
"give",
"any",
"disinfected",
"cdc",
"guideline",
"i",
"know",
"that",
"there",
"isn't",
"hello",
"greeting",
"we",
"have",
"this"
};
const unsigned int NUMDULLWORDS = sizeof( DullDictionary ) / sizeof( string ) ;


// This dictionary is used for SEMO only and is applied just before final dreg counting.
// You can put design words or others in here without fear of breaking what happens before this 
// dictionary is used.
static const string SEMODullDictionary[] =
{
  "are",
  "in",
  "the",
  "thank",
  "you",
  "thankyou",
  "thanks",
  "thanx",
  "tx",
  "thx",
  "copy",
  "wax",
  "demo",
  "for"
};

const unsigned int NUMSEMODULLWORDS = sizeof( SEMODullDictionary ) / sizeof( string ) ;

static const string PoliteDictionary[] =
{
"thanks",
"thankyou",
"thank",
"thanx",
"you",
"thx",
"please",
"pls",
"plz",
"happy",
"holiday",
};
const unsigned int NUMPOLITEWORDS = sizeof( PoliteDictionary ) / sizeof( string ) ;


static const string CommDictionary[] =
{
"call",
"email",
"contact",
"talk",
"question",
"?",
"?'"  // as in ?'s
};
const unsigned int NUMCOMMWORDS = sizeof( CommDictionary ) / sizeof( string ) ;

static const string ADTDictionary[] =
{
"Martin",
"Edgar",
"Dave",
"Wenzel",
"Szyumlo",
"Stephanie",
"Christina",
"Christine",
"Andrew",
"Terri",
"Luis",
"Jon"
};
const unsigned int NUMADTWORDS  = sizeof( ADTDictionary ) / sizeof( string ) ;


static const string ImperativeDictionary[] =
{
"imperative",
"concern",
"careful",
"urgent",
"must",
"not",
"no",
"avoid",
"decide",
"approve",
"aprove",
"approval",
"appoval", //?
"discuss",
"verify",
"verifies",
"asap",
"view",
"review",
"prior",
"before",
"shade", // together with repeat in Shipping, causes ship+impertative
"check",
"need"
};
const unsigned int NUMIMPERATIVEWORDS = sizeof( ImperativeDictionary ) / sizeof( string ) ;

static const string HistoricalDictionary[] =
{
"OE",
"dr",
"dr.",
"dentist",
"he",
"she",
"doctor",
"patient",
"lost",
"pour",
"forgot",
"may",
"will",
"be",
"being", //????
"end",
"had",
"future",
"been",
"after",
"using",
"extract",
"speaking",
"change",
"order",
"late",   // "order" modifiers
"later",
"remake",
"redo"
};
const unsigned int NUMHISTORICALWORDS = sizeof( HistoricalDictionary ) / sizeof( string ) ;



static const string ShippingDictionary[] =
{
"case",
"design",
"ship",
"send",
"deliver",
"delivery",
"process",
"careful",
"damage",
"fedex",
"photos",
"mill",
"milling",
"fed",
"ups",
"shade",
"back",
"together",
"return",
"rush",
"hurry",
"asap",
"extra",
"xtra",
"track",
"delay",
"quickly",
"expedite",
"due",
"finish",
"billable",
//"do", //???
"lab",
"monday",
"tuesday",
"wednesday",
"thursday",
"friday"
};
const unsigned int NUMSHIPPINGWORDS = sizeof( ShippingDictionary ) / sizeof( string ) ;


static const string MetaDentalDictionary[] =
{
"ideal",
"correct",
"best",
"best",
"rx",
"form",
"cpp",
"spec",
"default",
"custom",
"prescription",
"case",
"design",
"model",
"mock",
TEXTCAST,
"diagnostic",
"mandibular",
"maxillary",
"removable",
"wax",
"wax_up",
"arch",
"registration"
};
const unsigned int NUMMETADENTALWORDS = sizeof( MetaDentalDictionary ) / sizeof( string ) ;

static const string BoxDictionary[] =  
{
  // noun
  "model",
  "die",
  "wax",
  "wax_up",
  "waxup",
  "cast",
  "case",
  "articulate",
  "articulator",
  "artic",
  "counter",
  "scan",
  "registration"
  "line",
  "mark",
  //adjective
  "diagnostic",
  "removable",
  "bite",
//  "red",
//  "blue",
//  "black",
  // verbs
  "image",
  "pic",
  "sent",
  "sending",
  "include",
  "enclose",
  "provide"
};
const unsigned int NUMBOXWORDS = sizeof( BoxDictionary ) / sizeof( string ) ;


// stores weak design indicators
static const string WeakDesignDictionary[] =  
{
//"implant",
"smile",
"tiss",
"strong",
"bite",
"registration",
"restoration",
"resteration",
"abutment",
"abut",
// verbs
"design"
"note", // occurs in non-design contexts
"see",
"consider",
"take",
"make",
"edit",
"build",
"use",
"fabricate"
};
const unsigned int NUMWEAKDESIGNWORDS = sizeof( WeakDesignDictionary ) / sizeof( string ) ;


// some design words appear by themselves with or without modifiers. So the needed relationships
// which are present in design specs, take the form of a relation with itself, so word count is 
// different for these words
// these alarms will be added to the set of imperative words - all are used to flag the need for a human reader.
static const string AlarmDictionary[]=
{
  "°", // CleanParse() should separate this from adjacent #
  "ø", // same
  "corefile",
  "core",
  "hex",
  "senare",     //for incorrect SEMO "Later Order"
  "complaint",
  "complain",
  "???",        // some foreign language characters end up like this
  "????",
  "?????",
  "??????",
  "???????",
  "protrusive",
//  "rescanned", // add this if you want Later Order rescanned *** to be considered an alarm. Note alread handled as a criteria item
  "conus",
  "tissue",
  "resubmit",
  "submit",
  "mimic",
  "mirror",
  "copy",
  "match",
  "angle",   // the verb
  "drawing", // customer drawing is important (should move to seeRx label)
  "diagram",
  "preference",
  "mistake",
//  "ignore",  // indicates note overrides order. [So one reading is important you bail????? hold off on that]
  "remake",
  "redo",
//  "sure",  // "Make sure"... but unfortunatetly also "I'm no sure"....could create a ConstLabel
  "stock", // sorry, these are hot button words
  "pfm",
  "pfm'",
  "emax",
  "extract",
  "drawn",
  "molar",
  "premolar",
  "pre-molar",
  "primolar",
  "bicuspid",
  "bisuspid",
  "sulcus",
  "fossa",
  "bridge", // or in design??
  "brigde",
  "splint",
  "crossbite",
  "cross-bite",
  "diastema",
  "diestema",
  "diastama",
  "axis",
  "draw",
  "like",  // counts unless appearing in "would like" (see ConstantLabel wouldLike( ))
  "parallel",
  "paralell",
  "parrallel",
  "parallell",  // standard misspelling
  "paralel",
  "parelel",   // this is getting ridiculous, how about parelall
  "parrellel",
  "parrellel",
  "parellell",
  "parallelism",
  "parralle",
  "paarallel",
  "eps",        // appear as single words occasionally
  "esp",
  "ets",
  "straight",
  "striaght",
  "srtaight",
  "concave",
  "convave", // I interpret it as concave (one letter wrong) not convex (three letters wrong)
  "convex",
  "cantilever",
  "cantlever",
  "cantilever",
  "cantiliver",
  "cantilevering", // does not capture all the mis-spellings
  "catilever",
  "chamfer",
  "champher",
  "anatomical",
  "anatomic",
  "anotomical",
  "bevel",     // in phrase "NO BEVEL", there is nothing else to go on.
  "blanch",     // in "Please blanch"
  "blanching",
  "gingival",  // put before shortened version, so "l" is not stripped during cleaning
  "equigingival",
  "supgingival",
  "subgingival",
  "supragingival",
  "supra-gingival",
  "sub-gingival",
  "subginival",
  "supergingival",
  "gingiva",
  "sub-g",
  "subging",
  "supra-g",
  "sub",
  "golf",  // this is stupid
  "correction", // used in relation to tooth number confusions
  "groove",   // in "retentive groove" or "anti-rotational groove"
  "retention",
  "retentive",
  "hold",
  "bad",
  "automate",
  "mill",
  "milling",
  "resolution",
  "lap",
  "molded",
  "screwmentable", //huh?
  "mentable",
  "moulded",
  "shoulder",  // this should raise an alarm until we can read shoulder design statements safely.
  "sholder",
  "shoulders",
  "pin",
  "section",
  "veneer",
  "sleeve",
  "cap",
  "small",
  "peak",
  "valley",
  "stump",
  "stub",
  "bone",
  "cej",
  "smooth"
};
const unsigned int NUMALARMWORDS = sizeof( AlarmDictionary ) / sizeof( string ) ;


// special design words that can occur in a self relation (not a relation between two things)
// sometimes with no modifier...like "EPS"
static const string DesignSDictionary[] =  
{
"tissue",
"study", // "follow study model" is a design statement
"extra",
"pre_op",
"margin",
"collar",
"taper",
"shoulder",
"chamfer",
"champher",
"core",
"bellied",
"belly",
"emergence",
"emergense",
"emergency", //in europe
"emmergence",
"eps",
"esp",  // common mis-spelling
"profile",
"contour",
"wall",
"option",
"opt",
"placement",
"show",
"showing",
"crown",
"concave", // used alone
"convex",
"bucc",
"buc",
"buck",
"buccal",
"baccal",
"buccul",
"bucca",
"bucall",
"buccally",
"baccal",
"buccual",
"lingual",
"palatinal",
"palatal",
"palate",
"ling",
"lin",
"lingually",
"palatinal",
"palatal",
"facial",
"facially",
"mes",
"mesial",
"meaisl",
"messial",
"mesially",
"mes",
"dist",
"distal",
"distaal",
"distally",
"labial",
"labially",
"palatally",
"connection",
"edge",
"embrasure",
"cusp",
"alignment"
};
const unsigned int NUMDESIGNSWORDS = sizeof( DesignSDictionary ) / sizeof( string ) ;


static const string DesignDictionary[] =  
{
"blanch",
"retained", // (I know, but it behaves like a material)
"preparation",
"provisional",
"fill",
"German",
"option",
"opt",
"tooth",
"site",
"teeth",
"stock",
"jaw",
"gingiva",
"gingival",
"subgingival",
"supragingival",
"supra-gingival",
"sub-gingival",
"supergingival",
"sub-g",
"supra-g",
"sub",
"gum",
"vestibule",
"curve",
"collar",
"cingulum",
"crest",
"ridge",
"gingiva",
"ging",
"crests",
"occlusion",
"occlusal",
"occlusial",
"occ",
"occl",
"opposing",
"opp",
"clearance",
"clerance",
"clearence",
"post",
"platform",
"bicuspid",
"bisuspid",
"canine",
"incisor",
"incisal",
"interface",
"gearing",
"prep",
"prepped",
"mastication",
"channel",
//"cantilever",
"anatomic",
"root",
"pontic",
"bow",
"hole",
"gap",
"ridge",
"space",
"room",
"groove",
"temp",
"healing",
"healingabut",
"healingabutment",
"support",
// adjectives
"forward",
"palatal",
"central",
"lateral",
"proximal",
"interproximal",
"protrusive",
"B/F",
"F/B",
"M/D",
"B",
"M",
"F",
"D",
"L",
"mesial",
"distal",
"lingual",
"palate",
"palatal",
"palatinal",
"buc",
"buccal",
"baccal",
"buck",
"all sides",
"upper",
"lower",
"analog",
"anolog",
"anterior",
"posterior",
"occlusal",
"telescope",
"proximal",
"interproximal",
"bevel",
"fare",
"flare",
"flair",
"conicity",
"conical",
"class I",
"class II",
"class III",
// cast or model specific instructions
"line",
"mark",
"red",
"blue",
"black"
};
const unsigned int NUMDESIGNWORDS = sizeof( DesignDictionary ) / sizeof( string ) ;

static const string SizePosDictionary[] =
{
// generic words
"+", // as an isolated token means "positive"
//"size",
"dimension",
"direction",
"shape",
"more",
"much",
"slight",
"tall",
"huge",
"big",
"bigger",
"large",
"larger",
"small",
"smaller",
"tiny",
"little",
"long",
"length",
"lenght",
"short",
"wide",
"wider",
"width",
"deep",
"deeper",
"depth",
"height",
"heavy",
"full",
"soft",
"sharp",
"sarp",
"round",
"flat",
//"counter",
"axial",
"angulation",
"inclination",
"rotation",
"neighbor",
"neighboring",
"adjacent",
"adjecent",
"narrow",
"narrower",
"thick",
"accurate",
"open",
"closed",
"negative",
// shape words
"rectangle",
"rectangular",
"circle",
"circular",
"oval"
};
const unsigned int NUMSIZEPOSWORDS = sizeof( SizePosDictionary ) / sizeof( string ) ;


static const string DesignVerbDictionary[] =
{
"lingualize",
"labialize",
"position",
//"keep",
"bring",
"scoop",
"vent",
"trim",
"tilt",
"angle",
"lean",
"leave",
"pull",
"offset",
"move",
"push",
"close", // as in the verb "close the door" but unfortunately not the relation "close to the door" 
"expand",
"extend",
"place",
"fill",
"soften",
"seat",
"connect",
"correct" // unfortunately the adjective "correct" is near meaningless
};
const unsigned int NUMDESIGNVERBWORDS = sizeof( DesignVerbDictionary ) / sizeof( string ) ;

static const string UnitsDictionary[] =
{
"degree",
"mm",
"mn", // misspelling
"millimeter"
};
const unsigned int NUMUNITSWORDS = sizeof( UnitsDictionary ) / sizeof( string ) ;


static const string RelationDictionary[] =  
{
"minimal",
"min",
"minimize",
"max",
"maximal",
"maximize",
"low",
"high",
"lowest",
"highest",
"visible",
"sub",
"sub_g",
"sbgingival",
"subcrestal",
"supra",
"over",
"at",
"@",
"up",
"down",
"under",
"above",
"below",
"between",
"level",
"align",
"even",
"follow",
"following",
"toward",
"allow",
"copy",
"according", // after design...according
"match",
"follow",
"room",
"away",
"accommodate",
"guide",
"towards",
"near",
"far",
"fit",
"harmony",
"adjust",
"vertical",
"contralateral",
"reverse",
"center",
"distance",
"side",
"impingement",
"pressure",
"presure",
"compression",
"displacement",
"displacment",
"displace",
"diplace", //spelling
"tight",
"close", // disambiguate with "close to"???
"light",
"on"
};
const unsigned int NUMRELATIONWORDS = sizeof( RelationDictionary ) / sizeof( string ) ;
///////////////////////////////////////////////////////////////
////////////////////// MARGIN DICTIONARIES ///////////////
//Need some dictionaries
static const string MarginFaceD[] = 
{
"all",
"360", //?
//"around",
"rest",    // as in "...the rest of the margins..."
"other",   // as in "...the other margins...."
"buccal",
"buc",
"bucc",
"buccul",
"bucca",
"bucall",
"baccal",
"buck",
"B",
"lingual",
"palatinal",
"ling",
"B/F",
"B&F",
"buccal/facial",
"f/b",
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
"values",
"value"
};
const unsigned int NUMMARGINFACEWORDS = sizeof( MarginFaceD ) / sizeof( string ) ;


// CAUTION!!!!!!! This dictionary is sliced and diced in examineMarginInfo(). Any changes
// here need to be paralleled over there
static const string MarginHeightReferenceD[] = 
{
  // interface
"interface",
"implant",
  // neighbor
"neighbor",
"neighboring",
"adjacent",
"surrounding",
 // line
"line",
"mark",
  // tissue
"tissue", // used in both height and width descriptions
"gingiva",
"gingival",
"gum",
"crest",
"supgingival", // these words contain a position and a reference
"subgingival",
"supragingival",
"supra-gingival",
"sub-gingival",
"supergingival",
"sub-g",
"supra-g",
"subg",
"sub",
"subging",
"subginival",
"supra"
};
const unsigned int NUMMARGINHEIGHTREFWORDS = sizeof( MarginHeightReferenceD ) / sizeof( string ) ;


static const string MarginHeightPositionD[] = 
{
  // at
"level",
"even",
"at",
"flush",
"@",
  // near
"close",
"closest",
  // neighbor
"follow",
  // above
"above",
"over",
"positive",
"high",
"height",
"hiegth", //slob!
"up",
  // below
"below",
"depth",
"deep",
"low",
"lowest",
"negative",
"under",
"down"
};
const unsigned int NUMMARGINHEIGHTPOSWORDS = sizeof( MarginHeightPositionD ) / sizeof( string ) ;


static const string MarginWidthD[] = 
{
"tissue",
"width",
"support",
"sculpt",
"fill",
"full",
"flare",
"pressure",
"press",
"blanch",
"blanching",
"push",
"out",
"expand",
"impinge",
"impingement",
"displacement",
"displace"
};
const unsigned int NUMMARGINWIDTHWORDS = sizeof( MarginWidthD ) / sizeof( string ) ;


/////////////////////////////////////////////////////




///////////////////////////////////////////
// METHODS
//////////////////////////////////////////

// ONE GLOBAL DICTIONARY CONTAINER, initialized by MapAllDictionaries()
std::map< string , DictionaryInfo > DICTIONARY;

// associates a string name to each dictionary, for global access
// MUST BE CALLED ON PROGRAM INITIALIZATION (see AutoNotes constructor)
void MapAllDictionaries( )
{
  DictionaryInfo info;
  info.isUnit = true;
  DICTIONARY.insert( pair<string,DictionaryInfo>( "null", info ) );


  // single word dictionaries
  info.clear();
  info.loadFromArray( mmD, NUMMMWORDS );
  info.isUnit    = true;
  DICTIONARY.insert( pair<string,DictionaryInfo>( "mm", info ) );


  info.clear();
  info.loadFromArray( degreeD, NUMDEGREEWORDS );
  info.isUnit    = true;
  DICTIONARY.insert( pair<string,DictionaryInfo>( "degree", info ) );

  // for eps
  info.clear();
  info.loadFromArray(profValD, NUMPROFVALWORDS);
  DICTIONARY.insert( pair<string,DictionaryInfo>( "profile", info ) );


  info.clear();
  info.loadFromArray(clearanceD, NUMCLEARANCEWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "clearance", info ) );

  info.clear();
  info.loadFromArray(occlusalD, NUMOCCLUSALWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "occlusal", info ) );

  info.clear();
  info.loadFromArray(epsD, NUMEPSWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "eps", info ) );

  info.clear();
  info.loadFromArray(optionD, NUMOPTIONWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "option", info ) );

  info.clear();
  info.loadFromArray(negationD, NUMNEGATIONWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "negation", info ) );

  info.clear();
  info.loadFromArray(fiveD, NUMFIVEWORDS);
  DICTIONARY.insert( pair<string,DictionaryInfo>( "five", info ) );

  info.clear(); 
  info.loadFromArray(sixD, NUMSIXWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "six", info ) );

  info.clear();
  info.loadFromArray(optionNumberD, NUMOPNUMWORDS);
  DICTIONARY.insert( pair<string,DictionaryInfo>( "optionnumber", info ) );

  // margin dictionaries
  info.clear();
  info.loadFromArray(MarginFaceD, NUMMARGINFACEWORDS);
  DICTIONARY.insert( pair<string,DictionaryInfo>( "mhface", info ) );


  info.clear();
  info.loadFromArray( MarginHeightReferenceD, NUMMARGINHEIGHTREFWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "mhref", info ) );


  info.clear();
  info.loadFromArray(MarginHeightPositionD, NUMMARGINHEIGHTPOSWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "mhpos", info ) );


  info.clear();
  info.loadFromArray(MarginWidthD, NUMMARGINWIDTHWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "mwidth", info ) );


  // others
  info.clear();
  info.loadFromArray(DullDictionary ,NUMDULLWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "dull", info ) );

  info.clear();
  info.loadFromArray(SEMODullDictionary, NUMSEMODULLWORDS );
  DICTIONARY.insert(pair<string,DictionaryInfo>( "semodull", info ) );


  info.clear();
  info.loadFromArray( MaterialsDictionary , NUMMATERIALSWORDS);
  DICTIONARY.insert( pair<string,DictionaryInfo>( "material", info ) );

  info.clear();
  info.loadFromArray(PoliteDictionary, NUMPOLITEWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "polite", info ) );

  info.clear();
  info.loadFromArray(CommDictionary, NUMCOMMWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "comm", info ) );

  // -----------ADT names are loaded from db type=NoteReader name=AdtList.
  info.clear();
  if( ! info.loadAdtList() )
  {
    info.clear();
    info.loadFromArray(ADTDictionary, NUMADTWORDS );
  }
  DICTIONARY.insert( pair<string,DictionaryInfo>( "adt", info ) );
  //----------------------------


  info.clear();
  info.loadFromArray(ImperativeDictionary, NUMIMPERATIVEWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "imperative", info ) );

  info.clear();
  info.loadFromArray( HistoricalDictionary, NUMHISTORICALWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "history", info ) );


  info.clear();
  info.loadFromArray( ShippingDictionary, NUMSHIPPINGWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "ship", info ) );

  info.clear();
  info.loadFromArray( MetaDentalDictionary, NUMMETADENTALWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "metadental", info ) );

  info.clear();
  info.loadFromArray( BoxDictionary, NUMBOXWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "box", info ) );


  info.clear();
  info.loadFromArray(WeakDesignDictionary, NUMWEAKDESIGNWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "weakdesign", info ) );

  info.clear();
  info.loadFromArray(DesignSDictionary, NUMDESIGNSWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "designS", info ) );

  info.clear();
  info.loadFromArray(DesignDictionary, NUMDESIGNWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "design", info ) );

  info.clear();
  info.loadFromArray(DesignVerbDictionary , NUMDESIGNVERBWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "designV", info ) );

  info.clear();
  info.loadFromArray(RelationDictionary, NUMRELATIONWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "relation", info ) );

  info.clear();
  info.loadFromArray(SizePosDictionary, NUMSIZEPOSWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "sizepos", info ) );

  info.clear();
  info.loadFromArray( AlarmDictionary, NUMALARMWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "alarm", info ) );

  info.clear(); 
  info.loadFromArray(UnitsDictionary, NUMUNITSWORDS );
  DICTIONARY.insert( pair<string,DictionaryInfo>( "unit", info ) );
}


bool findInDictionary( const string & nameD, const string & token)
{
  DictionaryUsage dict( nameD );

  if( findInDictionary( token, dict._info)>=0 )
    return true;
  else
    return false;
}

bool getDictionaryInfo( const string & dictionary, DictionaryInfo & info )
{
  try
  {
    info = DICTIONARY.at(dictionary); // throws exception if no such dictionary
    return true;
  }
  catch(exception& e)
  {
    e;
    info = NODICTIONARY;
    return false;
  }
}

///////////////////////////// DictionaryUsage ////////////////////////////
// returns -1 or index of word in dictionary
int findInDictionary( const string token, const DictionaryInfo & info )
{
  string tokenL = token;
  ToLower( tokenL );

    // remove trailing "-"
  size_t_int len = tokenL.length();
  if( tokenL.c_str()[len-1]=='-' )
  {
    string temp = tokenL.substr(0, len-1 );
    tokenL = temp;
  }

  for(unsigned int i=0; i<info.dictionary.size(); i++)
  {
    string word = info.dictionary[i];
    string wordL = word;
    ToLower( wordL );
    string wordED = wordL+"ed";
    string wordD  = wordL+"d";
    string wordS  = wordL+"s";
    string wordLY  = wordL+"ly";

    if( tokenL==wordL ) // || tokenL.find(wordL)!=string::npos )
      return i;
    else if( tokenL==wordED || tokenL==wordD || tokenL==wordS || tokenL==wordLY)
      return i;

  }
  return -1;
}

// matches dictionary words to substrings of token (eg to find "mm" in "1.2mm" )
int findSubInfoInDictionary( const string token, const DictionaryInfo & info )
{
  string tokenL = token;
  ToLower( tokenL );

    // remove trailing "-"
  size_t_int len = tokenL.length();
  if( tokenL.c_str()[len-1]=='-' )
  {
    string temp = tokenL.substr(0, len-1 );
    tokenL = temp;
  }

  for(unsigned int i=0; i<info.dictionary.size(); i++)
  {
    string word = info.dictionary[i];
    string wordL = word;
    ToLower( wordL );

    if( tokenL.find( wordL )!=string::npos )
      return i;
  }
  return -1;
}

int findSubInDictionary( const string dname, const string token, string & subtok )
{
  subtok = "";

  DictionaryInfo info;
  if( !getDictionaryInfo( dname, info ) )
    return -1;

  int ret = findSubInfoInDictionary( token, info );


  if( ret>-1 )
    subtok = info.dictionary[ ret ];

  ToLower(subtok);

  return ret;
}



void DictionaryUsage::ReportMyWords( const vector<string> & tokens, std::vector<bool> & tok_used)
{
  clear();
#ifdef _DEBUG
  cout << "\n";
  cout<< _header; 
#endif
  for(unsigned int i=0; i<tokens.size(); i++)
  {
    int j;

    j = findInDictionary( tokens[i], _info );

    if( j>=0 )
    {
#ifdef _DEBUG
      cout << "\n  "<< _Dictionary[j]  << " (in "<< tokens[i] <<")" ;
#endif
      tok_used[i] = true;
      _used[j] = true;
    }
  }
}

void maskTokens(  vector<string> & token, vector<bool> token_used )
{
  for(unsigned int i=0; i<token.size(); i++)
  {
    if( i<token_used.size() && token_used[i] )
      token[i] = "dull";
  }
}

void maskPreDullTokens(  vector<string> & token, vector<bool> token_used )
{
  size_t firstDull = token.size();

  for(size_t i=0; i<token.size(); i++)
  {
    if( token[i].find( "dull" )!=string::npos )
    {
      firstDull = i;
      break;
    }
  }

  for(size_t i=0; i<firstDull; i++)
  {
    if( token_used[i] )
      token[i] = "dull";
  }

}
/////////////////////////////////////////


void DictionaryInfo::loadFromArray( const string DArray[], const unsigned int numwords )
{
  dictionary.clear();

  for(unsigned int i=0; i<numwords; i++)
    dictionary.push_back( DArray[i] );

  numWords = numwords;

}

bool DictionaryInfo::loadAdtList()
{
  std::string adtList;
  try 
  {
    adtList = AC::utils::getAdtList();
  }
  catch(...)
  {
    return false;
  }

  dictionary.clear();
  numWords = (unsigned int)DelimTokenize( adtList, dictionary, "," );

  return true;
}

void DictionaryInfo::loadFromFile(const string & filepath, string & dictName)
{
  dictName="";
  numWords=0;

  ifstream fb; 
  fb.open( filepath.c_str() );
  if( ! fb.is_open() )
    return;
  string word;

  size_t numlines=0;
  while( fb.good() )
  {
    getline( fb, word);
    if( numlines++==0 ) // save dictionary name
      dictName = word;
    else if( word.size()>0 )
      dictionary.push_back( word );
  }
  fb.close();
  
  if( dictionary.size()==0 )
    return;

  numWords = (unsigned int)dictionary.size();
}



} // end namespace AC