# -*- coding: utf-8 -*-
"""
Created on Mon Jan 01 10:08:15 2018

@author: Steven Weigand
"""
from __future__ import print_function
import string,re,os,tempfile,zipfile,shutil,sys,types
from collections import Counter

import xml.etree.cElementTree as et

VERBOSITY = 0
PRINTOMIT = ['fTag','fParent','fCharacter','fPortfolio','statText','statHtml','statXml','fAttr','fSub','_fAbbreviate','minions','minionsList']
SIZEDICT = {
      'F':'Fine',
      'D':'Diminutive',
      'T':'Tiny',
      'S':'Small',
      'M':'Medium',
      'L':'Large',
      'H':'Huge',
      'G':'Gargantuan',
      'C':'Colossal',
      None:''
}

def printFeatureList(myList,name='',**kwargs):
    """recursive function to print out feature list"""
    myList.sort()
    myFile = 'toFile' in kwargs and type(kwargs['toFile']) == file and kwargs['toFile'] or sys.stdout
    myEncoding = 'encode' in kwargs and kwargs['encode'] or 'utf8'
    for idx,l in enumerate(myList):
        if not isinstance(l,list) and not isinstance(l,Feature):
            if type(l) == Icon:
                toPrint =  "%s[%s].imageHigh = %s\n" % (name,idx,l.imageHigh)
                toPrint += "%s[%s].imageLow = %s" % (name,idx,l.imageLow)
            else:
                toPrint = "%s[%s] = %s" % (name,idx,l)
            print(toPrint.encode(myEncoding),file=myFile)
        elif isinstance(l,Feature):
            printFeature(l,"%s[%s]" % (name,idx),**kwargs)
        elif isinstance(l,list):
            printFeatureList(l,"%s[%s]" % (name,idx),**kwargs)

def printFeature(myFeature,name='',**kwargs):
    """recursive function to print out the feature tree"""
    global PRINTOMIT
    printOmit = 'printOmit' in kwargs and kwargs['printOmit'] or PRINTOMIT
    myKeys = myFeature.__dict__.keys()
    myKeys.sort()
    myFile = 'toFile' in kwargs and type(kwargs['toFile']) == file and kwargs['toFile'] or sys.stdout
    myEncoding = 'encode' in kwargs and kwargs['encode'] or 'utf8'
    for fkey in myKeys:
        if fkey in printOmit: continue
        val = getattr(myFeature,fkey)
        if not isinstance(val,list) and not isinstance(val,Feature):
            if type(val) == Icon:
                toPrint =  "%s.%s.imageHigh = %s\n" % (name,fkey,val.imageHigh)
                toPrint += "%s.%s.imageLow = %s" % (name,fkey,val.imageLow)
            else:
                toPrint = "%s.%s = %s" % (name,fkey,val)
            print(toPrint.encode(myEncoding),file=myFile)
        elif isinstance(val,Feature):
            printFeature(val,"%s.%s" % (name,fkey),**kwargs)
        elif isinstance(val,list):
            printFeatureList(val,"%s.%s" % (name,fkey),**kwargs)

def _setOtherSpeeds(oldElement,speedsText,*args,**kwargs):
    """set non-land speeds based on values from the HTML"""
    moveAttr = {}
    for speed in speedsText.split(","):
        # non-land speed movements start with a word (fly, swim, etc)
        moveTypeMatch = re.search(r'\s*(\w+)\s+(\d+)\s*ft.\s*',speed)
        if moveTypeMatch:
            (moveType,moveSpeed) = moveTypeMatch.groups()
            # fly also has a maneuverability quality modifier
            moveQualMatch = re.search(r'ft.\s*\((\w+)\)',speed)
            moveQual = moveQualMatch and moveQualMatch.groups()[0] or None
            # assign attributes for tag
            moveAttr['name'] =  moveType
            moveAttr['text'] = "%d'" % int(moveSpeed)
            moveAttr['value'] = int(moveSpeed)
            if moveQual: moveAttr['maneuverability'] = moveQual
            # append element
            et.SubElement(oldElement,moveType.lower(),moveAttr)
            et.SubElement(oldElement,"other",moveAttr)
    return oldElement

def _getTypesSubtypes(typesText):
    """ get lists of all types and subtypes from text"""
    myTypes = []
    mySubtypes = []
    typesOnly = string.strip(re.sub(r'\([^\)]+\)','',typesText))
    myTypes = [string.capwords(string.strip(item)) for item in typesOnly.split(",")]
    subtypesMatch = re.search(r'\(([^\)]+)\)',typesText)
    if subtypesMatch:
        mySubtypes = [string.capwords(string.strip(item)) for item in subtypesMatch.groups()[0].split(",")]
    return(myTypes,mySubtypes)

def _modSubelements(elem,*args,**kwargs):
    """replace or append subelements for an element

    Args:
       elem: (Element) parent element
       one or more tuple pairs of tag, attrDict sets for subelements

    Kwargs:
       append: (boolean) delete existing subelements if False
    """
    if 'append' not in kwargs or not kwargs['append']:
        attr = elem.items()
        elem.clear()
        [elem.set(*a) for a in attr]
    for subelem in args:
        tag = subelem[0].lower()
        attrs = dict([(item[0].lower(),item[1]) for item in subelem[1].items()])
        et.SubElement(elem,tag,attrs)
    return elem

def _setTrueTypes(oldElement,typesText,*args,**kwargs):
    """ return element with the true types as determined from HTML typesText"""
    mySubs = [('type',{'name':item}) for item in _getTypesSubtypes(typesText)[0]]
    return _modSubelements(oldElement,*mySubs)

def _setTrueSubtypes(oldElement,typesText,*args,**kwargs):
    """ return element with the true subtypes as determined from HTML typesText"""
    mySubs = [('subtype',{'name':item}) for item in _getTypesSubtypes(typesText)[1]]
    return _modSubelements(oldElement,*mySubs)

