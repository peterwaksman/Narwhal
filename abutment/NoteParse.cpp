/*
 * Copyright 2013, DENTSPLY Implants, All Rights Reserved.
 * This file contains proprietary information, and may not be viewed, copied,
 * distributed, sold, published, or disseminated without express permission
 * of DENTSPLY Implants.
 */

/*
NoteParse.cpp
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

// replaces extra carriage return line feeds with ". "
void replaceENTER(string & text)
{
  if( text.size()<1 )
    return;

  string note = text + "\n"; // working copy, make sure it has a terminator

  string next="", newnote="";
  while(1)
  {
    size_t found=note.find( "\n" );
    if( found!=string::npos )
    {
      if( found<note.length()-1 )
        newnote += note.substr(0,found) + " ";
      else
        newnote += note.substr(0,found) + ". ";
    }
    else
    {
      newnote += next;
      break;
    }
    next = note.substr(found+1);
    note = next;
  }

  text = newnote;
}



void markDigits( const string & text, vector<bool> & isDigit )
{
  isDigit.clear();
  for(unsigned int i=0; i<text.size(); i++)
  {
    if( text[i]>0 && isdigit(text[i]) )
      isDigit.push_back(true);
    else
      isDigit.push_back(false);
  }
}

/*look for pattern 
    "#,#" (only if first char is #)
    "#,# " (only if first char is #)
    " #,# "
    followed by "mm"
*/
void  replaceEuropeanDecimals(string & text)
{
  vector<bool> isDigit;
  markDigits( text, isDigit ); // a key player.

  size_t S = isDigit.size();
  std::vector<size_t> ifound;
  size_t i;
  for(i=0; i<S; i++)   // look for pattern "#,#"
  {
    if(i+2>S-1)
      continue;

    if( isDigit[i] && text[i+1]==',' && isDigit[i+2] ) // starts with number
    {
      ifound.push_back(i);
    }
  }

  if( ifound.size()==0 ) // no pattern found
    return;

  for(size_t j=0; j<ifound.size(); j++)
  {
    i = ifound[j];
    if( i>0 && text[i-1]!=' ') // must be proceeded by ' ' unless start of text
      continue;

    // do not check at the end of the text or beyond
    if( i+5>S-1 )
      break;

    size_t pos=i+1;
    if( ( text[i+3]==' ' && text[i+4]=='m' && text[i+5]=='m' )  //"#,# mm"
      ||( text[i+3]=='m' && text[i+4]=='m' ) )                  //"#,#mm"
      text.replace(pos, 1, ".");                                // replace comma with period
  }
}



void removeParens(string & text  )
{
  // replace either " n)" or "(n)" with STDSDEPARATOR
  // DISCARDS step by step instruction indices (does not work for two digit indices)
  for(unsigned int i=0; i<text.size(); i++)
  {
    if( text[i]==')' && i==1 )
    {
      if( isdigit( text[ i-1 ] ) )
      {
        text[i-1] = ' ';
        text[i]   = ' ';
      }
    }
    else if( text[i]==')' && i>=2 )
    {
      if( isdigit( text[ i-1 ] ) && ( text[i-2]=='(' || text[i-2]==' ' ) )
      {
        text[i-2] = ' ';
        text[i-1] = STDSEPARATOR;
        text[i]   = ' ';
      }
    }
  }
  // all other parens are replaced with space
  for(unsigned int i=0; i<text.size(); i++)
  {
    if( text[i]==')' || text[i]=='(' )
      text[i] = ' ';
  }
}





// also removes semicolons
void removeCommas(string & text  )
{
  if( text.size()==0 )
    return;

  string temp="";
  unsigned int i=0;
  for( i=0; i<text.size()-1; i++)
  {
    if( text[i]==',' || text[i]==';'  )
    {
      temp += sSTDSEPARATOR;
    }
    else
    {
      temp += text[i];
    }
  }

  // for last index, only use space
  if( text[i]==',' || text[i] ==';'  )
    temp += ' ';
  else
    temp += text[i];

  text = temp;
}

