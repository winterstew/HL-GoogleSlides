# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:41:38 2018

@author: steve
"""
import re
from HeroLabStatBase import VERBOSITY,Character

OPERATORS = ["<",">","==",">=","<=","<>","!=","is","not","in","and","or"]

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

      ``head:?``
        This is replaced with the *head* text if the value evaluation results
        in something, however only the head test is returned.

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
        if 'verbosity' not in kwargs: kwargs['verbosity'] = VERBOSITY
        self.verbosity = kwargs['verbosity']
        assert type(character) == Character, "First argument must be a Character instance: %s" % character
        assert type(matcherDictionary) == dict, "Second argument must be dictionary: %s" % matcherDictionary
        assert matcherType == 'text' or matcherType == 'image' or matcherType == 'boolean',"matcherType must be either 'text', 'image', or 'boolean': %s"% matcherType
        self._character = character
        self.name = "%s.%s %s" % (character.myIndex,character.characterIndex,character.name)
        self.type = matcherType
        self.matcherDictionary = matcherDictionary

    def _exists(self,toTest,*args,**kwargs):
        """check if the attribute exists within the character attribute tree

        Returns: a siz member tuple
          isAttr: (boolean) this attribute exists
          testObj: value returned from final test object's attribute
          lastTestObj: (Feature) final test object
          testAttr: (string) final attribute of the feature being tested
          testList: (Feature list) if lastTestObj is a member
          testAttrIdx (int or str)
        """
        toTestList = toTest.split(".")
        testObj = self._character
        lastTestObj = testObj
        testList = []
        attrCount = 0
        isAttr = True
        testAttr = ''
        for (attrCount,myAttr) in enumerate(toTestList):
            lastTestObj = testObj
            attrMatch = re.match(r'([^\[\]]+)(\[(.+?)\])?',myAttr)
            if attrMatch:
                testAttr = attrMatch.group(1)
                testAttrIdx = None
                if len(attrMatch.groups()) == 3:
                    testAttrIdx = attrMatch.group(3)
                isAttr = hasattr(testObj,testAttr)
                if not isAttr: break
                if testAttrIdx != None:
                    testList = getattr(testObj,testAttr)
                    if type(testList) == list:
                        if int(testAttrIdx) >= len(testList):
                            isAttr = False
                            break
                        testObj = testList[int(testAttrIdx)]
                    elif type(testList) == dict:
                        testObj = testList[testAttrIdx]
                    else:
                        isAttr = False
                        break
                else:
                    testObj = getattr(testObj,testAttr)
            else:
                isAttr = False
        #if self.type == 'image':
        #    for testAttr in ['imageLow','imageHigh']:
        #        isAttr = hasattr(testObj,testAttr)
        #        if isAttr:
        #            lastTestObj = testObj
        #            testObj = getattr(testObj,testAttr)
        #            break
        if lastTestObj not in testList: testList = []
        if not isAttr: testObj = toTest
        return (isAttr,testObj,lastTestObj,testAttr,testList,testAttrIdx)

    def getMatch(self,keyText,*args,**kwargs):
        """Return the match from the included character based on keyText

        Args:
           keyText: (str) keyword from matcherDictionary possibly with modifiers
             for head, parenthesis, lists, image resolution, and/or abbreviation

        \x1c
        \x1d separate conditional from replacement
        \x1e serarate replacement values when using multiple (which will be joined with a apace)
        \x1f separate keyswords in replacement when nesting keywords
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
        hMatch = re.search(r'^([^:]+[:]?):([?]?[^:].*)$',myKey)
        if hMatch: (headText,myKey) = hMatch.groups()
        hOnlyMatch = re.search(r'^[?]',myKey)
        if hOnlyMatch: myKey = re.sub(r'^\?','',myKey)
        # identify any repeating characters and strip it off the myKey
        repeatText = ''
        rMatch = re.search(r'^\.(.)\.(.+)$',myKey)
        if rMatch: (repeatText,myKey) = rMatch.groups()
        # assign flag for abbreviation
        abbreviate = False
        if re.match(r'^_',myKey) and self.type != 'image': abbreviate = True
        # addign image resultion
        imageRes = ''
        if self.type == 'image':
            imageRes = 'imageLow'
            if re.match(r'^h_',myKey):
                imageRes = 'imageHigh'
        # match for the list  option and separator based on flag
        listMatch = re.search(r'\.\.(.*)$',myKey)
        # strip off all rest of the flags down to the key
        myKey = re.sub(r'\.\..*$','',re.sub(r'^(h_|l_|_)','',myKey))
        # some matchers use the striped key, some use the full key
        keyWord = myKey in self.matcherDictionary and myKey or keyText
        if keyWord not in self.matcherDictionary:
            if self.verbosity >= 2: print("Warning: key is not in Matcher, %s returned" % keyWord)
            return keyWord
        rtnList = []
        myValue = self.matcherDictionary[keyWord]
        testedValue = (False,None,None,str(),list(),None)
        # if the value is also keys split them up and get the values
        if re.search("\x1f",myValue):
            for kw in re.split("\x1f",myValue):
                rtnList.append(self.getMatch(kw))
        else:
            # a special type of text match where two values are separated by a group separator
            # in this case the first is evaluated as a boolean which determins if the second is
            # displayed.
            conditional = False
            conditionalResult = []
            itemCount = 1
            if re.search("\x1d",self.matcherDictionary[keyWord]):
                conditional = True
                (myConditional,myValue) = re.split("\x1d",myValue)
                conditionalList = re.split(r' ',myConditional)
                # evaluate each part of the conditional which is a feature to its attribute
                # each part of the conditional is also then expanded to a list
                for (condIdx,condItem) in enumerate(conditionalList):
                    testedItem = self._exists(condItem)
                    # if the keyword asks for a list, the attribute exists, and the attribute comes from a list member
                    if listMatch and testedItem[0] and testedItem[4]:
                        # go through each feature in the list and get the relavant attribute
                        conditionalList[condIdx] = [hasattr(lf,testedItem[3]) and getattr(lf,testedItem[3]) for lf in testedItem[4]]
                        itemCount = len(conditionalList[condIdx]) > itemCount and len(conditionalList[condIdx]) or itemCount
                    else:
                        conditionalList[condIdx] = [testedItem[1]]
                # duplicate the last element in the conditional list part until all are the same length
                for (condIdx,condItem) in enumerate(conditionalList):
                    while len(condItem) < itemCount:
                        condItem.append(condItem[len(condItem)-1])
                    conditionalList[condIdx] = condItem
                # evaluate set of conditionals for each possible list item
                for itemIdx in range(itemCount):
                    tempConditionalList = []
                    for condIdx in range(len(conditionalList)):
                        # all numbers are evaluated as floats
                        try:
                            float(conditionalList[condIdx][itemIdx])
                            tempConditionalList.append("float(%s)" % conditionalList[condIdx][itemIdx])
                        except(ValueError):
                            if conditionalList[condIdx][itemIdx] not in OPERATORS:
                                tempConditionalList.append('"'+conditionalList[condIdx][itemIdx]+'"')
                            else:
                                tempConditionalList.append(conditionalList[condIdx][itemIdx])
                    try:
                        conditionalResult.append(eval(" ".join(tempConditionalList)))
                    except:
                        print(tempConditionalList)
                        raise
                # I now have a list of boolean stored in conditionalResult, one for each
                # attribute in the list, or a list of one for non-list attributes
            # Now lets go through all the values.
            valueList = []
            maxCount = 0
            # loop through each of the \x1e separated values
            # these will be enterleaved as space separated
            # values for each one in a list (if it is a list)
            for (valCount,myValue) in enumerate(re.split("\x1e",myValue)):
                valueList.append(list())
                # append imageRes for images or '' for all else
                if self.type == 'image':
                    myValue = re.sub(r'.image(High|Low)','',myValue)
                    myValue += "." + imageRes
                testedValue = self._exists(myValue)
                # it is does not exist append empty result to the list
                if not testedValue[0]:
                    if self.verbosity >= 1: print("Warning: key:%s -> %s is not in Character %s, empty text returned" % (keyWord,myValue,self.name))
                    #if self.type == 'boolean': return False
                    #if self.type == 'boolean':
                    #    valueList[valCount].append('false')
                    #elif self.type == 'image':
                    #    valueList[valCount].append(('',''))
                    #else:
                    #    valueList[valCount].append('')
                    valueList[valCount].append(None)
                    continue
                # if we have the value add it/them to the list
                feature = testedValue[2]
                attr = testedValue[3]
                if listMatch and testedValue[4]:
                    featureList = testedValue[4]
                    if abbreviate:
                        valueList[valCount] += [hasattr(f,attr) and f.abbreviate(attr) for f in featureList]
                    else:
                        valueList[valCount] += [hasattr(f,attr) and getattr(f,attr) for f in featureList]
                else:
                    if abbreviate:
                        valueList[valCount] += [feature.abbreviate(attr)]
                    else:
                        valueList[valCount] += [getattr(feature,attr)]
                # keep track of max values per valCount
                maxCount = len(valueList[valCount]) > maxCount and len(valueList[valCount]) or maxCount
            for cntr in range(maxCount):
                if conditional:
                    # use the cntr to find the relavant conditional or if they are mismatched
                    # just use the last conditional
                    idx = cntr < len(conditionalResult) and cntr or len(conditionalResult) -1
                    if not conditionalResult[idx]:
                        continue

                toJoinList = []
                for vIdx in range(len(valueList)):
                    if cntr < len(valueList[vIdx]):
                        if (valueList[vIdx][cntr]): toJoinList.append(valueList[vIdx][cntr])
                if self.type == 'text':
                    rtnList.append(" ".join(toJoinList))
                # multiple value separated by \x1e are ignored for boolean and images
                else:
                    rtnList.append(valueList[0][cntr])
        # Now we have a return list of strings or tuples
        if rMatch:
            newList = []
            for i in rtnList:
                try:
                    newList.append(repeatText * int(i))
                except ValueError:
                    if self.verbosity >= 1: print("Warning: key:%s -> %s attribute %s was not an integer for Character %s, 1 repeat used" % (keyWord,testedValue[2],testedValue[3],self.name))
                    newList.append(repeatText)
            rtnList = newList[:]
        # if this is a boolean, change the list to boolean list
        if self.type == 'boolean':
            rtnList = [self._booleanDict[b.lower()] for b in rtnList]
        # return the result(s)
        rtnList = filter(lambda i:i,rtnList)
        if len(rtnList) == 0:
            if self.verbosity >= 1: print("Warning: key:%s -> nothing stored in %s attribute %s for Character %s, empty text returned" % (keyWord,testedValue[2],testedValue[3],self.name))
            if self.type == 'boolean': return False
            if self.type == 'image': return ('','')
            return ''
        if self.type != 'text':
            if len(rtnList) == 1:
                return rtnList[0]
            return rtnList
        if hOnlyMatch: rtnList = []
        joiner = ''
        if listMatch:
            joiner = listMatch.group(1)
        return ''.join([pStart,headText,joiner.join(rtnList),pEnd])

    def getKeys(self,*args,**kwargs):
        """return the list of possible keys for this matcher"""
        return self.matcherDictionary.keys()