def _setTrueSpellclass(oldElement,spellText,*args,**kwargs):
    """ return element the correct spells per level set. """
    spellclasses = [] # list of tuples of tag, attrs, and levels
    # split between alternate casting classes
    for spClass in re.split(r'(?m)<br/>\n<b>',spellText):
        spellclass = ['spellclass'] # list of tag,attrs, and levels
        # match the spellclass listings only
        clMatch = re.match(r'^([A-Za-z ()]+) (Spells|Extracts) (Known|Prepared)\s*</b>',spClass)
        if not clMatch: continue
        # get the element attributes we will need
        (clName,junk,typeKey) = clMatch.groups()
        clType = {'Known':'Spontaneous','Prepared':'Memorized'}[typeKey]
        if clName == 'Arcanist': clType = "Flexible Book"
        if clName in ['Alchemist','Magus','Witch','Wizard']: clType = "Spellbook"
        # if there is a spellclass subelement for this class lets use its type instead
        clMax = None
        if oldElement.find("spellclass[@name='%s'] % clName") != None:
            clType = oldElement.find("spellclass[@name='%s']" % clName).get('spells') or clType
            clMax = oldElement.find("spellclass[@name='%s']" % clName).get('maxspelllevel') or None
        # figure out the subelement spelllevel
        levels = []
        maxcasts = []
        unlimited = []
        used = []
        emphasis = {}
        # split between spell levels, the first line has no spell levels
        for spList in re.split(r'(?m)<br/>\n&nbsp;&nbsp;&nbsp;',spClass)[1:]:
            # extract level and castings
            levelMatch = re.match(r'(?P<level>\d)([a-z][a-z])?( +\((?P<castings>[^\)]+)\))?\xe2\x80\x94',spList)
            spellCount = 0
            # only look as spell list lines
            if levelMatch:
                levelDict = levelMatch.groupdict()
                # number of start italics tags = the number of spells in list
                spellCount = str(len(re.split(r'<i>',spList)) - 1)
                # append extracted level to the list
                levels.append(levelDict['level'])
                # if castings exists it is either a cantrip or a spontaneous caster
                if levelDict['castings']:
                    # for cantrips and orisons
                    if levelDict['castings'] == 'at will':
                        unlimited.append("yes")
                        maxcasts.append(None)
                        used.append('0')
                    # for spondtaneous with a daily limit
                    elif re.match(r'\d\/',levelDict['castings']):
                        unlimited.append(None)
                        maxcasts.append(re.match(r'(\d)\/',levelDict['castings']).group(1))
                        used.append('0')
                    # something else in the parenthetical after the level that I do not know
                    else:
                        unlimited.append(None)
                        maxcasts.append(levelDict['castings'])
                        used.append('0')
                # for prepared casters assuming that they prepared their max number
                # which is not necessaryily the case but I have nothing else to go on
                else:
                    unlimited.append(None)
                    maxcasts.append(spellCount)
                    used.append(spellCount)
            else:
                emphasisMatch = re.match(r'(<b>(?P<footnote>[A-Z])</b>\s+(?P<footnotetext>[^;]+);\s*)?<b>(?P<emphasistype>[A-Za-z]+)</b>\s+(?P<emphasis>[A-Za-z, ]+)(\s<b>(?P<emphasisextra>[A-Za-z, ]+)</b>\s*)?$',spList)
                if emphasisMatch:
                    emphasis = emphasisMatch.groupdict()
        # if there are listed levels and no clMax yet lets use the levels
        if levels and not clMax: clMax = max(levels)
        spellclass.append(dict([('name',clName),('maxspelllevel',clMax),('spells',clType)] + emphasis.items()))
        spellclass.append([]) # starting empty list for spelllevels        
        # if we have levels from the HTML lets use them
        if levels:
            # use max spell level and count up to populate subelements
            for level in range(int(clMax)+1):
                lattr = {}
                # casters like rangers and alchemists have no level 0 spells
                if level == 0 and str(level) not in levels:
                    lattr = {'level':'0','maxcasts':'0','used':'0'}
                # as long as the level is in the list of levels
                elif str(level) in levels:
                    lidx = levels.index(str(level))
                    lattr['level'] = levels[lidx]
                    lattr['used'] = used[lidx]
                    if unlimited[lidx]: lattr['unlimited'] = unlimited[lidx]
                    if maxcasts[lidx]: lattr['maxcasts'] = maxcasts[lidx]
                # if not in list, skip it
                else: continue
                spellclass[2].append(('spelllevel',lattr))
        # if no levels from HTML lets use the XML
        else:
            for splElem in oldElement.findall("spellclass[@name='%s']/spelllevel" % clName):
                spellclass[2].append(('spelllevel',dict(splElem.items())))
        # append spellclass as tuple to list of classes
        spellclasses.append(tuple(spellclass))
    # clean out old element, but keep attributes (if there are any)
    attr = oldElement.items()
    oldElement.clear()
    [oldElement.set(*a) for a in attr]
    # add all spellclass sub elements
    for spClass in spellclasses:
        elem = et.SubElement(oldElement,spClass[0],spClass[1])
        for spLevel in spClass[2]:
            et.SubElement(elem,spLevel[0],spLevel[1])
    return oldElement

def _addBetterNpcInfo(oldElement,*args,**kwargs):
    """append elements for better arragement of npc features"""
    tagMatch = {"basics":[('Motivations & Goals',"goal"),
                          ('Schemes, Plots & Adventure Hooks',"hook"),
                          ('Boon',"boon"),
                         ],
                "tactics":[('Tactics - Before Combat',"beforecombat"),
                           ('Tactics - During Combat',"duringcombat"),
                           ('Tactics - Morale',"morale"),
                           ('Base Statistics','basestat'),
                          ],
                "ecology":[('Ecology - Environment',"environment"),
                           ('Ecology - Organization',"organization"),
                           ('Ecology - Treasure',"treasure"),
                          ],
               }
    # find and append elements
    for elem in list(oldElement):
        matchList = []
        if elem.tag in tagMatch:
            matchList = tagMatch[elem.tag]
            #for toFind in toAppend[elem.tag]:
            #    e = elem.find(toFind[0])
            #    if e:
            #        print("found %s in %s" % (toFind[0],elem))
            #        se = et.SubElement(elem,toFind[1],name=e.get("name"))
            #        se.text = e.text
        for e in elem.findall("npcinfo"):
            newtag = re.sub(r'[^A-Za-z]','',re.sub(r'&.+?;','',e.get("name"))).lower()
            for m in matchList:
                if e.get("name") == m[0]: newtag = m[1]
            se = et.SubElement(elem,newtag,name=e.get("name"))
            se.text = e.text
    return oldElement

def _addBetterSkillsElements(oldElement,*args,**kwargs):
    # find and append elements
    for elem in list(oldElement):
        nameList = re.split(r'[\s().;,:]',elem.get('name'))
        # first add elements with tags besed on specific subname
        newTag = nameList[0].lower() + "".join([i.capitalize() for i in nameList[1:]])
        newDict = dict(elem.items())
        newText = elem.text
        newTail = elem.tail
        newSubs = list(elem)
        if re.search(r'[()]',elem.get('name')):
            newDict['subname'] = " ".join([i.capitalize() for i in nameList[1:]])
        else:
            newDict['subname'] = ''
        newDict['text'] = "%+d" % int(newDict['value'])
        if 'armorcheck' in newDict and {'Yes':'yes','yes':'yes'}[newDict['armorcheck']] == "yes":
            if 'fullXml' in kwargs:
                acp = int(kwargs['fullXml'].find("penalties/penalty[@name='Armor Check Penalty']").get('value'))
                newDict['valuenoacp'] = str(int(newDict['value']) - acp)
                if acp < 0:
                    newDict['text'] = "%+d/%+d" % (int(newDict['value']),int(newDict['valuenoacp']))
        if 'trainedonly' in newDict and newDict['trainedonly'] == 'yes':
            if int(newDict['ranks']) <= 0:
                del newDict['value']
                if 'valuenoacp' in newDict: del newDict['valuenoacp']
                #newDict['text'] = u'\u2014' # em-dash
                newDict['text'] = 'N/A'
        # reset the current element with new attributes
        elem.clear()
        [elem.set(*a) for a in newDict.items()]
        elem.text = newText
        elem.tail = newTail
        elem.extend(newSubs)
        # create a new subelement of the parent with the new tag and atributes
        se = et.SubElement(oldElement,newTag,newDict)
        se.text = newText
        se.tail = newTail
        se.extend(newSubs)
        if nameList[0] in ['Craft','Knowledge','Perform','Profession']:
            # now do the same but with just the main name as the tag
            newTag = nameList[0].lower()
            se = et.SubElement(oldElement,newTag,newDict)
            se.text = newText
            se.tail = newTail
            se.extend(newSubs)
    return oldElement

def _addFeatsAttributes(oldElement,*args,**kwargs):
    # find and append elements
    for elem in list(oldElement):
        newDict = dict(elem.items())
        newText = elem.text
        newTail = elem.tail
        newSubs = list(elem)
        if 'profgroup' not in newDict:
            newDict['profgroup'] = 'no'
        if 'useradded' not in newDict:
            newDict['useradded'] = 'yes'
        # reset the current element with new attributes
        elem.clear()
        [elem.set(*a) for a in newDict.items()]
        elem.text = newText
        elem.tail = newTail
        elem.extend(newSubs)
    return oldElement

def _addBetterNamedElements(oldElement,*args,**kwargs):
    # find and append elements
    for elem in list(oldElement):
        if (elem.get('name')):
            nameList = re.split(r'[\s().;,:]',elem.get('name'))
            # first add elements with tags besed on specific subname
            newTag = nameList[0].lower() + "".join([i.capitalize() for i in nameList[1:]])
            newDict = dict(elem.items())
            newText = elem.text
            se = et.SubElement(oldElement,newTag,newDict)
            se.text = newText
            se.extend(list(elem))
    return oldElement