// go through text with goal of replacing "." by sSTDSEPARATOR
// but leave the "." alone if it has a number on the right
// Also leave alone if followed by "com" as in DOTcom
// needs some thorough testing
void removePunctuationPeriods(string & text  )
{
  if( 0==text.size() )
    return;

  string temp="";
  size_t i=0;
  char prev=' ';
  for(i=0; i<text.size()-1; i++)
  {
    if( i>0 )
      prev = text[i-1];

    if( text[i] != '.' )
    {
      temp += text[i];
      continue;
    }
    // so now text[i]=='.'

    // is there a number to the right?
    if( ( isdigit( text[i+1]) && '.'!=prev )
     || (i+3<text.size() && text[i+1]=='c' && text[i+2]=='o' && text[i+3]=='m' ) )
    {
      temp += text[i]; // leave well enough alone
      continue;
    }

    temp += sSTDSEPARATOR;
  }
  // special handling for last index
  if( text[i] != '.' )
    temp += text[i];

  text = temp;

  // remove trailing '|' and space
  temp = "";
  i = text.size()-1;
  while(i>1)
  {
    if( text[i]==' ' || text[i]==STDSEPARATOR )
      text[i--] = ' ';
    else
      break;
  }
}


bool isMinus(const string & text, unsigned int pos)
{
  if( pos>text.size()-1 )
    return false;

  char leftC='a', rightC='a';
  bool hasLeftNum=false, hasRightNum=false;

  if( pos>0 )
    leftC = text[pos-1];
  if( pos<text.size()-1 )
    rightC = text[pos+1];

   if( rightC=='.' ) // for "-.4"
    hasRightNum = true;
   else if( isInteger(rightC) )
     hasRightNum = true;

   if( isInteger(leftC) )
     hasLeftNum = true;

   // if have n-m where n and m are both numbers, this is a range indicator, not a minus
   if( hasLeftNum && hasRightNum )
     return false;

   return hasLeftNum || hasRightNum;
}

void addspaceBeforeHash( string & text )
{
  if( text.empty() )
    return;

  string temp="";
  unsigned int i;
  for( i=0; i<text.size(); i++)
  {
    if( i>0 && text[i]=='#' && text[i-1]!=' ')
      temp += " #";
    else
      temp += text[i];
  }
  text = temp;
}

void replaceSupraSubG(string & text)
{
  if( text.size()<2 )
    return;

  for(size_t i=0; i<text.size()-2 ; i++)
  {
    if( text[i]=='-' && (text[i+1]=='g' || text[i+1]=='G' ))
      text[i] = '_';
  }

}


void replaceNonNumericDash( string & text, const string & replacement)
{
  if( text.empty() )
    return;

  char D='-';
  string temp="";
  unsigned int i;
  for( i=0; i<text.size()-1 ; i++)
  {
    if( text[i]==D && !isMinus(text, i) )
      temp += replacement;
//    else if( text[i]==D && isMinus(text,i) )
//      temp += replacement + "-"; // add space left of minus
    else
      temp += text[i];
  }
  if( text[i]!=D ) // special, for last index
    temp += text[i];

  text = temp;

}

void  replaceNonNumericSlash( string & text )
{
  if( text.empty() )
    return;
  char D = '/';

  string temp="";

  // go through other entries
  if( text[0]==D )
    text[0]=' ';

  temp += text[0];

  size_t i;
  for( i=1; i<text.size()-1; i++)
  {
    if( text[i]==D ) // see a '/' 
    { 
                                      //bypass b/f and m/d
      if(  ( text[i-1]=='b' && text[i+1]=='f') || ( text[i-1]=='m' && text[i+1]=='d') )
      {
        temp += text[i]; // keep the '/'
      }
      else if( isInteger( text[i+1]) ) //bypass denominators
      {
        temp += text[i]; // keep the '/'
      }
      else
        temp += ' ';    // replace '/' with space
    }
    else
      temp += text[i]; // keep the '/'
  }

  if( text[i]==D ) // special, for last index
    temp += " "; 

  text = temp;

}


