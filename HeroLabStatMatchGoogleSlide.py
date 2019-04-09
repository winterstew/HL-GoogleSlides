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
    {{head|_keyword}}
    {{(head|_keyword)}}
    {{head|keyword..}}
    {{head|?keyword..}}
    {{head|.c.keyword}}
    {{(head|_keyword..)}}
    {{head|_keyword_..}}

      ``keyword``
        must have a match in the dictionary to give a value which will be
        evaluated.  It must also not have a ``..`` (double period) as part of it.

      ``()``
        must be the outer most element, but inside the double brackets.  If
        the value evaluation results in something parenthesis are placed around it

      ``head|``
        This is replaced with the *head* text if the value evaluation results
        in something.  The ``|`` (vetical bar) may not be used anywhere else.

      ``head|?``
        This is replaced with the *head* text if the value evaluation results
        in something, however only the head text is returned.

      ``_``
        This is used before a keyword to indicate that instead of the evaluated 
        value the parent Feature's abbreviate method should ne called with the 
        final attribute as the argument.  
        If it is used after the keyword, the parent Feature's describe method
        is called and the result returned. 

      ``.c.``
        This before the keyword is used for tracking item lists.  The value
        should evaluate to an integer value.  The ``c`` can be any single character
        that character will be repeated interger times based onthe evaluated value

      ``..``
        This after a keyword is used to indicate a possible list.  The value
        should evaluate to an attribute from the first element in the list.  The
        list should be one element up from the attribute.  The result will be the
        same attribute from all the elements in the list.  Any text following
        the ``..`` will be used as separators between the items in the list.

    The value for each item in the text match dictionary should evaluate to the
    text which will replace the keyword in the template document, or as mentioned
    above the text for the first attribute in a list.
    
    There are also some simple operations which can be done as part of the value
    evaluation.  These include multiple attribute evaluation, keyword nesting, 
    and simple conditionals.
    
        ``\x1f``
          This is used to indicate that there are multiple attributes references
          in the keyword item's value.  Each attribute is listed with this 
          character as the separator and will evaluate as a space separated list
          
        ``\x1e``
           This is used to nest keywords in the values.  The double brackets
           are not used.  However, all the modifiers can be used.  Each is 
           separated with thsi character and will be result in a list of values

        ``\x1d``
          This is used to separate a conditional from the following replacement
          The conditional can only be very simple with operators as in the global
          OPERATORS, all numbers will be treated as floats, sring comparisons 
          should be listed without any quotes and any attribute replacements
          must be very simple.
    """
    SLIDENAMEMATCH = {
    }
    TEXTMATCH = {
    'role': 'role', # pc, npc, etc
    'align': 'feature.alignment.name', # alignment written out
    'name': 'name', # character name
    'master': "isMinion\x1dparent.name", # name of a minions master
    'NPC-Noncombat-Noimage': 'name', # character name
    'NPC-Noncombat-Image': 'name', # character name
    'NPC-Combat-Noimage': 'name', # character name
    'NPC-Combat-Image': 'name', # character name
    'BestiaryStyle-Noimage': 'name', # character name
    'BestiaryStyle-Image': 'name', # character name
    'BestiaryStyle-Noimage-Page2': 'name', # character name
    'BestiaryStyle-Image-Page2': 'name', # character name
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
    'CR': 'feature.challengerating.value', # challenge rating with CR prepended
    'XP': 'feature.xpaward.value', # XP awarded for creature (comma for thousands and XP appended)
    'classes summary': 'feature.classes.summary', # summary list of all classes
    'type': 'feature.types.typeList[0].name', # get name of creature type
    'subtype': 'feature.subtypes.subtypeList[0].name)', # get name of creatrue subtype
    'hero': "feature.heropoints.enabled == yes\x1dfeature.heropoints.total", # get hero points
    'senses': "feature.senses.specialList[0].shortname", # Scent, Low-light, etc
    'auras': "feature.auras.specialList[0].name", # Good, Evil, Fear, etc
    'favoredclasses': "feature.favoredclasses.favoredclassList[0].name", # favored classes for level bonus
    'HP': "feature.health.hitpoints", # total hit points
    'HD': "feature.health.hitdice", # number and type of hit dice
    'xp': "feature.xp.total", # total experience points earned
    'money': "feature.money.total", # total gold piece worth
    'gender': "feature.personal.gender", # Male, Female, etc
    'age': "feature.personal.age and feature.personal.age > 0\x1dfeature.personal.age", # years since birth
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
    'defense special': "feature.defensive.special.name", # special defensive abilities (name includes type, shortname does not)
    'DR': "feature.damagereduction.special.shortname", # DR
    'SR': "feature.resistances.specialList[0].type == spells\x1dfeature.resistances.specialList[0].value", # SR 
    'immune special': "feature.immunities.specialList[0].shortname", # special immunities
    'resist special': "feature.resistances.specialList[0].shortname", # special resistances
    'weak special': "feature.weaknesses.specialList[0].shortname", # special vulnerabilities
    'AC': "feature.armorclass.ac", #
    'tAC': "feature.armorclass.touch", #
    'ffAC': "feature.armorclass.flatfooted", #
    'ACs': "feature.armorclass.situationalmodifiers.text",
    'ACP': "feature.penalties.armorCheckPenalty.text",
    'MaxDex': "feature.penalties.maxDexBonus.value < 99\x1dfeature.penalties.maxDexBonus.text",
    'CMB': "feature.maneuvers.cmb",
    'CMD': "feature.maneuvers.cmd",
    'ffCMD': "feature.maneuvers.cmdflatfooted",
    'CMBothers': " blow:|CMBblow\x1f rush:|CMBrush\x1f trick:|CMBtrick\x1f dsarm:|CMBdisarm\x1f drag:|CMBdrag\x1f feint:|CMBfeint\x1f grpl:|CMBgrapple\x1f over:|CMBoverrun\x1f pull:|CMBpull\x1f push:|CMBpush\x1f repo:|CMBreposition\x1f steal:|CMBsteal\x1f sndr:|CMBsunder\x1f trip:|CMBtrip",
    'CMBblow': "feature.maneuvers.cmb != feature.maneuvers.awesomeBlow.cmb\x1dfeature.maneuvers.awesomeBlow.cmb",
    'CMBrush': "feature.maneuvers.cmb != feature.maneuvers.bullRush.cmb\x1dfeature.maneuvers.bullRush.cmb",
    'CMBtrick': "feature.maneuvers.cmb != feature.maneuvers.dirtyTrick.cmb\x1dfeature.maneuvers.dirtyTrick.cmb",
    'CMBdisarm': "feature.maneuvers.cmb != feature.maneuvers.disarm.cmb\x1dfeature.maneuvers.disarm.cmb",
    'CMBdrag': "feature.maneuvers.cmb != feature.maneuvers.drag.cmb\x1dfeature.maneuvers.drag.cmb",
    'CMBfeint': "feature.maneuvers.cmb != feature.maneuvers.feint.cmb\x1dfeature.maneuvers.feint.cmb",
    'CMBgrapple': "feature.maneuvers.cmb != feature.maneuvers.grapple.cmb\x1dfeature.maneuvers.grapple.cmb",
    'CMBoverrun': "feature.maneuvers.cmb != feature.maneuvers.overrun.cmb\x1dfeature.maneuvers.overrun.cmb",
    'CMBpull': "feature.maneuvers.cmb != feature.maneuvers.pull.cmb\x1dfeature.maneuvers.pull.cmb",
    'CMBpush': "feature.maneuvers.cmb != feature.maneuvers.push.cmb\x1dfeature.maneuvers.push.cmb",
    'CMBreposition': "feature.maneuvers.cmb != feature.maneuvers.reposition.cmb\x1dfeature.maneuvers.reposition.cmb",
    'CMBsteal': "feature.maneuvers.cmb != feature.maneuvers.steal.cmb\x1dfeature.maneuvers.steal.cmb",
    'CMBsunder': "feature.maneuvers.cmb != feature.maneuvers.sunder.cmb\x1dfeature.maneuvers.sunder.cmb",
    'CMBtrip': "feature.maneuvers.cmb != feature.maneuvers.trip.cmb\x1dfeature.maneuvers.trip.cmb",
    'CMDothers': " blow:|CMDblow\x1f rush:|CMDrush\x1f trick:|CMDtrick\x1f dsarm:|CMDdisarm\x1f drag:|CMDdrag\x1f feint:|CMDfeint\x1f grpl:|CMDgrapple\x1f over:|CMDoverrun\x1f pull:|CMDpull\x1f push:|CMDpush\x1f repo:|CMDreposition\x1f steal:|CMDsteal\x1f sndr:|CMDsunder\x1f trip:|CMDtrip",
    'CMDblow': "feature.maneuvers.cmd != feature.maneuvers.awesomeBlow.cmd\x1dfeature.maneuvers.awesomeBlow.cmd",
    'CMDrush': "feature.maneuvers.cmd != feature.maneuvers.bullRush.cmd\x1dfeature.maneuvers.bullRush.cmd",
    'CMDtrick': "feature.maneuvers.cmd != feature.maneuvers.dirtyTrick.cmd\x1dfeature.maneuvers.dirtyTrick.cmd",
    'CMDdisarm': "feature.maneuvers.cmd != feature.maneuvers.disarm.cmd\x1dfeature.maneuvers.disarm.cmd",
    'CMDdrag': "feature.maneuvers.cmd != feature.maneuvers.drag.cmd\x1dfeature.maneuvers.drag.cmd",
    'CMDfeint': "feature.maneuvers.cmd != feature.maneuvers.feint.cmd\x1dfeature.maneuvers.feint.cmd",
    'CMDgrapple': "feature.maneuvers.cmd != feature.maneuvers.grapple.cmd\x1dfeature.maneuvers.grapple.cmd",
    'CMDoverrun': "feature.maneuvers.cmd != feature.maneuvers.overrun.cmd\x1dfeature.maneuvers.overrun.cmd",
    'CMDpull': "feature.maneuvers.cmd != feature.maneuvers.pull.cmd\x1dfeature.maneuvers.pull.cmd",
    'CMDpush': "feature.maneuvers.cmd != feature.maneuvers.push.cmd\x1dfeature.maneuvers.push.cmd",
    'CMDreposition': "feature.maneuvers.cmd != feature.maneuvers.reposition.cmd\x1dfeature.maneuvers.reposition.cmd",
    'CMDsteal': "feature.maneuvers.cmd != feature.maneuvers.steal.cmd\x1dfeature.maneuvers.steal.cmd",
    'CMDsunder': "feature.maneuvers.cmd != feature.maneuvers.sunder.cmd\x1dfeature.maneuvers.sunder.cmd",
    'CMDtrip': "feature.maneuvers.cmd != feature.maneuvers.trip.cmd\x1dfeature.maneuvers.trip.cmd",
    'init': "feature.initiative.total",
    'init situational': "feature.initiative.situationalmodifiers.text",
    'basespeed': "feature.movement.basespeed.text",
    'speed': "feature.movement.speed.text",
    'climbspeed': "feature.movement.climb.text",
    'fly':"{{fly:|flyspeed}}\x1f{{(_flymaneuver)}}",
    'flyspeed': "feature.movement.fly.text",
    'flymaneuver': 'feature.movement.fly.maneuverability',
    'swimspeed': "feature.movement.swim.text",
    'burrowspeed': "feature.movement.burrow.text",
    'jetspeed': "feature.movement.jet.text",
    'surgespeed': "feature.movement.surge.text",
    'leap': "feature.movement.leap.name",
    'icewalking': "feature.movement.icewalking.name",
    'earthglide': "feature.movement.earthGlide.name",
    'airwalk': "feature.movement.airWalk.name",
    'waterwalk': "feature.movement.waterWalk.name",
    'cloudwalking': "feature.movement.cloudwalking.name",
    'swiftflight': "feature.movement.swiftFlight.name",
    'sidewaysscuttle': "feature.movement.sidewaysScuttle.name",
    'gracefulflight': "feature.movement.gracefulFlight.name",
    'otherspeed': "{{fly:|fly.. }}\x1f{{climb:|climbspeed}}\x1f{{swim:|swimspeed}}\x1f{{burrow:|burrowspeed}}\x1f{{jet:|jetspeed}}\x1f{{surge:|surgespeed}}\x1f{{leap}}\x1f{{icewalking}}\x1f{{earthglide}}\x1f{{airwalk}}\x1f{{waterwalk}}\x1f{{cloudwalking}}\x1f{{cloudwalking}}\x1f{{swiftflight}}\x1f{{sidewaysscuttle}}\x1f{{gracefulflight}}",
    'encumlight': "feature.encumbrance.light",
    'encummedium': "feature.encumbrance.medium",
    'encumheavy': "feature.encumbrance.heavy",
    'encum': "{{encumlight}}\x1f{{encummedium}}\x1f{{encumheavy}}",
    'carry': "feature.encumbrance.carried",
    'load': "feature.encumbrance.level",
    'percep': "feature.skills.perception.text",
    'percep situational': "feature.skills.perception.situationalmodifiers.text",
    'all skills': "feature.skills.skillList[0].name\x1efeature.skills.skillList[0].text",
    'trained skills': "feature.skills.skillList[0].ranks > 0\x1dfeature.skills.skillList[0].name\x1efeature.skills.skillList[0].text", 
    'best skills': "feature.skills.skillList[0].ranks > 0 or feature.skills.skillList[0].value > 4\x1dfeature.skills.skillList[0].name\x1efeature.skills.skillList[0].text", 
    'acrobatics':"feature.skills.acrobatics.text",
    'appraise':"feature.skills.appraise.text",
    'bluff':"feature.skills.bluff.text",
    'climb':"feature.skills.climb.text",
    'craft':"feature.skills.craft.text",
    'craftAlchemy':"feature.skills.craftAlchemy.text",
    'craftArmor':"feature.skills.craftArmor.text",
    'craftBaskets':"feature.skills.craftBaskets.text",
    'craftBooks':"feature.skills.craftBooks.text",
    'craftBows':"feature.skills.craftBows.text",
    'craftCalligraphy':"feature.skills.craftCalligraphy.text",
    'craftCarpentry':"feature.skills.craftCarpentry.text",
    'craftCloth':"feature.skills.craftCloth.text",
    'craftClothing':"feature.skills.craftClothing.text",
    'craftCrystalCarving':"feature.skills.craftCrystalCarving.text",
    'craftGlass':"feature.skills.craftGlass.text",
    'craftJewelry':"feature.skills.craftJewelry.text",
    'craftLeather':"feature.skills.craftLeather.text",
    'craftLocks':"feature.skills.craftLocks.text",
    'craftPaintings':"feature.skills.craftPaintings.text",
    'craftPottery':"feature.skills.craftPottery.text",
    'craftSculptures':"feature.skills.craftSculptures.text",
    'craftShips':"feature.skills.craftShips.text",
    'craftShoes':"feature.skills.craftShoes.text",
    'craftStonemasonry':"feature.skills.craftStonemasonry.text",
    'craftTraps':"feature.skills.craftTraps.text",
    'craftWeapons':"feature.skills.craftWeapons.text",
    'craftLeather':"feature.skills.craftLeather.text",
    'craftTraps':"feature.skills.craftTraps.text",
    'diplomacy':"feature.skills.diplomacy.text",
    'disableDevice':"feature.skills.disableDevice.text",
    'disguise':"feature.skills.disguise.text",
    'escapeArtist':"feature.skills.escapeArtist.text",
    'fly':"feature.skills.fly.text",
    'handleAnimal':"feature.skills.handleAnimal.text",
    'heal':"feature.skills.heal.text",
    'intimidate':"feature.skills.intimidate.text",
    'knowledgeArcana':"feature.skills.knowledgeArcana.text",
    'knowledgeDungeoneering':"feature.skills.knowledgeDungeoneering.text",
    'knowledgeEngineering':"feature.skills.knowledgeEngineering.text",
    'knowledgeGeography':"feature.skills.knowledgeGeography.text",
    'knowledgeHistory':"feature.skills.knowledgeHistory.text",
    'knowledgeLocal':"feature.skills.knowledgeLocal.text",
    'knowledgeNature':"feature.skills.knowledgeNature.text",
    'knowledgeNobility':"feature.skills.knowledgeNobility.text",
    'knowledgePlanes':"feature.skills.knowledgePlanes.text",
    'knowledgeReligion':"feature.skills.knowledgeReligion.text",
    'knowArcana':"feature.skills.knowledgeArcana.text",
    'knowDungeoneering':"feature.skills.knowledgeDungeoneering.text",
    'knowEngineering':"feature.skills.knowledgeEngineering.text",
    'knowGeography':"feature.skills.knowledgeGeography.text",
    'knowHistory':"feature.skills.knowledgeHistory.text",
    'knowLocal':"feature.skills.knowledgeLocal.text",
    'knowNature':"feature.skills.knowledgeNature.text",
    'knowNobility':"feature.skills.knowledgeNobility.text",
    'knowPlanes':"feature.skills.knowledgePlanes.text",
    'knowReligion':"feature.skills.knowledgeReligion.text",
    'linguistics':"feature.skills.linguistics.text",
    'perception':"feature.skills.perception.text",
    'perform':"feature.skills.perform.text",
    'performAct':"feature.skills.performAct.text",
    'performComedy':"feature.skills.performComedy.text",
    'performDance':"feature.skills.performDance.text",
    'performKeyboard':"feature.skills.performKeyboard.text",
    'performOratory':"feature.skills.performOratory.text",
    'performPercussion':"feature.skills.performPercussion.text",
    'performString':"feature.skills.performString.text",
    'performWind':"feature.skills.performWind.text",
    'performSing':"feature.skills.performSing.text",
    'perf':"feature.skills.perform.text",
    'perfAct':"feature.skills.performAct.text",
    'perfComedy':"feature.skills.performComedy.text",
    'perfDance':"feature.skills.performDance.text",
    'perfKeyboard':"feature.skills.performKeyboard.text",
    'perfOratory':"feature.skills.performOratory.text",
    'perfPercussion':"feature.skills.performPercussion.text",
    'perfString':"feature.skills.performString.text",
    'perfWind':"feature.skills.performWind.text",
    'perfSing':"feature.skills.performSing.text",
    'profession':"feature.skills.profession.text",
    'professionArchitect':"feature.skills.professionArchitect.text",
    'professionBaker':"feature.skills.professionBaker.text",
    'professionBarrister':"feature.skills.professionBarrister.text",
    'professionBrewer':"feature.skills.professionBrewer.text",
    'professionButcher':"feature.skills.professionButcher.text",
    'professionClerk':"feature.skills.professionClerk.text",
    'professionCook':"feature.skills.professionCook.text",
    'professionCourtesan':"feature.skills.professionCourtesan.text",
    'professionDriver':"feature.skills.professionDriver.text",
    'professionEngineer':"feature.skills.professionEngineer.text",
    'professionFarmer':"feature.skills.professionFarmer.text",
    'professionFisherman':"feature.skills.professionFisherman.text",
    'professionGambler':"feature.skills.professionGambler.text",
    'professionGardener':"feature.skills.professionGardener.text",
    'professionHerbalist':"feature.skills.professionHerbalist.text",
    'professionInnkeeper':"feature.skills.professionInnkeeper.text",
    'professionLibrarian':"feature.skills.professionLibrarian.text",
    'professionMerchant':"feature.skills.professionMerchant.text",
    'professionMidwife':"feature.skills.professionMidwife.text",
    'professionMiller':"feature.skills.professionMiller.text",
    'professionMiner':"feature.skills.professionMiner.text",
    'professionPorter':"feature.skills.professionPorter.text",
    'professionSailor':"feature.skills.professionSailor.text",
    'professionScribe':"feature.skills.professionScribe.text",
    'professionShepherd':"feature.skills.professionShepherd.text",
    'professionStableMaster':"feature.skills.professionStableMaster.text",
    'professionSoldier':"feature.skills.professionSoldier.text",
    'professionTanner':"feature.skills.professionTanner.text",
    'professionTrapper':"feature.skills.professionTrapper.text",
    'professionWoodcutter':"feature.skills.professionWoodcutter.text",
    'prof':"feature.skills.profession.text",
    'profArchitect':"feature.skills.professionArchitect.text",
    'profBaker':"feature.skills.professionBaker.text",
    'profBarrister':"feature.skills.professionBarrister.text",
    'profBrewer':"feature.skills.professionBrewer.text",
    'profButcher':"feature.skills.professionButcher.text",
    'profClerk':"feature.skills.professionClerk.text",
    'profCook':"feature.skills.professionCook.text",
    'profCourtesan':"feature.skills.professionCourtesan.text",
    'profDriver':"feature.skills.professionDriver.text",
    'profEngineer':"feature.skills.professionEngineer.text",
    'profFarmer':"feature.skills.professionFarmer.text",
    'profFisherman':"feature.skills.professionFisherman.text",
    'profGambler':"feature.skills.professionGambler.text",
    'profGardener':"feature.skills.professionGardener.text",
    'profHerbalist':"feature.skills.professionHerbalist.text",
    'profInnkeeper':"feature.skills.professionInnkeeper.text",
    'profLibrarian':"feature.skills.professionLibrarian.text",
    'profMerchant':"feature.skills.professionMerchant.text",
    'profMidwife':"feature.skills.professionMidwife.text",
    'profMiller':"feature.skills.professionMiller.text",
    'profMiner':"feature.skills.professionMiner.text",
    'profPorter':"feature.skills.professionPorter.text",
    'profSailor':"feature.skills.professionSailor.text",
    'profScribe':"feature.skills.professionScribe.text",
    'profShepherd':"feature.skills.professionShepherd.text",
    'profStableMaster':"feature.skills.professionStableMaster.text",
    'profSoldier':"feature.skills.professionSoldier.text",
    'profTanner':"feature.skills.professionTanner.text",
    'profTrapper':"feature.skills.professionTrapper.text",
    'profWoodcutter':"feature.skills.professionWoodcutter.text",
    'ride':"feature.skills.ride.text",
    'senseMotive':"feature.skills.senseMotive.text",
    'sleightOfHand':"feature.skills.sleightOfHand.text",
    'spellcraft':"feature.skills.spellcraft.text",
    'stealth':"feature.skills.stealth.text",
    'survival':"feature.skills.survival.text",
    'swim':"feature.skills.swim.text",
    'acrobaticss':"feature.skills.acrobatics.situationalmodifiers.text",
    'appraises':"feature.skills.appraise.situationalmodifiers.text",
    'bluffs':"feature.skills.bluff.situationalmodifiers.text",
    'climbs':"feature.skills.climb.situationalmodifiers.text",
    'crafts':"feature.skills.craft.situationalmodifiers.text",
    'craftAlchemys':"feature.skills.craftAlchemy.situationalmodifiers.text",
    'craftArmors':"feature.skills.craftArmor.situationalmodifiers.text",
    'craftBasketss':"feature.skills.craftBaskets.situationalmodifiers.text",
    'craftBookss':"feature.skills.craftBooks.situationalmodifiers.text",
    'craftBowss':"feature.skills.craftBows.situationalmodifiers.text",
    'craftCalligraphys':"feature.skills.craftCalligraphy.situationalmodifiers.text",
    'craftCarpentrys':"feature.skills.craftCarpentry.situationalmodifiers.text",
    'craftCloths':"feature.skills.craftCloth.situationalmodifiers.text",
    'craftClothings':"feature.skills.craftClothing.situationalmodifiers.text",
    'craftCrystalCarvings':"feature.skills.craftCrystalCarving.situationalmodifiers.text",
    'craftGlasss':"feature.skills.craftGlass.situationalmodifiers.text",
    'craftJewelrys':"feature.skills.craftJewelry.situationalmodifiers.text",
    'craftLeathers':"feature.skills.craftLeather.situationalmodifiers.text",
    'craftLockss':"feature.skills.craftLocks.situationalmodifiers.text",
    'craftPaintingss':"feature.skills.craftPaintings.situationalmodifiers.text",
    'craftPotterys':"feature.skills.craftPottery.situationalmodifiers.text",
    'craftSculpturess':"feature.skills.craftSculptures.situationalmodifiers.text",
    'craftShipss':"feature.skills.craftShips.situationalmodifiers.text",
    'craftShoess':"feature.skills.craftShoes.situationalmodifiers.text",
    'craftStonemasonrys':"feature.skills.craftStonemasonry.situationalmodifiers.text",
    'craftTrapss':"feature.skills.craftTraps.situationalmodifiers.text",
    'craftWeaponss':"feature.skills.craftWeapons.situationalmodifiers.text",
    'craftLeathers':"feature.skills.craftLeather.situationalmodifiers.text",
    'craftTrapss':"feature.skills.craftTraps.situationalmodifiers.text",
    'diplomacys':"feature.skills.diplomacy.situationalmodifiers.text",
    'disableDevices':"feature.skills.disableDevice.situationalmodifiers.text",
    'disguises':"feature.skills.disguise.situationalmodifiers.text",
    'escapeArtists':"feature.skills.escapeArtist.situationalmodifiers.text",
    'flys':"feature.skills.fly.situationalmodifiers.text",
    'handleAnimals':"feature.skills.handleAnimal.situationalmodifiers.text",
    'heals':"feature.skills.heal.situationalmodifiers.text",
    'intimidates':"feature.skills.intimidate.situationalmodifiers.text",
    'knowledgeArcanas':"feature.skills.knowledgeArcana.situationalmodifiers.text",
    'knowledgeDungeoneerings':"feature.skills.knowledgeDungeoneering.situationalmodifiers.text",
    'knowledgeEngineerings':"feature.skills.knowledgeEngineering.situationalmodifiers.text",
    'knowledgeGeographys':"feature.skills.knowledgeGeography.situationalmodifiers.text",
    'knowledgeHistorys':"feature.skills.knowledgeHistory.situationalmodifiers.text",
    'knowledgeLocals':"feature.skills.knowledgeLocal.situationalmodifiers.text",
    'knowledgeNatures':"feature.skills.knowledgeNature.situationalmodifiers.text",
    'knowledgeNobilitys':"feature.skills.knowledgeNobility.situationalmodifiers.text",
    'knowledgePlaness':"feature.skills.knowledgePlanes.situationalmodifiers.text",
    'knowledgeReligions':"feature.skills.knowledgeReligion.situationalmodifiers.text",
    'knowArcanas':"feature.skills.knowledgeArcana.situationalmodifiers.text",
    'knowDungeoneerings':"feature.skills.knowledgeDungeoneering.situationalmodifiers.text",
    'knowEngineerings':"feature.skills.knowledgeEngineering.situationalmodifiers.text",
    'knowGeographys':"feature.skills.knowledgeGeography.situationalmodifiers.text",
    'knowHistorys':"feature.skills.knowledgeHistory.situationalmodifiers.text",
    'knowLocals':"feature.skills.knowledgeLocal.situationalmodifiers.text",
    'knowNatures':"feature.skills.knowledgeNature.situationalmodifiers.text",
    'knowNobilitys':"feature.skills.knowledgeNobility.situationalmodifiers.text",
    'knowPlaness':"feature.skills.knowledgePlanes.situationalmodifiers.text",
    'knowReligions':"feature.skills.knowledgeReligion.situationalmodifiers.text",
    'linguisticss':"feature.skills.linguistics.situationalmodifiers.text",
    'perceptions':"feature.skills.perception.situationalmodifiers.text",
    'performs':"feature.skills.perform.situationalmodifiers.text",
    'performActs':"feature.skills.performAct.situationalmodifiers.text",
    'performComedys':"feature.skills.performComedy.situationalmodifiers.text",
    'performDances':"feature.skills.performDance.situationalmodifiers.text",
    'performKeyboards':"feature.skills.performKeyboard.situationalmodifiers.text",
    'performOratorys':"feature.skills.performOratory.situationalmodifiers.text",
    'performPercussions':"feature.skills.performPercussion.situationalmodifiers.text",
    'performStrings':"feature.skills.performString.situationalmodifiers.text",
    'performWinds':"feature.skills.performWind.situationalmodifiers.text",
    'performSings':"feature.skills.performSing.situationalmodifiers.text",
    'perfs':"feature.skills.perform.situationalmodifiers.text",
    'perfActs':"feature.skills.performAct.situationalmodifiers.text",
    'perfComedys':"feature.skills.performComedy.situationalmodifiers.text",
    'perfDances':"feature.skills.performDance.situationalmodifiers.text",
    'perfKeyboards':"feature.skills.performKeyboard.situationalmodifiers.text",
    'perfOratorys':"feature.skills.performOratory.situationalmodifiers.text",
    'perfPercussions':"feature.skills.performPercussion.situationalmodifiers.text",
    'perfStrings':"feature.skills.performString.situationalmodifiers.text",
    'perfWinds':"feature.skills.performWind.situationalmodifiers.text",
    'perfSings':"feature.skills.performSing.situationalmodifiers.text",
    'professions':"feature.skills.profession.situationalmodifiers.text",
    'professionArchitects':"feature.skills.professionArchitect.situationalmodifiers.text",
    'professionBakers':"feature.skills.professionBaker.situationalmodifiers.text",
    'professionBarristers':"feature.skills.professionBarrister.situationalmodifiers.text",
    'professionBrewers':"feature.skills.professionBrewer.situationalmodifiers.text",
    'professionButchers':"feature.skills.professionButcher.situationalmodifiers.text",
    'professionClerks':"feature.skills.professionClerk.situationalmodifiers.text",
    'professionCooks':"feature.skills.professionCook.situationalmodifiers.text",
    'professionCourtesans':"feature.skills.professionCourtesan.situationalmodifiers.text",
    'professionDrivers':"feature.skills.professionDriver.situationalmodifiers.text",
    'professionEngineers':"feature.skills.professionEngineer.situationalmodifiers.text",
    'professionFarmers':"feature.skills.professionFarmer.situationalmodifiers.text",
    'professionFishermans':"feature.skills.professionFisherman.situationalmodifiers.text",
    'professionGamblers':"feature.skills.professionGambler.situationalmodifiers.text",
    'professionGardeners':"feature.skills.professionGardener.situationalmodifiers.text",
    'professionHerbalists':"feature.skills.professionHerbalist.situationalmodifiers.text",
    'professionInnkeepers':"feature.skills.professionInnkeeper.situationalmodifiers.text",
    'professionLibrarians':"feature.skills.professionLibrarian.situationalmodifiers.text",
    'professionMerchants':"feature.skills.professionMerchant.situationalmodifiers.text",
    'professionMidwifes':"feature.skills.professionMidwife.situationalmodifiers.text",
    'professionMillers':"feature.skills.professionMiller.situationalmodifiers.text",
    'professionMiners':"feature.skills.professionMiner.situationalmodifiers.text",
    'professionPorters':"feature.skills.professionPorter.situationalmodifiers.text",
    'professionSailors':"feature.skills.professionSailor.situationalmodifiers.text",
    'professionScribes':"feature.skills.professionScribe.situationalmodifiers.text",
    'professionShepherds':"feature.skills.professionShepherd.situationalmodifiers.text",
    'professionStableMasters':"feature.skills.professionStableMaster.situationalmodifiers.text",
    'professionSoldiers':"feature.skills.professionSoldier.situationalmodifiers.text",
    'professionTanners':"feature.skills.professionTanner.situationalmodifiers.text",
    'professionTrappers':"feature.skills.professionTrapper.situationalmodifiers.text",
    'professionWoodcutters':"feature.skills.professionWoodcutter.situationalmodifiers.text",
    'profs':"feature.skills.profession.situationalmodifiers.text",
    'profArchitects':"feature.skills.professionArchitect.situationalmodifiers.text",
    'profBakers':"feature.skills.professionBaker.situationalmodifiers.text",
    'profBarristers':"feature.skills.professionBarrister.situationalmodifiers.text",
    'profBrewers':"feature.skills.professionBrewer.situationalmodifiers.text",
    'profButchers':"feature.skills.professionButcher.situationalmodifiers.text",
    'profClerks':"feature.skills.professionClerk.situationalmodifiers.text",
    'profCooks':"feature.skills.professionCook.situationalmodifiers.text",
    'profCourtesans':"feature.skills.professionCourtesan.situationalmodifiers.text",
    'profDrivers':"feature.skills.professionDriver.situationalmodifiers.text",
    'profEngineers':"feature.skills.professionEngineer.situationalmodifiers.text",
    'profFarmers':"feature.skills.professionFarmer.situationalmodifiers.text",
    'profFishermans':"feature.skills.professionFisherman.situationalmodifiers.text",
    'profGamblers':"feature.skills.professionGambler.situationalmodifiers.text",
    'profGardeners':"feature.skills.professionGardener.situationalmodifiers.text",
    'profHerbalists':"feature.skills.professionHerbalist.situationalmodifiers.text",
    'profInnkeepers':"feature.skills.professionInnkeeper.situationalmodifiers.text",
    'profLibrarians':"feature.skills.professionLibrarian.situationalmodifiers.text",
    'profMerchants':"feature.skills.professionMerchant.situationalmodifiers.text",
    'profMidwifes':"feature.skills.professionMidwife.situationalmodifiers.text",
    'profMillers':"feature.skills.professionMiller.situationalmodifiers.text",
    'profMiners':"feature.skills.professionMiner.situationalmodifiers.text",
    'profPorters':"feature.skills.professionPorter.situationalmodifiers.text",
    'profSailors':"feature.skills.professionSailor.situationalmodifiers.text",
    'profScribes':"feature.skills.professionScribe.situationalmodifiers.text",
    'profShepherds':"feature.skills.professionShepherd.situationalmodifiers.text",
    'profStableMasters':"feature.skills.professionStableMaster.situationalmodifiers.text",
    'profSoldiers':"feature.skills.professionSoldier.situationalmodifiers.text",
    'profTanners':"feature.skills.professionTanner.situationalmodifiers.text",
    'profTrappers':"feature.skills.professionTrapper.situationalmodifiers.text",
    'profWoodcutters':"feature.skills.professionWoodcutter.situationalmodifiers.text",
    'rides':"feature.skills.ride.situationalmodifiers.text",
    'senseMotives':"feature.skills.senseMotive.situationalmodifiers.text",
    'sleightOfHands':"feature.skills.sleightOfHand.situationalmodifiers.text",
    'spellcrafts':"feature.skills.spellcraft.situationalmodifiers.text",
    'stealths':"feature.skills.stealth.situationalmodifiers.text",
    'survivals':"feature.skills.survival.situationalmodifiers.text",
    'swims':"feature.skills.swim.situationalmodifiers.text",
    'feats': "feature.feats.featList[0].name",
    'nonproffeats': "feature.feats.featList[0].profgroup == no\x1dfeature.feats.featList[0].name",
    'traits': "feature.traits.traitList[0].name",
    'flaws': "feature.flaws.flawList[0].name",
    'skilltricks': "feature.skilltricks.skilltrickList[0].name",
    'animaltricks': "feature.animaltricks.animaltrickList[0].name",
    'BAB': "feature.attack.baseattack",
    'meleeB': "feature.attack.meleeattack",
    'rangeB': "feature.attack.rangedattack",
    'attack special': "feature.attack.specialList[0].name",
    'melee weapons': "feature.melee.weaponList[0].summary",
    'range weapons': "feature.ranged.weaponList[0].summary",
    'melee equipped weapons': "feature.melee.weaponList[0].equipped\x1dfeature.melee.weaponList[0].summary",
    'range equipped weapons': "feature.ranged.weaponList[0].equipped\x1dfeature.ranged.weaponList[0].summary",
    'defenses armor': "feature.defenses.armorList[0].equipped == yes\x1dfeature.defenses.armorList[0].namequant",
    'magic items': "feature.magicitems.itemList[0].quantity > 0\x1dfeature.magicitems.itemList[0].namequant",
    'gear items': "feature.gear.itemList[0].quantity > 0\x1dfeature.gear.itemList[0].namequant",
    'spelllike special': "feature.spelllike.specialList[0].name",
    'tracked items': "feature.trackedresources.trackedresourceList[0].name",
    'tracked resource': "feature.trackedresources.trackedresourceList[0].namequant",
    'other special': "feature.otherspecials.specialList[0].name",
    'spells known': "feature.spellsknown.spellSort(0)",
    'spells memorized': "feature.spellsmemorized.spellSort(0)",
    'spell book': "feature.spellbook.spellSort(0)",
    'spell classes': "feature.spellclasses.spellClassSort(0)",
    'npc additional': "feature.npc.additional.npcinfoList[0].name\x1efeature.npc.additional.npcinfoList[0].fText",
    'npc description': "feature.npc.descriptionList[0].fText",
    'npc basics': "feature.npc.basics.npcinfoList[0].name\x1efeature.npc.basics.npcinfoList[0].fText",
    'npc basics-goal': "feature.npc.basics.goalList[0].fText",
    'npc basics-goals': "feature.npc.basics.goalList[0].fText",
    'npc basics-motivation': "feature.npc.basics.goalList[0].fText",
    'npc basics-motivations': "feature.npc.basics.goalList[0].fText",
    'npc basics-plot': "feature.npc.basics.hookList[0].fText",
    'npc basics-plots': "feature.npc.basics.hookList[0].fText",
    'npc basics-hook': "feature.npc.basics.hookList[0].fText",
    'npc basics-hooks': "feature.npc.basics.hookList[0].fText",
    'npc basics-boon': "feature.npc.basics.boonList[0].fText",
    'npc basics-boons': "feature.npc.basics.boonList[0].fText",
    'npc ecology-stats': "get_textformatch(character.find('npc'),('tactics','npcinfo'),('name','Base Statistics'))",
    'npc ecology-environment': "feature.npc.ecology.environmentList[0].fText",
    'npc ecology-organization': "feature.npc.ecology.organizationList[0].fText",
    'npc ecology-treasure': "feature.npc.ecology.treasureList[0].fText",
    'npc tactics': "feature.npc.tactics.npcinfoList[0].name\x1efeature.npc.tactics.npcinfoList[0].fText",
    'npc tactics-base': "feature.npc.tactics.basestatList[0].fText",
    'npc tactics-before': "feature.npc.tactics.beforecombatList[0].fText",
    'npc tactics-during': "feature.npc.tactics.duringcombatList[0].fText",
    'npc tactics-morale': "feature.npc.tactics.moraleList[0].fText",
    'npc history': "feature.npc.additional.historyList[0].fText",
    'npc history-goals': "feature.npc.additional.historygoalsList[0].fText",
    'npc history-goals-boons': "feature.npc.additional.historygoalsboonsList[0].fText",
    'npc personality-mannerisms': "feature.npc.additional.personalitymannerismsList[0].fText",
    'npc pc-interactions': "feature.npc.additional.pcinteractionsList[0].fText",
    'npc pc-interaction': "feature.npc.additional.pcinteractionList[0].fText",
    'npc interactions': "feature.npc.additional.interactionsList[0].fText",
    'npc interaction': "feature.npc.additional.interactionList[0].fText",
    'source book': "feature.bookinfoList[0].name",
    }
    """

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
    'typeIcon': 'feature.types.type.typeIcon', # creatrue type icon
    'image': 'images.image', # character image
    'terrainIcon':'feature.npc.ecology.environment.terrainIcon', #terrain icon
    'climateIcon': 'feature.npc.ecology.environment.climateIcon', #climate icon
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