def _addMeleeAttributes(oldElement,*args,**kwargs):
    # find and append elements
    for elem in list(oldElement):
        if elem.tag != "weapon": continue
        newDict = dict(elem.items())
        newText = elem.text
        newTail = elem.tail
        newSubs = list(elem)
        if 'summary' not in newDict:
            newDict['summary'] = "%(name)s(%(typetext)s)" % newDict
            if 'equipped' in newDict: newDict['summary'] += " %s" % newDict['equipped']
            newDict['summary'] += " %(attack)s (%(damage)s %(crit)s)" % newDict
        if 'namequant' not in newDict:
            newDict['namequant'] = _getNameQuant(newDict)
        if 'weightLbs' not in newDict:
            newDict['weightLbs'] = _getWeightLbs(elem)
        if 'costGp' not in newDict:
            newDict['costGp'] = _getCostGp(elem)
        # reset the current element with new attributes
        elem.clear()
        [elem.set(*a) for a in newDict.items()]
        elem.text = newText
        elem.tail = newTail
        elem.extend(newSubs)
    return oldElement

def _addRangedAttributes(oldElement,*args,**kwargs):
    # find and append elements
    for elem in list(oldElement):
        if elem.tag != "weapon": continue
        newDict = dict(elem.items())
        newText = elem.text
        newTail = elem.tail
        newSubs = list(elem)
        if 'summary' not in newDict:
            newDict['summary'] = "%(name)s(%(typetext)s)" % newDict
            if 'equipped' in newDict: newDict['summary'] += " %s" % newDict['equipped']
            if elem.find('rangedattack') != None:
                newDict['summary'] += " %(attack)s %(range)s" % {'attack':elem.find('rangedattack').get('attack',newDict['attack']),
                                                                     'range':elem.find('rangedattack').get('rangeinctext','')}
            else:
                newDict['summary'] += " %(attack)s" % newDict
            newDict['summary'] += " (%(damage)s %(crit)s)" % newDict
        if 'namequant' not in newDict:
            newDict['namequant'] = _getNameQuant(newDict)
        if 'weightLbs' not in newDict:
            newDict['weightLbs'] = _getWeightLbs(elem)
        if 'costGp' not in newDict:
            newDict['costGp'] = _getCostGp(elem)
        # reset the current element with new attributes
        elem.clear()
        [elem.set(*a) for a in newDict.items()]
        elem.text = newText
        elem.tail = newTail
        elem.extend(newSubs)
    return oldElement

def _getNameQuant(newDict):
    q = 1
    nq = ''
    if 'left' in newDict and newDict['left']:
        q = int(newDict['left'])
    elif 'quantity' in newDict and newDict['quantity']:
        q = int(newDict['quantity'])
    if q == 0:
        if re.search(r'(?i)at will',newDict['name']): nq = newDict['name']
    elif q > 1:
        nq = "%s [%d]" % (newDict['name'],q)
    else:
        nq = newDict['name']
    return nq
    
def _getWeightLbs(elem):
    if elem.findall('weight'):
        return elem.findall('weight')[0].get('value')
    else:
        return ''

def _getCostGp(elem):
    if elem.findall('cost'):
        return elem.findall('cost')[0].get('value')
    else:
        return ''
        
def _addNameQuantAttribute(oldElement,*args,**kwargs):
    # find and append elements
    for elem in list(oldElement):
        newDict = dict(elem.items())
        newText = elem.text
        newTail = elem.tail
        newSubs = list(elem)
        if 'namequant' not in newDict:
            newDict['namequant'] = _getNameQuant(newDict)
        if 'weightLbs' not in newDict:
            newDict['weightLbs'] = _getWeightLbs(elem)
        if 'costGp' not in newDict:
            newDict['costGp'] = _getCostGp(elem)
        # reset the current element with new attributes
        elem.clear()
        [elem.set(*a) for a in newDict.items()]
        elem.text = newText
        elem.tail = newTail
        elem.extend(newSubs)
    return oldElement

def _addItemAttributes(oldElement,*args,**kwargs):
    # find and append elements
    for elem in list(oldElement):
        newDict = dict(elem.items())
        newText = elem.text
        newTail = elem.tail
        newSubs = list(elem) 
        if elem.tag == "weapon" or 'realmworkscategory' in newDict and re.search(r'(?i)weapon',newDict['realmworkscategory']):
            if 'summary' not in newDict:
                newDict['summary'] = 'size' in newDict and SIZEDICT[newDict['size'][1]] + " " or ""
                newDict['summary'] += "%(name)s(%(typetext)s)" % newDict
                if 'equipped' in newDict: newDict['summary'] += " %s" % newDict['equipped']
                if elem.find('rangedattack') != None:
                    newDict['summary'] += " %(attack)s %(range)s" % {'attack':elem.find('rangedattack').get('attack',newDict['attack']),
                                                                         'range':elem.find('rangedattack').get('rangeinctext','')}
                else:
                    newDict['summary'] += " %(attack)s" % newDict
                newDict['summary'] += " (%(damage)s %(crit)s)" % newDict
            if elem.find('rangedattack') != None:
                newDict['rangeattack'] = elem.find('rangedattack').get('attack',newDict['attack'])
                newDict['rangeinc'] = elem.find('rangedattack').get('rangeinctext','')
            if elem.find('situationalmodifiers') != None:
                newDict['situational'] = elem.find('situationalmodifiers').get('text','')
        if elem.find('itemslot') != None:
            newDict['itemslottext'] = elem.find('itemslot').text
        if 'namequant' not in newDict:
            newDict['namequant'] = _getNameQuant(newDict)
        if 'weightLbs' not in newDict:
            newDict['weightLbs'] = _getWeightLbs(elem)
            #if newDict['weightLbs'] == '': del newDict['weightLbs']
        if 'costGp' not in newDict:
            newDict['costGp'] = _getCostGp(elem)
            #if newDict['costGp'] == '': del newDict['costGp']
        #if 'size' not in newDict:
        newDict['size'] = 'size' in newDict and SIZEDICT[newDict['size'][1]] or " "
        #if newDict['size'] == '': del newDict['size']
        # reset the current element with new attributes

        for k in ['summary','quantity','weightLbs','costGp','name','categorytext',
              'typetext','attack','crit','damage','rangeattack','rangeinc',
              'ac','itemslottext','size','situational','realmworkscategory']:
            if k not in newDict:
                newDict[k] = ' ';

        elem.clear()
        [elem.set(*a) for a in newDict.items()]
        elem.text = newText
        elem.tail = newTail
        elem.extend(newSubs)
    return oldElement
    
def _addTypeAndValueAttribute(oldElement,*args,**kwargs):
    # find and append elements
    for elem in list(oldElement):
        newDict = dict(elem.items())
        newText = elem.text
        newTail = elem.tail
        newSubs = list(elem)
        if 'type' not in newDict and 'value' not in newDict and 'shortname' in newDict:
            (newDict['type'],newDict['value']) = re.split(r' ',newDict['shortname'])
        # reset the current element with new attributes
        elem.clear()
        [elem.set(*a) for a in newDict.items()]
        elem.text = newText
        elem.tail = newTail
        elem.extend(newSubs)
    return oldElement


class Icon(object):
    """
    Class to contain an individual icon reference which may point to one or more images

    attributes are
    name: short identifiing name
    group: group of thing to which the icon applies
    summary: summary of the icon
    index: index number for icon
    imageHigh: (filename,fullpath) tupple for high resolution image
    imageLow: (filename,fullpath) tupple for low resolution image
    """
    def __init__(self,iconFile,indexIconElement,*args,**kwargs):
        """
        iconFile is an open zipfile of the icon data
        indexIconElement is the element from the index.xml refering to the current icon
        """
        if 'verbosity' not in kwargs: kwargs['verbosity'] = VERBOSITY
        self.verbosity = kwargs['verbosity']
        self.indexXml = indexIconElement
        self.name = self.indexXml.get('name')
        self.group = self.indexXml.get('group')
        self.summary = self.indexXml.get('summary')
        self.index = int(self.indexXml.get('iconindex'))
        self.imageHigh = None
        self.imageLow = None
        # extract the image files and copy them to a temporary directory
        if 'tempDir' in kwargs and os.path.isdir(kwargs['tempDir']):
            self.tempDir = kwargs['tempDir']
        else:
            self.tempDir = tempfile.mkdtemp(prefix='HL-GoogleSlides-Icon-')
        for image in self.indexXml.findall('./images/image'):
            if image.get("resolution") == "high":
                try:
                    self.imageHigh = (
                        image.get('filename'),
                        iconFile.extract("%s/%s" % (image.get('folder'),image.get('filename')),self.tempDir))
                except KeyError:
                    print("WARNING: There is no high resolution icon %s/%s for %s (%s)" %
                        (image.get('folder'),image.get('filename'),self.name,self.group))
            else:
                try:
                    self.imageLow = (
                        image.get('filename'),
                        iconFile.extract("%s/%s" % (image.get('folder'),image.get('filename')),self.tempDir))
                except KeyError:
                    print("WARNING: There is no low resolution icon %s/%s for %s (%s)" %
                        (image.get('folder'),image.get('filename'),self.name,self.group))