// The behavior is to do the replacement, except if it is a last char of text. Then just use space
void replaceChar( string & text , const char C , const string & replacement )
{
  if( text.empty() )
    return;

  string temp="";
  unsigned int i;
  for( i=0; i<text.size()-1 ; i++)
  {
    if( text[i]==C )
      temp += replacement;
    else
      temp += text[i];
  }
  if( text[i]!=C ) // special, for last index
    temp += text[i];

  text = temp;
}

void replaceCharExcept( string & text , const char C , const string & replacement , const string & except)
{
  if( text.empty() )
    return;

  string newtext = " " + text + " "; // add padding

  size_t pos = newtext.find( except );

  if( pos==string::npos ) // could not find the exception
  {
    replaceChar( text, C, replacement );
    return;
  }

  string pretext = "";
  if( pos>1 )
    pretext = newtext.substr(0, pos );

  string posttext = "";
  if( pos+except.size()< newtext.size() )
    posttext = newtext.substr(pos+except.size(), newtext.size() );

  replaceChar( pretext, C, replacement);
  replaceChar( posttext,C, replacement);

  string temp=pretext+except+posttext;

  text = temp;
}


// replaces only the first occurance of the inPattern
void replacePattern( string & text, const string & inPattern, const string & outPattern)
{
  if( text.empty() )
  {
    return;
  }

  string newtext = " " + text + " "; // add padding

  size_t pos = newtext.find( inPattern );

  if( pos==string::npos ) // could not find the exception
  {
    return;
  }

  string pretext = "";
  if( pos>1 )
  {
    pretext = newtext.substr(0, pos );
  }

  string posttext = "";
  if( pos+inPattern.size()< newtext.size() )
  {
    posttext = newtext.substr(pos+inPattern.size(), newtext.size() );
  }

  string temp = pretext+outPattern+posttext;

  text = temp;
}

void  replaceALSO( string & noteOut, const string & sSTDSEPARATOR )
{
  replacePattern(noteOut, "also", sSTDSEPARATOR);
  replacePattern(noteOut, "ALSO", sSTDSEPARATOR);
  replacePattern(noteOut, "Also", sSTDSEPARATOR);
}



string splitOffDegrees(const string & noteIn)
{
  std::vector<string> tokens;
  string tmp = noteIn;
  Tokenize( tmp, tokens );

  string tok, newstring;
  size_t L;
  for(unsigned int i=0; i<tokens.size(); i++)
  {
    tok = tokens[i];
    L = tok.length();

    if( tok[L-1]==-8 )//|| tok[L-1]==-80 || (int)tok[L-1]==167)// a degree symbol preceeded by a number
    {      
      if( L>1  ) //&& (int)tok[L-2]>0 ) //&& isdigit( tok[L-2] ) )
      {
        tok[L-1] = ' ';
        newstring += " " + tok + " degree";
      }
      else if( L==1 )
        newstring += " degree"; // "°" becomes " degrees"
      else
        newstring += " " + tok;
    }
    else
    {
      if(i>0 )
        newstring += " " + tok;
      else
        newstring += tok;
    }
  }
  return newstring;
}


