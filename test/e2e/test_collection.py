# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from os.path import join
from refdoc.objects import Module, Package


def _get_lib_package_content(path):
    def is_child(file):
        child_path = join(path, file)
        return Module.is_module(child_path) or Package.is_pkg(child_path)

    return [f for f in os.listdir(path) if is_child(f)]


def test_collects_root_package():
    pkg = Package.create('src/refdoc')

    assert pkg.name == 'refdoc'
    assert pkg.fullname == 'refdoc'
    assert pkg.path == join(os.getcwd(), 'src/refdoc')


def test_finds_all_children():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=False)

    files = _get_lib_package_content('src/refdoc')
    children = [p.fullname for p in pkg.children]
    assert len(children) == (len(files))


def test_children_have_proper_names():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=False)

    names = frozenset((child.name for child in pkg.children))
    expected = frozenset((
        'cli',
        'logic',
        'objects',
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
        'refdoc/logic.py',
        'refdoc/objects',
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
        'refdoc.logic',
        'refdoc.objects',
        'refdoc.rst',
        'refdoc.toctree',
        'refdoc.util'
    ))

    assert names == expected


def test_can_get_child():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=False)

    objects = pkg.get_child('objects')
    assert objects is not None
    assert objects.fullname == 'refdoc.objects'


def test_can_collect_recursively():
    pkg = Package.create('src/refdoc')
    pkg.collect_children(recursive=True)

    objects = pkg.get_child('objects')

    names = frozenset((child.fullname for child in objects.children))
    expected = frozenset((
        'refdoc.objects.base',
        'refdoc.objects.module',
        'refdoc.objects.package',
    ))

    assert names == expected