class Icons(object):
    """
    Class to contain icon image references for things like
    creature type, terrain, and climate.
    """
    def __init__(self,iconFile,*args,**kwargs):
        """
        An icon file is a zip file similar to how a HeroLab portfilo works
        there is an index.xml which defines and points to all the icon images
        """
        if 'verbosity' not in kwargs: kwargs['verbosity'] = VERBOSITY
        self.verbosity = kwargs['verbosity']
        if type(iconFile) is not zipfile.ZipFile:
            iconFile = zipfile.ZipFile(iconFile,'r')
        if self.verbosity >= 2: print("icons filename: %s" % iconFile.filename)
        self.iconFile = iconFile
        self.filename = iconFile.filename
        self.filepath = os.path.split(iconFile.filename)[0]
        self.filecore = os.path.splitext(os.path.basename(iconFile.filename))[0]
        if self.verbosity >= 2: print("icons filecore: %s" % self.filecore)
        indexXml = iconFile.open('index.xml')
        indexTree = et.parse(indexXml)
        indexXml.close()
        if self.verbosity >= 6:
            print("Dump of Index XML:")
            et.dump(indexTree)
        # create a temporary directory for icon images
        self.tempDir = tempfile.mkdtemp(prefix='HL-GoogleSlides-Icons-')
        if self.verbosity >= 2: print("Temp Icon Directory: %s" % self.tempDir)
        self.icons = []
        for i in indexTree.findall('./icons/icon'):
            self.icons.append(Icon(self.iconFile,i,*args,tempDir=self.tempDir,**kwargs))

        # debug printing and create names attribute
        self.names = {}
        for i in self.icons:
            if i.group not in self.names: self.names[i.group] = []
            self.names[i.group].append(i.name)
            if self.verbosity >= 3:
                print("icon #%d: %s (%s)" % (i.index,i.name,i.group))
            if self.verbosity >= 4:
                print("  images:")
                if i.imageHigh: print("    high %s: %s" % i.imageHigh)
                if i.imageLow: print("    low %s: %s" % i.imageLow)

        # close the iconFile
        self.iconFile.close()

    def getIcon(self,iconName,iconGroup="type",**kwargs):
        """
        supply the name and group to retrieve the Icon instance
        """
        for i in self.icons:
            if i.group == iconGroup.lower() and i.name == iconName.lower():
                return i
        return None

    def getMatches(self,sourceText,iconGroup="type",**kwargs):
        """
        sourceText is split into words and a list of icon instances
        of iconGroup are returned
        """
        rtnList = []
        for word in re.split(r'\W+',sourceText):
            if len(word) < 3: continue
            for name in self.names[iconGroup]:
                if re.search(name,word,re.I):
                    myIcon = self.getIcon(name,iconGroup)
                    if myIcon: rtnList.append(myIcon)
        # the "any" icons are reserved to be used if nothing else fits
        # this should work as long as there are not two "any" icons in a row
        if len(rtnList) > 1:
            for idx,icon in enumerate(rtnList):
                if icon.name == "any":
                    del rtnList[idx]
        return rtnList

    def close(self):
        """
        clean up temporary files and directories
        """
        shutil.rmtree(self.tempDir)

class Feature(object):
    """Class for a feature of a character (each element and attribute of the XML)

    Methods:
       abbreviate: abbreviate the value of a string attribute

    Attributes:
       fTag: (str) the XML element tag  for the feature
       fText: (str) text between start and end XML element tags (no child tags)
       fAttr: (list) list of attributes from the XML tag
       fSub: (list) list of Features generated from subelements of this Feature
       xxx: (Feature/str) each XML tag attribute gets an instance attribute which
          hold the string of the value for that attribute.
          Any subelement which has a unique tag within the element gets
          a feature attribute.
       xxxList: (list) if there are multiple subelements with the same tag,
         they appended to a list based on their tag
       fParent: (Feature) parent Feature of nested instance
       fCharacter: (Character) parent Character of nested instance
       fPortfolio: (Portfolio) parent Portfolio of fCharacter
       _fAbbreviate: (list) abbreviation tuples for values and text
    """
    def __init__(self,element,parent,*args,**kwargs):
        """Create a feature for the character

        Args:
           element: (et.Element) instance XML element on which this feature
              will be based
           parent: (Feature/Character) parent of nested Feature

        Kwargs:
            portfolio: (Portfolio) instance of portfolio containing character
        """
        # element must be an et.Element
        assert et.iselement(element),"%s is not an XML element" % element
        assert isinstance(parent,Character) or isinstance(parent,Feature), \
                        "parent %s is must be a Character or Feature" % parent
        # assign identifying and text attributes
        self.fParent = parent
        if type(parent) == Character:
            self.fCharacter = parent
        else:
            self.fCharacter = self.fParent.fCharacter
        if 'portfolio' in kwargs and type(kwargs['portfolio']) == Portfolio:
            self.fPortfolio = kwargs['portfolio']
        # assign any abbreviations
        self._fAbbreviate = element.tag in Character.abbreviations and \
            Character.abbreviations[element.tag] or []
        # perform any swapOuts
        if element.tag in Character.swapOuts and Character.swapOuts[element.tag]:
            # find match in character's HTML
            (myPattern,myFunction) = Character.swapOuts[element.tag]
            myMatch = re.search(myPattern,self.fCharacter.statHtml)
            #print(myPattern,self.fCharacter.name)
            #assert myMatch, "No match in HTML for %s attribute" % element.tag
            # use et.fromstring and the swapOut's function to replace the element
            if myMatch: element = myFunction(element,*myMatch.groups(),fullXml=self.fCharacter.statXml)
        self.fTag = element.tag
        self.fText = element.text
        self.fAttr = element.keys()
        self.fSub = []
        # assign Feature attributes from element items
        [setattr(self,item[0],item[1]) for item in element.items()]
        #if element.tag == "spelllevel":
        #    print("level:",element.items())
        
        ### Doing it this way works for creating subelements
        ### but for choosing the featrure class to use
        ### while creating the element, I need to make the check in the
        ### element items loop
        ## determine class for subelements
        #if element.tag in Character.featureClass and Character.featureClass[element.tag]:
        #    FeatureClass = Character.featureClass[element.tag]
        #else:
        #    FeatureClass = Feature
        ## append Features to the fSub array for subfeatures
        #[self.fSub.append(FeatureClass(elem,self)) for elem in list(element)]
        ### So I will do it this way
        for elem in list(element):
            if elem.tag in Character.featureClass and Character.featureClass[elem.tag]:
                FeatureClass = Character.featureClass[elem.tag]
            else:
                FeatureClass = Feature
            self.fSub.append(FeatureClass(elem,self))
                
        myCount = Counter([item.fTag for item in self.fSub])
        for idx,sub in enumerate(self.fSub):
            if myCount[sub.fTag] == 1:
                setattr(self,sub.fTag,sub)
            myList = hasattr(self,"%sList" % sub.fTag) and \
                     getattr(self,"%sList" % sub.fTag) or []
            myList.append(sub)
            setattr(self,"%sList" % sub.fTag,myList[:])
        ##  This was for test print statements only
        if False and element.tag in Character.featureClass and Character.featureClass[element.tag]:
            if len(self.fSub) > 0: 
                    print(element.tag,dir(self),len(self.fSub))
                    print(dir(self.fSub),dir(self.fSub[-1]))
                    if hasattr(self,'spellSort'):
                        print(list(self.spellSort(0)))
                    if hasattr(self,'spellClassSort'):
                        print(list(self.spellClassSort(0)))

    def abbreviate(self,attribute,abbrList=[],**kwargs):
        """abbreviate feature values with re.sub based on Feature tag

        Args:
           attribute: (str) name of attribute which will be abbreviated
           abbrList: (list) alternate list of abbreviations tuples to use
        """
        assert hasattr(self,attribute),"%s must be an attribute of %s" % (attribute,self)
        inString = getattr(self,attribute)
        assert type(inString) == str or type(inString) == unicode, "%s must be a string not %s" % (inString,type(inString))
        # figure out list of abbreviation tuples
        myAbbreviate = abbrList
        # if there are no abbrList consider alternatives
        if not myAbbreviate:
            # first if there is a 'abbr' attribute return it instead
            if hasattr(self,"%sabbr" % attribute): return getattr(self,"%sabbr" % attribute)
            # second if the attr is 'text' and there is a 'value' return it instead
            if attribute == 'text' and hasattr(self,'value'): return getattr(self,'value')
            # next dig up in order to find abbreviations
            myAbbreviate = hasattr(self,'_fAbbreviate') and self._fAbbreviate or []
            myTarget = self.fParent
            while not myAbbreviate and hasattr(myTarget,'_fAbbreviate'):
                myAbbreviate = myTarget._fAbbreviate
                myTarget = myTarget.fParent
        # if there are still no abbreviation just return the unaltered value
        if not myAbbreviate:
            return inString
        # apply all abbreviations
        for a in myAbbreviate:
                inString = re.sub(a[0],a[1],inString)
        return inString

    def describe(self,attribute,prepend=None,**kwargs):
        """return description text for the feature

        Args:
           attribute: (str) name of attribute for which to find decription text
        """
        myDescription = prepend and "%s: " % prepend or ""
        assert hasattr(self,attribute),"%s must be an attribute of %s" % (attribute,self)
        if hasattr(self,'description') and hasattr(getattr(self,'description'),'fText'):
            # return the description fText, but replacing any new lines for spaces
            return re.sub(r'(?m)[\n\r\f\v]',' ',"%s%s" % (myDescription,getattr(getattr(self,'description'),'fText')))
        else:
            return myDescription

