#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quiz.Question import Question
from quiz.Category import Category


class ShortAnswer(Question):

    def __init__(self, stem, answer="", explanation=None):
        Question.__init__(self, Category.ShortAnswer, stem, answer, explanation)
