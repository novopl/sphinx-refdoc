# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from refdoc.util import gen_ref_file_tree, Package


def test_works():
    pkgs = [
        Package(fullname='fake_pkg'),
        Package(fullname='fake_pkg.pkg1', modules=['mod11', 'mod12']),
        Package(fullname='fake_pkg.pkg2', modules=['mod21']),
    ]
    tree = gen_ref_file_tree(pkgs)

    expected = '\n'.join([
        '├── fake_pkg',
        '├── fake_pkg.pkg1',
        '|   ├── mod11',
        '|   └── mod12',
        '└── fake_pkg.pkg2',
        '    └── mod21',
    ])
    assert tree == expected
