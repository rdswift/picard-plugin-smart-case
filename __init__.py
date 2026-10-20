#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Smart Case" plugin for Picard
#
# Copyright (C) 2026 Bob Swift (rdswift)
#
# this is based on the Smart Title Case plugin by Sophist and
# updated for use with Picard v2.0 by Bob Swift (rdswift).
#
# The original Sophist Picard v1 plugin is based on the Title
# Case plugin by Javier Kohen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


import re
import unicodedata

from picard.plugin3.api import PluginApi


MATCHER = re.compile(r'\w[^-,;:\./\s\u2010\u2011]*')


def _process_match(match: re.Match) -> str:
    word = match.group(0)
    if word == word.lower():
        word = word[0].upper() + word[1:]
    return word


def smartcase(text: str) -> str:
    """Convert the provided text to a modified form of Title Case.

    Args:
        text (str): String to process.

    Returns:
        str: Converted string.

    Tests:
    >>> smartcase('make title case')
    'Make Title Case'
    >>> smartcase('Already Title Case')
    'Already Title Case'
    >>> smartcase('mIxEd cAsE')
    'mIxEd cAsE'
    >>> smartcase('a')
    'A'
    >>> smartcase("apostrophe's apostrophe’s")
    "Apostrophe's Apostrophe’s"
    >>> smartcase('(bracketed text)')
    '(Bracketed Text)'
    >>> smartcase("'single quotes'")
    "'Single Quotes'"
    >>> smartcase('"double quotes"')
    '"Double Quotes"'
    >>> smartcase('a,b')
    'A,B'
    >>> smartcase('a-b')
    'A-B'
    >>> smartcase('a/b')
    'A/B'
    >>> smartcase('a.b')
    'A.B'
    >>> smartcase('a;b')
    'A;B'
    >>> smartcase('a:b')
    'A:B'
    >>> smartcase('a-B')
    'A-B'
    >>> smartcase('flügel')
    'Flügel'
    >>> smartcase('HARVEST STORY by 杉山清貴')
    'HARVEST STORY By 杉山清貴'
    """
    if not isinstance(text, str) or not text:
        return ''
    return MATCHER.sub(_process_match, unicodedata.normalize("NFKC", text))


def func_smart_case(parser, text):
    try:
        return smartcase(text)
    except Exception as ex:
        api = PluginApi.get_api()
        api.logger.error(f"Error smart casing: {text} (Exception: {ex})")
    return ""


def enable(api: PluginApi):
    """Called when plugin is enabled."""

    # Register script function
    api.register_script_function(
        func_smart_case,
        name="smart_case",
        signature=api.tr('help.smartcase.signature', '$smart_case(text)'),
        documentation=api.tr(
            'help.smartcase.documentation',
            (
                "Capitalize The First Character On Every Word Of The Text. Words containing "
                "embedded uppercase are left as-is (i.e. USA or DoA)."
            )
        )
    )
