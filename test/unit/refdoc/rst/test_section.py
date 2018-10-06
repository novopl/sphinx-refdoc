# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals
from refdoc import rst


def test_generates_proper_directive():
    assert rst.section('test title') == '\n'.join([
        '',
        'test title',
        '==========',
        '',
    ])


def test_can_specify_the_underline():
    assert rst.section('test title', '-') == '\n'.join([
        '',
        'test title',
        '----------',
        '',
    ])


def test_underline_can_be_anything():
    assert rst.section('test title', 'x') == '\n'.join([
        '',
        'test title',
        'xxxxxxxxxx',
        '',
    ])