// you "pre" tokenize, clean tokens, then put them back into a single string
string CleanCompoundTokens( const string & noteIn )
{
  std::vector<string> tokens;
  string tmp = noteIn;
  Tokenize( tmp, tokens );

  string tok, subtok, lefttok, righttok, newstring;
  for(unsigned int i=0; i<tokens.size(); i++)
  {
    tok = tokens[i];

    subtok.clear();
    findSubInDictionary("alarm", tok, subtok );       // try alarm dictionary

    if( subtok=="" )
      findSubInDictionary("designS", tok, subtok );   // or singular design term dictionary
    if( subtok=="" )
      findSubInDictionary( "design", tok, subtok );  // that ought to do it.

    if( subtok == "" ) // not in any of these dictionaries
    {
      newstring += tok;
    }
    else
    {
      splitToken( tok, subtok, lefttok, righttok );

      // Want to know if lefttok ends with a digit, or right tok begins with one.
      // HOW COME isdigit() crashes on neg int and atoi() confuses return values with error code,
      // and string::back() crashes on empty string????!!!!
      // CUZ OF THAT, need to write your own code to check if ending or starting with a digit:
      char h; 
      bool isLeftDigit = false;
      if( lefttok.size()>0 ) // avoid illegal .back() call
      {
        h = lefttok.back(); 
        if(0<=h && h<256 && isdigit((int)h)) // avoid illegal isdigit() call
          isLeftDigit = true;
      }
      bool isRightDigit=false;
      if( righttok.size()>0 )
      {
        const char * p = righttok.c_str();
        h = p[0];
        if(0<=h && h<256 && isdigit((int)h))
          isRightDigit = true;
      }

      if (subtok.length() >= 5 || // long enough to separate
          (lefttok=="" || isLeftDigit) && // or safe to separate from numbers
          (righttok == "" || isRightDigit) )
      {
        newstring += lefttok + " " + subtok + " " + righttok;
      }
      else
      {
        newstring += tok;
      }
    }
    newstring += " ";
  }

  string other = splitOffDegrees(newstring);
  newstring = other;

  return newstring;
}


// replaces "-" or "/" with a special character "\" for dates and phone#s
string  CleanPhone_Date( const string & noteIn  )
{
  std::vector<string> tokens;
  string tmp = noteIn;
  Tokenize( tmp, tokens );

  string newstring;

  for(unsigned int i=0; i<tokens.size(); i++)
  {
    std::vector<string> subtokens;
    char delims[] = "/-";
    string foo = tokens[i];
    DelimTokenize( foo, subtokens, delims);
    
    if( 2==subtokens.size() && isInteger(subtokens[0]) && isInteger(subtokens[1]) )
    {
      if( (subtokens[0].length()==2 || subtokens[0].length()==3) && subtokens[1].length()==4 ) 
      {
        newstring += subtokens[0] + "\\"; //ATTN!!!!! do not change this without changing date\time handling in NoteUtils
        newstring += subtokens[1] +" ";
      }
      else
        newstring += tokens[i] + " ";
    }
    else if( 2==subtokens.size() )
    {
      newstring += subtokens[0] + "-" + subtokens[1] + " ";
    }
    else if( 3==subtokens.size() && isInteger(subtokens[0]) && isInteger(subtokens[1]) && isInteger(subtokens[2]) )
    {
      // is it a phone number?
      if( subtokens[0].length()==3 && subtokens[1].length()==3 && subtokens[2].length()==4 )
      {
        newstring += subtokens[0] + "\\";
        newstring += subtokens[1] + "\\";
        newstring += subtokens[2] + " ";
      }
      else
        newstring += tokens[i] + " ";
    }
    else
    {
      string tmp = tokens[i];
      tmp += " ";
      string tmpp = newstring + tmp;
      newstring = tmpp;
    }
  }
  return newstring;
}


int CharToInt( char c )
{
  return c - '0';
}


void removeTerminalSeparator( std::string & noteOut)
{
  size_t len = noteOut.length();

  if(len<4 )
    return;

  if( noteOut[ len-3 ]==STDSEPARATOR && noteOut[ len-2]==' ' && noteOut[ len-1]==' ' )
    noteOut[len-3] = ' ';
  if( noteOut[ len-2 ]==STDSEPARATOR && noteOut[ len-1]==' ')
    noteOut[len-2] = ' ';
  if( noteOut[ len-1 ] ==STDSEPARATOR )
    noteOut[len-1] = ' ';
}