class SpellFeature(Feature):
    def spellSort(self,*args,**kwargs):
        spells = hasattr(self,'spellList') and sorted([(i.level,i.name) for i in self.spellList],key=lambda x:("0" + x[0])[-2:]+x[1]) or []
        lvl = -1
        for sp in spells:
            levelText = lvl < sp[0] and " (%s):%s" % sp or "%s" % sp[1]
            lvl = sp[0]
            yield levelText

class SpellClassFeature(Feature):
    def spellClassSort(self,*args,**kwargs):
        classes = hasattr(self,'spellclassList') and sorted([i for i in self.spellclassList],key=lambda x:x.name) or []
        for cls in classes:
            if hasattr(cls,"maxspelllevel") and type(cls.maxspelllevel) and not type(None) and int(cls.maxspelllevel) > -1:
                if hasattr(cls,"spelllevelList") and len(cls.spelllevelList) > 0:
                    yield cls.name + " " + ",".join(["%s/%s" % (i.level,getattr(i,'maxcasts',hasattr(i,'unlimited') and i.unlimited == "yes" and '*' or '')) for i in cls.spelllevelList])

class Character(object):
    """Class for a single character from a portfolio

    Methods:

    Class Attribute:
       abbreviations: XML element tag keyed dictionary of regexp substitutions.

    Attributes:
       verbosity: (int) level of verbose debug message
       indexXml: (Element) instance of character from index.xml
       statText: (str) character's entire text statblock
       statHtml: (str) character's entire HTML statblock
       statXml: (Element) instance of character from the xml statblock
       isMinion: (bool): is this character a minion of another character
       parent: (Character) instance of minion's parent Character
       tempDir: (str) absolute path of temporary directory for image extraction
       imageList: (list) list of (filename,absFilename) tuples for character in order
       image: (tuple) first (filename,absFilename) tuple for extracted images
       feature: (Feature) top level charater feature drawn from the statblock
       portfolio: (Portfolio) reference to portfolio containing the character
    """
    # abbreviations is a list of tuples which has a regexp pattern as the first
    # value in the tuple and the replacement text as the second value.
    # such that re.sub(val[0],val[1],string)
    #  would return the modified string
    abbreviations = {
     'skills':[
      (r'(?i)Acrobatics', r'Acro'),
      (r'(?i)Appraise', r'Appr'),
      (r'(?i)Bluff', r'Bluf'),
      (r'(?i)Climb', r'Clmb'),
      (r'(?i)Craft\b(\s*\(\s*(\w*?)\s*\))', r'Crft(\2)'),
      (r'(?i)Diplomacy', r'Dipl'),
      (r'(?i)Disable Device', r'DsDv'),
      (r'(?i)Disguise', r'Disg'),
      (r'(?i)Escape Artist', r'Escp'),
      (r'(?i)Fly', r'Fly'),
      (r'(?i)Handle Animal', r'HdAn'),
      (r'(?i)Heal', r'Heal'),
      (r'(?i)Intimidate', r'Intm'),
      (r'(?i)Knowledge\b(\s*\(\s*(\w*?)\s*\))', r'Know(\2)'),
      (r'(?i)Linguistics', r'Ling'),
      (r'(?i)Perception', r'Perc'),
      (r'(?i)Perform\b(\s*\(\s*(\w*?)\s*\))', r'Prfm(\2)'),
      (r'(?i)Profession\b(\s*\(\s*(\w*?)\s*\))', r'Prof(\2)'),
      (r'(?i)Ride', r'Ride'),
      (r'(?i)Sense Motive', r'SnsM'),
      (r'(?i)Sleight of Hand', r'SHnd'),
      (r'(?i)Spellcraft', r'Spel'),
      (r'(?i)Stealth', r'Slth'),
      (r'(?i)Survival', r'Surv'),
      (r'(?i)Swim', r'Swim'),
      (r'(?i)Use Magic Device', r'UMDv'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*alchemy\s*\)', r'Crft(alch)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*armor\s*\)', r'Crft(armr)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*baskets\s*\)', r'Crft(bskt)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*books\s*\)', r'Crft(book)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*bows\s*\)', r'Crft(bow)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*calligraphy\s*\)', r'Crft(cali)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*carpentry\s*\)', r'Crft(cpnt)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*cloth\s*\)', r'Crft(fbrc)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*fabric\s*\)', r'Crft(fbrc)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*clothing\s*\)', r'Crft(clos)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*glass\s*\)', r'Crft(glas)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*jewlery\s*\)', r'Crft(jelr)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*leather\s*\)', r'Crft(lthr)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*locks\s*\)', r'Crft(lcks)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*paintings\s*\)', r'Crft(pait)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*pottery\s*\)', r'Crft(potr)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*sculptures\s*\)', r'Crft(sclp)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*ships\s*\)', r'Crft(ship)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*shoes\s*\)', r'Crft(shoe)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*stonemasonry\s*\)', r'Crft(ston)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*traps\s*\)', r'Crft(trap)'),
      (r'(?i)(Craft)|(Crft)\b\s*\(\s*weapons\s*\)', r'Crft(wpn)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*arcana\s*\)', r'Know(arca)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*dungeoneering\s*\)', r'Know(dugn)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*engineering\s*\)', r'Know(egnr)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*geography\s*\)', r'Know(geog)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*history\s*\)', r'Know(hist)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*local\s*\)', r'Know(locl)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*nature\s*\)', r'Know(natr)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*nobility\s*\)', r'Know(nobl)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*planes\s*\)', r'Know(plan)'),
      (r'(?i)Know(ledge)?\b\s*\(\s*religion\s*\)', r'Know(relg)'),
      (r'(?i)(Perform)|(Prfm)\b\s*\(\s*act\s*\)', r'Prfm(act)'),
      (r'(?i)(Perform)|(Prfm)\b\s*\(\s*comedy\s*\)', r'Prfm(cmdy)'),
      (r'(?i)(Perform)|(Prfm)\b\s*\(\s*dance\s*\)', r'Prfm(danc)'),
      (r'(?i)(Perform)|(Prfm)\b\s*\(\s*keyboard(\s?instruments?)?\s*\)', r'Prfm(key)'),
      (r'(?i)(Perform)|(Prfm)\b\s*\(\s*oratory\s*\)', r'Prfm(orat)'),
      (r'(?i)(Perform)|(Prfm)\b\s*\(\s*percussion(\s?instruments?)?\s*\)', r'Prfm(prcs)'),
      (r'(?i)(Perform)|(Prfm)\b\s*\(\s*string(\s?instruments?)?\s*\)', r'Prfm(strg)'),
      (r'(?i)(Perform)|(Prfm)\b\s*\(\s*wind(\s?instruments?)?\s*\)', r'Prfm(wind)'),
      (r'(?i)(Perform)|(Prfm)\b\s*\(\s*sing\s*\)', r'Prfm(sing)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*architect\s*\)', r'Prof(arct)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*baker\s*\)', r'Prof(bake)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*barrister\s*\)', r'Prof(brst)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*brewer\s*\)', r'Prof(brew)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*butcher\s*\)', r'Prof(butc)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*clerk\s*\)', r'Prof(clrk)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*cook\s*\)', r'Prof(cook)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*courtesan\s*\)', r'Prof(crts)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*driver\s*\)', r'Prof(driv)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*engineer\s*\)', r'Prof(egnr)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*farmer\s*\)', r'Prof(farm)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*fisherman\s*\)', r'Prof(fish)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*gambler\s*\)', r'Prof(gmbl)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*gardener\s*\)', r'Prof(grdn)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*herbalist\s*\)', r'Prof(herb)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*innkeeper\s*\)', r'Prof(innk)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*librarian\s*\)', r'Prof(libr)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*merchant\s*\)', r'Prof(mrch)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*mecenary\s*\)', r'Prof(merc)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*midwife\s*\)', r'Prof(midw)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*miller\s*\)', r'Prof(mill)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*miner\s*\)', r'Prof(mine)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*porter\s*\)', r'Prof(port)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*sailor\s*\)', r'Prof(sail)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*scribe\s*\)', r'Prof(scrb)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*shepherd\s*\)', r'Prof(shep)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*stable master\s*\)', r'Prof(stbl)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*soldier\s*\)', r'Prof(sldr)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*tanner\s*\)', r'Prof(tanr)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*trapper\s*\)', r'Prof(trap)'),
      (r'(?i)Prof(ession)?\b\s*\(\s*woodcutter\s*\)', r'Prof(wood)'),
     ],
     'gear':[
      (r'(?i)(M)asterwork', r'\1wk'),
      (r'(?i)(F)avored', r'\1vrd'),
     ],
     'dc' :[
      (r'DC (\d+)(?!\d)',r'DC\1'),
     ],
     'alignment':[
      (r'(?i)Lawful Good','LG'),
      (r'(?i)Lawful Neutral','LN'),
      (r'(?i)Lawful Evil','LE'),
      (r'(?i)Neutral Good','NG'),
      (r'(?i)Neutral','N'),
      (r'(?i)True Neutral','N'),
      (r'(?i)Neutral Evil','NE'),
      (r'(?i)Chaotic Good','CG'),
      (r'(?i)Chaotic Neutral','CN'),
      (r'(?i)Chaotic Evil','CE'),
     ],
     'size':[
      (r'Colossal','C'),
      (r'Gargantuan','G'),
      (r'Huge','H'),
      (r'Large','L'),
      (r'Medium','M'),
      (r'Small','S'),
      (r'Tiny','T'),
      (r'Diminutive','D'),
      (r'Fine','F'),
     ],
     'senses':[
      (r'(?i)(A)ll-Around Vision',r'\1ll-\1rnd'),
      (r'(?i)(B)lindsense',r'\1lndsns'),
      (r'(?i)(B)lindsight',r'\1lndsght'),
      (r'(?i)(D)arkvision',r'\1ark'),
      (r'(?i)(D)ragon Senses',r'\1rgn sns'),
      (r'(?i)(G)reensight',r'\1reen'),
      (r'(?i)(K)een (S)cent',r'\1een \2cnt'),
      (r'(?i)(L)ifesense',r'\1ifesns'),
      (r'(?i)(L)ow-Light Vision',r'\1ow'),
      (r'(?i)(M)istsight',r'\1ist'),
      (r'(?i)(S)cent',r'\1cent'),
      (r'(?i)(S)ee in (D)arkness',r'\1ee \2ark'),
      (r'(?i)(T)houghtsense',r'\1hghtsns'),
      (r'(?i)(T)remorsense',r'\1remor'),
      (r'(?i)(X)-Ray Vision',r'\1-ray'),
     ],
     'auras':[
      (r'(?i)Aura of (G)ood',r'\1ood'),
      (r'(?i)Aura of (E)vil',r'\1vil'),
      (r'(?i)Aura of (L)aw(ful)?',r'\1aw'),
      (r'(?i)Aura of (C)hao(s|tic)',r'\1haos'),
      (r'(?i)Aura of (D)estruct(ion|ive)',r'\1estry'),
      (r'(?i)Aura of (C)ourage',r'\1ourge'),
      (r'(?i)Aura of (C)owardice',r'\1owrd'),
      (r'(?i)Aura of (R)esolve',r'\1slv'),
      (r'(?i)Aura of (F)ear',r'\1ear'),
      (r'(?i)(G)ood( Aura)?',r'\1ood'),
      (r'(?i)(E)vil( Aura)?',r'\1vil'),
      (r'(?i)(L)aw(ful)?( Aura)?',r'\1aw'),
      (r'(?i)(C)hao(s|tic)( Aura)?',r'\1haos'),
      (r'(?i)(D)estruct(ion|ive)( Aura)?',r'\1estry'),
      (r'(?i)(C)ourage( Aura)?',r'\1ourge'),
      (r'(?i)(C)owardice( Aura)?',r'\1owrd'),
      (r'(?i)(R)esolve( Aura)?',r'\1slv'),
      (r'(?i)(F)ear( Aura)?',r'\1ear'),
      (r'(?i)(E)motion( Aura)?',r'\1mtn'),
      (r'(?i)(F)rightful (P)resence( Aura)?',r'\1rght \2rsnc'),
      (r'(?i)(M)ental (S)tatic( Aura)?',r'\1ntl \2ttc'),
      (r'(?i)(S)tench( Aura)?',r'\1tnch'),
      (r'(?i)(U)nnatural( Aura)?',r'\1nntrl'),
     ],
     'personal':[
      (r'(?i)Female','F'),
      (r'(?i)Male','M'),
     ],
     'resistances':[
      (r'(?i)spells\s*(\d+)\b',r'SR\1'),
     ],
     'damagereduction':[
      (r'(?i)^(\d+)/',r'DR\1/'),
     ],
     'penalties':[
      (r'(?i)Armor Check( Penalty)?',r'ACP'),
      (r'(?i)Max(imum)? Dex(terity)? Bonus',r'MaxDEX'),
     ],
     'maneuvers':[
      (r'(?i)(A)ll',r'\1ll'),
      (r'(?i)(A)wesome (B)low',r'\2low'),
      (r'(?i)(B)ull (R)ush',r'\1ull'),
      (r'(?i)(D)irty (T)rick',r'\2rck'),
      (r'(?i)(D)isarm',r'\1srm'),
      (r'(?i)(D)rag',r'\1rag'),
      (r'(?i)(F)eint',r'\1eint'),
      (r'(?i)(G)rapple',r'\1rppl'),
      (r'(?i)(O)verrun',r'\1vrrn'),
      (r'(?i)(P)ull',r'\1ull'),
      (r'(?i)(P)ush',r'\1ush'),
      (r'(?i)(R)eposition',r'\1epos'),
      (r'(?i)(S)teal',r'\1tl'),
      (r'(?i)(S)under',r'\1ndr'),
      (r'(?i)(T)rip',r'\1rp'),
     ],
     'movement':[
      (r'\b(\d+)\s*ft.',r"\1'"),
      (r'(?i)basespeed','base'),
      (r'(?i)\bspeed','crnt'),
      (r'(?i)burrow','brrw'),
      (r'(?i)swim','swim'),
      (r'(?i)fly','fly'),
      (r'(?i)climb','clmb'),
      (r'(?i)earth glide','erth gld'),
      (r'(?i)jet','jet'),
      (r'(?i)clumsy','clmsy'),
      (r'(?i)poor','poor'),
      (r'(?i)average','ave'),
      (r'(?i)good','good'),
      (r'(?i)perfect','prfct'),
     ],
     'encumbrance':[
      (r'(?i)encumbrance( Load)?','E'),
      (r'(?i)Over( Load)?','OL'),
      (r'(?i)Heavy( Load)?','H'),
      (r'(?i)Medium( Load)?','M'),
      (r'(?i)Light( Load)?','L'),
     ],
     'animaltricks':[
      (r'(?i)\s?\[Trick\]',''),
     ],
     'weapon':[
      (r'(?i)(M)asterwork', r'\1wk'),
     ],
    }
    abbreviations['all'] = [item for sublist in abbreviations.values() for item in sublist]
    abbreviations['none'] = []
    alignment = {
      'LG':'Lawful Good',
      'LN':'Lawful Neutral',
      'LE':'Lawful Evil',
      'NG':'Neutral Good',
      'N':'True Neutral',
      'NE':'Neutral Evil',
      'CG':'Chaotic Good',
      'CN':'Chaotic Neutral',
      'CE':'Chaotic Evil',
    }
    sizes = SIZEDICT

    # the swapOuts dictionary has element tags as the keys, and a two item
    # tuple for each value.  The first item is a regular expression string
    # which can be searched for (re.search) in the statHtml.  The second item
    # is a function used to replace the element.  The function should return
    # the replacement et.Element.  The first argument passed to the function
    # is the element to be replaced, the rest of the arguments are the
    # resultant groups() from the re.search match
    swapOuts = {
     'movement': (r'<b>Speed\s*</b>([^<]+)\s*<br/>',_setOtherSpeeds),
     'types': (r'(?m)<br/>\s*[LCN][ENG]?\s+[CGHLMSTDF]\w*\s+([^<]+)<br/>',_setTrueTypes),
     'subtypes': (r'(?m)<br/>\s*[LCN][ENG]?\s+[CGHLMSTDF]\w*\s+([^<]+)<br/>',_setTrueSubtypes),
     'spellclasses': (r'(?ms)<br/>\n<b>([^<]+ (Spells|Extracts) (Known|Prepared)\s*</b>\s*\(CL.*)<br/>\n<hr/><b>Statistics',_setTrueSpellclass),
     'npc': (r'(?m)^(.*)$',_addBetterNpcInfo),
     'skills': (r'(?m)^(.*)$',_addBetterSkillsElements),
     'feats': (r'(?m)^(.*)$',_addFeatsAttributes),
     'penalties': (r'(?m)^(.*)$',_addBetterNamedElements),
     'attributes': (r'(?m)^(.*)$',_addBetterNamedElements),
     'saves': (r'(?m)^(.*)$',_addBetterNamedElements),
     'maneuvers': (r'(?m)^(.*)$',_addBetterNamedElements),
     'melee': (r'(?m)^(.*)$',_addItemAttributes),
     'ranged': (r'(?m)^(.*)$',_addItemAttributes),
     'defenses': (r'(?m)^(.*)$',_addItemAttributes),
     'magicitems': (r'(?m)^(.*)$',_addItemAttributes),
     'spelllike': (r'(?m)^(.*)$',_addItemAttributes),
     'gear': (r'(?m)^(.*)$',_addItemAttributes),
     'allitems': (r'(?m)^(.*)$',_addItemAttributes),
     'trackedresources': (r'(?m)^(.*)$',_addItemAttributes),
     'resistances': (r'(?m)^(.*)$',_addTypeAndValueAttribute),
    }
    #htmlTypeSearch = r'(?m)<br/>\s*%s %s ([A-Za-z ]+)\b\s+(\(.*\))?<br/>' # % (align,size)
    #htmlSubtypeSearch = r'(?m)<br/>\s*%s %s [A-Za-z ]+\b\s+\((.*)\)<br/>' # % (align,size)
    #htmlMovementSearch = r'<b>Speed\s*</b>(.*)\s*<br/>'

    featureClass = {
      'spellsknown':SpellFeature,
      'spellsmemorized':SpellFeature,
      'spellbook':SpellFeature,
      'spellclasses':SpellClassFeature,
    }

    # featureIcons is used for matching icons to features
    # the key is the icon group, and the value is a two member tuple
    # where the first member is another two member tuple.  The first
    # member of this tuple is the flag to match, the second is a dictionary
    # of any attributes to narrow the fTag match.
    # The second member of the value tuple is the attribute to match
    # with the name of the icon.  This match is case in-sensitve
    # and with an optional appended 's' (which is really only
    # useful for some of the terrain group icons).  Only the first match is used
    # If a match is found an icon attribute is added to the feature
    # with the value from the result of getIcon.
    featureIcons = {
     'type':(('type',),'name'),
     'terrain':(('npcinfo',{'name':'Ecology - Environment'}),'fText'),
     'climate':(('npcinfo',{'name':'Ecology - Environment'}),'fText'),
    }
    
    # I want to be able to import the comma sepatated item lists into Realm Works
    # using the Realm Works importer.  So I want to match inventory items to
    # Realm Works categories.  This is a terrible way to do this, but oh well
    realmWorksCategoryName = {
      'melee/weapon':'Mundane Weapon',
      'ranged/weapon':'Mundane Weapon',
      'defenses/armor':'Mundane Armor/Shield',
      'magicitems/item':'Magic Item',
      'gear/item':'Mundane Item'
    }

    def __init__(self,porFile,indexCharacterElement,*args,**kwargs):
        """Create a Character from a porFile and an element from index.xml

        Args:
           porFile: (ZipFile) instance of open to read portfolio file
           indexCharacterElement: (Element) chacter element from index.xml

        Kwargs:
            parent: (Character) instance of a minion's parent, flag current as minion
            verbosity: (int) level of verbosity for debug messages
            portfolio: (Portfolio) portfolio which contains this character
        """
        if 'verbosity' not in kwargs: kwargs['verbosity'] = VERBOSITY
        self.verbosity = kwargs['verbosity']
        if 'portfolio' in kwargs and type(kwargs['portfolio']) == Portfolio:
            self.portfolio = kwargs['portfolio']
        self.indexXml = indexCharacterElement
        self.statText = None
        self.statHtml = None
        self.statXml = None
        self.isMinion = False
        # assign the identifying attributes from the xml to the Character instance
        self.name = self.indexXml.get('name')
        self.summary = self.indexXml.get('summary')
        self.herolabLeadIndex = int(self.indexXml.get('herolableadindex'))
        self.characterIndex = int(self.indexXml.get('characterindex'))
        self.myIndex = self.herolabLeadIndex
        if ('parent' in kwargs):
            assert type(kwargs['parent']) == Character, "%s is not a Character" % kwargs['parent']
            self.parent = kwargs['parent']
            # for minions, myIndex is the herolableadindex of the parent
            self.myIndex = self.parent.herolabLeadIndex
            self.isMinion = True
            # do not want this parent to get passed on to the Feature
            del kwargs['parent']
        # read in text statblock
        sb = self.indexXml.find("./statblocks/statblock[@format='text']")
        if (et.iselement(sb)):
            self.statText = porFile.read("%s/%s" % (sb.get('folder'),sb.get('filename')))
        # read in html statblock
        sb = self.indexXml.find("./statblocks/statblock[@format='html']")
        if (et.iselement(sb)):
            self.statHtml = porFile.read("%s/%s" % (sb.get('folder'),sb.get('filename')))
        # locate the XML or parent XML statblock and identify the minion status
        if self.isMinion:
            # for minions their xml is contained within the parent
            sb = self.parent.indexXml.find("./statblocks/statblock[@format='xml']")
        else:
            sb = self.indexXml.find("./statblocks/statblock[@format='xml']")
        # parse the XML file and get the statblock
        if (et.iselement(sb)):
            xmlFile = porFile.open("%s/%s" % (sb.get('folder'),sb.get('filename')))
            xml = et.parse(xmlFile)
            if self.isMinion:
                # extract the minion statblock specifically from the parents using the minion characterindex
                xmlPath = "./*/character/minions/character[@characterindex='%s']" % self.indexXml.get('characterindex')
                self.statXml = xml.find(xmlPath)
            else:
                # extract the xml statblock Element for the character
                self.statXml = xml.find("./*/character")
            xmlFile.close()
        # create a spetial allitems element which has all unique items from 
        allitems = et.SubElement(self.statXml,'allitems')
        # melee/weapons, ranged/weapon, defenses/armor, magicitems/item, and gear/item
        for itemStore in ["melee/weapon","ranged/weapon","defenses/armor","magicitems/item","gear/item"]:
            for item in self.statXml.findall(itemStore):
                if allitems.find("item") == None or not item.get('name') in [i.get('name') for i in list(allitems)]:
                    if 'useradded' in item.keys() and item.get('useradded') == 'no': break
                    newItem = et.SubElement(allitems,'item',dict(item.items()))
                    newItem.set('realmworkscategory',self.realmWorksCategoryName[itemStore])
                    newItem.text = item.text
                    newItem.tail = item.tail
                    newItem.extend(list(item))
        # extract the image files and copy them to a temporary directory
        if 'tempDir' in kwargs and os.path.isdir(kwargs['tempDir']):
            self.tempDir = kwargs['tempDir']
        else:
            self.tempDir = tempfile.mkdtemp(prefix='HL-GoogleSlides-Character-')
        #self.imageList = []
        #self.image = ()
        #for image in self.indexXml.findall('./images/image'):
        #    iFilename = image.get('filename')
        #    iAbsFilename = porFile.extract("%s/%s" % (image.get('folder'),image.get('filename')),self.tempDir)
        #    self.imageList.append((iFilename,iAbsFilename))
        #if self.imageList: self.image = self.imageList[0]
        self.images = None
        self.images = Feature(self.indexXml.find('./images'),self)
        if hasattr(self.images,'imageList'):
            for i in self.images.imageList:
                iAbsFilename = porFile.extract("%s/%s" % (i.folder,i.filename),self.tempDir)
                i.imageHigh = (i.filename,iAbsFilename)
                i.imageLow = (i.filename,iAbsFilename)
        # set all the rest of the character attributes
        for item in self.statXml.items():
            if not hasattr(self,item[0]):
                setattr(self,item[0],item[1])
        # create the feature which contains all the character stat info
        self.feature = Feature(self.statXml,self,**kwargs)
        # now that we have our feature tree, lets assign some icons
        if hasattr(self,'portfolio') and hasattr(self.portfolio,'icons'):
            if hasattr(self.feature,'types'):
                if hasattr(self.feature.types,'typeList'):
                    matchType = self.feature.types.typeList[0].name
                    matchIcon = self.portfolio.icons.getIcon(matchType,'type')
                    if matchIcon:
                        setattr(self.feature.types.typeList[0],'typeIcon',matchIcon)
            if hasattr(self.feature,'npc'):
                if hasattr(self.feature.npc,'ecology'):
                    if hasattr(self.feature.npc.ecology,'environment'):
                        matchText = self.feature.npc.ecology.environment.fText
                        for matchType in ['terrain','climate']:
                            matchIcons = self.portfolio.icons.getMatches(matchText,matchType)
                            if matchIcons:
                                setattr(self.feature.npc.ecology.environment,"%sIcon" % matchType,matchIcons[0])
                                setattr(self.feature.npc.ecology.environment,"%sIconList" % matchType,matchIcons)
                            else:
                                setattr(self.feature.npc.ecology.environment,"%sIcon" % matchType,self.portfolio.icons.getIcon('any',matchType))
                                setattr(self.feature.npc.ecology.environment,"%sIconList" % matchType,[self.portfolio.icons.getIcon('any',matchType)])



