#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dep import NLSFactory
from quiz.Config import Config


class Question:

    def __init__(self, category, stem, answer=None, explanation=None):
        self.category = category
        self.nCategory = self.getCategoryName()

        self.stem = stem
        self.answer = answer
        self.explanation = explanation

    def getCategory(self):
        return self.category

    def getCategoryName(self):
        return NLSFactory.getNLSText('N-' + self.category)

    def setAnswer(self, answer):
        self.answer = answer

    def setExplanation(self, explanation):
        self.explanation = explanation

    def stemToWord(self, doc, lead='', level=2, config=Config()):
        doc.add_paragraph(lead + self.stem + self.getStemTail(), 'h' + str(level))

    def answerToWord(self, doc):
        p = doc.add_paragraph()
        p.add_run(NLSFactory.getNLSText('msgAnswer'), 'ptitle')
        if self.answer is not None:
            p.add_run(self.answer, 'pcontent')

    def explanationToWord(self, doc):
        p = doc.add_paragraph()
        p.add_run(NLSFactory.getNLSText('msgExplanation'), 'ptitle')
        if self.explanation is not None:
            p.add_run(self.explanation, 'pcontent')

    def toWord(self, doc, lead='', level=2, config=Config()):
        # to stem
        self.stemToWord(doc, lead, level, config)

        # to answer
        if config.isTrue('answer', self.category):
            self.answerToWord(doc)

        # to explanation
        if config.isTrue('explanation', self.category):
            self.explanationToWord(doc)

        # Keep a blank paragraph
        doc.add_paragraph('', 'pstyle')

    def getStemTail(self):
        return ''

    def __str__(self):
        tmp = ['(', self.nCategory, ')', self.stem, self.getStemTail(), '\n']

        if self.answer is not None:
            tmp.extend([NLSFactory.getNLSText('msgAnswer'), self.answer, '\n'])
        else:
            tmp.extend([NLSFactory.getNLSText('msgAnswer'), '\n'])

        # tmp.append('\n')
        if self.explanation is not None:
            tmp.extend([NLSFactory.getNLSText('msgExplanation'), self.explanation, '\n'])
        else:
            tmp.extend([NLSFactory.getNLSText('msgExplanation'), '\n'])

        return ''.join(tmp)

    __repr__ = __str__
