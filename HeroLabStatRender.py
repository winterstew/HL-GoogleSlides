# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 05:23:12 2018

@author: steve
"""
from HeroLabStatBase import *

class Renderer(object):
    """
    A Renderer takes a Portfolio and the Character and creates the output
    document from either a template and the Matcher or just based on the
    Matcher keywords alone.

    Methods:
      startPortfolio: issued after creating a Portfolio object to start rendering
      eachCharacter
      endPortfolio

    Attributes:

    """
    def __init__(self,portfolio,matcherClass,*args,**kwargs):
        self.portfolio = portfolio
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