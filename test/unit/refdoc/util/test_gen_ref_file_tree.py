# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from refdoc.util import gen_ref_file_tree, Package
_local = lambda x: 'refdoc.util.{}'.format(x)


def test_works():
    pkgs = [
        Package(fullname='fakepkg'),
        Package(fullname='fakepkg.pkg1', modules=['mod11', 'mod12']),
        Package(fullname='fakepkg.pkg2', modules=['mod21']),
    ]
    tree = gen_ref_file_tree(pkgs)

    expected = '\n'.join([
        '├── fakepkg',
        '├── fakepkg.pkg1',
        '|   ├── mod11',
        '|   └── mod12',
        '└── fakepkg.pkg2',
        '    └── mod21',
    ])
    assert tree == expected
