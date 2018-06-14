#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quiz.Category import Category


class Config:
    config = dict({
        Category.SChoice: {'answer': True, 'explanation': True},
        Category.MChoice: {'answer': True, 'explanation': True},
        Category.Glossary: {'answer': True, 'explanation': False},
        Category.TrueFalse: {'answer': True, 'explanation': True},
        Category.GapFilling: {'answer': True, 'explanation': False},
        Category.ShortAnswer: {'answer': True, 'explanation': False}
    })

    def __init__(self, obj=None):
        if obj is not None:
            for pn in obj:
                self.setConfig(pn, obj[pn])

    def setConfig(self, pn, pv, category=None):
        if pn is None:
            return

        tobj = self.config
        if category is not None:
            tobj = tobj.get(category)
            if tobj is None:
                tobj[category] = {}

        tobj[pn] = pv

    def getConfig(self, pn, category=None):
        pv = None
        if pn is None:
            return pv

        tobj = self.config
        if category is not None:
            tobj = tobj.get(category)

        if tobj is not None:
            pv = tobj.get(pn)

        return pv

    def isTrue(self, pn, category=None):
        if self.getConfig(pn, category) is True:
            return True
        else:
            return False

    def isFalse(self, pn, category=None):
        if self.getConfig(pn, category) is False:
            return True
        else:
            return False