string separateMM(string & noteOut)
{
  string tmp = noteOut;
  std::vector<string> tokens;
  Tokenize( tmp, tokens );

  string newstring = ""; 
  for( size_t i=0; i<tokens.size(); i++)
  {
    string tok = tokens[i];
    size_t L = tok.length();

    if( L>=4 && tok[L-1]=='m' && tok[L-2]=='m' && isdigit( tok[L-3] ) )
    {
      string foo = tok.substr(0, L-2);
      newstring +=  " " + foo + " mm" + " ";
    }
    else
    {
      newstring += " " + tok + " ";
      continue;
    }
  }

  return newstring;
}

void separatePlusSigns(string & text )
{
  string newtext;
  for(size_t i=0; i<text.size(); i++)
  {
    if( text[i]=='+' )
    {
      newtext += " ";
      newtext += '+';
      newtext += " ";
    }
    else
      newtext += text[i];
  }

  text = newtext;
}

/* Some words in dictionary need to be hyphenated, liseparateke "pre-op" and "wax-up".
But I wish to clean up other uses of "-", So before removing dash, we replace it
with an underbar "_" and list the word in the dictuioary using the underbar.
*/
string  PrepareHyphenExceptions( const string & noteIn  )
{
  std::vector<string> tokens;
  string tmp = noteIn;
  Tokenize( tmp, tokens );

  string newstring;

  for(unsigned int i=0; i<tokens.size(); i++)
  {
    if( tokens[i]=="pre-op" )
    {
      newstring += "pre_op ";
    }
    else
      newstring += tokens[i] + " ";
  }
  return newstring;
}

// look for the pattern (with d=digit and n=nondigit) " d d/dn"
// so this will read " 1 1/2 " as 1.5 and " 1/2 " as 0.5. But does not see much else
void cleanFractionalRemainders( string & text)
{
  string temp = "    " + text + "   "; // ensures index safety

  size_t pos = temp.find( "/" );
  if( string::npos==pos )
    return;

  if( pos<4 || pos>temp.length()-3 )
    return;

  char a = temp[pos-4];
  char b = temp[pos-3];
  char c = temp[pos-2];
  char d = temp[pos-1];
  char e = temp[pos+1];
  char f = temp[pos+2];
  // so we have abcd/ef in the string

  double F=0;

  int posOffset = 0;

  // look for "1 1/2" form
  if( a==' ' && isdigit(b) && c==' ' && isdigit(d) && isdigit(e) && !isdigit(f) )
  {
    int B = CharToInt(b);
    int D = CharToInt(d);
    int E = CharToInt(e);
    if( 0==E )
      return;
    F = (double)B + (double)D/(double)E; // to insert into string
    posOffset = 3;
  }
  // look for " 1/2" form
  else if( !isdigit(b) && c==' ' && isdigit(d) && isdigit(e) && !isdigit(f) )
  {
    int D = CharToInt(d);
    int E = CharToInt(e);
    if( 0==E )
      return;
    F = (double)D/(double)E; // to insert into string
    posOffset = 1;
  }
  else
  {
    return;
  }

  char dat[10];

  sprintf_s( dat, sizeof(dat), "%.2lf", F );

  string insert(dat); // this should be a 3 char string;
  if( insert.length()!=4 )
    return;

  string pre  = temp.substr(0,pos-posOffset);
  string post = temp.substr(pos+2, temp.length());

  text = pre+insert+post;

  return;
}



bool CleanLaterOrderText( const string & noteIn, string & noteOut )
{
  size_t found=0, found2=0;
  found=noteIn.find( "later order" );
  found2=noteIn.find("***");

  if( found==string::npos || found2==string::npos)
    return false;

  noteOut = noteIn;
  replaceChar( noteOut , '\n' , " " );
  replaceChar( noteOut , '\r' , "" );

  return true;
}

bool CleanRemakeText( const string & noteIn, string & noteOut )
{
  size_t found=0;
  found=noteIn.find( "remake" );

  if( found==string::npos )
    return false;

  noteOut = noteIn;
  replaceChar( noteOut , '\n' , " " );
  replaceChar( noteOut , '\r' , "" );

  return true;
}

