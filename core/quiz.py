#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
core.core
~~~~~~~~~~~~~~~~~~

This module define all question categories.

"""
import re
from core import nls


class Category:
    Question = 'Question'
    SChoice = 'SChoice'
    MChoice = 'MChoice'
    Glossary = 'Glossary'
    TrueFalse = 'TrueFalse'
    GapFilling = 'GapFilling'
    ShortAnswer = 'ShortAnswer'


class Config:
    """
    Define the configuration for QizPaper parser and output.
    """
    config = dict({
        Category.SChoice: {'answer': True, 'explanation': True},
        Category.MChoice: {'answer': True, 'explanation': True},
        Category.Glossary: {'answer': True, 'explanation': False},
        Category.TrueFalse: {'answer': True, 'explanation': True},
        Category.GapFilling: {'answer': True, 'explanation': False},
        Category.ShortAnswer: {'answer': True, 'explanation': False}
    })

    def __init__(self, obj=None):
        if obj is not None:
            for pn in obj:
                self.setConfig(pn, obj[pn])

    def setConfig(self, pn, pv, category=None):
        if pn is None:
            return

        tobj = self.config
        if category is not None:
            tobj = tobj.get(category)
            if tobj is None:
                tobj[category] = {}

        tobj[pn] = pv

    def getConfig(self, pn, category=None):
        pv = None
        if pn is None:
            return pv

        tobj = self.config
        if category is not None:
            tobj = tobj.get(category)

        if tobj is not None:
            pv = tobj.get(pn)

        return pv

    def isTrue(self, pn, category=None):
        if self.getConfig(pn, category) is True:
            return True
        else:
            return False

    def isFalse(self, pn, category=None):
        if self.getConfig(pn, category) is False:
            return True
        else:
            return False


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
        return nls.getNLSText('N-' + self.category)

    def setAnswer(self, answer):
        self.answer = answer

    def setExplanation(self, explanation):
        self.explanation = explanation

    def stemToWord(self, doc, lead='', level=2, config=Config()):
        doc.add_paragraph(lead + self.stem + self.getStemTail(),
                          'h' + str(level))

    def answerToWord(self, doc):
        p = doc.add_paragraph()
        p.add_run(nls.getNLSText('msgAnswer'), 'ptitle')
        if self.answer is not None:
            p.add_run(self.answer, 'pcontent')

    def explanationToWord(self, doc):
        p = doc.add_paragraph()
        p.add_run(nls.getNLSText('msgExplanation'), 'ptitle')
        if self.explanation is not None:
            p.add_run(self.explanation, 'pcontent')

    def toword(self, doc, lead='', level=2, config=Config()):
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
            tmp.extend([nls.getNLSText('msgAnswer'), self.answer, '\n'])
        else:
            tmp.extend([nls.getNLSText('msgAnswer'), '\n'])

        # tmp.append('\n')
        if self.explanation is not None:
            tmp.extend(
                [nls.getNLSText('msgExplanation'), self.explanation,
                 '\n'])
        else:
            tmp.extend([nls.getNLSText('msgExplanation'), '\n'])

        return ''.join(tmp)

    __repr__ = __str__


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

    def toword(self, doc, lead='', level=2, config=Config()):
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
                tmp.extend([nls.getNLSText('msgAnswer'), self.answer[0], '\n'])
            else:
                tmp.extend([nls.getNLSText('msgAnswer'), ''.join(self.answer), '\n'])
        else:
            tmp.extend([nls.getNLSText('msgAnswer'), '\n'])

        # tmp.append('\n')
        if self.explanation is None:
            tmp.extend([nls.getNLSText('msgExplanation'), '\n'])
        else:
            tmp.extend([nls.getNLSText('msgExplanation'), self.explanation, '\n'])

        return ''.join(tmp)


class SingleChoice(Choice):

    def __init__(self, stem, options=[], answer=[], explanation=None):
        Choice.__init__(self, Category.SChoice, stem, options, answer, explanation)


class MultipleChoice(Choice):

    def __init__(self, stem, options=[], answer=[], explanation=None):
        Choice.__init__(self, Category.SChoice, stem, options, answer, explanation)


class TrueFalse(Question):

    def __init__(self, stem, answer=None, explanation=None):
        Question.__init__(self, Category.TrueFalse, stem, answer, explanation)


class GapFilling(Question):
    rPidx = re.compile(r'\(\)')

    @staticmethod
    def getPosIdx(idx):
        return chr(97 + idx)

    def __init__(self, stem, answer=[], explanation=None):
        Question.__init__(self, Category.GapFilling, stem, answer, explanation)

        self.rstStem = None

    def setAnswer(self, i, v):
        self.answer[i] = v

    def getAnswer(self, i):
        rst = None
        if i < len(self.answer):
            rst = self.answer[i]

        return rst

    def makeupStem(self, fillWithAnswer=False):
        if self.rstStem is None:
            frags = self.rPidx.split(self.stem)
            cnt = len(frags)
            tmp = []
            for i in range(cnt):
                tmp.append(frags[i])

                if i < cnt - 1:
                    if fillWithAnswer is True:
                        txt = self.getAnswer(i)
                    else:
                        # txt = self.getPosIdx(i)
                        txt = ''

                    if txt is None:
                        txt = ''

                    tmp.extend(['(', txt, ')'])

            self.rstStem = ''.join(tmp)

        return self.rstStem

    def stemToWord(self, doc, lead='', level=2, config=Config()):
        stem = self.stem
        if config.isTrue('answer', self.category):
            stem = self.makeupStem(True)

        doc.add_paragraph(lead + stem + self.getStemTail(), 'h' + str(level))

    def answerToWord2(self, doc):
        tmp = []
        for i in range(len(self.answer)):
            tmp.extend([self.getPosIdx(i), ' ', self.answer[i], '\t'])

        p = doc.add_paragraph()
        p.add_run(nls.getNLSText('msgAnswer'), 'ptitle')
        p.add_run(''.join(tmp), 'pcontent')

        # Keep a blank paragraph
        doc.add_paragraph('', 'pstyle')

    def __str__(self):
        stem = self.makeupStem(True)
        tmp = ['(', self.nCategory, ')', stem, self.getStemTail(), '\n']

        # tmp.extend([nls.getNLSText('msgAnswer'), '\n'])
        # for i in range(len(self.answer)):
        #    tmp.extend([self.getPosIdx(i), ' ', self.answer[i], '\t'])

        if self.explanation is None:
            tmp.extend([nls.getNLSText('msgExplanation'), '\n'])
        else:
            tmp.extend([nls.getNLSText('msgExplanation'), self.explanation, '\n'])

        return ''.join(tmp)


class Glossary(Question):

    def __init__(self, stem, answer='', explanation=None):
        Question.__init__(self, Category.Glossary, stem, answer, explanation)


class ShortAnswer(Question):

    def __init__(self, stem, answer="", explanation=None):
        Question.__init__(self, Category.ShortAnswer, stem, answer, explanation)
