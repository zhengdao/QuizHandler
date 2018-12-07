#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
core.NLSFactory
~~~~~~~~~~~~~~~~~~

This module define the NLSFactory for handling and read nls item.

"""
import os
import core.runtime as runtime
import core.util as tools
from core.util import Locale

nlsProps = dict()


def getNLSProps(loc: Locale = None):
    if loc is None:
        loc = runtime.get_locale()
        lc = loc.__str__()

    ps = nlsProps.get(lc)
    if ps is None:
        path = os.path.abspath('.')
        fp = ''.join([path, '/i18n/', lc, '.properties'])
        ps = tools.parse(fp)
        nlsProps[lc] = ps

    return ps


def getNLSText(key, loc=None):
    ps = getNLSProps(loc)
    txt = key
    if ps is not None:
        txt = ps.get(key, key)

    return txt
