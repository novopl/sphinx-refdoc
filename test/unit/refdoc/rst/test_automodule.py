# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from refdoc import rst


def test_generates_proper_directive():
    assert rst.automodule('test.module') == '\n'.join([
        '',
        '.. automodule:: test.module',
        '    :members:',
        '',
    ])
