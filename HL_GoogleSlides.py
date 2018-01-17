# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 17:36:15 2017

@author: steve
"""
from __future__ import print_function
import __builtin__
import httplib2
import zipfile,tempfile
import os,re,urllib,shutil,string

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from HL_GoogleSlides_BaseClasses import *

import xml.etree.cElementTree as et

TEMPLATENAME = "StatBlock Template"
PAGENAME = "NPC-Combat-"
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

class Presentation:
    """
    This Class is used to create the Google Slides presentation file based on
    a provided template Google Slide name, a page name, and a Portfolio instance.
    """
    pass

class Slide:
    """
    This Class is for creating a single page Slide instance within a Presentation
    """
    pass

class Replacer:
    """
    This Class contains the dictionary which defines keywords
    to find in the Google Slide
    and their character instance replacement methods
    """
    def __init__(self,matchDict,*args,**kwargs):
        """
        matchDict is a dictionary of textKey strings followed by an eval-able string
        to apply to a character instance which returns the replacement string
        """
        pass

    def replace(self,textKey,*args,**kwargs):
        """
        textKey is the text from the Google Slide
        which will be replaced
        """
        pass

class Icon:
    """
    Class to contain an individual icon reference which may point to one or more images

    attributes are
    name: short identifiing name
    type: type of thing to which the icon applies
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
        self.type = self.indexXml.get('type')
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
                        (image.get('folder'),image.get('filename'),self.name,self.type))
            else:
                try:
                    self.imageLow = (
                        image.get('filename'),
                        iconFile.extract("%s/%s" % (image.get('folder'),image.get('filename')),self.tempDir))
                except KeyError:
                    print("WARNING: There is no low resolution icon %s/%s for %s (%s)" %
                        (image.get('folder'),image.get('filename'),self.name,self.type))

class Icons(IconsBase):
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

        # debug printing
        for i in self.icons:
            if self.verbosity >= 3:
                print("icon #%d: %s (%s)" % (i.index,i.name,i.type))
            if self.verbosity >= 4:
                print("  images:")
                if i.imageHigh: print("    high %s: %s" % i.imageHigh)
                if i.imageLow: print("    low %s: %s" % i.imageLow)

        # close the iconFile
        self.iconFile.close()

    def close(self):
        """
        clean up temporary files and directories
        """
        shutil.rmtree(self.tempDir)

class Character(CharacterBase):
    """
    Class for a single character element from a portfolio

    attributes are:
      indexXml -> The input character element
      statText -> the read in string of the text statblock
      statHtml -> the read in string of the html statblock
      statXml -> the character element from the xml statblock
      isMinion -> True if this character is a minion
      isMinionOf -> the chracter element from the minion's parent
    """

    def __init__(self,porFile,indexCharacterElement,*args,**kwargs):
        """
        porFile is the open ziped portfolio file
        indexCharacterElement is the character element from the index.xml

        if the keyword parent= is given, then it is assumed that the character
         is a minion and its parent character index element is the value for
         this keyword
        """
        if 'verbosity' not in kwargs: kwargs['verbosity'] = VERBOSITY
        self.verbosity = kwargs['verbosity']
        self.indexXml = indexCharacterElement
        self.statText = None
        self.statHtml = None
        self.statXml = None
        self.isMinion = False
        self.parentIndexXml = None
        self.parentStatXml = None
        # assign the identifying attributes from the xml to the Character instance
        self.name = self.indexXml.get('name')
        self.summary = self.indexXml.get('summary')
        self.herolabLeadIndex = int(self.indexXml.get('herolableadindex'))
        self.characterIndex = int(self.indexXml.get('characterindex'))
        self.myIndex = self.herolabLeadIndex
        if ('parent' in kwargs and et.iselement(kwargs['parent'])):
            self.parentIndexXml = kwargs['parent']
            # for minions, myIndex is the herolableadindex of the parent
            self.myIndex = int(self.parentIndexXml.get('herolableadindex'))
            self.isMinion = True
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
            sb = self.parentIndexXml.find("./statblocks/statblock[@format='xml']")
        else:
            sb = self.indexXml.find("./statblocks/statblock[@format='xml']")
        # parse the XML file and get the statblock
        if (et.iselement(sb)):
            xmlFile = porFile.open("%s/%s" % (sb.get('folder'),sb.get('filename')))
            xml = et.parse(xmlFile)
            self.statXml = xml.find("./*/character")
            if self.isMinion:
                # the first statblock belongs to the parent
                self.isMinionOf = self.statXml
                # also extract the minion statblock specifically from the parents using the minion characterindex
                xmlPath = "./*/character/minions/character[@characterindex='%s']" % self.indexXml.get('characterindex')
                self.statXml = xml.find(xmlPath)
            xmlFile.close()
        # extract the image files and copy them to a temporary directory
        if 'tempDir' in kwargs and os.path.isdir(kwargs['tempDir']):
            self.tempDir = kwargs['tempDir']
        else:
            self.tempDir = tempfile.mkdtemp(prefix='HL-GoogleSlides-Character-')
        self.images = []
        for image in self.indexXml.findall('./images/image'):
            self.images.append((image.get('filename'),
            porFile.extract("%s/%s" % (image.get('folder'),image.get('filename')),self.tempDir)))

