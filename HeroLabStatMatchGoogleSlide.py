# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:41:38 2018

@author: steve
"""
from HeroLabStatMatch import Matcher

class GoogleSlideMatcher(Matcher):
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
    SLIDENAMEMATCH = {
    }
    TEXTMATCH = {
    'role': 'role', # pc, npc, etc
    'align': 'feature.alignment.name', # alignment written out
    'name': 'name', # character name
    'NPC-Noncombat-Noimage': 'name', # character name
    'NPC-Noncombat-Image': 'name', # character name
    'NPC-Combat-Noimage': 'name', # character name
    'NPC-Combat-Image': 'name', # character name
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
    'hero': "feature.heropoints.enabled == 'yes'\x1dfeature.heropoints.total", # get hero points
    'senses': "feature.senses.specialList[0].shortname", # Scent, Low-light, etc
    'auras': "feature.auras.specialList[0].name", # Good, Evil, Fear, etc
    'favoredclasses': "feature.favoredclasses.favoredclassList[0].name", # favored classes for level bonus
    'HP': "feature.health.hitpoints", # total hit points
    'HD': "feature.health.hitdice", # number and type of hit dice
    'xp': "feature.xp.total", # total experience points earned
    'money': "feature.money.total", # total gold piece worth
    'gender': "feature.personal.gender", # Male, Female, etc
    'age': "feature.personal.age != '0'\x1dfeature.personal.age", # years since birth
    'hair': "feature.personal.hair", # hair color, description, name
    'eyes': "feature.personal.eyes", # eye color, number, etc
    'skin': "feature.personal.skin", # skin color, thickness, etc
    'height': "feature.personal.charheight.value > 0\x1dfeature.personal.charheight.text", # how far till your feet reach the floor
    'weight': "feature.personal.charweight.value > 0\x1dfeature.personal.charweight.text", # arbitrary measure of increasing isotropy
    'personal': "feature.personal.description.fText", # background detail from personal tab
    'languages': "feature.languages.languageList[0].name", # list of known languages
    'str': "feature.attributes.strength.attrvalue.text", # actual value of the attribute
    'dex': "feature.attributes.dexterity.attrvalue.text", # actual value of the attribute
    'con': "feature.attributes.constitution.attrvalue.text", # actual value of the attribute
    'int': "feature.attributes.intelligence.attrvalue.text", # actual value of the attribute
    'wis': "feature.attributes.wisdom.attrvalue.text", # actual value of the attribute
    'cha': "feature.attributes.charisma.attrvalue.text", # actual value of the attribute
    'STR': "feature.attributes.strength.attrbonus.text", # roll modifier for the attribute
    'DEX': "feature.attributes.dexterity.attrbonus.text", # roll modifier for the attribute
    'CON': "feature.attributes.constitution.attrbonus.text", # roll modifier for the attribute
    'INT': "feature.attributes.intelligence.attrbonus.text", # roll modifier for the attribute
    'WIS': "feature.attributes.wisdom.attrbonus.text", # roll modifier for the attribute
    'CHA': "feature.attributes.charisma.attrbonus.text", # roll modifier for the attribute
    'STRs': "feature.attributes.strength.situationalmodifiers.text", # situational modifier for the attribute
    'DEXs': "feature.attributes.dexterity.situationalmodifiers.text", # situational modifier for the attribute
    'CONs': "feature.attributes.constitution.situationalmodifiers.text", # situational modifier for the attribute
    'INTs': "feature.attributes.intelligence.situationalmodifiers.text", # situational modifier for the attribute
    'WISs': "feature.attributes.wisdom.situationalmodifiers.text", # situational modifier for the attribute
    'CHAs': "feature.attributes.charisma.situationalmodifiers.text", # situational modifier for the attribute
    'Save': "feature.saves.allsaves.save", # roll modifier for all saving throws
    'Saves': "feature.saves.allsaves.situationalmodifiers.situationalmodifierList[0].text", # situational modifier for all saving throws
    'Fort': "feature.saves.fortitudeSave.save", # roll modifier for fortitude saving throw
    'Forts': "feature.saves.fortitudeSave.situationalmodifiers.situationalmodifierList[0].text", # situational modifier for fortitude saving throw
    'Refl': "feature.saves.reflexSave.save", # roll modifier for reflex saving throw
    'Refls': "feature.saves.reflexSave.situationalmodifiers.situationalmodifierList[0].text", # situational modifier for reflex saving throw
    'Will': "feature.saves.willSave.save", # roll modifier for will saving throw
    'Wills': "feature.saves.willSave.situationalmodifiers.situationalmodifierList[0].text", # situational modifier for will saving throw

    'defence special': "feature.defensive.special.name", # special defensive abilities (name includes type, shortname does not)
    'DR': "feature.damagereduction.special.shortname", # DR 
    'immune special': "feature.immunities.special.shortname", # special immunities
    'resist special': "feature.resistances.special.shortname", # special resistances
    'weak special': "feature.weaknesses.special.shortname", # special vulnerabilities
    'AC': "feature.armorclass.ac", # 
    'tAC': "feature.armorclass.touch", # 
    'ffAC': "feature.armorclass.flatfooted", #
    'ACs': "feature.armorclass.situationalmodifiers.text",
    'ACP': "feature.penalties.armorCheckPenalty.text",
    'MaxDex': "feature.penalties.maxDexBonus.value < 99\x1dfeature.penalties.maxDexBonus.text",
    'CMB': "feature.maneuvers.cmb",
    'CMD': "feature.maneuvers.cmd",
    'CMBblow': "feature.maneuvers.cmb != feature.maneuvers.awesomeBlow.cmb\x1dfeature.maneuvers.awesomeBlow.cmb",
    'CMBrush': "feature.maneuvers.cmb != feature.maneuvers.bullRush.cmb\x1dfeature.maneuvers.bullRush.cmb",
    }
    """
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
