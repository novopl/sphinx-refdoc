# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from refdoc import rst


def test_generates_proper_directive():
    assert rst.title('test title') == '\n'.join([
        '',
        '==========',
        'test title',
        '==========',
        '',
    ])
