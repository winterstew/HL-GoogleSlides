# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:41:38 2018

@author: steve
"""
from HeroLabStatMatch import Matcher

class CSpdfMatcher(Matcher):

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
      'Character Name':'name',
      '_Alignment':'feature.alignment.name',
      'Player':'playername',
      '_Character Level.. - ':'feature.classes.level\x1efeature.classes.summary',
      'Deity':'feature.deity.name',
      'Homeland':'feature.race.ethnicity',
      'Race.., ':'feature.raceList[0].name',
      '_Size':'feature.size.name',
      '_Gender':'feature.personal.gender',
      'Age':'feature.personal.age',
      'Height':'feature.personal.charheight.text',
      'Weight':'feature.personal.charweight.text',
      'Hair':'feature.personal.hair',
      'Eyes':'feature.personal.eyes',
      'Natural Armor':'feature.armorclass.fromnatural',
      'Deflection Modifier':'feature.armorclass.fromdeflect',
      'Total Hp':'feature.health.hitpoints',
      'Damage Reduction':'feature.damagereduction.special.shortname',
      'Wounds/Current Hp':'feature.health.currenthp',
      'Nonlethal Damage':'feature.health.nonlethal',
      'Total Armor Class':'feature.armorclass.ac',
      'Total Initiative Modifier':'feature.initiative.total',
      'Armor Bonus':'feature.armorclass.fromarmor',
      'Shield Bonus':'feature.armorclass.fromshield',
      'Dex Modifier':'feature.armorclass.fromdexterity',
      'Base Speed':'feature.movement.basespeed.text',
      'Temp modifier':'',
      'Fly Maneuverability..   ':'feature.movement.fly.text\x1efeature.movement.fly.maneuverability',
      'Swim':'feature.movement.swim.text',
      'Climb':'feature.movement.climb.text',
      'Burrow':'feature.movement.burrow.text',
      'With Armor':'feature.movement.speed.text',
      'Touch Armor Class':'character.feature.armorclass.touch',
      'Flat-Footed Armor Class':'character.feature.armorclass.flatfooted',
      'Craft 1':'feature.skills.craftList[0].subname',
      'Craft 2':'feature.skills.craftList[1].subname',
      'Craft 3':'feature.skills.craftList[2].subname',
      'Perform 1':'feature.skills.performList[0].subname',
      'Perform 2':'feature.skills.performList[1].subname',
      'Profession 1':'feature.skills.professionList[0].subname',
      'Profession 2':'feature.skills.professionList[1].subname',
      'Total Bonus 1':'feature.skills.acrobatics.text',
      'Total Bonus 2':'feature.skills.appraise.text',
      'Total Bonus 3':'feature.skills.bluff.text',
      'Total Bonus 4':'feature.skills.climb.text',
      'Total Bonus 5':'feature.skills.craftList[0].text',
      'Total Bonus 6':'feature.skills.craftList[1].text',
      'Total Bonus 7':'feature.skills.craftList[2].text',
      'Total Bonus 8':'feature.skills.diplomacy.text',
      'Total Bonus 9':'feature.skills.disableDevice.text',
      'Total Bonus 10':'feature.skills.disguise.text',
      'Total Bonus 11':'feature.skills.escapeArtist.text',
      'Total Bonus 12':'feature.skills.fly.text',
      'Total Bonus 13':'feature.skills.handleAnimal.text',
      'Total Bonus 14':'feature.skills.heal.text',
      'Total Bonus 15':'feature.skills.intimidate.text',
      'Total Bonus 16':'feature.skills.knowledgeArcana.text',
      'Total Bonus 17':'feature.skills.knowledgeDungeoneering.text',
      'Total Bonus 18':'feature.skills.knowledgeEngineering.text',
      'Total Bonus 19':'feature.skills.knowledgeGeography.text',
      'Total Bonus 20':'feature.skills.knowledgeHistory.text',
      'Total Bonus 21':'feature.skills.knowledgeLocal.text',
      'Total Bonus 22':'feature.skills.knowledgeNature.text',
      'Total Bonus 23':'feature.skills.knowledgeNobility.text',
      'Total Bonus 24':'feature.skills.knowledgePlanes.text',
      'Total Bonus 25':'feature.skills.knowledgeReligion.text',
      'Total Bonus 26':'feature.skills.linguistics.text',
      'Total Bonus 27':'feature.skills.perception.text',
      'Total Bonus 28':'feature.skills.performList[0].text',
      'Total Bonus 29':'feature.skills.performList[1].text',
      'Total Bonus 30':'feature.skills.professionList[0].text',
      'Total Bonus 31':'feature.skills.professionList[1].text',
      'Total Bonus 32':'feature.skills.ride.text',
      'Total Bonus 33':'feature.skills.senseMotive.text',
      'Total Bonus 34':'feature.skills.sleightOfHand.text',
      'Total Bonus 35':'feature.skills.spellcraft.text',
      'Total Bonus 36':'feature.skills.stealth.text',
      'Total Bonus 37':'feature.skills.survival.text',
      'Total Bonus 38':'feature.skills.swim.text',
      'Total Bonus 39':'feature.skills.useMagicDevice.text',
      'Ability Mod. 1':'feature.skills.acrobatics.attrbonus',
      'Ability Mod. 2':'feature.skills.appraise.attrbonus',
      'Ability Mod. 3':'feature.skills.bluff.attrbonus',
      'Ability Mod. 4':'feature.skills.climb.attrbonus',
      'Ability Mod. 5':'feature.skills.craftList[0].attrbonus',
      'Ability Mod. 6':'feature.skills.craftList[1].attrbonus',
      'Ability Mod. 7':'feature.skills.craftList[2].attrbonus',
      'Ability Mod. 8':'feature.skills.diplomacy.attrbonus',
      'Ability Mod. 9':'feature.skills.disableDevice.attrbonus',
      'Ability Mod. 10':'feature.skills.disguise.attrbonus',
      'Ability Mod. 11':'feature.skills.escapeArtist.attrbonus',
      'Ability Mod. 12':'feature.skills.fly.attrbonus',
      'Ability Mod. 13':'feature.skills.handleAnimal.attrbonus',
      'Ability Mod. 14':'feature.skills.heal.attrbonus',
      'Ability Mod. 15':'feature.skills.intimidate.attrbonus',
      'Ability Mod. 16':'feature.skills.knowledgeArcana.attrbonus',
      'Ability Mod. 17':'feature.skills.knowledgeDungeoneering.attrbonus',
      'Ability Mod. 18':'feature.skills.knowledgeEngineering.attrbonus',
      'Ability Mod. 19':'feature.skills.knowledgeGeography.attrbonus',
      'Ability Mod. 20':'feature.skills.knowledgeHistory.attrbonus',
      'Ability Mod. 21':'feature.skills.knowledgeLocal.attrbonus',
      'Ability Mod. 22':'feature.skills.knowledgeNature.attrbonus',
      'Ability Mod. 23':'feature.skills.knowledgeNobility.attrbonus',
      'Ability Mod. 24':'feature.skills.knowledgePlanes.attrbonus',
      'Ability Mod. 25':'feature.skills.knowledgeReligion.attrbonus',
      'Ability Mod. 26':'feature.skills.linguistics.attrbonus',
      'Ability Mod. 27':'feature.skills.perception.attrbonus',
      'Ability Mod. 28':'feature.skills.performList[0].attrbonus',
      'Ability Mod. 29':'feature.skills.performList[1].attrbonus',
      'Ability Mod. 30':'feature.skills.professionList[0].attrbonus',
      'Ability Mod. 31':'feature.skills.professionList[1].attrbonus',
      'Ability Mod. 32':'feature.skills.ride.attrbonus',
      'Ability Mod. 33':'feature.skills.senseMotive.attrbonus',
      'Ability Mod. 34':'feature.skills.sleightOfHand.attrbonus',
      'Ability Mod. 35':'feature.skills.spellcraft.attrbonus',
      'Ability Mod. 36':'feature.skills.stealth.attrbonus',
      'Ability Mod. 37':'feature.skills.survival.attrbonus',
      'Ability Mod. 38':'feature.skills.swim.attrbonus',
      'Ability Mod. 39':'feature.skills.useMagicDevice.attrbonus',
      'Ranks 1':'feature.skills.acrobatics.ranks',
      'Ranks 2':'feature.skills.appraise.ranks',
      'Ranks 3':'feature.skills.bluff.ranks',
      'Rank 4':'feature.skills.climb.ranks',
      'Rank 5':'feature.skills.craftList[0].ranks',
      'Rank 6':'feature.skills.craftList[1].ranks',
      'Rank 7':'feature.skills.craftList[2].ranks',
      'Rank 8':'feature.skills.diplomacy.ranks',
      'Rank 9':'feature.skills.disableDevice.ranks',
      'Rank 10':'feature.skills.disguise.ranks',
      'Rank 11':'feature.skills.escapeArtist.ranks',
      'Rank 12':'feature.skills.fly.ranks',
      'Rank 13':'feature.skills.handleAnimal.ranks',
      'Rank 14':'feature.skills.heal.ranks',
      'Rank 15':'feature.skills.intimidate.ranks',
      'Rank 16':'feature.skills.knowledgeArcana.ranks',
      'Rank 17':'feature.skills.knowledgeDungeoneering.ranks',
      'Rank 18':'feature.skills.knowledgeEngineering.ranks',
      'Rank 19':'feature.skills.knowledgeGeography.ranks',
      'Rank 20':'feature.skills.knowledgeHistory.ranks',
      'Rank 21':'feature.skills.knowledgeLocal.ranks',
      'Rank 22':'feature.skills.knowledgeNature.ranks',
      'Rank 23':'feature.skills.knowledgeNobility.ranks',
      'Rank 24':'feature.skills.knowledgePlanes.ranks',
      'Rank 25':'feature.skills.knowledgeReligion.ranks',
      'Rank 26':'feature.skills.linguistics.ranks',
      'Rank 27':'feature.skills.perception.ranks',
      'Rank 28':'feature.skills.performList[0].ranks',
      'Rank 29':'feature.skills.performList[1].ranks',
      'Rank 30':'feature.skills.professionList[0].ranks',
      'Rank 31':'feature.skills.professionList[1].ranks',
      'Rank 32':'feature.skills.ride.ranks',
      'Rank 33':'feature.skills.senseMotive.ranks',
      'Rank 34':'feature.skills.sleightOfHand.ranks',
      'Rank 35':'feature.skills.spellcraft.ranks',
      'Rank 36':'feature.skills.stealth.ranks',
      'Rank 37':'feature.skills.survival.ranks',
      'Rank 38':'feature.skills.swim.ranks',
      'Rank 39':'feature.skills.useMagicDevice.ranks',
      'Misc Mod. 1':'',
      'Misc Mod. 2':'',
      'Misc Mod. 3':'',
      'Misc Mod. 4':'',
      'Misc Mod. 5':'',
      'Misc Mod. 6':'',
      'Misc Mod. 7':'',
      'Misc Mod. 8':'',
      'Misc Mod. 9':'',
      'Misc Mod. 10':'',
      'Misc Mod. 11':'',
      'Misc Mod. 12':'',
      'Misc Mod. 13':'',
      'Misc Mod. 14':'',
      'Misc Mod. 15':'',
      'Misc Mod. 16':'',
      'Misc Mod. 17':'',
      'Misc Mod. 18':'',
      'Misc Mod. 19':'',
      'Misc Mod. 20':'',
      'Misc Mod. 21':'',
      'Misc Mod. 22':'',
      'Misc Mod. 23':'',
      'Misc Mod. 24':'',
      'Misc Mod. 25':'',
      'Misc Mod. 26':'',
      'Misc Mod. 27':'',
      'Misc Mod. 28':'',
      'Misc Mod. 29':'',
      'Misc Mod. 30':'',
      'Misc Mod. 31':'',
      'Misc Mod. 32':'',
      'Misc Mod. 33':'',
      'Misc Mod. 34':'',
      'Misc Mod. 35':'',
      'Misc Mod. 36':'',
      'Misc Mod. 37':'',
      'Misc Mod. 38':'',
      'Misc Mod. 39':'',
      'Weapon Name Slot 1':'feature.melee.weaponList[0].name',
      'Attack Bonus slot 1':'feature.melee.weaponList[0].attack',
      'Critical Slot 1':'feature.melee.weaponList[0].crit',
      'Type Slot 1':'feature.melee.weaponList[0].typetext',
      'Range slot 1':'feature.melee.weaponList[0].rangedattack.attack\x1efeature.melee.weaponList[0].rangedattack.rangeinctext',
      'Ammunition Slot 1':'',
      'Damage Slot 1':'feature.melee.weaponList[0].damage',
      'Weapon Name Slot 2':'feature.melee.weaponList[1].name',
      'Attack Bonus slot 2':'feature.melee.weaponList[1].attack',
      'Critical Slot 2':'feature.melee.weaponList[1].crit',
      'Type Slot 2':'feature.melee.weaponList[1].typetext',
      'Range slot 2':'feature.melee.weaponList[1].rangedattack.attack\x1efeature.melee.weaponList[0].rangedattack.rangeinctext',
      'Ammunition Slot 2':'',
      'Damage Slot 2':'feature.melee.weaponList[1].damage',
      'Weapon Name Slot 3':'feature.melee.weaponList[2].name',
      'Attack Bonus slot 3':'feature.melee.weaponList[2].attack',
      'Critical Slot 3':'feature.melee.weaponList[2].crit',
      'Type Slot 3':'feature.melee.weaponList[2].typetext',
      'Range slot 3':'feature.melee.weaponList[2].rangedattack.attack\x1efeature.melee.weaponList[0].rangedattack.rangeinctext',
      'Ammunition Slot 3':'',
      'Damage Slot 3':'feature.melee.weaponList[2].damage',
      'Weapon Name Slot 4':'feature.ranged.weaponList[0].name',
      'Attack Bonus slot 4':'feature.ranged.weaponList[0].rangedattack.attack',
      'Critical Slot 4':'feature.ranged.weaponList[0].crit',
      'Type Slot 4':'feature.ranged.weaponList[0].typetext',
      'Range slot 4':'feature.ranged.weaponList[0].rangedattack.rangeinctext',
      'Ammunition Slot 4':'',
      'Damage Slot 4':'feature.ranged.weaponList[0].damage',
      'Weapon Name Slot 5':'feature.ranged.weaponList[1].name',
      'Attack Bonus slot 5':'feature.ranged.weaponList[1].attack',
      'Critical Slot 5':'feature.ranged.weaponList[1].crit',
      'Type Slot 5':'feature.ranged.weaponList[1].typetext',
      'Range slot 5':'feature.ranged.weaponList[1].rangedattack.rangeinctext',
      'Ammunition Slot 5':'',
      'Damage Slot 5':'feature.ranged.weaponList[1].damage',
      'Conditional Modifiers Line 1':'',
      'Conditional Modifiers Line 2':'',
      'Conditional Modifiers Line 3':'',
      'Languages Line 1':'feature.languages.languageList[0].name\x1efeature.languages.languageList[1].name\x1e.feature.languages.languageList[3].name\x1e.feature.languages.languageList[4].name',
      'Languages Line 2':'feature.languages.languageList[5].name\x1efeature.languages.languageList[6].name\x1e.feature.languages.languageList[7].name\x1e.feature.languages.languageList[8].name',
      'Languages Line 3':'feature.languages.languageList[9].name\x1efeature.languages.languageList[10].name\x1e.feature.languages.languageList[11].name\x1e.feature.languages.languageList[12].name',
      'Total Fortitude Save':'feature.saves.fortitudeSave.save',
      'Base Save Fortitude':'feature.saves.fortitudeSave.base',
      'Magic Modifier Fortitude':'feature.saves.fortitudeSave.fromresist',
      'Misc Modifier Fortitude':'feature.saves.fortitudeSave.frommisc',
      'Temporary Modifier Fortitude':'',
      'Total Reflex Save':'feature.saves.reflexSave.save',
      'Base Save Reflex':'feature.saves.reflexSave.base',
      'Magic Modifier Reflex':'feature.saves.reflexSave.fromresist',
      'Misc Modifier Reflex':'feature.saves.reflexSave.frommisc',
      'Temporary Modifier Reflex':'',
      'Total Will save':'feature.saves.willSave.save',
      'Base SaveWill':'feature.saves.willSave.base',
      'Magic Modifier Will':'feature.saves.willSave.fromresist',
      'Misc Modifier Will':'feature.saves.willSave.frommisc',
      'Temporary Modifier Will':'',
      'Spell Resistance':'feature.resistances.specialList[0].type == spells\x1dfeature.resistances.specialList[0].value',
      'Total CMB':'feature.maneuvers.cmb',
      'Total CMD':'feature.maneuvers.cmd',
      'Size Modifier':'',
      'Ability Score Dexterity':'feature.attributes.dexterity.attrvalue.base',
      'Ability Modifier Dexterity':'feature.attributes.dexterity.attrbonus.modified',
      'Temp Adjustment Dexterity':'feature.attributes.dexterity.attrvalue.base',
      'Temp Modifier Dexterity':'feature.attributes.dexterity.attrbonus.modified',
      'Ability Score Strength':'feature.attributes.strength.attrvalue.base',
      'Ability Modifier Strength':'feature.attributes.strength.attrbonus.modified',
      'Temp Adjustment Strength':'feature.attributes.strength.attrvalue.base',
      'Temp Modifier Strength':'feature.attributes.strength.attrbonus.modified',
      'Ability Score Constitution':'feature.attributes.constitution.attrvalue.base',
      'Ability Modifier Constitution':'feature.attributes.constitution.attrbonus.modified',
      'Temp Adjustment Constitution':'feature.attributes.constitution.attrvalue.base',
      'Temp Modifier Constitution':'feature.attributes.constitution.attrbonus.modified',
      'Ability Score Intelligence':'feature.attributes.intelligence.attrvalue.base',
      'Ability Modifier Intelligence':'feature.attributes.intelligence.attrbonus.modified',
      'Temp Adjustment Intelligence':'feature.attributes.intelligence.attrvalue.base',
      'Temp Modifier Intelligence':'feature.attributes.intelligence.attrbonus.modified',
      'Ability Score Wisdom':'feature.attributes.wisdom.attrvalue.base',
      'Ability Modifier Wisdom':'feature.attributes.wisdom.attrbonus.modified',
      'Temp Adjustment Wisdom':'feature.attributes.wisdom.attrvalue.base',
      'Temp Modifier Wisdom':'feature.attributes.wisdom.attrbonus.modified',
      'Ability Score Charisma':'feature.attributes.charisma.attrvalue.base',
      'Ability Modifier Charisma':'feature.attributes.charisma.attrbonus.modified',
      'Temp Adjustment Charisma':'feature.attributes.charisma.attrvalue.base',
      'Temp Modifier Charisma':'feature.attributes.charisma.attrbonus.modified',
      'Con Modifier':'feature.attributes.constitution.attrbonus.modified',
      'Wis Modifier':'feature.attributes.wisdom.attrbonus.modified',
      'Saving Throw Modifiers':'',
      'Str Modifier':'feature.attributes.strength.attrbonus.modified',
      'Base Attack Bonus':'feature.attack.baseattack',
      'CMB/CMD Modifiers':'',
      'Modifiers':'',
      'Initiative Misc Modifier':'',
      'AC Misc Modifier':'',
      'AC Items Slot 1':'',
      'AC Items Slot 3':'',
      'AC Items Slot 2':'',
      'AC Items Slot 4':'',
      'AC Items Slot 5':'',
      'Bonus 1':'',
      'Bonus 2':'',
      'Bonus 3':'',
      'Bonus 4':'',
      'Bonus 5':'',
      'Type 1':'',
      'Type 2':'',
      'Type 3':'',
      'Type 4':'',
      'Type 5':'',
      'Check Penalty 1':'',
      'Check Penalty 2':'',
      'Check Penalty 3':'',
      'Check Penalty 4':'',
      'Check Penalty 5':'',
      'Spell Failure 1':'',
      'Spell Failure 2':'',
      'Spell Failure 3':'',
      'Spell Failure 4':'',
      'Spell Failure 5':'',
      'Weight 1':'',
      'Weight 2':'',
      'Weight 3':'',
      'Weight 4':'',
      'Weight 5':'',
      'Properties 1':'',
      'Properties 2':'',
      'Properties 3':'',
      'Properties 4':'',
      'Properties 5':'',
      'Bonus Total':'',
      'Type Total':'',
      'Check Penalty Total':'',
      'Spell Failure Total':'',
      'Weight Total':'',
      'Properties Total':'',
      'Item 1':'',
      'Item 2':'',
      'Item 3':'',
      'Item 4':'',
      'Item 5':'',
      'Item 6':'',
      'Item 7':'',
      'Item 8':'',
      'Item 9':'',
      'Item 10':'',
      'Item 11':'',
      'Item 12':'',
      'Item 13':'',
      'Item 14':'',
      'Item 15':'',
      'Item 16':'',
      'Item 17':'',
      'Item 18':'',
      'Item 19':'',
      'Item 20':'',
      'Item 21':'',
      'Item 22':'',
      'Item 23':'',
      'Item 24':'',
      'Item 25':'',
      'Item 26':'',
      'WT. 1':'',
      'WT. 2':'',
      'WT. 3':'',
      'WT. 4':'',
      'WT. 5':'',
      'WT. 6':'',
      'WT. 7':'',
      'WT. 8':'',
      'WT. 9':'',
      'WT. 10':'',
      'WT. 11':'',
      'WT. 12':'',
      'WT. 13':'',
      'WT. 14':'',
      'WT. 15':'',
      'WT. 16':'',
      'WT. 17':'',
      'WT. 18':'',
      'WT. 19':'',
      'WT. 20':'',
      'WT. 21':'',
      'WT. 22':'',
      'WT. 23':'',
      'WT. 24':'',
      'WT. 25':'',
      'WT. 26':'',
      'Total WT':'',
      'Light Load':'',
      'Medium Load':'',
      'Heavy Load':'',
      'Lift Over Head':'',
      'Lift Off Ground':'',
      'Drag or Push':'',
      'Copper':'',
      'Silver':'',
      'Gold':'',
      'Platinum':'',
      'Second Class Experience Points':'',
      'First Class Experience Points':'',
      'First Class Next Level':'',
      'Second Class Next Level':'',
      'Feat 1':'',
      'Feat 2':'',
      'Feat 3':'',
      'Feat 4':'',
      'Feat 5':'',
      'Feat 6':'',
      'Feat 7':'',
      'Feat 8':'',
      'Feat 9':'',
      'Feat 10':'',
      'Feat 11':'',
      'Feat 12':'',
      'Feat 13':'',
      'Special Abilities 1':'',
      'Special Abilities 2':'',
      'Special Abilities 3':'',
      'Special Abilities 4':'',
      'Special Abilities 5':'',
      'Special Abilities 6':'',
      'Special Abilities 7':'',
      'Special Abilities 8':'',
      'Special Abilities 9':'',
      'Special Abilities 10':'',
      'Special Abilities 11':'',
      'Special Abilities 12':'',
      'Special Abilities 13':'',
      'Special Abilities 14':'',
      'Special Abilities 15':'',
      'Special Abilities 16':'',
      'Special Abilities 17':'',
      'Special Abilities 18':'',
      'Special Abilities 19':'',
      'Special Abilities 20':'',
      'Spells Known Level 0':'',
      'Spells Known Level 1':'',
      'Spells Known Level 2':'',
      'Spells Known Level 3':'',
      'Spells Known Level 4':'',
      'Spells Known Level 5':'',
      'Spells Known Level 6':'',
      'Spells Known Level 7':'',
      'Spells Known Level 8':'',
      'Spells Known Level 9':'',
      'Spell Save DC level 0':'',
      'Spell Save DC level 1':'',
      'Spell Save DC level 2':'',
      'Spell Save DC level 3':'',
      'Spell Save DC level 4':'',
      'Spell Save DC level 5':'',
      'Spell Save DC level 6':'',
      'Spell Save DC level 7':'',
      'Spell Save DC level 8':'',
      'Spell Save DC level 9':'',
      'Spells Per Day Level 0':'',
      'Spells Per Day Level 1':'',
      'Spells Per Day Level 2':'',
      'Spells Per Day Level 3':'',
      'Spells Per Day Level 4':'',
      'Spells Per Day Level 5':'',
      'Spells Per Day Level 6':'',
      'Spells Per Day Level 7':'',
      'Spells Per Day Level 8':'',
      'Spells Per Day Level 9':'',
      'Bonus Spells Level 1':'',
      'Bonus Spells Level 2':'',
      'Bonus Spells Level 3':'',
      'Bonus Spells Level 4':'',
      'Bonus Spells Level 5':'',
      'Bonus Spells Level 6':'',
      'Bonus Spells Level 7':'',
      'Bonus Spells Level 8':'',
      'Bonus Spells Level 9':'',
      'Conditional Modifiers':'',
      'Domains/Specialty School':'',
      'Spell Name Level 0 ~1':'',
      'Spell Name Level 0 ~2':'',
      'Spell Name Level 0 ~3':'',
      'Spell Name Level 0 ~4':'',
      'Spell Name Level 0 ~5':'',
      'Spell Name Level 0 ~6':'',
      'Spell Name Level 0 ~7':'',
      'Spell Name Level 0 ~8':'',
      'Spell Name Level 1 ~1':'',
      'Spell Name Level 1 ~2':'',
      'Spell Name Level 1 ~3':'',
      'Spell Name Level 1 ~4':'',
      'Spell Name Level 1 ~5':'',
      'Spell Name Level 1 ~6':'',
      'Spell Name Level 1 ~7':'',
      'Spell Name Level 1 ~8':'',
      'Spell Name Level 2 ~1':'',
      'Spell Name Level 2 ~2':'',
      'Spell Name Level 2 ~3':'',
      'Spell Name Level 2 ~4':'',
      'Spell Name Level 2 ~5':'',
      'Spell Name Level 2 ~6':'',
      'Spell Name Level 2 ~7':'',
      'Spell Name Level 3 ~1':'',
      'Spell Name Level 3 ~2':'',
      'Spell Name Level 3 ~3':'',
      'Spell Name Level 3 ~4':'',
      'Spell Name Level 3 ~5':'',
      'Spell Name Level 3 ~6':'',
      'Spell Name Level 4 ~1':'',
      'Spell Name Level 4 ~2':'',
      'Spell Name Level 4 ~3':'',
      'Spell Name Level 4 ~4':'',
      'Spell Name Level 4 ~5':'',
      'Spell Name Level 5 ~1':'',
      'Spell Name Level 5 ~2':'',
      'Spell Name Level 5 ~3':'',
      'Spell Name Level 5 ~4':'',
      'Spell Name Level 6 ~1':'',
      'Spell Name Level 6 ~2':'',
      'Spell Name Level 6 ~3':'',
      'Spell Name Level 6 ~4':'',
      'Spell Name Level 7 ~1':'',
      'Spell Name Level 7 ~2':'',
      'Spell Name Level 7 ~3':'',
      'Spell Name Level 7 ~4':'',
      'Spell Name Level 8 ~1':'',
      'Spell Name Level 8 ~2':'',
      'Spell Name Level 8 ~3':'',
      'Spell Name Level 9 ~1':'',
      'Spell Name Level 9 ~2':'',
      'Spell Name Level 9 ~3':'',
      'Spell Name Level 9 ~4':'',
      'Spell Name Level 9 ~5':'',
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
      'Acrobatics':'feature.skills.acrobatics.classskill',
      'Survival':'feature.skills.survival.classskill',
      'Craft Check 1':'feature.skills.craftList[0].classskill',
      'Craft Check 2':'feature.skills.craftList[1].classskill',
      'Craft Check3':'feature.skills.craftList[2].classskill',
      'Appraise Check':'feature.skills.fly.classskill',
      'Bluff Check':'feature.skills.bluff.classskill',
      'Climb check':'feature.skills.climb.classskill',
      'Diplomacy Check':'feature.skills.diplomacy.classskill',
      'Disable Device Check':'feature.skills.disableDevice.classskill',
      'Disguise Check':'feature.skills.disguise.classskill',
      'Escape Artist Check':'feature.skills.escapeArtist.classskill',
      'Fly Check':'feature.skills.fly.classskill',
      'Handle Animal Check':'feature.skills.handleAnimal.classskill',
      'Heal Check':'feature.skills.heal.classskill',
      'Intimidate Check':'feature.skills.intimidate.classskill',
      'Knowledge (Arcana) Check':'feature.skills.knowledgeArcana.classskill',
      'Knowledge (Dungeoneering) Check':'feature.skills.knowledgeDungeoneering.classskill',
      'Knowledge (Engineering) Check':'feature.skills.knowledgeEngineering.classskill',
      'Knowledge (Geography) Check':'feature.skills.knowledgeGeography.classskill',
      'Knowledge (History) Check':'feature.skills.knowledgeHistory.classskill',
      'Knowledge (Local) Check':'feature.skills.knowledgeLocal.classskill',
      'Knowledge (Nature) Check':'feature.skills.knowledgeNature.classskill',
      'Knowledge (Nobility) Check':'feature.skills.knowledgeNobility.classskill',
      'Knowledge (Planes) Check':'feature.skills.knowledgePlanes.classskill',
      'Knowledge (Religion) Check':'feature.skills.knowledgeReligion.classskill',
      'Linguistics Check':'feature.skills.linguistics.classskill',
      'Perception Check':'feature.skills.perception.classskill',
      'Perform 1 check':'feature.skills.performList[0].classskill',
      'Perform 2 Check':'feature.skills.performList[1].classskill',
      'Profession 1 Check':'feature.skills.professionList[0].classskill',
      'Profession 3 Check':'feature.skills.professionList[1].classskill',
      'Ride Check':'feature.skills.ride.classskill',
      'Sense Motive Check':'feature.skills.senseMotive.classskill',
      'Sleight Of Hand Check':'feature.skills.sleightOfHand.classskill',
      'SpellCraft Check':'feature.skills.spellcraft.classskill',
      'Stealth Check':'feature.skills.stealth.classskill',
      'Swim Check':'feature.skills.swim.classskill',
      'Use Magic Device Check':'feature.skills.useMagicDevice.classskill',
      'Spells Known Check Box Level 0 ~1':'',
      'Spells Known Check Box Level 0 ~2':'',
      'Spells Known Check Box Level 0 ~3':'',
      'Spells Known Check Box Level 0 ~4':'',
      'Spells Known Check Box Level 0 ~5':'',
      'Spells Known Check Box Level 0 ~6':'',
      'Spells Known Check Box Level 0 ~7':'',
      'Spells Known Check Box Level 0 ~8':'',
      'Spells Known Check Box Level 0 ~9':'',
      'Spells Known Check Box Level 1 ~1':'',
      'Spells Known Check Box Level 1 ~2':'',
      'Spells Known Check Box Level 1 ~3':'',
      'Spells Known Check Box Level 1 ~4':'',
      'Spells Known Check Box Level 1 ~5':'',
      'Spells Known Check Box Level 1 ~6':'',
      'Spells Known Check Box Level 1 ~7':'',
      'Spells Known Check Box Level 1 ~8':'',
      'Spells Known Check Box Level 1 ~9':'',
      'Spells Known Check Box Level 2 ~1':'',
      'Spells Known Check Box Level 2 ~2':'',
      'Spells Known Check Box Level 2 ~3':'',
      'Spells Known Check Box Level 2 ~4':'',
      'Spells Known Check Box Level 2 ~5':'',
      'Spells Known Check Box Level 2 ~6':'',
      'Spells Known Check Box Level 2 ~7':'',
      'Spells Known Check Box Level 2 ~8':'',
      'Spells Known Check Box Level 2 ~9':'',
      'Spells Known Check Box Level 3 ~1':'',
      'Spells Known Check Box Level 3 ~2':'',
      'Spells Known Check Box Level 3 ~3':'',
      'Spells Known Check Box Level 3 ~4':'',
      'Spells Known Check Box Level 3 ~5':'',
      'Spells Known Check Box Level 3 ~6':'',
      'Spells Known Check Box Level 3 ~7':'',
      'Spells Known Check Box Level 3 ~8':'',
      'Spells Known Check Box Level 3 ~9':'',
      'Spells Known Check Box Level 4 ~1':'',
      'Spells Known Check Box Level 4 ~2':'',
      'Spells Known Check Box Level 4 ~3':'',
      'Spells Known Check Box Level 4 ~4':'',
      'Spells Known Check Box Level 4 ~5':'',
      'Spells Known Check Box Level 4 ~6':'',
      'Spells Known Check Box Level 4 ~7':'',
      'Spells Known Check Box Level 4 ~8':'',
      'Spells Known Check Box Level 4 ~9':'',
      'Spells Known Check Box Level 5 ~1':'',
      'Spells Known Check Box Level 5 ~2':'',
      'Spells Known Check Box Level 5 ~3':'',
      'Spells Known Check Box Level 5 ~4':'',
      'Spells Known Check Box Level 5 ~5':'',
      'Spells Known Check Box Level 5 ~6':'',
      'Spells Known Check Box Level 5 ~7':'',
      'Spells Known Check Box Level 5 ~8':'',
      'Spells Known Check Box Level 5 ~9':'',
      'Spells Known Check Box Level 6 ~1':'',
      'Spells Known Check Box Level 6 ~2':'',
      'Spells Known Check Box Level 6 ~3':'',
      'Spells Known Check Box Level 6 ~4':'',
      'Spells Known Check Box Level 6 ~5':'',
      'Spells Known Check Box Level 6 ~6':'',
      'Spells Known Check Box Level 6 ~7':'',
      'Spells Known Check Box Level 6 ~8':'',
      'Spells Known Check Box Level 6 ~9':'',
      'Spells Known Check Box Level 7 ~1':'',
      'Spells Known Check Box Level 7 ~2':'',
      'Spells Known Check Box Level 7 ~3':'',
      'Spells Known Check Box Level 7 ~4':'',
      'Spells Known Check Box Level 7 ~5':'',
      'Spells Known Check Box Level 7 ~6':'',
      'Spells Known Check Box Level 7 ~7':'',
      'Spells Known Check Box Level 7 ~8':'',
      'Spells Known Check Box Level 7 ~9':'',
      'Spells Known Check Box Level 8 ~1':'',
      'Spells Known Check Box Level 8 ~2':'',
      'Spells Known Check Box Level 8 ~3':'',
      'Spells Known Check Box Level 8 ~4':'',
      'Spells Known Check Box Level 8 ~5':'',
      'Spells Known Check Box Level 8 ~6':'',
      'Spells Known Check Box Level 8 ~7':'',
      'Spells Known Check Box Level 8 ~8':'',
      'Spells Known Check Box Level 8 ~9':'',
      'Spells Known Check Box Level 9 ~1':'',
      'Spells Known Check Box Level 9 ~2':'',
      'Spells Known Check Box Level 9 ~3':'',
      'Spells Known Check Box Level 9 ~4':'',
      'Spells Known Check Box Level 9 ~5':'',
      'Spells Known Check Box Level 9 ~6':'',
      'Spells Known Check Box Level 9 ~7':'',
      'Spells Known Check Box Level 9 ~8':'',
      'Spells Known Check Box Level 9 ~9':'',
    }
    _booleanDict = {
      'yes':'Yes',
      'no':'',
      'true':'Yes',
      'false':'',
      'on':'Yes',
      'off':'',
    }
