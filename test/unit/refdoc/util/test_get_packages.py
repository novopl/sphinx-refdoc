# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from mock import patch, Mock
from refdoc.util import get_packages


def patch_local(member, *args, **kw):
    return patch('refdoc.util.{}'.format(member), *args, **kw)


def mock_is_pkg(results):
    def fake_is_pkg(path):
        return results[path]
    return fake_is_pkg


@patch_local('walk', Mock(return_value=[
    ('fake_pkg',      ['pkg1', 'pkg2', 'docs'], ['__init__.py']),
    ('fake_pkg/pkg1', [], ['__init__.py', 'mod11.py', 'mod12.py']),
    ('fake_pkg/pkg2', [], ['__init__.py', 'mod21.py']),
    ('fake_pkg/docs', [], ['doc1.rst', 'doc2.rst']),
]))
def test_finds_3_packages():
    assert len(get_packages('fake_root')) == 3


@patch_local('walk', Mock(return_value=[
    ('fake_pkg',      ['pkg1', 'pkg2', 'docs'], ['__init__.py']),
    ('fake_pkg/pkg1', [], ['__init__.py']),
    ('fake_pkg/pkg2', [], ['__init__.py']),
    ('fake_pkg/docs', [], ['doc1.rst']),
]))
def test_does_not_pick_up_dirs_without_init_py():
    assert 'fake_pkg.docs' not in (
        p.fullname for p in get_packages('fake_root')
    )


@patch_local('walk', Mock(return_value=[
    ('fake_dir',      ['pkg1', 'pkg2'], []),
    ('fake_dir/pkg1', [], ['__init__.py']),
    ('fake_dir/pkg2', [], ['__init__.py']),
]))
def test_picks_up_packages_even_if_nested_within_a_plain_subdirectory():
    assert len(get_packages('fake_root')) == 2


@patch_local('walk', Mock(return_value=[
    ('fake_pkg',      ['pkg1', 'pkg2'], ['__init__.py']),
    ('fake_pkg/pkg1', [], ['__init__.py']),
    ('fake_dir',      ['pkg1', 'pkg2'], []),
    ('fake_dir/pkg1', [], ['__init__.py']),
]))
@patch_local('is_pkg', mock_is_pkg({
    'fake_pkg': True,
    'fake_pkg/pkg1': True,
    'fake_dir': False,
    'fake_dir/pkg1': True,
}))
def test_correctly_parses_package_names():
    pkgs = get_packages('')

    names = [p.fullname for p in pkgs]
    assert len(pkgs) == 3
    assert names == [
        'fake_pkg',
        'fake_pkg.pkg1',
        'pkg1',
    ]
