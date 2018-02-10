# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 05:23:12 2018

@author: steve
"""
from HeroLabStatBase import *
from HeroLabStatRender import Renderer
import pypdftk


class CSpdfRenderer(Renderer):
    """
    CSpdf uses a fillable character sheet PDF file
    and fills in the values based on the keys in the matcher.  Outputing an
    fillable PDF for each character with the values filled in.
    """

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
