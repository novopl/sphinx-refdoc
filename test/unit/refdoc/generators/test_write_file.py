# -*- coding: utf-8 -*-
from __future__ import absolute_import
from mock import patch, Mock, mock_open
from os.path import dirname
from refdoc.generators import write_file
_local = lambda x: 'refdoc.generators.{}'.format(x)


@patch(_local('exists'), Mock(return_value=False))
@patch(_local('makedirs'))
def test_create_parent_dirs_if_they_do_not_exist(makedirs):

    m_open = mock_open()
    with patch(_local('open'), m_open):
        write_file('fakepath', "test text")

    makedirs.assert_called_once_with(dirname('fakepath'))


@patch(_local('exists'), Mock(return_value=True))
@patch(_local('makedirs'))
def test_doesnt_create_parent_dirs_if_they_exist(makedirs):

    m_open = mock_open()

    with patch(_local('open'), m_open):
        write_file('fakepath', "test text")

    makedirs.assert_not_called()


@patch(_local('exists'), Mock(return_value=True))
@patch(_local('makedirs'), Mock())
def test_correct_file_is_opened():

    m_open = mock_open()
    m_open.return_value.write = Mock()

    with patch(_local('open'), m_open):
        write_file('fakepath', "test text")

        args, kw = m_open.call_args
        assert args[0] == 'fakepath'


@patch(_local('exists'), Mock(return_value=True))
@patch(_local('makedirs'), Mock())
def test_correct_text_is_written():

    m_open = mock_open()
    m_open.return_value.write = Mock()

    with patch(_local('open'), m_open):
        write_file('fakepath', "test text")

        args, kw = m_open.return_value.write.call_args
        assert args[0] == "test text"
