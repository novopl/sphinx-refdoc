# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from mock import patch, Mock
from refdoc.generators import gen_reference_docs
from refdoc import rst
from refdoc.toctree import Toctree
from refdoc.util import Package


def patch_local(member, *args, **kw):
    return patch('refdoc.generators.{}'.format(member), *args, **kw)


@patch_local('gen_pkg_reference')
@patch_local('write_file', Mock())
@patch_local('get_packages', Mock(return_value=[
    Package(fullname='fake_pkg'),
    Package(fullname='fake_pkg.pkg1', modules=['mod11', 'mod12']),
    Package(fullname='fake_pkg.pkg2', modules=['mod21']),
]))
def test_generates_ref_for_all_pkgs(m_gen_pkg_reference):
    m_gen_pkg_reference.return_value = 'fake_file.rst'

    gen_reference_docs('fake_src', 'fake_dst')

    assert len(m_gen_pkg_reference.call_args_list) == 3
    processed_pkgs = [
        args[0].fullname for args, kw in m_gen_pkg_reference.call_args_list
    ]
    assert processed_pkgs == [
        'fake_pkg',
        'fake_pkg.pkg1',
        'fake_pkg.pkg2',
    ]


@patch_local('write_file')
@patch_local('gen_pkg_reference', Mock(return_value='fakefile.rst'))
@patch_local('get_packages', Mock(return_value=[
    Package(fullname='fake_pkg'),
    Package(fullname='fake_pkg.pkg1', modules=['mod11', 'mod12']),
    Package(fullname='fake_pkg.pkg2', modules=['mod21']),
]))
def test_writes_index_file(m_write_file):
    gen_reference_docs('fake_src', 'fake_dst')

    m_write_file.assert_called_once()
    assert m_write_file.call_args[0][0] == 'fake_dst/index.rst'


@patch_local('write_file')
@patch_local('gen_pkg_reference', Mock(return_value='fake_file.rst'))
@patch_local('get_packages', Mock(return_value=[
    Package(fullname='fake_pkg'),
    Package(fullname='fake_pkg.pkg1', modules=['mod11', 'mod12']),
    Package(fullname='fake_pkg.pkg2', modules=['mod21']),
]))
def test_index_file_has_a_proper_title(m_write_file):
    gen_reference_docs('fake_src', 'fake_dst')

    index_content = m_write_file.call_args[0][1]

    assert rst.title('Reference documentation') in index_content


@patch_local('write_file')
@patch_local('gen_pkg_reference', Mock(return_value='fake_file.rst'))
@patch_local('get_packages', Mock(return_value=[
    Package(fullname='fake_pkg'),
    Package(fullname='fake_pkg.pkg1', modules=['mod11', 'mod12']),
    Package(fullname='fake_pkg.pkg2', modules=['mod21']),
]))
def test_index_has_proper_toc(m_write_file):
    gen_reference_docs('fake_src', 'fake_dst')

    expected_toc = Toctree()
    expected_toc.add('fake_file.rst')
    expected_toc.add('fake_file.rst')
    expected_toc.add('fake_file.rst')

    index_content = m_write_file.call_args[0][1]
    assert rst.section('Packages') in index_content
    assert str(expected_toc) in index_content
