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
        in something.

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
    'role': 'role', # pc, npc, etc
    'align': 'feature.alignment.name', # alignment written out
    'name': 'name', # character name
    'summary': 'summary', # usually the creature's race, class, alignment abbrev, size, and creature type
    'character type': 'type', # Hero, Arcane Familiar, Animal Commpanion, etc
    'player': 'playername',
    'racetext': 'feature.race.racetext', # race and ethnicity (if one)
    'race': 'feature.race.name', # race only text
    'ethnicity': 'feature.race.ethnicity', # ethnicity
    'size': 'feature.size.name', # size of creature (Small, Medium, etc)
    'space': 'feature.size.space.text', # space a creature  takes up with units
    'reach': 'feature.size.reach.text', # space a creature threatens beyond its own square
    'deity': 'feature.deity.name', # deity worshiped
    'CR': 'feature.challengerating.text', # challenge rating with CR prepended
    'XP': 'feature.xpaward.text', # XP awarded for creature (comma for thousands and XP appended)
    'classes summary': 'feature.classes.summary', # summary list of all classes
    'type': 'feature.types.typeList[0].name', # get name of creature type
    'subtype': 'feature.subtypes.subtypeList[0].name)', # get name of creatrue subtype
    }

    """
    'hero': "(character.find('heropoints').get('enabled') == 'yes') and character.find('heropoints').get('total') or '-'",
    'senses': "get_attrlist(character,'senses','special','shortname',fmt=JOINVOWELLESS)",
    'auras': "get_attrlist(character,'auras','special','name')",
    'auras head': "get_attrlisthead(character,'auras','special','\\nAuras: ')",
    'favoredclasses': "get_attrlist(character,'favoredclasses','favoredclass','name',fmt=JOINVOWELLESS)",
    'HP': "character.find('health').get('hitpoints')",
    'HD': "character.find('health').get('hitdice')",
    'xp': "character.find('xp').get('total')",
    'money': "character.find('money').get('total')+'gp'",
    'gender': "character.find('personal').get('gender').lower()",
    'age': "character.find('personal').get('age')",
    'hair': "character.find('personal').get('hair')",
    'eyes': "character.find('personal').get('eyes')",
    'skin': "character.find('personal').get('skin')",
    'height': "re.sub(r' ','',character.find('personal').find('charheight').get('text'))",
    'weight': "character.find('personal').find('charweight').get('text')",
    'personal': "character.find('personal').find('description').text",
    'personal description':'''re.sub(r'w/  skin  hair and  eyes.  ','',
      re.sub(r'^0[^1-9][^1-9]* yr old ','',
        get_nested(character,'{{height}} {{(weight)}} {{age}} yr old w/ {{skin}} skin {{hair}} hair and {{eyes}} eyes.  {{personal}}')
      ))''',
    'languages': "get_attrlist(character,'languages','language','name')",
    'strength': "get_ability(character,'Strength')",
    'dexterity': "get_ability(character,'Dexterity')",
    'constitution': "get_ability(character,'Constitution')",
    'intelligence': "get_ability(character,'Intelligence')",
    'wisdom': "get_ability(character,'Wisdom')",
    'charisma': "get_ability(character,'Charisma')",
    'str': "get_ability_value(character,'Strength')",
    'dex': "get_ability_value(character,'Dexterity')",
    'con': "get_ability_value(character,'Constitution')",
    'int': "get_ability_value(character,'Intelligence')",
    'wis': "get_ability_value(character,'Wisdom')",
    'cha': "get_ability_value(character,'Charisma')",
    'STR': "get_ability_mod(character,'Strength')",
    'DEX': "get_ability_mod(character,'Dexterity')",
    'CON': "get_ability_mod(character,'Constitution')",
    'INT': "get_ability_mod(character,'Intelligence')",
    'WIS': "get_ability_mod(character,'Wisdom')",
    'CHA': "get_ability_mod(character,'Charisma')",
    'STRs': "get_ability_sit(character,'Strength')",
    'DEXs': "get_ability_sit(character,'Dexterity')",
    'CONs': "get_ability_sit(character,'Constitution')",
    'INTs': "get_ability_sit(character,'Intelligence')",
    'WISs': "get_ability_sit(character,'Wisdom')",
    'CHAs': "get_ability_sit(character,'Charisma')",
    'Fortitude Save': "get_save(character,'Fortitude Save')",
    'Fort': "get_save_mod(character,'Fortitude Save')",
    'Forts': "get_save_sit(character,'Fortitude Save')",
    'Reflex Save': "get_save(character,'Reflex Save')",
    'Ref': "get_save_mod(character,'Reflex Save')",
    'Refs': "get_save_sit(character,'Reflex Save')",
    'Will Save': "get_save(character,'Will Save')",
    'Will': "get_save_mod(character,'Will Save')",
    'Wills': "get_save_sit(character,'Will Save')",
    'Saves': "get_save_sit(character,'All Save')",
    'defence special..': "get_attrlist(character,'defensive','special','shortname')",
    'dr special..': "re.sub(r'^','DR ',get_attrlist(character,'damagereduction','special','shortname'))",
    'immune special..': "get_attrlist(character,'immunities','special','shortname')",
    'resist special..': "get_attrlist(character,'resistances','special','shortname')",
    'weak special..': "get_attrlist(character,'weaknesses','special','shortname')",
    'AC': "character.find('armorclass').get('ac')",
    'tAC': "character.find('armorclass').get('touch')",
    'ffAC': "character.find('armorclass').get('flatfooted')",
    'ACs': "character.find('armorclass').find('situationalmodifiers').get('text')",
    'ACP': "get_attrlist(character,'penalties','penalty','text',test=('name','%s == \"Armor Check Penalty\"'))",
    'MaxDex': "get_attrlist(character,'penalties','penalty','text',test=('name','%s == \"Max Dex Bonus\"'))",
    'CMB': "character.find('maneuvers').get('cmb')",
    'CMBothers': "get_varied_maneuvers(character,'cmb')",
    'CMD': "character.find('maneuvers').get('cmd')",
    'CMDothers': "get_varied_maneuvers(character,'cmd')",
    'ffCMD': "character.find('maneuvers').get('cmdflatfooted')",
    'init': "character.find('initiative').get('total')",
    'init situational': "character.find('initiative').find('situationalmodifiers').get('text')",
    'basespeed': "character.find('movement').find('basespeed').get('value')",
    'speed': "character.find('movement').find('speed').get('value')",
    'encum': "character.find('encumbrance').get('light') + '/' + character.find('encumbrance').get('medium') + '/' + character.find('encumbrance').get('heavy') + ' (' + character.find('encumbrance').get('carried') + ')' + character.find('encumbrance').get('level')[0:1]",
    'percep': "re.sub(r'\+-','-','+' + get_attr(character.find('skills').findall('skill'),('name','Perception'),(None,'value')))",
    'percep situational': "get_attr(character.find('skills').findall('skill'),('name','Perception'),('situationalmodifiers','text'))",
    'all skills..': "get_skills(character,minRank=0,minMod=-9999)",
    'trained skills..': "get_skills(character,minRank=1,minMod=4)",
    'feats..': "get_attrlist(character,'feats','feat','name',test=('profgroup','%s != \"yes\"'))",
    'traits..': "get_attrlist(character,'traits','trait','name')",
    'flaws..': "get_attrlist(character,'flaws','flaw','name')",
    'skilltricks..': "get_attrlist(character,'skilltricks','skilltrick','name')",
    'animaltricks..': "get_attrlist(character,'animaltricks','animaltrick','name')[0:-8]",
    'BAB': "character.find('attack').get('baseattack')",
    'meleeB': "character.find('attack').get('meleeattack')",
    'rangeB': "character.find('attack').get('rangedattack')",
    'attack special..': "get_attrlist(character,'attack','special','shortname')",
    'melee weapons..': "get_weaponlist(character,'melee',onlyEquipped=False)",
    'range weapons..': "get_weaponlist(character,'ranged',onlyEquipped=False)",
    'melee equipped weapons..': "get_weaponlist(character,'melee',onlyEquipped=True)",
    'range equipped weapons..': "get_weaponlist(character,'ranged',onlyEquipped=True)",
    'defenses armor..': "get_attrlist(character,'defenses','armor','name',quant=True)",
    'magic items..': "get_attrlist(character,'magicitems','item','name',quant=True)",
    'gear items..': "get_attrlist(character,'gear','item','name',quant=True)",
    'spelllike special..': "get_attrlist(character,'spelllike','special','name',quant=True)",
    'tracked items..': "get_attrlist(character,'trackedresources','trackedresource','name',quant=True)",
    'other special..': "get_attrlist(character,'otherspecials','special','name')",
    'spells known..': "get_sortedspells(character,'spellsknown')",
    'spells memorized..': "get_sortedspells(character,'spellsmemorized')",
    'spells book..': "get_sortedspells(character,'spellbook')",
    'spellclasses..': "get_spellclasses(character.find('spellclasses'))",
    'npc description': "get_textformatch(character.find('npc'),('description',''),('',''))",
    'npc basics': "get_textformatch(character.find('npc'),('description',''),('',''))",
    'npc basics-goals': "get_textformatch(character.find('npc'),('basics','npcinfo'),('name','Motivations & Goals'))",
    'npc basics-motivation': "get_textformatch(character.find('npc'),('basics','npcinfo'),('name','Motivations & Goals'))",
    'npc basics-plots': "get_textformatch(character.find('npc'),('basics','npcinfo'),('name','Schemes, Plots & Adventure Hooks'))",
    'npc basics-hooks': "get_textformatch(character.find('npc'),('basics','npcinfo'),('name','Schemes, Plots & Adventure Hooks'))",
    'npc basics-boons': "get_textformatch(character.find('npc'),('basics','npcinfo'),('name','Boon'))",
    'npc tactics-before': "get_textformatch(character.find('npc'),('tactics','npcinfo'),('name','Tactics - Before Combat'))",
    'npc tactics-during': "get_textformatch(character.find('npc'),('tactics','npcinfo'),('name','Tactics - During Combat'))",
    'npc tactics-morale': "get_textformatch(character.find('npc'),('tactics','npcinfo'),('name','Tactics - Morale'))",
    'npc ecology-stats': "get_textformatch(character.find('npc'),('tactics','npcinfo'),('name','Base Statistics'))",
    'npc ecology-environment': "get_textformatch(character.find('npc'),('ecology','npcinfo'),('name','Ecology - Environment'))",
    'npc ecology-organization': "get_textformatch(character.find('npc'),('ecology','npcinfo'),('name','Ecology - Organization'))",
    'npc ecology-trerasure': "get_textformatch(character.find('npc'),('ecology','npcinfo'),('name','Ecology - Treasure'))",
    'npc history': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','History'))",
    'npc history-goals': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','History / Goals'))",
    'npc history-goals-boons': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','History / Goals / Boons'))",
    'npc personality-mannerisms': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','Personality / Mannerisms'))",
    'npc pc-interactions': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','PC Interactions'))",
    'npc pc-interaction': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','PC Interaction'))",
    'npc interaction': "get_textformatch(character.find('npc'),('additional','npcinfo'),('name','Interaction'))"
    }

    IMAGEMATCH
    ==========
    The image match dictionary is for replacing shape placeholders named with the
    keyword or just just the keyword as the placeholder.  Examples of using the
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
    object with an imageHigh and/or imageLow attriburte (default imageHigh).  The
    value of this attribute is a tuple containing the filename afor the image
    nd the absolute path filename for the image.  If the value is the first in
    a list and the `..`` modifier is used, imageHigh and/or imageLow is evaluated
    for each item in the list and returned as a list of tuples
    """
    IMAGEMATCH = {
    'typeIcon': 'feature.types.typeList[0].typeIcon', # creatrue type icon
    'image': 'images.imageList[0]', # character image
    'terrainIcon':'feature.npc.ecology.environment.terrainIconList[0]', #terrain icon
    'climateIcon': 'feature.npc.ecology.environment.climateIconList[0]', #climate icon
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
        hMatch = re.search(r'^([^:]+):([^:].*)$',myKey)
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
        # some matchers use the stribes key, some use the full key
        keyWord = myKey in self.matcherDictionary and myKey or keyText
        if keyWord not in self.matcherDictionary:
            print("Warning: %s is not in Matcher, empty text returned" % keyWord)
            if self.type == 'boolean': return False
            return ''
        rtnList = []
        for myValue in re.split("\0",self.matcherDictionary[keyWord]):
            if not self._exists(myValue):
                print("Warning: %s is not in Character %s, empty text returned" % (keyWord,self.name))
                if self.type == 'boolean': return False
                rtnList.append('')
                continue
            # if this is not an image matcher lets get the final attribute name
            #print(myValue)
            if self.type != 'image':
                (myValue,finalAttr) = re.search('^(.*\.)?([^.]+)$',myValue).groups()
                #print(myValue,finalAttr)
                myValue = myValue and re.sub(r'\.$','',myValue) or myValue
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
        if len(rtnList) == 0:
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