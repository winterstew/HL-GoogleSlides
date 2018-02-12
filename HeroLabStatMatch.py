# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:41:38 2018

@author: steve
"""
import re
from HeroLabStatBase import Character

class Matcher(object):
    """
    Container for attributes and methods related to finding replacement values
    from the character and returning  those values

    Methods:
      getMatch: returns resuult  of evaluating the match value
      getKeys: returns the list of possible keywords for templates

    Attributes:
      name = (str) deriverd from character name
      type = (str) 'text' or 'image'
      matcherDictionary: (dict) provided matcher dictionary
    """

    """
    ********
    Matching
    ********
    The matching method uses keywords surrounded by double wavy brackets and
    modified with prefix and suffix elements.

    TEXTMATCH
    ==========
    The text match dictionary is for replacing keyworded and bracketed text with
    the result of evaluation of the value for each item.  Examples of using the
    format in a template document are as follows::

    {{keyword}}}
    {{(keyword)}}
    {{head:_keyword}}
    {{(head:_keyword)}}
    {{head:_keyword..}}
    {{head:.c.keyword}}
    {{(head:_keyword..)}}

      ``keyword``
        must have a match in the dictionary to give a value which will be
        evaluated.  It must also not have a ``..`` (double period) as part of it.

      ``()``
        must be the outer most element, but inside the double brackets.  If
        the value evaluation results in something parenthesis are placed around it

      ``head:``
        This is replaced with the *head* text if the value evaluation results
        in something.  The *head* text may only have one ``:`` (colon) as part
        of it as the last character.

      ``_``
        This is used to indicate that instead of the evaluated value the parent
        Feature's abbreviate method should ne called with the final attribute
        as the argument.  If the method does not exist, just the value is returned

      ``.c.``
        This before the keyword is used for tracking item lists.  The value
        should evaluate to an integer value.  The ``c`` can be any single character
        that character will be repeated interger times based onthe evaluated value

      ``..``
        This after a keyword is used to indicate a possible list.  The value
        should evaluate to an attribute from the first element in the list.  The
        list should be one element up from the attribute.  The result will be the
        same attribute from all the elements in the list.  Any text following
        the ``..`` will be used as separators between the images.

    The value for each item in the text match dictionary should evaluate to the
    text which will replace the keyword in the template document, or as mentioned
    above the text for the first attribute in a list.
    """
    TEXTMATCH = {
    }

    """
    IMAGEMATCH
    ==========
    The image match dictionary is for replacing shape placeholders containing
    just the keyword as the placeholder.  Examples of using the
    format in a template document are as follows::

    {{keyword}}
    {{h_keyword..}}
    {{l_keyword..}}

      ``keyword``
        must have a match in the dictionary to give a value which will be
        evaluated.  It must also not have a ``..`` (double period) as part of it.

      ``h_ or l_``
        This is used to indicate the resolution for the image.  The value has to
        evaluate to an object with imageHigh and/or imageLow (default) attribute.

      ``..``
        This is used to indicate a possible list.  The value should evaluate to
        an attribute from the first element in the list.  The list should be
        one element up from the attribute.  The result will be the same attribute
        from all the elements in the list.

    The value for each item in the image match dictionary should evaluate to an
    object with an imageHigh and/or imageLow attribute (default imageHigh).  The
    value of this attribute is a tuple containing the filename for the image
    and the absolute path filename for the image.  If the value is the first in
    a list and the `..`` modifier is used, imageHigh and/or imageLow is evaluated
    for each item in the list and returned as a list of tuples
    """

    IMAGEMATCH = {
    }

    """
    BOOLEANMATCH
    ==========
    The boolean match dictionary is for replacing a keyword with a returned boolean:
    True or False based on the value(s) from the evaluated character attribute.
    Examples of using the format in a template document are as follows::

    {{keyword}}
    {{keyword..}}

      ``keyword``
        must have a match in the dictionary to give a value which will be
        evaluated.  It must also not have a ``..`` (double period) as part of it.

      ``..``
        This is used to indicate a possible list.  The value should evaluate to
        an attribute from the first element in the list.  The list should be
        one element up from the attribute.  The result will be derived from the
        same attribute from all the elements in the list.

    The value for each item in the boolean match dictionary should evaluate to a
    case insensityve string of yes, no, true, false, on, or off.  These are
    then interpreted as a boolean and returned either as a single result of a list.
    """
    BOOLEANMATCH = {
    }

    _booleanDict = {
      'yes':True,
      'no':False,
      'true':True,
      'false':False,
      'on':True,
      'off':False,
    }
    def __init__(self,character,matcherDictionary=TEXTMATCH,matcherType='text',**kwargs):
        """create a matcher give the character and the match dictionary

        Args:
           character: (Character) instance from which the data is drawn
           matcherDictionary: (dict) dictionary of keywords which are matched
              and the values are replacement chracter subobjects which when
              evaluated return a string, a boolean, or None for 'text' type
              matchers.  Alternativelty these vales may return a tuple of
              (image filename, image absolute path filename) for 'image'
              type matchers
           matchType: (string) either 'text' or 'image' or 'boolean'
        """
        assert type(character) == Character, "First argument must be a Character instance: %s" % character
        assert type(matcherDictionary) == dict, "Second argument must be dictionary: %s" % matcherDictionary
        assert matcherType == 'text' or matcherType == 'image' or matcherType == 'boolean',"matcherType must be either 'text', 'image', or 'boolean': %s"% matcherType
        self._character = character
        self.name = "%s.%s %s" % (character.myIndex,character.characterIndex,character.name)
        self.type = matcherType
        self.matcherDictionary = matcherDictionary

    def _exists(self,toTest,*args,**kwargs):
        """check if the attribute exists within the character attribute tree"""
        testList = toTest.split(".")
        testObj = self._character
        isAttr = True
        for myAttr in testList:
            attrMatch = re.match(r'([^\[\]]+)(\[(.+?)\])?',myAttr)
            if attrMatch:
                testAttr = attrMatch.group(1)
                testAttrIdx = None
                if len(attrMatch.groups()) == 3:
                    testAttrIdx = attrMatch.group(3)
                isAttr = hasattr(testObj,testAttr)
                if not isAttr: break
                if testAttrIdx != None:
                    if type(getattr(testObj,testAttr)) == list:
                        if int(testAttrIdx) >= len(getattr(testObj,testAttr)):
                            isAttr = False
                            break
                        testObj = getattr(testObj,testAttr)[int(testAttrIdx)]
                    elif type(getattr(testObj,testAttr)) == dict:
                        testObj = getattr(testObj,testAttr)[testAttrIdx]
                    else:
                        isAttr = False
                        break
                else:
                    testObj = getattr(testObj,testAttr)
            else:
                isAttr = False
        if self.type == 'image':
            isAttr = hasattr(testObj,'imageHigh') or hasattr(testObj,'imageLow')
        return isAttr

    def getMatch(self,keyText,*args,**kwargs):
        """Return the match from the included character based on keyText

        Args:
           keyText: (str) keyword from matcherDictionary possibly with modifiers
             for head, parenthesis, lists, image resolution, and/or abbreviation
        """
        # just in case the keyText is passed with the brackets
        myKey = re.sub('^\{\{(.*)\}\}$',r'\1',keyText)
        # identify any brackets and strip them off the myKey
        (pStart,pEnd) = ('','')
        pMatch = re.search(r'^\{(.*)\}$',myKey)
        if pMatch: (myKey,pStart,pEnd) = (pMatch.group(1),'{','}')
        pMatch = re.search(r'^\[(.*)\]$',myKey)
        if pMatch: (myKey,pStart,pEnd) = (pMatch.group(1),'[',']')
        pMatch = re.search(r'^\((.*)\)$',myKey)
        if pMatch: (myKey,pStart,pEnd) = (pMatch.group(1),'(',')')
        # identify any header and strip it off the myKey
        headText = ''
        hMatch = re.search(r'^([^:]+:?):([^:].*)$',myKey)
        if hMatch: (headText,myKey) = hMatch.groups()
        # identify any repeating characters and strip it off the myKey
        repeatText = ''
        rMatch = re.search(r'^\.(.)\.(.+)$',myKey)
        if rMatch: (repeatText,myKey) = rMatch.groups()
        # assign image attribute based on possible flag
        finalAttr = 'imageLow'
        if re.match(r'^h_',myKey) and self.type == 'image': finalAttr = 'imageHigh'
        # assign flag for abbreviation
        abbreviate = False
        if re.match(r'^_',myKey) and self.type != 'image': abbreviate = True
        # match for the list  option and separator based on flag
        listMatch = re.search(r'\.\.(.*)$',myKey)
        # strip off all rest of the flags down to the key
        myKey = re.sub(r'\.\..*$','',re.sub(r'^(h_|l_|_)','',myKey))
        # some matchers use the striped key, some use the full key
        keyWord = myKey in self.matcherDictionary and myKey or keyText
        if keyWord not in self.matcherDictionary:
            print("Warning: %s is not in Matcher, empty text returned" % keyWord)
            #if self.type == 'boolean': return False
            #return ''
            #print("Warning: key is not in Matcher, %s returned" % keyWord)
            return keyWord
        rtnList = []
        # a special type of text match where two values are separated by a group separator
        # in this case the first is evaluated as a boolean which determins if the second is
        # displayed.
        conditional = re.search(r'\x1d',self.matcherDictionary[keyWord]) and True or False
        for (valCount,myValue) in enumerate(re.split("[\x1d\x1e]",self.matcherDictionary[keyWord])):
            # if this is the first part of a conditional value pull off the value from the start
            if conditional and valCount == 0:
                conditionalList = re.split(r' ',myValue)
                myValue = conditionalList[0]
            if not self._exists(myValue):
                print("Warning: %s is not in Character %s, empty text returned" % (keyWord,self.name))
                #if self.type == 'boolean': return False
                if self.type == 'boolean':
                    rtnList.append('false')
                elif self.type == 'image':
                    rtnList.append(('',''))
                else:
                    rtnList.append('')
                continue
            # if this is not an image matcher lets get the final attribute name
            #print(myValue)
            if self.type != 'image':
                (myValue,finalAttr) = re.search('^(.*\.)?([^.]+)$',myValue).groups()
                #print(myValue,finalAttr)
                myValue = myValue and re.sub(r'\.$','',myValue) or myValue
            # if this is the first part of a conditional evaluate to see if we go on
            if conditional and valCount == 0:
                conditionalList[0] = myValue and "getattr(self._character.%s,'%s')" % (myValue,finalAttr)
                print(conditionalList)
                if eval(" ".join(conditionalList)):
                    continue
                else:
                    break
            if listMatch:
                myValue = myValue and re.sub(r'(\[[^\[\]]+\])$','',myValue) or myValue
                #print(myValue,finalAttr)
            evalList = myValue and eval("self._character.%s" % myValue) or self._character
            # make everything a list
            if not type(evalList) == list:
                evalList = [evalList]
            #print(evalList)
            # get the return list
            if abbreviate:
                rtnList += [i.abbreviate(finalAttr) for i in evalList]
            else:
                rtnList += [getattr(i,finalAttr) for i in evalList]
        if rMatch:
            newList = []
            for i in rtnList:
                try:
                    newList.append(repeatText * int(i))
                except ValueError:
                    print("Warning: %s.%s was not an integer for Character %s, 1 used" % (myValue,finalAttr,self.name))
                    newList.append(repeatText)
            rtnList = newList[:]
        # if this is a boolean, change the list to boolean
        if self.type == 'boolean':
            rtnList = [self._booleanDict[b.lower()] for b in rtnList]
        # return the result(s)
        if len(filter(lambda i:i,rtnList)) == 0:
            print("Warning: nothing stored in %s.%s for Character %s, empty text returned" % (myValue,finalAttr,self.name))
            if self.type == 'boolean': return False
            return ''
        if self.type != 'text':
            if len(rtnList) == 1:
                return rtnList[0]
            return rtnList
        joiner = ''
        if listMatch:
            joiner = listMatch.group(1)
        return ''.join([pStart,headText,joiner.join(rtnList),pEnd])

    def getKeys(self,*args,**kwargs):
        """return the list of possible keys for this matcher"""
        return self.matcherDictionary.keys()