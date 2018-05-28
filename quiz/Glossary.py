#!/usr/bin/env python
# -*- coding: utf-8 -*-
from quiz.GapFilling import GapFilling
from quiz.Question import Question


class Glossary(Question):

    def __init__(self, category, stem, answer='', explanation=None):
        Question.__init__(self, category, stem, answer, explanation)

    def toWord(self):
        pass
