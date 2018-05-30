#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd

from quiz.QuizPaper import QuizPaper
from quiz.MultipleChoice import MultipleChoice
from quiz.TrueFalse import TrueFalse
from quiz.Glossary import Glossary
from quiz.GapFilling import GapFilling
from quiz.ShortAnswer import ShortAnswer


class QuizHandler:

    def __init__(self):
        self.paper = QuizPaper()

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
            self.paper.addQuestion(category, question)

    def toWord(self, file, title=None):
        if title is not None:
            self.paper.setTitle(title)

        self.paper.toWord(file)


if __name__ == '__main__':
    handler = QuizHandler()
    handler.handle('res/Anatomy.xls')

    print(handler.paper)

    title = u'2018中国医科大《系统解剖学》考试复习题集'
    handler.toWord('res/Anatomy.docx', title)