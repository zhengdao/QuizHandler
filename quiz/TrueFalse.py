#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quiz.Question import Question
from quiz.Category import Category


class TrueFalse(Question):

    def __init__(self, stem, answer=None, explanation=None):
        Question.__init__(self, Category.TrueFalse, stem, answer, explanation)
