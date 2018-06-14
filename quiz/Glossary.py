#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quiz.Question import Question
from quiz.Category import Category


class Glossary(Question):

    def __init__(self, stem, answer='', explanation=None):
        Question.__init__(self, Category.Glossary, stem, answer, explanation)
