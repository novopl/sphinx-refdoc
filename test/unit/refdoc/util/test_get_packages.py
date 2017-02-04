# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from mock import patch, Mock
from refdoc.util import get_packages
_local = lambda x: 'refdoc.util.{}'.format(x)


def mock_is_pkg(results):
    def fake_is_pkg(path):
        return results[path]
    return fake_is_pkg


@patch(_local('walk'), Mock(return_value=[
    ('fakepkg',      ['pkg1', 'pkg2', 'docs'], ['__init__.py']),
    ('fakepkg/pkg1', [], ['__init__.py', 'mod11.py', 'mod12.py']),
    ('fakepkg/pkg2', [], ['__init__.py', 'mod21.py']),
    ('fakepkg/docs', [], ['doc1.rst', 'doc2.rst']),
]))
def test_finds_3_packages():
    assert len(get_packages('fake_root')) == 3


@patch(_local('walk'), Mock(return_value=[
    ('fakepkg',      ['pkg1', 'pkg2', 'docs'], ['__init__.py']),
    ('fakepkg/pkg1', [], ['__init__.py']),
    ('fakepkg/pkg2', [], ['__init__.py']),
    ('fakepkg/docs', [], ['doc1.rst']),
]))
def test_does_not_pick_up_dirs_without_init_py():
    assert 'fakepkg.docs' not in (p.fullname for p in get_packages('fake_root'))


@patch(_local('walk'), Mock(return_value=[
    ('fakedir',      ['pkg1', 'pkg2'], []),
    ('fakedir/pkg1', [], ['__init__.py']),
    ('fakedir/pkg2', [], ['__init__.py']),
]))
def test_picks_up_packages_even_if_nested_within_a_plain_subdirectory():
    assert len(get_packages('fake_root')) == 2


@patch(_local('walk'), Mock(return_value=[
    ('fakepkg',      ['pkg1', 'pkg2'], ['__init__.py']),
    ('fakepkg/pkg1', [], ['__init__.py']),
    ('fakedir',      ['pkg1', 'pkg2'], []),
    ('fakedir/pkg1', [], ['__init__.py']),
]))
@patch(_local('is_pkg'), mock_is_pkg({
    'fakepkg': True,
    'fakepkg/pkg1': True,
    'fakedir': False,
    'fakedir/pkg1': True,
}))
def test_correctly_parses_package_names():
    pkgs = get_packages('')

    names = [p.fullname for p in pkgs]
    assert len(pkgs) == 3
    assert names == [
        'fakepkg',
        'fakepkg.pkg1',
        'pkg1',
    ]
