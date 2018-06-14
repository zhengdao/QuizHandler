#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import locale

from dep import Properties

nlsProps = dict()


def getNLSProps(loc=None):
    lc = 'en_US'
    if loc is None:
        loc = locale.getlocale()
        lc = loc[0]

    ps = nlsProps.get(lc)
    if ps is None:
        path = os.path.abspath('.')
        fp = ''.join([path, '/i18n/', lc, '.properties'])
        ps = Properties.parse(fp)
        nlsProps[lc] = ps

    return ps


def getNLSText(key, loc=None):
    ps = getNLSProps(loc)
    txt = key
    if ps is not None:
        txt = ps.get(key, key)

    return txt