class Portfolio:
    """
    Class for and entire HeroLab portfolio
      porFile is either a ZipFile instance or a full path filename to the
      portfolio file
    """
    def __init__(self, porFile,*args,**kwargs):
        if 'verbosity' not in kwargs: kwargs['verbosity'] = VERBOSITY
        self.verbosity = kwargs['verbosity']
        if type(porFile) is not zipfile.ZipFile:
            porFile = zipfile.ZipFile(porFile,'r')
        if self.verbosity >= 2: print("filename: %s" % porFile.filename)
        self.porFile = porFile
        self.filename = porFile.filename
        self.filepath = os.path.split(porFile.filename)[0]
        self.filecore = os.path.splitext(os.path.basename(porFile.filename))[0]
        if self.verbosity >= 2: print("filecore: %s" % self.filecore)
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
        self.tempDir = tempfile.mkdtemp(prefix='HL-GoogleSlides-Porfolio-')
        if self.verbosity >= 2: print("Temp Image Directory: %s" % self.tempDir)
        # build up the character list creating Character instances for each
        self.characters = []
        for c in indexTree.findall('./characters/character'):
            self.characters.append(Character(self.porFile,c,*args,tempDir=self.tempDir,**kwargs))
            for m in c.findall('./minions/character'):
                self.characters.append(Character(self.porFile,m,*args,parent=c,tempDir=self.tempDir,**kwargs))

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
                if c.images: print("  Images:")
                for i in c.images:
                    print("    %s: %s" % i)

        # close the protfolio
        self.porFile.close()

    def close(self):
        """
        clean up temporary files and directories
        """
        shutil.rmtree(self.tempDir)


def main():
    global VERBOSITY
    try:
        import argparse
        parser = argparse.ArgumentParser(parents=[tools.argparser],description="""
        This Program takes a HeroLab protfolio file as an argument.
        It finds a Google Slide document named "%s" or the one provided by the --template flag
        and selects the slide based on matching the key '%s' or the --page flag.  For each character in turn
        which is part of the protfolio, it copies the Google Slide page to a the new presentation
        (named from the portfolito name) and replaces all the template keys within the page
        with approriate values from the character""" % (TEMPLATENAME,PAGENAME))
        parser.add_argument('--template', '-t', default=TEMPLATENAME, help="template presentation name")
        parser.add_argument('--page', '-p', default=PAGENAME, help="key name identifying page to use")
        parser.add_argument('--verbose', '-v', action='count')
        parser.add_argument('--icons', '-i', default=ICONFILE, help="HL-GoogleSlides icon file")
        parser.add_argument('portfolioFile', type=lambda f:zipfile.ZipFile(f,'r'), help='HeroLab Protfolio file')
        #flags = parser.parse_args()
        flags = parser.parse_args(['C:\Users\steve\Documents\Hero Lab\portfolios\pathfinder\Ironfang Invation\old\Test Nasty.por','--icons','iconsPaizo.zip'])
        #flags = parser.parse_args(['C:\Users\steve\Documents\Hero Lab\portfolios\pathfinder\Ironfang Invation\old\Test Nasty.por','--icons','iconsPaizo.zip','-v','-v','-v','-v'])
    except ImportError:
        flags = None
    if (flags.verbose): VERBOSITY = flags.verbose
    portfolio = Portfolio(flags.portfolioFile,verbosity=VERBOSITY)
    #icons = Icons(flags.icons,verbosity=VERBOSITY)
    icons = Icons(flags.icons,verbosity=0)
    for c in portfolio.characters:
        print(c.name)
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
        print(c.getSpecialAttack(asList=True,longForm=True))
        print('-'*10)
    #print(portfolio.characters[1].getSkill('Craft (stonemasonry)',valueOnly=True,withRank=True,atLeast=10))
    #print(portfolio.characters[1].getAlignment())
    portfolio.close()
    icons.close()

if __name__ == '__main__':
    main()