#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd

from quiz.MultipleChoice import MultipleChoice
from quiz.TrueFalse import TrueFalse
from quiz.Glossary import Glossary
from quiz.GapFilling import GapFilling
from quiz.ShortAnswer import ShortAnswer


class QuizHandler:

    def __init__(self):
        self.questions = dict()

    def handle(self, file):
        workbook = xlrd.open_workbook(file)
        sheet = workbook.sheet_by_index(0)
        rcnt = sheet.nrows
        for i in range(rcnt):
            if i == 0:
                continue
            else:
                self.buildQuestion(sheet.row_values(i, 1, 4))

    def buildQuestion(self, row):
        category = row[0]
        stem = row[1]

        if category == u'单选题':
            options = row[2].split(u"〓")
            question = MultipleChoice(category, stem, options)

        elif category == u'多选题':
            options = row[2].split(u"〓")
            question = MultipleChoice(category, stem, options)
            pass

        elif category == u'名词解释':
            question = Glossary(category, stem)
            pass

        elif category == u'判断题':
            question = TrueFalse(category, stem)
            pass

        elif category == u'填空题':
            question = GapFilling(category, stem)
            pass

        elif category == u'问答题':
            question = ShortAnswer(category, stem)
            pass

        else:
            pass

        if question is not None:
            print(question)
            self.cacheQuestionByType(category, question)

    def getCacheByType(self, category):
        cache = self.questions.get(category)
        if cache is None:
            self.questions[category] = []

        return self.questions[category]

    def cacheQuestionByType(self, category, question):
        cache = self.getCacheByType(category)
        cache.append(question)

    def toWord(self):
        pass


if __name__ == '__main__':
    handler = QuizHandler()
    handler.handle('res/Anatomy.xls')