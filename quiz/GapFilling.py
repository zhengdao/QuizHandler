#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from dep import NLSFactory
from quiz.Question import Question
from quiz.Config import Config
from quiz.Category import Category


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
        p.add_run(NLSFactory.getNLSText('msgAnswer'), 'ptitle')
        p.add_run(''.join(tmp), 'pcontent')
        
        # Keep a blank paragraph
        doc.add_paragraph('', 'pstyle')

    def __str__(self):
        stem = self.makeupStem(True)
        tmp = ['(', self.nCategory, ')', stem, self.getStemTail(), '\n']

        # tmp.extend([NLSFactory.getNLSText('msgAnswer'), '\n'])
        # for i in range(len(self.answer)):
        #    tmp.extend([self.getPosIdx(i), ' ', self.answer[i], '\t'])

        if self.explanation is None:
            tmp.extend([NLSFactory.getNLSText('msgExplanation'), '\n'])
        else:
            tmp.extend([NLSFactory.getNLSText('msgExplanation'), self.explanation, '\n'])

        return ''.join(tmp)
