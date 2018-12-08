#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import os.path
import tempfile


class Locale:

    def __init__(self, language: str, country: str = None):
        self.__language = language
        self.__country = country

    @property
    def language(self):
        """
        Return the language code of this Locale.

        :return: str | none
        """
        return self.__language

    @language.setter
    def language(self, language):
        """
        Set the language of current Locale. Language always be lower case.
        If the specified language isn't be the valid string, a blank string
        will be used.

        :param language: str 2 or 3 letter language code.
        """
        if isinstance(language, str):
            self.__language = language

    @property
    def country(self):
        """
        Returns the country code of this Locale.

        :return: str
        """
        return self.__country

    @country.setter
    def country(self, country):
        """
        Sets the country for the Locale. Country always be upper case.
        If the specified country isn't be the valid string, a blank string
        will be used.

        :param country: str An ISO 3166 alpha-2 country code or a UN M.49 numeric-3
               area code.
        """
        if isinstance(country, str):
            self.__country = country

    def __str__(self):
        locstr = self.__language
        if isinstance(self.__country, str):
            locstr = '_'.join([self.__language, self.__country])

        return locstr

    __repr__ = __str__

    @staticmethod
    def getDefaultLocale():
        return Locale("en", "US")


class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}

        try:
            fopen = open(self.file_name, 'r', encoding='UTF-8')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]

        return default_value

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + value, True)


def parse(file_name):
    return Properties(file_name)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    file = tempfile.TemporaryFile()

    if os.path.exists(file_name):
        r_open = open(file_name, 'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open:
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            file.write(line)

        if not found and append_on_not_exists:
            file.write('\n' + to_str)

        r_open.close()
        file.seek(0)

        content = file.read()

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name, 'w')
        w_open.write(content)
        w_open.close()

        file.close()
    else:
        print(f"file {file_name} not found!")


def get_filename(path):
    return os.path.splitext(path)[0]


def get_fileext(path):
    return os.path.splitext(path)[1]
