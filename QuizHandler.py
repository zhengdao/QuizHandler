#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale
import xlrd

from quiz.Config import Config
from quiz.Category import Category
from quiz.QuizPaper import QuizPaper
from quiz.SingleChoice import SingleChoice
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
            question = SingleChoice(stem, options)

        elif category == u'多选题':
            options = row[2].split(u"〓")
            question = MultipleChoice(stem, options)
            pass

        elif category == u'名词解释':
            question = Glossary(stem)
            pass

        elif category == u'判断题':
            question = TrueFalse(stem)
            pass

        elif category == u'填空题':
            question = GapFilling(stem)
            pass

        elif category == u'问答题':
            question = ShortAnswer(stem)
            pass

        else:
            pass

        if question is not None:
            self.paper.addQuestion(question.getCategory(), question)

    def toWord(self, file, title=None, config=None):
        if title is not None:
            self.paper.setTitle(title)

        if config is None:
            self.paper.toWord(file)
        else:
            self.paper.toWord(file, config)


if __name__ == '__main__':
    loc = locale.getlocale()
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')

    handler = QuizHandler()
    handler.handle('res/Anatomy.xlsx')

    print(handler.paper)

    title = u'2018年6月中医大《系统解剖学》考试复习题集'
    handler.toWord('res/Anatomy.docx', title)

    pconfig = Config({
        Category.SChoice: {'answer': True, 'explanation': False},
        Category.MChoice: {'answer': True, 'explanation': False},
        Category.Glossary: {'answer': True, 'explanation': False},
        Category.TrueFalse: {'answer': True, 'explanation': False},
        Category.GapFilling: {'answer': True, 'explanation': False},
        Category.ShortAnswer: {'answer': True, 'explanation': False}
    })
    # handler.toWord('res/Print.docx', title, pconfig)

    locale.setlocale(locale.LC_ALL, loc)
