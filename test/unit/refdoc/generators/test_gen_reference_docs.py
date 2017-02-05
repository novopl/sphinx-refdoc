# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from mock import patch, Mock
from refdoc.generators import gen_reference_docs
from refdoc import rst
from refdoc.toctree import Toctree
from refdoc.util import Package
_local = lambda x: 'refdoc.generators.{}'.format(x)


@patch(_local('gen_pkg_reference'))
@patch(_local('write_file'), Mock())
@patch(_local('get_packages'), Mock(return_value=[
    Package(fullname='fakepkg'),
    Package(fullname='fakepkg.pkg1', modules=['mod11', 'mod12']),
    Package(fullname='fakepkg.pkg2', modules=['mod21']),
]))
def test_generates_ref_for_all_pkgs(m_gen_pkg_reference):
    m_gen_pkg_reference.return_value='fakefile.rst'

    gen_reference_docs('fakesrc', 'fakedst')

    assert len(m_gen_pkg_reference.call_args_list) == 3
    processed_pkgs = [
        args[0].fullname for args, kw in m_gen_pkg_reference.call_args_list
    ]
    assert processed_pkgs == [
        'fakepkg',
        'fakepkg.pkg1',
        'fakepkg.pkg2',
    ]


@patch(_local('write_file'))
@patch(_local('gen_pkg_reference'), Mock(return_value='fakefile.rst'))
@patch(_local('get_packages'), Mock(return_value=[
    Package(fullname='fakepkg'),
    Package(fullname='fakepkg.pkg1', modules=['mod11', 'mod12']),
    Package(fullname='fakepkg.pkg2', modules=['mod21']),
]))
def test_writes_index_file(m_write_file):
    gen_reference_docs('fakesrc', 'fakedst')

    m_write_file.assert_called_once()
    assert m_write_file.call_args[0][0] == 'fakedst/index.rst'


@patch(_local('write_file'))
@patch(_local('gen_pkg_reference'), Mock(return_value='fakefile.rst'))
@patch(_local('get_packages'), Mock(return_value=[
    Package(fullname='fakepkg'),
    Package(fullname='fakepkg.pkg1', modules=['mod11', 'mod12']),
    Package(fullname='fakepkg.pkg2', modules=['mod21']),
]))
def test_index_file_has_a_proper_title(m_write_file):
    gen_reference_docs('fakesrc', 'fakedst')

    index_content = m_write_file.call_args[0][1]

    assert rst.title('Reference documentation') in index_content


@patch(_local('write_file'))
@patch(_local('gen_pkg_reference'), Mock(return_value='fakefile.rst'))
@patch(_local('get_packages'), Mock(return_value=[
    Package(fullname='fakepkg'),
    Package(fullname='fakepkg.pkg1', modules=['mod11', 'mod12']),
    Package(fullname='fakepkg.pkg2', modules=['mod21']),
]))
def test_index_has_proper_toc(m_write_file):
    gen_reference_docs('fakesrc', 'fakedst')

    expected_toc = Toctree()
    expected_toc.add('fakefile.rst')
    expected_toc.add('fakefile.rst')
    expected_toc.add('fakefile.rst')

    index_content = m_write_file.call_args[0][1]
    assert rst.section('Packages') in index_content
    assert str(expected_toc) in index_content

