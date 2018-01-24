# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 05:23:12 2018

@author: steve
"""
from HeroLabStatBase import *
from HeroLabStatRender import Renderer
import pypdftk


class CSfdfRenderer(Renderer):
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
        fieldDict = {}
        for match in [self.matcherClass(character,self.matcherClass.TEXTMATCH,'text'),
                      self.matcherClass(character,self.matcherClass.BOOLEANMATCH,'boolean')]:
            for keyText in match.getKeys():
                keyWord = re.sub(r'\.\..*$','',re.sub(r'^(h_|l_|_)','',keyText))
                fieldDict[keyWord] = match.getMatch(keyText)
        outFile="\"%s.pdf\""%character.name
        #print(pypdftk.gen_xfdf(fieldDict))
        generatedPdf = pypdftk.fill_form(pdf_path='"C:\Users\steve\Projects\HL-GoogleSlides\Character Sheet fillable.pdf"',datas=fieldDict,out_file=outFile,flatten=False)


    def endPortfolio(self,*args,**kwargs):
        pass