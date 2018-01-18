# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 15:41:38 2018

@author: steve
"""
# for IMAGEMATCH the result of evaluating the dictionary value
# has to provide an object with a imageHigh and imageLow attribute
# each of which holds a (filename,absFilename) tuple OR
# the result of  evaluation the dictionary value has to provide the
# tuple itself
IMAGEMATCH = {
'typeIcon': 'character.feature.types.typeList[0].typeIcon', # get icon (which has imageHigh and imageLow attributes) for filename tuple for icon matching  the creature type
'image': 'characer.image', # get the filename tuple for the  first character image
}

# for TEXTMATCH the result of evaluating the dictionary value
# should be the replacement text.  The parent Feature object of this
# attribute should also have an abbreviate function if needed
TEXTMATCH = {
'role': 'character.role', # pc, npc, etc
'align': 'character.feature.alignment.name', # alignment written out
'name': 'character.name', # character name
'summary': 'character.summary', # usually the creature's race, class, alignment abbrev, size, and creature type
'character type': 'character.type', # Hero, Arcane Familiar, Animal Commpanion, etc
'player': 'character.playername',
'racetext': 'character.feature.race.racetext', # race and ethnicity (if one)
'race': 'character.feature.race.name', # race only text
'ethnicity': 'character.feature.race.ethnicity', # ethnicity
'size': 'character.feature.size.name', # size of creature (Small, Medium, etc)
'space': 'character.feature.size.space.text', # space a creature  takes up with units
'reach': 'character.feature.size.reach.text', # space a creature threatens beyond its own square
'deity': 'character.feature.deity.name', # deity worshiped
'CR': 'character.feature.challengerating.text' # challenge rating with CR prepended
'XP': 'character.feature.xpaward.text',# XP awarded for creature (comma for thousands and XP appended)
'classes summary': 'character.feature.classes.summary', # summary list of all classes
'type': 'character.feature.types.typeList[0].name', # get first (and likely only) type
'types..': '", ".join([item.name in character.feature.types.typeList])', # combine all the creature types
'subtypes..': '", ".join([item.name in character.feature.subtypes.subtypeList])', # combine all the creature subtypes

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
'personal description':"""re.sub(r'w/  skin  hair and  eyes.  ','',
  re.sub(r'^0[^1-9][^1-9]* yr old ','',
    get_nested(character,'{{height}} {{(weight)}} {{age}} yr old w/ {{skin}} skin {{hair}} hair and {{eyes}} eyes.  {{personal}}')
  ))""",
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
