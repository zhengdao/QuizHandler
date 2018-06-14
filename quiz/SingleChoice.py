#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quiz.Choice import Choice
from quiz.Category import Category


class SingleChoice(Choice):

    def __init__(self, stem, options=[], answer=[], explanation=None):
        Choice.__init__(self, Category.SChoice, stem, options, answer, explanation)