class Portfolio(object):
    """Class contains entire HeroLab portfolio

    Methods:
       close: clean up temporary files and directory

    Attributes:
       verbosity: (int) level of verbose debug message
       porFile: (ZipFile) portfolio file opened for reading
       filename: (str) pathless filename of the protfolio file
       filepath: (str) absolute path of the portfolio file directory location
       filecore: (str) pathless,extentionless name of the portfolio file
       game: (str) game for which this portfolio file was created
       gameVersion: (str) vertion of the HeroLab data file for the game
       tempDir: (str) absolute path of temporary directory for image extraction
       characters: (list) list of Character instances from the portfolio
       icons: (Icons) icons instance with a getIcon method
    """
    def __init__(self, porFile,*args,**kwargs):
        """Create a Portfolio instance from a filename or ZipFile instance

        Args:
           porFile: (str or ZipFile) HeroLab protfolio file

        Kwargs:
           verbosity: (int) set the level of debug messages
           icons: (Icons) instance used to get icon images and filenames
        """
        if 'verbosity' not in kwargs: kwargs['verbosity'] = VERBOSITY
        self.verbosity = kwargs['verbosity']
        if type(porFile) is not zipfile.ZipFile:
            porFile = zipfile.ZipFile(porFile,'r')
        if self.verbosity >= 2: print("filename: %s" % porFile.filename)
        self.porFile = porFile
        self.filename = porFile.filename
        self.keepTemp = False
        self.filepath = os.path.split(porFile.filename)[0]
        self.filecore = os.path.splitext(os.path.basename(porFile.filename))[0]
        if self.verbosity >= 2: print("filecore: %s" % self.filecore)
        if 'icons' in kwargs and type(kwargs['icons']) == Icons:
            self.icons = kwargs['icons']
        indexXml = porFile.open('index.xml')
        indexTree = et.parse(indexXml)
        indexXml.close()
        if self.verbosity >= 5:
            print("Dump of Index XML:")
            et.dump(indexTree)
        # identifiy the game and version
        self.game = indexTree.find('./game[@name]').get('name')
        self.gameVersion = float(indexTree.find('./game/version').get('version'))
        if self.verbosity >= 5: print("game: %s version: %g" % (self.game,self.gameVersion))
        if self.game != "Pathfinder Roleplaying Game" or self.gameVersion < 14.1:
            print("WARNING: HL-GoogleSlides has only been tested to work with HeroLab's Pathfinder ruleset version 14.1")
        # create a temporary directory for Character images
        self.tempDir = tempfile.mkdtemp(prefix='HL-GoogleSlides-Portfolio-')
        if self.verbosity >= 2: print("Temp Image Directory: %s" % self.tempDir)
        # build up the character list creating Character instances for each
        self.characters = []
        for cElem in indexTree.findall('./characters/character'):
            character = Character(self.porFile,cElem,*args,tempDir=self.tempDir,portfolio=self,**kwargs)
            self.characters.append(character)
            for mElem in cElem.findall('./minions/character'):
                self.characters.append(Character(self.porFile,mElem,*args,parent=character,portfolio=self,tempDir=self.tempDir,**kwargs))

        # debug printing
        for c in self.characters:
            if self.verbosity >= 3:
                print("character #%d.%d: %s -> %s" % (c.myIndex,c.characterIndex,c.name,c.summary))
            if self.verbosity >= 6: print("  STAT BLOCK TEXT:\n%s" % c.statText)
            if self.verbosity >= 6: print("  STAT BLOCK HTML:\n%s" % c.statHtml)
            if self.verbosity >= 4: print("  XML name: %s" % c.statXml.get('name'))
            if self.verbosity >= 6:
                print("STAT BLOCK XML:")
                et.dump(c.statXml)
            if self.verbosity >= 4:
                if hasattr(c.images,'imageList'):
                    print("  Images:")
                    for i in c.images.imageList:
                        print("     %s" % i.filename)

        # close the protfolio
        self.porFile.close()

    def close(self):
        """
        clean up temporary files and directories
        """
        if not self.keepTemp:
            shutil.rmtree(self.tempDir)

