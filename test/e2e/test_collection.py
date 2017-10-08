# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from os.path import join
from refdoc.models.package import Package


def test_collects_root_package():
    pkg = Package.create('src/refdoc')

    assert pkg.name == 'refdoc'
    assert pkg.fullname == 'refdoc'
    assert pkg.path == join(os.getcwd(), 'src/refdoc')


def test_finds_all_children():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=False)

    files = [f for f in os.listdir('src/refdoc') if not f.startswith('__')]
    assert len(pkg.children) == (len(files))


def test_children_have_proper_names():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=False)

    names = frozenset((child.name for child in pkg.children))
    expected = frozenset((
        'cli',
        'generators',
        'logic',
        'models',
        'rst',
        'toctree',
        'util'
    ))

    assert names == expected


def test_children_have_the_correct_rel_paths():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=False)

    rel_paths = frozenset((child.rel_path for child in pkg.children))
    expected = frozenset((
        'refdoc/cli.py',
        'refdoc/generators.py',
        'refdoc/logic.py',
        'refdoc/models',
        'refdoc/rst.py',
        'refdoc/toctree.py',
        'refdoc/util.py'
    ))

    assert rel_paths == expected


def test_children_have_proper_fullname():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=False)

    names = frozenset((child.fullname for child in pkg.children))
    expected = frozenset((
        'refdoc.cli',
        'refdoc.generators',
        'refdoc.logic',
        'refdoc.models',
        'refdoc.rst',
        'refdoc.toctree',
        'refdoc.util'
    ))

    assert names == expected


def test_can_get_child():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=False)

    models = pkg.get_child('models')
    assert models is not None
    assert models.fullname == 'refdoc.models'


def test_can_collect_recursively():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=True)

    models = pkg.get_child('models')

    names = frozenset((child.fullname for child in models.children))
    expected = frozenset((
        'refdoc.models.base',
        'refdoc.models.module',
        'refdoc.models.package',
    ))

    assert names == expected
