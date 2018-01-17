# -*- coding: utf-8 -*-
"""
Created on Mon Jan 01 10:08:15 2018
BaseClasses is meant to hold all the long lists of abbriviations and
substitutions so that the main code looks cleaner

@author: steve
"""
from __future__ import print_function
import string,re

class IconsBase:
    """
    base definitions for icons class
    """
    def getIcon(self,iconName,iconType="creature type",iconResolution="low",*args,**kwargs):
        """
        supply the name, type, and resolution to retieve the tuple of icon
        filename and fullpath
        """
        for i in self.icons:
            if i.type == iconType.lower() and i.name == iconName.lower():
                if re.search(r'(?i)high',iconResolution):
                    return i.imageHigh
                else:
                    return i.imageLow

class CharacterBase:
    """
    This is a base definition for an individual Character
    mainly to hold the long attribute definitions
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
     'gender':[
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
    htmlTypeSearch = r'(?m)<br/>\s*%s %s ([A-Za-z ]+)\b\s+(\(.*\))?<br/>' # % (align,size)
    htmlSubtypeSearch = r'(?m)<br/>\s*%s %s [8A-Za-z ]+\b\s+\((.*)\)<br/>' # % (align,size)
    htmlMovementSearch = r'<b>Speed\s*</b>(.*)\s*<br/>'

    def abbreviate(self,abbrSet='all',*args,**kwargs):
        """
          use self.abbreviations to shorten the input strings or string
        """
        if abbrSet not in self.abbreviations: abbrSet = 'none'
        outList = []
        for inString in args:
            for a in self.abbreviations[abbrSet]:
                inString = re.sub(a[0],a[1],inString)
            outList.append(inString)
        return outList

    def getElement(self,xmlPath,*args,**kwargs):
        """
         Returns either a list of tuples, or a list of strings.
        The first argument is the xmlPath for the element or elements.  A
        list of elements is always returned.
         The remeinder of the non-keyword arguments are attrubute names which
        are being requiested.  If only a single attribue is requested
        the list of elements is a list of attribute strings.  If multiple
        attributes are being requested, an element list of attribute tuples is
        returned.
        """
        elementList = self.statXml.findall("./%s" % xmlPath)
        # loop
        for i in range(len(elementList)):
            attributeList = []
            attributeDict = {}
            attributeNames = list(args[:])
            # use the argument 'allattributes' to retieve all the attributes
            #  unfortunately they are in arbitrary order
            if (len(attributeNames) == 1 and attributeNames[0] == "allattributes"):
                attributeNames = [item[0] for item in elementList[i].items()]
                if 'attrNamesOnly' in kwargs and kwargs['attrNamesOnly']:
                    return attributeNames
            # use the argument 'TAG' to include the element tag as the first
            #  return "attribute"
            if 'TAG' in attributeNames:
                attributeNames[attributeNames.index('TAG'):attributeNames.index('TAG')+1]=[]
                attributeList.append(elementList[i].tag)
                attributeDict['TAG'] = elementList[i].tag
            # loop trhrough all attributes to get their value and possibly modify
            #  them.  If the attribute argument was given with a default as
            #  'attrname=default' then use the default if there is no value.
            #  Also to create an attribute dictionary.
            for myArg in attributeNames:
                (attribute,default) = re.match(r'([^=]+)=?(.*)',myArg).groups()
                myValue = elementList[i].get(attribute,default)
                if 'modWith' in kwargs:
                    myValue = kwargs['modWith'](myValue)
                attributeList.append(myValue)
                attributeDict[myArg] = myValue
            # if the element has a description tag child, and the kwarg
            # getDesc is true add its text as an attribute.
            if 'getDesc' in kwargs and kwargs['getDesc']:
                description = elementList[i].find('description')
                descriptionText = None
                if type(description) is type(elementList[i]):
                    descriptionText = "".join(description.itertext())
                attributeList.append(descriptionText)
                if 'description' not in attributeDict:
                    attributeDict['description'] = descriptionText
            # if there are any attributes, apply requested
            # abbreviations.  if there are more than one make it
            # a tuple otherwise keep it  a single value
            if len(attributeList) > 0:
                if 'longForm' not in kwargs or not kwargs['longForm']:
                    abbrSet = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'all'
                    attributeList = self.abbreviate(abbrSet,*attributeList)
                if 'attrDict' in kwargs and kwargs['attrDict']:
                    elementList[i] = attributeDict.copy()
                elif len(attributeList) > 1:
                    elementList[i] = tuple(attributeList)
                else:
                    elementList[i] = attributeList[0]
            # if there are no  attributes requested, return the contained text
            else:
                elementList[i] = "".join(elementList[i].itertext())
        if self.verbosity >= 5:
            print("    elementList from %s attributes %s: %s" % (xmlPath,attributeNames,elementList))
        # return the full list with asList keyword
        if 'asList' in kwargs and kwargs['asList']:
            return elementList
        # otherwise return a string of everything joined together
        if 'joinWith' not in kwargs or not isinstance(kwargs['joinWith'],str):
            kwargs['joinWith'] = " "
        for i in range(len(elementList)):
            if isinstance(elementList[i],tuple): elementList[i] = kwargs['joinWith'].join(elementList[i])
        return kwargs['joinWith'].join(elementList)

    def _getSpecialElements(self,element,*args,**kwargs):
        myList = self.getElement("%s/special" % element,'name','shortname','type=notype','sourcetext=innate',asList=True,longForm=True)
        if 'asList' in kwargs and kwargs['asList']: return myList
        if 'longForm' in kwargs and kwargs['longForm']:
            myList = map(lambda s:s[0],myList)
        else:
            abbrSet = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'all'
            myList = map(lambda s:s[1],myList)
            myList = self.abbreviate(abbrSet,*myList)
        if 'modWith' not in kwargs:
            return string.join(myList,", ")
        else:
            return re.sub(r'dc( ?\d+)(?!\d)',r'DC\1',kwargs['modWith'](string.join(myList,", ")))

    def _getFeatTraitFlawTrick(self,elemType,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or elemType.lower()+'s'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['getDesc']=True
        kwargs['asList']=True
        elemList = self.getElement("%ss/%s" % (elemType,elemType),
           'TAG','name','categorytext','profgroup=no','useradded=yes',**kwargs)
        if 'noProf' in kwargs and kwargs['noProf']:
            newElemList = filter(lambda e:e[3]!='yes',elemList)
            elemList = newElemList
        if asList: return elemList
        if 'longForm' in kwargs and kwargs['longForm']:
            return elemType.upper() + "S::\n" + "\n\n\n".join(["%s (%s):\n%s" % (item[1],item[2],item[5]) for item in elemList])
        else:
            return ", ".join([item[1] for item in elemList])

    def getAlignment(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'alignment'
        align = self.getElement("alignment",'name',**kwargs)
        if 'longForm' in kwargs and kwargs['longForm']: return self.alignment[align]
        return align

    def getAnimalTricks(self,*args,**kwargs):
        return self._getFeatTraitFlawTrick('animaltrick',*args,**kwargs)

    def getAC(self,*args,**kwargs):
        return self.getArmorClass(*args,**kwargs)

    def getArmorClass(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'armorclass'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        acAttrList = ["ac","touch","flatfooted","fromarmor","fromshield","fromdexterity","fromwisdom","fromcharisma","fromsize","fromnatural","fromdeflect","fromdodge","frommisc"]
        if self.verbosity >= 6: print("      attribute list for armorclass %s" % acAttrList)
        acList = self.getElement("armorclass",*acAttrList,**kwargs)
        sitList = self.getElement("armorclass/situationalmodifiers/situationalmodifier",'text','source',**kwargs)
        if asList: return acList + sitList
        if 'longForm'in kwargs and kwargs['longForm']:
            rtnText = "AC:%s, touch:%s, flat-footed:%s (" % acList[0][0:3]
            for idx,attr in enumerate(acAttrList):
                fromMatch = re.search(r'^from(.*)$',attr)
                if fromMatch:
                    rtnText += acList[0][idx] and "%s:%s, " % (fromMatch.groups()[0].lower(),acList[0][idx])
            rtnText = re.sub(r'^(.*),\s*$',r'\1)',rtnText)
        else:
            rtnText = "AC:%s, tch:%s, flat:%s" % acList[0][0:3]
        return rtnText

    def getSpecialAttack(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'attack'
        attack = self.getElement('attack','attackbonus','meleeattack','rangedattack','baseattack',**kwargs)
        special = self._getSpecialElements('attack',**kwargs)
        if 'asList' in kwargs and kwargs['asList']:
            return attack + special

    def getAttribute(self,attribute,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'none'
        return self.getElement("attributes/attribute[@name='%s']/*" % attribute.capitalize(),
                               'text','base=x','modified=x',*args,**kwargs)

    def getAttributes(self,*args,**kwargs):
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        attrList = []
        for a in ['strength','dexterity','constitution','intelligence','wisdom','charisma']:
            thisAttr = self.getAttribute(a,*args,**kwargs)
            attrList.append((a,thisAttr[0][0],thisAttr[1][0],thisAttr[2][0]))
        if asList: return attrList
        rtnList = []
        joinWith = " "
        for a in attrList:
            if 'longForm' in kwargs and kwargs['longForm']:
                rtnList.append("%s: %s(%s)" % (a[0].capitalize(),a[1],a[2]))
                joinWith = "\n"
            else:
                rtnList.append("%s %s(%s)" % (a[0][0:3].capitalize(),a[1],a[2]))
        return joinWith.join(rtnList)

    def getAuras(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'auras'
        return self._getSpecialElements('auras',*args,**kwargs)

    def getBookInfo(self,*args,**kwargs):
        pass

    def getChallengeRating(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'none'
        return self.getElement("challengerating","value","text",**kwargs)

    def getCR(self,*args,**kwargs):
        return self.getChallengeRating(*args,**kwargs)

    def getClasses(self,*args,**kwargs):
        """
        return a class list string for the character
        """
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'classes'
        (characterLevel,classesSummary,classesSummaryAbbr) = self.getElement("classes",'level','summary','summaryabbr',longForm=True,asList=True)[0]
        if 'longForm' in kwargs and kwargs['longForm']:
            if 'asList' in kwargs and kwargs['asList']:
                return self.getElement("classes/class",'name','level','spells','casterlevel','concentrationcheck','overcomespellresistance','basespelldc','castersource',longForm=True,asList=True)
            else:
                return classesSummary
        else:
            if 'asList' in kwargs and kwargs['asList']:
                return [(characterLevel,classesSummaryAbbr)]
            else:
                return classesSummaryAbbr

    def getDR(self,*args,**kwargs):
        return self.getDamageReduction(*args,**kwargs)

    def getDamageReduction(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'damagereduction'
        return self._getSpecialElements('damagereduction',*args,**kwargs)

    def getDefenses(self,*args,**kwargs):
        pass

    def getSpecialDefensive(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'defensive'
        return self._getSpecialElements('defensive',*args,**kwargs)

    def getDeity(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'deity'
        return self.getElement("deity","name",**kwargs)

    def getEncumbrance(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'encumbrance'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        longForm = 'longForm' in kwargs and kwargs['longForm'] or False
        kwargs['asList']=True
        myEncum = self.getElement("encumbrance",'TAG','carried','encumstr','light','medium','heavy','level',**kwargs)[0]
        if asList: return [myEncum]
        else:
            if longForm: return "%s: %s/%s/%s (%slbs. carried) %s" % (myEncum[0].capitalize(),myEncum[3],myEncum[4],myEncum[5],myEncum[1],myEncum[6])
            else: return "%s:%s/%s/%s (%s)%s" % (myEncum[0],myEncum[3],myEncum[4],myEncum[5],myEncum[1],myEncum[6])

    def getFactions(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'factions'
        return self.getElement("factions/faction","name","tpa","cpa",asList=True,**kwargs)

    def getFaction(self,*args,**kwargs):
        """
        returns the first faction of whichever number specified in the first argument
        """
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'factions'
        index = len(args) > 0 and int(args[0])-1 or 0
        factions = self.getElement("factions/faction","name","tpa","cpa",asList=True,**kwargs)
        if len(factions) > index: return factions[index]
        else: return ()

    def getFavoredClass(self,*args,**kwargs):
        classes = self.getFavoredClasses(self,*args,**kwargs)
        if type(classes) is list:
            return classes[0]
        else:
            return classes

    def getFavoredClasses(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'classes'
        favoredClasses = self.getElement('favoredclasses/favoredclass','name',longForm=True,asList=True)
        classes = self.getClasses(asList=True)
        if len(favoredClasses) < 1:
            if len(classes) == 1:
                favoredClass = re.sub(r'^([^(]+)\s*(\(.*\))?$',r'\1',classes[0][0])
            elif len(classes) == 0:
                favoredClass = 'No Class'
            else:
                favoredClass = 'Unknown'
        else:
            if 'asList' in kwargs and kwargs['asList']: return favoredClasses
            favoredClass = string.join(favoredClasses,', ')
        if 'modWith' in kwargs: favoredClass = kwargs['modWith'](favoredClass)
        if 'asList' in kwargs and kwargs['asList']: return [favoredClass]
        return favoredClass

    def getFeats(self,*args,**kwargs):
        return self._getFeatTraitFlawTrick('feat',*args,**kwargs)

    def getDrawbacks(self,*args,**kwargs):
        """
        drawbacks are listed under otherspecials/special not traits but with sourcetext=Trait
        """
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'drawbacks'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        longForm = 'longForm' in kwargs and kwargs['longForm'] or False
        kwargs['longForm']=True
        kwargs['getDesc']=True
        kwargs['asList']=True
        specialList = self.getElement("otherspecials/special[@sourcetext='Trait']",
                            'name','shortname','sourcetext',**kwargs)
        for idx,special in enumerate(specialList):
            specialList[idx] = tuple(['drawback',special[0],'Drawback','no','yes',special[-1]])
        if asList: return specialList
        if longForm:
            return "DRAWBACKS::\n" + "\n\n\n".join(["%s:\n%s" % (item[1],item[5]) for item in specialList])
        else:
            return ", ".join([item[1] for item in specialList])

    def getFlaws(self,*args,**kwargs):
        return self._getFeatTraitFlawTrick('flaw',*args,**kwargs)

    def getGear(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'gear'
        pass

    def getHealth(self,*args,**kwargs):
        return self.getElement('health',"hitdice","hitpoints","damage","nonlethal","currenthp",*args,**kwargs)

    def getHD(self,*args,**kwargs):
        return self.getElement('health','hitdice',*args,**kwargs)

    def getTotalHP(self,*args,**kwargs):
        return self.getElement('health','hitpoints',*args,**kwargs)

    def getCurrentHP(self,*args,**kwargs):
        return self.getElement('health','currenthp',*args,**kwargs)

    def getHeroPoints(self,*args,**kwargs):
        return self.getElement("heropoints","enabled","total",asList=True,**kwargs)

    def getImages(self,*args,**kwargs):
        pass

    def getImmunities(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'immunities'
        return self._getSpecialElements('immunities',*args,**kwargs)

    def getInitiative(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'initiative'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        initiativeList = self.getElement('initiative','total','attrtext','misctext','attrname',**kwargs)
        sitList = self.getElement("initiative/situationalmodifiers/situationalmodifier",'text','source',**kwargs)
        if asList:
            return [initiativeList,sitList]
        else:
            return initiativeList[0][0]

    def getJournals(self,*args,**kwargs):
        pass

    def getLanguages(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'languages'
        if 'asList' in kwargs and kwargs['asList']:
            return self.getElement("languages/language","name","useradded=yes",**kwargs)
        return self.getElement("languages/language","name",**kwargs)

    def getMagicItems(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'magicitems'
        pass

    def getManeuvers(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'maneuvers'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        maneuverList = self.getElement('maneuvers','name=All','bonus=0','cmb','cmd','cmdflatfooted',**kwargs)
        sitList = self.getElement("maneuvers/situationalmodifiers/situationalmodifier",'text','source',**kwargs)
        maneuverList = maneuverList + self.getElement('maneuvers/maneuvertype','name','bonus','cmb','cmd',**kwargs)
        sitList = sitList + self.getElement("maneuvers/maneuvertype/situationalmodifiers/situationalmodifier",'text','source',**kwargs)
        if asList:
            return [maneuverList,sitList]
        else:
            rtnList = []
            for m in maneuverList:
                if m[0] == "all" or m[0] == "All":
                    rtnList.append("CMB:%s CMD:%s: CMDflat:%s" % m[2:5])
                elif m[2] != maneuverList[0][2] or m[3] != maneuverList[0][3]:
                    manStr = '%s ' % m[0]
                    if m[2] != maneuverList[0][2]:
                        manStr += "cmb:%s" % m[2]
                    else:
                        manStr += "cmd:%s" % m[3]
                    rtnList.append(manStr)
            return ", ".join(rtnList)

    def getCMB(self,*args,**kwargs):
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        maneuverList = self.getManeuvers(**kwargs)[0]
        rtnList = []
        for m in maneuverList:
            if m[0] == "all" or m[0] == "All":
                rtnList.append("CMB:%s" % m[2])
            elif m[2] != maneuverList[0][2]:
                rtnList.append("%s cmb:%s" % (m[0],m[2]))
        return ", ".join(rtnList)

    def getCMD(self,*args,**kwargs):
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        maneuverList = self.getManeuvers(**kwargs)[0]
        rtnList = []
        for m in maneuverList:
            if m[0] == "all" or m[0] == "All":
                rtnList.append("CMD:%s CMDflat:%s" % m[3:5])
            elif m[3] != maneuverList[0][3]:
                rtnList.append("%s cmd:%s" % (m[0],m[3]))
        return ", ".join(rtnList)

    def getMelee(self,*args,**kwargs):
        pass

    def getMinions(self,*args,**kwargs):
        pass

    def getMoney(self,*args,**kwargs):
        return self.getElement('money','total','pp','gp','sp','cp',*args,**kwargs)

    def getTotalMoney(self,*args,**kwargs):
        return self.getElement('money','total',*args,**kwargs)

    def getPP(self,*args,**kwargs):
        return self.getElement('money','pp',*args,**kwargs)

    def getGP(self,*args,**kwargs):
        return self.getElement('money','gp',*args,**kwargs)

    def getSP(self,*args,**kwargs):
        return self.getElement('money','sp',*args,**kwargs)

    def getCP(self,*args,**kwargs):
        return self.getElement('money','cp',*args,**kwargs)

    def getMovement(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'movement'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        longForm = 'longForm' in kwargs and kwargs['longForm'] or False
        modWith = 'modWith' in kwargs and kwargs['modWith'] or False
        kwargs['longForm']=True
        kwargs['asList']=True
        kwargs['modWith']=string.lower
        myMovement = self.getElement("movement/*","TAG","text","value",**kwargs)
        # fly, swim, climb,etc speeds are all missing fromthe XML
        myHtmlMovementSearch = re.search(self.htmlMovementSearch,self.statHtml)
        myHtmlMovement = []
        if myHtmlMovementSearch:
            myHtmlMovement = map(lambda t:string.strip(string.lower(t)," "),myHtmlMovementSearch.groups()[0].split(","))
            for move in myHtmlMovement:
                move = re.sub(r'\s?ft.',"'",move)
                if not re.match(r"^\d+\s*'\s*",move):
                    move = move.split()
                    move[2:2] = [re.sub(r'^(\d+)[^\d]*$',r'\1',move[1])]
                    if move [0] not in [item[0] for item in myMovement]: myMovement.append(tuple(move))
        if modWith or not longForm:
            myModMovement = []
            for move in myMovement:
                move = list(move)
                move[0] = modWith(move[0])
                if not longForm: move = self.abbreviate('movement',*move)
                myModMovement.append(tuple(move))
            myMovement = myModMovement[:]
        if asList:
            return [myMovement]
        rtnList= []
        for move in myMovement:
            myRtn = "%s:%s" % (move[1],move[0])
            if len(move)>3: myRtn += " ".join(move[3:])
            rtnList.append(myRtn)
        return ", ".join(rtnList)

    def getNPC(self,*args,**kwargs):
        pass

    def getOtherSpecials(self,*args,**kwargs):
        pass

    def getPenalties(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'penalties'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        penaltyList = self.getElement('penalties/penalty','name','text','value',*args,**kwargs)
        if asList:
            return penaltyList
        else:
            rtnList = []
            for p in penaltyList:
                if p[0] == "ACP" or p[0] == "Armor Check Penalty":
                    if float(p[2]) > 0: continue
                elif p[0] == "Max Dex Bonus" or p[0] == "MaxDEX":
                    if float(p[2]) > 999: continue
                rtnList.append("%s:%s" % p[0:2])
            return ", ".join(rtnList)

    def getACP(self,*args,**kwargs):
        return "ACP:%s" % self.getPenalties(asList=True)[0][1]

    def getPersonal(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'personal'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        (gender,age,hair,eyes,skin) = \
          self.getElement("personal",'gender','age','hair','eyes','skin',**kwargs)[0]
        (heightText,heightValue) = \
          self.getElement("personal/charheight",'text','value',**kwargs)[0]
        (weightText,weightValue) = \
          self.getElement("personal/charweight",'text','value',**kwargs)[0]
        kwargs['abbrSet'] = 'personalbackground'
        (description) = \
          self.getElement("personal/description",**kwargs)[0]
        if asList:
            return [(gender,age,hair,eyes,skin,heightText,heightValue,weightText,weightValue,description)]
        else:
            rtnList = []
            if age != "0":
                rtnList.append("%s year old," % age)
            if weightValue != "0": rtnList.append(weightText)
            if heightValue != "0": rtnList.append(heightText)
            rtnList.append(gender)
            kwargs['asList']=False
            rtnList.append(self.getRace(**kwargs))
            if hair or eyes or skin:
                rtnList.append("w/")
                if hair: rtnList.append("%s hair," % hair)
                if eyes: rtnList.append("%s eyes," % eyes)
                if skin: rtnList.append("%s skin" % skin)
            return " ".join(rtnList)

    def getGender(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'gender'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        if asList: return [self.getPersonal(**kwargs)[0][0]]
        else: return self.getPersonal(**kwargs)[0][0]

    def getAge(self,*args,**kwargs):
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        if asList: return [self.getPersonal(**kwargs)[0][1]]
        else: return self.getPersonal(**kwargs)[0][1]

    def getPersonalBackground(self,*args,**kwargs):
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        if asList: return [self.getPersonal(**kwargs)[0][-1]]
        else: return self.getPersonal(**kwargs)[0][-1]

    def getRace(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'race'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        (race,ethnicity) = self.getElement("race",'racetext','ethnicity',**kwargs)[0]
        if asList: return [(race,ethnicity)]
        if 'withEthnicity' in kwargs and kwargs['withEthnicity']:
            if ethnicity: return "%s (%s)" % (race,ethnicity)
        return race

    def getRanged(self,*args,**kwargs):
        pass

    def getResistances(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'resistances'
        return self._getSpecialElements('resistances',*args,**kwargs)

    def getSave(self,save,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'saves'
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        if save != 'all':
            saveList = self.getElement("saves/save[@abbr='%s']" % save.capitalize(),
             'name','abbr','save','base','fromattr','fromresist','frommisc',
             *args,**kwargs)
            sitList = self.getElement("saves/save[@abbr='%s']/situationalmodifiers/situationalmodifier" % save.capitalize(),
             'text','source',*args,**kwargs)
        else:
            saveList = self.getElement("saves/allsaves",
             'name=All Saves','abbr=All','save','base','fromattr=0',
             'fromresist','frommisc',*args,**kwargs)
            sitList = self.getElement("saves/allsaves/situationalmodifiers/situationalmodifier",
             'text','source',*args,**kwargs)
        if asList: return saveList + sitList
        else:
            if save != 'all':
                return "%s %s" % (saveList[0][1],saveList[0][2])
            else:
                return "; ".join(map(lambda s:"%s: %s" % (s[1],s[0]),sitList))

    def getSaves(self,*args,**kwargs):
        asList = 'asList' in kwargs and kwargs['asList'] or False
        kwargs['asList']=True
        saveList = []
        rtnList = []
        rtnListLong = []
        for s in ['fort','ref','will','all']:
            save = self.getSave(s,*args,**kwargs)
            saveList.append(save)
            if s != 'all':
                rtnList.append("%s %s" % (save[0][1].capitalize(),save[0][2]))
                rtnListLong.append("%s %.0s%s (%s base %s attr %s resist %s misc)" % save[0])
        if asList: return saveList
        sitSlice = saveList[3][1:]
        if 'longForm' in kwargs and kwargs['longForm']:
            return "\n".join(rtnListLong) + "\n" + "; ".join(map(lambda s:"%s: %s" % (s[1],s[0]),sitSlice))
        return ", ".join(rtnList) + " : " + "; ".join(map(lambda s:s[0],sitSlice))

    def getSenses(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'senses'
        return self._getSpecialElements('senses',*args,**kwargs)

    def getSettings(self,*args,**kwargs):
        pass

    def getSize(self,*args,**kwargs):
        return self.getElement("size","name",**kwargs)

    def getSizeSpace(self,*args,**kwargs):
        return self.getElement("size/space","text",**kwargs)

    def getSizeReach(self,*args,**kwargs):
        return self.getElement("size/reach","text",**kwargs)

    def getSkillAbilities(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'skillabilities'
        return self._getSpecialElements('skillabilities',*args,**kwargs)

    def getSkill(self,*args,**kwargs):
        """
        return a skill list string for the character
        """
        skillList = self.getElement("skills/skill",'name','ranks','value',longForm=True,asList=True)
        # if a single skill is asked for only get that one
        if len(args) > 0 and args[0]:
            skillList = filter(lambda s:s[0] == args[0],skillList)
            if self.verbosity >= 4: print("    skill list only %s: %s" % (args[0],skillList))
        # only list if the character has a rank in the skill
        if 'withRank' in kwargs and kwargs['withRank']:
            skillList = filter(lambda s:int(s[1]) > 0,skillList)
            if self.verbosity >= 4: print("    skill list with ranks: %s" % skillList)
        # only list if the character has at least a certain bonus
        if 'atLeast' in kwargs and kwargs['atLeast']:
            skillList = filter(lambda s:int(s[2]) >= int(kwargs['atLeast']),skillList)
            if self.verbosity >= 4: print("    skill list with value > %s: %s" % (kwargs['atLeast'],skillList))
        if 'valueOnly' in kwargs and kwargs['valueOnly']:
            skillList = map(lambda s:s[2],skillList)
            if self.verbosity >= 4: print("    skill list value only: %s" % skillList)
        else:
            skillList = map(lambda s:"%s %s" % (s[0],s[2]),skillList)
            if self.verbosity >= 4: print("    skill list before re.sub: %s" % skillList)
            skillList = self.abbreviate('skills',*skillList)
            if self.verbosity >= 4: print("    skill list after re.sub: %s" % skillList)
        joinWith = 'joinWith' in kwargs and kwargs['joinWith'] or ', '
        return joinWith.join(skillList)

    def getSkills(self,*args,**kwargs):
        """
        get a list of skills
        """
        # do not pass the arg list because that is used to select an individual skill
        return self.getSkill(**kwargs)

    def getSkillTricks(self,*args,**kwargs):
        return self._getFeatTraitFlawTrick('skilltrick',*args,**kwargs)

    def getSpellbook(self,*args,**kwargs):
        pass

    def getSpellClasses(self,*args,**kwargs):
        pass

    def getSpellLike(self,*args,**kwargs):
        pass

    def getSpellsKnown(self,*args,**kwargs):
        pass

    def getSpellsMemorized(self,*args,**kwargs):
        pass

    def getSubtypes(self,*args,**kwargs):
        mySubtypes = self.getElement("subtypes/subtype","name",asList=True,modWith=string.lower)
        # If some cases I have seen a subtype gets assigned instead as the main type
        # so I lets also check the HTML statblock for subtypes.
        align = self.getAlignment(longForm=False)
        size = self.getSize(longForm=True)
        myHtmlSubtypeSearch = re.search(self.htmlSubtypeSearch % (align,size),self.statHtml)
        if myHtmlSubtypeSearch:
            myHtmlSubtypes = map(lambda t:string.strip(string.lower(t)," "),myHtmlSubtypeSearch.groups()[0].split(","))
            for subtype in myHtmlSubtypes:
                if subtype not in mySubtypes: mySubtypes.append(subtype)
        if 'longForm' not in kwargs or not kwargs['longForm']:
            mySubtypes = self.abbreviate('subtypes',*mySubtypes)
        return ", ".join(mySubtypes)

    def getTemplates(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'templates'
        return self.getElement("templates","summary",**kwargs)

    def getTrackedResources(self,*args,**kwargs):
        pass

    def getTraits(self,*args,**kwargs):
        return self._getFeatTraitFlawTrick('trait',*args,**kwargs)

    def getTypes(self,*args,**kwargs):
        myType = self.getType(**kwargs)
        mySubtypes = self.getSubtypes(**kwargs)
        if mySubtypes:
            return "%s (%s)" % (myType,mySubtypes)
        else:
            return myType

    def getType(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'types'
        (myType,typeActive) = self.getElement("types/type","name","active=no",asList=True,**kwargs)[0]
        if re.match(r'(?i)yes|true',typeActive):
            return myType
        # If some cases I have seen the actual main type not in the XML
        # in these cases the active="yes" flag is not set, so when this happens
        # lets get the actual type from the HTML statblock
        else:
            align = self.getAlignment(longForm=False)
            size = self.getSize(longForm=True)
            myTypes = re.search(self.htmlTypeSearch % (align,size),self.statHtml)
            if myTypes:
                return string.capwords(myTypes.groups()[0])
            else:
                return ''

    def getValidation(self,*args,**kwargs):
        pass

    def getWeaknesses(self,*args,**kwargs):
        kwargs['abbrSet'] = 'abbrSet' in kwargs and kwargs['abbrSet'] or 'weaknesses'
        return self._getSpecialElements('weaknesses',*args,**kwargs)

    def getXP(self,*args,**kwargs):
        return self.getElement("xp","total",**kwargs)

    def getXPAward(self,*args,**kwargs):
        return self.getElement("xpaward","value","text",**kwargs)
"""
"""