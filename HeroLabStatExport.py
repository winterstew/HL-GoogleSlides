# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 17:36:15 2017

@author: steve
"""
from __future__ import print_function
import zipfile,sys
import os.path

from HeroLabStatBase import *
from HeroLabStatRender import Renderer
from HeroLabStatMatch import Matcher

ICONFILE = "icons.zip"
VERBOSITY = 1


# higher levels of VERBOSITY include all those below
# 0 = silent
# 1 = minimal per portfolio messages
# 2 = more verbose portfolio messages
# 3 = minimal per character messages
# 4 = more verbose per character messages
# 5 = dump of index xml file
# 6 = dump of everything

def main():
    global VERBOSITY
    try:
        import argparse
        #parser = argparse.ArgumentParser(parents=[tools.argparser],description="""
        parser = argparse.ArgumentParser(description="""
        This Program takes a HeroLab portfolio file as an argument.
        It then renders each character in the portfolio using the renderer
        and matcher requested.""")
        parser.add_argument('--matcher', '-M', default=None, help="matcher to use")
        parser.add_argument('--matcher-options', '-m', default=None, help="comma separated list of matcher options")
        parser.add_argument('--renderer', '-R', default=None, help="renderer to use")
        parser.add_argument('--renderer-options', '-r', default=None, help="comma separated list of renderer options")
        parser.add_argument('--verbose', '-v', action='count')
        parser.add_argument('--icons', '-i', default=ICONFILE, help="icon file which gets tied into the portfolio")
        parser.add_argument('portfolioFiles', action='append', type=lambda f:zipfile.ZipFile(f,'r'), help='HeroLab Protfolio file')
        flags = parser.parse_args()
        #flags = parser.parse_args(['C:\Users\steve\Documents\Hero Lab\portfolios\pathfinder\Ironfang Invation\old\Test Nasty.por','--icons','iconsPaizo.zip'])
        #flags = parser.parse_args(['C:\Users\steve\Documents\Hero Lab\portfolios\pathfinder\Ironfang Invation\old\Test Nasty.por','--icons','iconsPaizo.zip','-v','-v','-v','-v'])
        #flags = parser.parse_args(['C:\Users\steve\Documents\Hero Lab\portfolios\pathfinder\Ironfang Invation\old\Test Nasty.por','--icons','iconsPaizo.zip','--renderer','CSpdf','--matcher','CSpdf'])
        #flags = parser.parse_args(['C:\Users\steve\Documents\Hero Lab\portfolios\pathfinder\Ironfang Invation\old\Test Nasty.por','--icons','iconsPaizo.zip','--renderer','GoogleSlide','--renderer-options','StatBlock Template,NPC-Noncombat-Image','--matcher','GoogleSlide'])
    except ImportError:
        flags = None
    if (flags.verbose): VERBOSITY = flags.verbose

    if (flags.renderer):
        rendererModule = "from HeroLabStatRender%s import %sRenderer as Renderer\nfrom HeroLabStatRender%s import DEFAULTMATCHER" % (flags.renderer,flags.renderer,flags.renderer)
        try:
            exec rendererModule in globals(),locals()
            if hasattr(flags,'matcher') and not flags.matcher and DEFAULTMATCHER:
                flags.matcher = DEFAULTMATCHER
        except ImportError:
            print("WARNING: Module HerLabStatRender%s or class %sRenderer not found, using default" % (flags.renderer,flags.renderer))
    if (flags.matcher):
        matcherModule  = "from HeroLabStatMatch%s import %sMatcher as Matcher" % (flags.matcher,flags.matcher)
        try:
            exec matcherModule in globals(),locals()
        except ImportError:
            print("WARNING: Module HerLabStatMatch%s or global dictionaries not found, using default" % (flags.matcher))

    icons = Icons(flags.icons,verbosity=VERBOSITY)
    #icons = Icons(flags.icons,verbosity=0)
    for portfolioFile in flags.portfolioFiles:
        if VERBOSITY > 0: print ("loading portfolio '%s'" % os.path.basename(portfolioFile.filename))
        portfolio = Portfolio(portfolioFile,icons=icons,verbosity=VERBOSITY)
        for c in portfolio.characters:
            #print(c.name)
            #charFile = open("%s.txt"%c.name,'w')
            #printFeature(c,'character',toFile=charFile)
            #printFeature(c,'c')
            #charFile.close()
            #print(c.portfolio.icons.names)
            #print(c.feature.types.type.typeIcon.name)
            #if hasattr(c.feature,'npc'):
            #    if hasattr(c.feature.npc,'ecology'):
            #        if hasattr(c.feature.npc.ecology,'environment'):
            #            print(c.feature.npc.ecology.environment.fText)
            #            if hasattr(c.feature.npc.ecology.environment,'terrainIcon'):
            #                print(c.feature.npc.ecology.environment.terrainIcon.name)
            #            if hasattr(c.feature.npc.ecology.environment,'climateIcon'):
            #                print(c.feature.npc.ecology.environment.climateIcon.name)
            #print(c.feature.fAttr)
            #print(c.feature.skills.fAttr)
            #print(c.feature.skills.skillList[3].abbreviate('name',))
            #print(c.feature.skills.skillList[3].abbreviate('name',[(r'Climb','Cm')]))
            #print([(item.fTag,item.text) for item in c.feature.movement.fSub])
            #print([(item.fTag,item.name) for item in c.feature.types.fSub])
            #print([(item.fTag,item.name) for item in c.feature.subtypes.fSub])
            #if hasattr(c.feature.spellclasses,'spellclassList'):
            #    for sc in c.feature.spellclasses.spellclassList:
            #        print((sc.name,sc.maxspelllevel))
            #        if hasattr(sc,'spelllevelList'):
            #            for sl in sc.spelllevelList:
            #                print((sl.level,sl.used))
            #if hasattr(c.feature.spellclasses,'spellclass'):
            #    sc = c.feature.spellclasses.spellclass
            #    print((sc.name,sc.maxspelllevel))
            #    if hasattr(sc,'spelllevelList'):
            #        for sl in sc.spelllevelList:
            #            print((sl.level,sl.used))
            #print(c.feature.classes.summary)
            #print(c.feature.classes.abbreviate('summary'))
            #print(c.feature.movement.speed.text)
            #print(c.feature.movement.speed.abbreviate('text'))
            #print(c.feature.types.type.icon)
            #print(c.getAlignment(longForm=False))
            #print(c.getRace(longForm=True,withEthnicity=True))
            #print(c.getTemplates())
            #print(c.getSize())
            #print(c.getSizeSpace())
            #print(c.getSizeReach())
            #print(c.getDeity())
            #print(c.getChallengeRating(asList=True)[0][1])
            #print(c.getClasses(asList=False,longForm=False))
            #print(c.getFactions())
            #print(c.getFaction(1,longForm=True))
            #print(c.getTypes(modWith=string.lower))
            #print(c.getSubtypes(asList=False,longForm=False))
            #print(icons.getIcon(c.getType(modWith=string.lower),'creature type','high'))
            #print(c.getSenses(asList=True,longForm=True))
            #print(c.getSenses(asList=False,longForm=False,modWith=string.lower))
            #print(c.getAuras(asList=True,longForm=True))
            #print(c.getAuras(asList=False,longForm=False,modWith=string.lower))
            #print(c.getFavoredClasses(asList=False,longForm=False,modWith=string.lower))
            #print(c.getHealth(asList=True,longForm=True))
            #print("max %shp" % c.getTotalHP(asList=False))
            #print("%sgp as %spp, %sgp, %ssp, %scp" % c.getMoney(asList=True)[0])
            #print(c.getPersonal(asList=False))
            #print(c.getPersonalBackground(asList=False))
            #print(c.getGender(asList=False,longForm=False))
            #print(c.getLanguages(asList=False,modWith=string.lower,joinWith=", "))
            #print(c.getAttribute('intelligence',asList=True))
            #print(c.getAttributes(asList=False,longForm=False))
            #print(c.getSave('fort',asList=False))
            #print(c.getSave('ref',asList=False))
            #print(c.getSave('will',asList=True))
            #print(c.getSave('all',asList=True))
            #print(c.getSaves(asList=False,longForm=False))
            #print(c.getSpecialDefensive(asList=False,longForm=False))
            #print(c.getDR(asList=False,longForm=False))
            #print("immune-> %s" % c.getImmunities(asList=False,longForm=False))
            #print("resist-> %s"% c.getResistances(asList=False,longForm=False))
            #print("weak-> %s" % c.getWeaknesses(asList=False,longForm=False))
            #print(c.getAC(asList=False,longForm=False))
            #print(c.getPenalties(asList=False,longForm=False))
            #print(c.getACP(asList=False,longForm=False))
            #print(c.getManeuvers(asList=False,longForm=False))
            #print(c.getCMB(asList=False,longForm=False,modWith=string.lower))
            #print(c.getCMD(asList=False,longForm=False,modWith=string.lower))
            #print(c.getInitiative(asList=False,longForm=False))
            #print(c.getMovement(asList=False,longForm=False,modWith=string.capitalize))
            #print(c.getEncumbrance(asList=False,longForm=False))
            #print(c.getSkill(withRank=True))
            #print(c.getSkillAbilities(asList=False,longForm=False))
            #print(c.getFeats(asList=False,longForm=True,noProf=True))
            #print(c.getTraits(asList=False,longForm=True))
            #print(c.getDrawbacks(asList=False,longForm=False))
            #print(c.getAnimalTricks(asList=False,longForm=False))
            #print(c.getSpecialAttack(asList=True,longForm=True))
            #print('-'*10)
            sys.stdout.flush()
        #print(portfolio.characters[1].getSkill('Craft (stonemasonry)',valueOnly=True,withRank=True,atLeast=10))
        #print(portfolio.characters[1].getAlignment())
        renderer = Renderer(portfolio,flags,matcherClass=Matcher,verbosity=VERBOSITY)
        renderer.render()
        portfolio.close()
        sys.stdout.flush()
    icons.close()

if __name__ == '__main__':
    main()