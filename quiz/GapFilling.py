#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from quiz.Question import Question


class GapFilling(Question):

    rPidx = re.compile(r'\(\)')

    @staticmethod
    def getPosIdx(idx):
        return chr(97 + idx)

    def __init__(self, category, stem, answer=[], explanation=None):
        Question.__init__(self, category, stem, answer, explanation)
       
    def stemToWord(self, doc, lead='', level=2):
        stem = self.makeupStem()
        doc.add_paragraph(lead + stem + self.getStemTail(), 'h' + str(level))
        
    def answerToWord(self, doc):
        tmp = []
        for i in range(len(self.answer)):
            tmp.extend([self.getPosIdx(i), ' ', self.answer[i], '\t'])

        p = doc.add_paragraph()
        p.add_run(u'答案：', 'ptitle')
        p.add_run(''.join(tmp), 'pcontent')
        
        # Keep a blank paragraph
        doc.add_paragraph('', 'pstyle')

    def makeupStem(self):
        frags = self.rPidx.split(self.stem)
        cnt = len(frags)
        tmp = []
        for i in range(cnt):
            tmp.append(frags[i])

            if i < cnt - 1:
                tmp.extend(['(', self.getPosIdx(i), ')'])

        return ''.join(tmp)

    def __str__(self):
        stem = self.makeupStem()
        tmp = ['(', self.category, ')', stem, self.getStemTail(), '\n']

        tmp.extend(['答案：', '\n'])
        for i in range(len(self.answer)):
            tmp.extend([self.getPosIdx(i), ' ', self.answer[i], '\t'])

        tmp.append('\n')
        if self.explanation is None:
            tmp.extend(['解析：', '\n'])
        else:
            tmp.extend(['解析：', self.explanation, '\n'])

        return ''.join(tmp)
