# -*- coding: utf-8 -*-
"""
Various commands that do not fit another category but there's not enough of them
to justify a separate module.
"""
from __future__ import absolute_import, unicode_literals
import os
from .common import _repo_path, _rm_glob


def clean():
    """ Remove temporary files like python cache, swap files, etc. """
    patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.swp',
    ]

    os.chdir(_repo_path('.'))

    for pattern in patterns:
        _rm_glob(pattern)
