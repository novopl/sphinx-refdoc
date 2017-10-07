# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from mock import patch, Mock
from refdoc.generators import gen_pkg_reference
from refdoc.util import Package


def patch_local(member, *args, **kw):
    return patch('refdoc.generators.{}'.format(member), *args, **kw)


def mkpkg(**kw):
    defaults = dict(
        fullname='fake.package',
        path='/absolute/fake/path',
        relpath='fake/path',
        modules=[]
    )
    defaults.update(kw)

    fullname = defaults.pop('fullname')
    return Package(fullname, **defaults)


@patch_local('write_file')
@patch_local('exists', Mock(return_value=True))
@patch_local('gen_module_doc', Mock(return_value=''))
def test_only_pkg_doc_written_if_no_modules_given(m_write_file):
    pkg = mkpkg()
    gen_pkg_reference(pkg, '/fake/dist/dir')

    m_write_file.assert_called_once()

    args, kw = m_write_file.call_args
    assert args[0] == '/fake/dist/dir/fake_package/index.rst'


@patch_local('write_file')
@patch_local('exists', Mock(return_value=True))
@patch_local('gen_module_doc', Mock(return_value=''))
def test_write_file_called_for_each_module(m_write_file):
    pkg = mkpkg(modules=['mod1', 'mod2'])
    gen_pkg_reference(pkg, '/fake/dist/dir')

    assert len(m_write_file.call_args_list) == 3

    args, kw = m_write_file.call_args_list[0]
    assert args[0] == '/fake/dist/dir/fake_package/mod1.rst'

    args, kw = m_write_file.call_args_list[1]
    assert args[0] == '/fake/dist/dir/fake_package/mod2.rst'

    args, kw = m_write_file.call_args_list[-1]
    assert args[0] == '/fake/dist/dir/fake_package/index.rst'


@patch_local('write_file', Mock())
@patch_local('exists', Mock(return_value=True))
@patch_local('makedirs')
@patch_local('gen_module_doc', Mock(return_value=''))
def test_do_not_make_pkg_dir_if_it_exists(m_makedirs):
    gen_pkg_reference(mkpkg(), '/fake/dist/dir')
    m_makedirs.assert_not_called()


@patch_local('write_file', Mock())
@patch_local('exists', Mock(return_value=False))
@patch_local('makedirs')
@patch_local('gen_module_doc', Mock(return_value=''))
def test_make_pkg_dir_if_it_does_not_exist(m_makedirs):
    gen_pkg_reference(
        mkpkg(fullname='fake.pkg'),
        '/fake/dist/dir'
    )
    m_makedirs.assert_called_once_with('/fake/dist/dir/fake_pkg')
