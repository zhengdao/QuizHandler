#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quiz.Config import Config


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

    def stemToWord(self, doc, lead='', level=2):
        doc.add_paragraph(lead + self.stem + self.getStemTail(), 'h' + str(level))

    def answerToWord(self, doc):
        p = doc.add_paragraph()
        p.add_run(u'答案：', 'ptitle')
        if self.answer is not None:
            p.add_run(self.answer, 'pcontent')

    def explanationToWord(self, doc):
        p = doc.add_paragraph()
        p.add_run(u'解析：', 'ptitle')
        if self.explanation is not None:
            p.add_run(self.explanation, 'pcontent')

    def toWord(self, doc, lead='', level=2, config=Config()):
        # to stem
        self.stemToWord(doc, lead, level)

        # to answer
        if config.isTrue('answer'):
            self.answerToWord(doc)

        # to explanation
        if config.isTrue('explanation'):
            self.explanationToWord(doc)

        # Keep a blank paragraph
        doc.add_paragraph('', 'pstyle')

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