void removeForeignPrefix( string & text )
{
  string & tmp = text;
  if( tmp.length()>3 && tmp[0]=='ï' && tmp[1]=='»' && tmp[2]=='¿' )
  {
    tmp[0] = tmp[1] = tmp[2] = ' ';

    string tmp2 = tmp.substr(3);
    text = tmp2;
  }
}

void RestoreUmlaut( string & text )
{
  char c;

  for(size_t i=0 ; i<text.size(); i++)
  {
    c = text[i];

    if( c==-124 )
      text[i]=-28;
    else if( c==-126 )
      text[i] = -23;
  }

}


void CleanParse( const string & noteIn, string & noteOut )
{
  noteOut = noteIn; // we will modify noteOut in place

  if( noteIn.size()<1 )
  {
    return;
  }



  removeForeignPrefix(noteOut);

  ToLower( noteOut );

  if( !CleanLaterOrderText( noteOut, noteOut )  && !CleanRemakeText(noteOut, noteOut) )
  {
    replaceENTER(noteOut); // replaces "\n" with ". "
  }

  if ("SE"==AC::GetAtlantisFacility() ) // APAC, including Japan, generally use "." as decimal separator (Indonesia and Vietnam are exceptions). https://en.wikipedia.org/wiki/Decimal_mark
    replaceEuropeanDecimals( noteOut );

  separatePlusSigns( noteOut );

  removeParens( noteOut );       // replaces with space or a STDSEPARATOR, erases instruction step counters

  replacePattern( noteOut, "e.p.s", " eps");

  // replacement with separator
  replaceChar( noteOut, ',', sSTDSEPARATOR );
  replaceChar( noteOut, ';', sSTDSEPARATOR );
  removePunctuationPeriods( noteOut ); // (includes special handling of instruction step indices)
  replaceALSO( noteOut, sSTDSEPARATOR );

  removeTerminalSeparator( noteOut);

  // replacement with white space
  replaceChar( noteOut, '!', " " );
  replaceChar( noteOut, ':', " " );
  replaceChar( noteOut, '"', " " );
  replaceCharExcept( noteOut, '*', " ", " *** "); // replace all *s with spaces, except in " *** "

  replacePattern( noteOut, " s t ", " soft tissue "); //F'in abbreviations

  replacePattern( noteOut, " st ", " soft tissue "); //F'in abbreviations

  string sep(sSTDSEPARATOR);
  replacePattern( noteOut, " and ", sep);


  // or clean up over-grouped items
  replaceChar( noteOut, '=', " = ");

  replaceChar( noteOut, '°', " °"); // maybe need also for 'mm'
  replaceChar( noteOut, 'ø', " ø ");


  string newstring = separateMM(noteOut);
  noteOut = newstring;

  //Before removing "-" we have some special handling cases
  //??
  newstring = CleanPhone_Date( noteOut  );
  noteOut = newstring;

  newstring = PrepareHyphenExceptions( noteOut );
  noteOut = newstring;


  // some special stuff
  replaceSupraSubG( noteOut );

  // remove "-" if no neighboring numbers occur
  replaceNonNumericDash( noteOut, " ");

  replaceNonNumericSlash( noteOut );

  addspaceBeforeHash( noteOut );

  for(unsigned int k=0; k<4; k++ ) // each pass can replace one fraction with one decimal respresentation
  {
    cleanFractionalRemainders( noteOut );
  }

  // make "#mm"-->"# mm"
//MOVE to earlier
//  separateMM(noteOut);

  //// CLEAN SINGLE TOKENS
  newstring = CleanCompoundTokens( noteOut );
  noteOut = newstring;


  RestoreUmlaut(noteOut);

#ifdef _DEBUG
  cout <<"******************************\n";
  cout << "CLEANED: " << noteOut << "\n";
  cout <<"******************************\n";
#endif

}

} // end namespace AC