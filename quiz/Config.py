#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config:
    config = dict({'answer': True, 'explanation': False})

    def __init__(self, obj=None):
        if obj is not None:
            for pn in obj:
                self.setConfig(pn, obj[pn])

    def setConfig(self, pn, pv):
        if pn is not None:
            self.config[pn] = pv

    def getConfig(self, pn):
        return self.config[pn]

    def isTrue(self, pn):
        if self.getConfig(pn) is True:
            return True
        else:
            return False
