#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quiz.Question import Question


class MultipleChoice(Question):

    def __init__(self, category, stem, options=[], answer=[], explanation=None):
        Question.__init__(self, category, stem, answer, explanation)

        if options is None:
            self.options = list()
        else:
            self.options = list(options)

    def addOption(self, option):
        self.options.append(option)

    def toWord(self):
        pass

    def getStemTail(self):
        return u'：'

    def __str__(self):
        tmp = ['(', self.category, ')', self.stem, self.getStemTail(), '\n']
        for i in range(len(self.options)):
            tmp.extend([chr(65 + i), ' ', self.options[i], '\n'])

        tmp.append('\n')
        if len(self.answer) > 0:
            if self.category == u'单选题':
                tmp.extend(['答案：', self.answer[0], '\n'])
            else:
                tmp.extend(['答案：', ','.join(self.answer), '\n'])
        else:
            tmp.extend(['答案：', '\n'])

        # tmp.append('\n')
        if self.explanation is None:
            tmp.extend(['解析：', '\n'])
        else:
            tmp.extend(['解析：', self.explanation, '\n'])

        return ''.join(tmp)
