# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 05:23:12 2018

@author: steve
"""
from HeroLabStatBase import *

class Renderer(object):
    """
    A Renderer takes a Portfolio and the Character and creates the output
    document by calling render.  This can use just the Renderer, the
    same with a matcher created from the matcherClass, or both with an
    additional template file.

    Methods:
      render: render the portfolio and all its characters
      startPortfolio: run once as start of render for the portfolio
      eachCharacter: run for each character in the portfolio
      endPortfolio: run once at end of render for the portfolio

    Attributes:
      portfolio (Portfolio): portfolio to render
      matcherClass (Class): class to use when creating matcher

    """
    def __init__(self,portfolio,flags,matcherClass,*args,**kwargs):
        if 'verbosity' not in kwargs: kwargs['verbosity'] = VERBOSITY
        self.verbosity = kwargs['verbosity']
        self.flags = flags
        self.portfolio = portfolio
        self.options = hasattr(flags,'renderer_options') and flags.renderer_options and flags.renderer_options.split(",") or []
        self.matcherClass = matcherClass

    def render(self,*args,**kwargs):
        self.startPortfolio()
        for c in self.portfolio.characters:
            self.eachCharacter(c)
        self.endPortfolio()

    def startPortfolio(self,*args,**kwargs):
        pass

    def eachCharacter(self,character,*args,**kwargs):
        charFile = open("%s.txt" % character.name,'w')
        printOmit = PRINTOMIT[:]
        #del printOmit[printOmit.index('fText')]
        printFeature(character,'character',toFile=charFile,printOmit=printOmit)
        #printFeature(c,'c')
        charFile.close()

    def endPortfolio(self,*args,**kwargs):
        pass