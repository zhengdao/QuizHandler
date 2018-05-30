#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quiz.Question import Question


class TrueFalse(Question):

    def __init__(self, category, stem, answer=None, explanation=None):
        Question.__init__(self, category, stem, answer, explanation)
