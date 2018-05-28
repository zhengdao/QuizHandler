#!/usr/bin/env python
# -*- coding: utf-8 -*-
from builtins import range


class Question:

    def __init__(self, category, stem, answer=None, explanation=None):
        self.category = category
        self.stem = stem
        self.answer = answer
        self.explanation = explanation

    def setAnswer(self, answer):
        self.answer = answer

    def setExplanation(self, explanation):
        self.explanation = explanation

    def toWord(self):
        pass

    def getStemTail(self):
        return ''

    def __str__(self):
        tmp = ['(', self.category, ')', self.stem, self.getStemTail(), '\n']

        if self.answer is not None:
            tmp.extend(['答案：', self.answer, '\n'])
        else:
            tmp.extend(['答案：', '\n'])

        # tmp.append('\n')
        if self.explanation is not None:
            tmp.extend(['解析：', self.explanation, '\n'])
        else:
            tmp.extend(['解析：', '\n'])

        return ''.join(tmp)

    __repr__ = __str__
