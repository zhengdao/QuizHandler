#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
core.runtime
~~~~~~~~~~~~~~~~~~

This module define the runtime context for maintaining the context
and runtime env.

"""
from core.util import Locale

env = dict()


def set_context_attr(key: str, value):
    if isinstance(key, str) and value is not None:
        env[key] = value


def get_context_attr(key: str):
    return env.get(key)


def set_context(kvmap: dict):
    for (key, value) in kvmap.items():
        set_context_attr(key, value)


def get_locale():
    loc = get_context_attr('locale')
    if loc is None:
        loc = Locale.getDefaultLocale()

    return loc
