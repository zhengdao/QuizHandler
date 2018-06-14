#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dep import NLSFactory
from quiz.Category import Category
from quiz.Question import Question
from quiz.Config import Config


class Choice(Question):

    def __init__(self, category, stem, options=None, answer=[], explanation=None):
        Question.__init__(self, category, stem, answer, explanation)

        if options is None:
            self.options = list()
        else:
            self.options = list(options)

    def stemToWord(self, doc, lead='', level=2, config=Config()):
        tmp = [lead, self.stem, self.getStemTail(), u'(']
        if config.isTrue('answer', self.category) and len(self.answer) > 0:
            if self.category == Category.SChoice:
                tmp.append(self.answer[0])
            else:
                tmp.append(''.join(self.answer))
        else:
            tmp.append('')

        tmp.append(')')

        doc.add_paragraph(''.join(tmp), 'h' + str(level))

    def addOption(self, option):
        self.options.append(option)

    def optionsToWord(self, doc):
        for i in range(len(self.options)):
            tmp = [chr(65 + i), ' ', self.options[i]]
            doc.add_paragraph(''.join(tmp), 'pstyle')

    def toWord(self, doc, lead='', level=2, config=Config()):
        # to stem
        self.stemToWord(doc, lead, level)

        # to options
        self.optionsToWord(doc)

        # to answer
        # if config.isTrue('answer', self.category):
        #    self.answerToWord(doc)

        # to explanation
        if config.isTrue('explanation', self.category):
            self.explanationToWord(doc)

        # Keep a blank paragraph
        doc.add_paragraph('', 'pstyle')

    def getStemTail(self):
        return u'：'

    def __str__(self):
        tmp = ['(', self.nCategory, ')', self.stem, self.getStemTail(), '\n']
        for i in range(len(self.options)):
            tmp.extend([chr(65 + i), ' ', self.options[i], '\n'])

        tmp.append('\n')
        if len(self.answer) > 0:
            if self.category == Category.SChoice:
                tmp.extend([NLSFactory.getNLSText('msgAnswer'), self.answer[0], '\n'])
            else:
                tmp.extend([NLSFactory.getNLSText('msgAnswer'), ''.join(self.answer), '\n'])
        else:
            tmp.extend([NLSFactory.getNLSText('msgAnswer'), '\n'])

        # tmp.append('\n')
        if self.explanation is None:
            tmp.extend([NLSFactory.getNLSText('msgExplanation'), '\n'])
        else:
            tmp.extend([NLSFactory.getNLSText('msgExplanation'), self.explanation, '\n'])

        return ''.join(tmp)
