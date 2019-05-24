#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import threading

import core.runtime as runtime
import core.util as util
from core.quiz import *
from core.util import *
from core.paper import *


class QuizHandler:

    def __init__(self):
        self.__paper = QuizPaper()

    def handle(self, file):
        workbook = xlrd.open_workbook(file)
        sheet = workbook.sheet_by_index(0)
        rcnt = sheet.nrows
        for i in range(rcnt):
            if i == 0:
                continue
            else:
                self.buildquestion(sheet.row_values(i, 1, 4))

        return self.__paper

    def buildquestion(self, row):
        category = row[0]
        stem = row[1]

        if category == u'单选题':
            options = str(row[2]).split(u"〓")
            question = SingleChoice(stem, options)

        elif category == u'多选题':
            options = str(row[2]).split(u"〓")
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
            question = None
            pass

        if question is not None:
            self.__paper.addquestion(question.getCategory(), question)

    def toword(self, file, title=None, config=None):
        if title is not None:
            self.__paper.settitle(title)

        if config is None:
            self.__paper.toword(file)
        else:
            self.__paper.toword(file, config)


class PaperBuilder(threading.Thread):
    def __init__(self, cinfo, config=None):
        threading.Thread.__init__(self)
        self.name = util.get_filename(course.get('file').replace(' ', '-'))
        self.__course = cinfo
        self.__config = config

        self.__handler = QuizHandler()

    def run(self):
        qh = self.__handler

        cfile = self.__course.get('file')
        paper = qh.handle('res' + os.path.sep + cfile)

        ctitle = self.__course.get('title')
        paper.settitle(ctitle)

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        print(paper)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")

        # output = 'res' + os.path.sep + util.get_filename(cfile) + '.docx'
        output = 'res' + os.path.sep + util.get_filename(ctitle) + '.docx'
        qh.toword(output, ctitle)
        # output = 'res' + os.path.sep + util.get_filename(cfile) + '-print.docx'
        output = 'res' + os.path.sep + util.get_filename(ctitle) + u'[打印版].docx'
        qh.toword(output, ctitle, self.__config)


def buildpaper(cinfo, config):
    qh = QuizHandler()

    cfile = cinfo.get('file')
    paper = qh.handle('res' + os.path.sep + cfile)

    ctitle = cinfo.get('title')
    paper.settitle(ctitle)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    print(paper)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")

    # output = 'res' + os.path.sep + util.get_filename(cfile) + '.docx'
    output = 'res' + os.path.sep + util.get_filename(ctitle) + '.docx'
    qh.toword(output, ctitle)
    # output = 'res' + os.path.sep + util.get_filename(cfile) + '[Print].docx'
    output = 'res' + os.path.sep + util.get_filename(ctitle) + u'[打印版].docx'
    qh.toword(output, ctitle, config)


if __name__ == '__main__':
    loc = Locale('zh', 'CN')
    runtime.set_context_attr('locale', loc)

    pconfig = Config({
        Category.SChoice: {'answer': True, 'explanation': True},
        Category.MChoice: {'answer': True, 'explanation': True},
        Category.Glossary: {'answer': True, 'explanation': False},
        Category.TrueFalse: {'answer': True, 'explanation': True},
        Category.GapFilling: {'answer': True, 'explanation': False},
        Category.ShortAnswer: {'answer': True, 'explanation': False}
    })

    courses = [
        {'file': 'Pathobiology.xlsx', 'title': u'中医大2019年6月《病理学(本科)》考试复习题集'},
        {'file': 'Clinical Pharmacotherapeutics.xlsx', 'title': u'中医大2019年6月《临床药物治疗学(本科)》考试复习题集'},
        {'file': 'Pharmacology.xlsx', 'title': u'中医大2019年6月《药理学(本科)》考试复习题集'}
    ]

    '''
    for index, course in enumerate(courses):
        buildpaper(course, pconfig)

    '''
    threads = []
    for index, course in enumerate(courses):
        t = PaperBuilder(course, pconfig)
        threads.append(t)

    for index, t in enumerate(threads):
        t.start()

    for index, t in enumerate(threads):
        t.join()
