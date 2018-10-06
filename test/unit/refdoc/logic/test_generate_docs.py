# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

from functools import wraps

from refdoc import logic
from mock import patch, Mock, MagicMock, mock_open


@patch('refdoc.logic.generate_pkg_docs', Mock())
@patch('refdoc.logic.generate_root_index_rst')
@patch('refdoc.logic.Package.create', Mock(return_value={}))
def test_does_not_generate_index_by_default(p_generate_root_index_rst):
    """
    :param Mock p_generate_root_index_rst:
    """

    with patch('refdoc.logic.open', mock_open()) as p_open:
        logic.generate_docs('fake_pkgs', 'fake_out')

        p_open.assert_not_called()

    p_generate_root_index_rst.assert_not_called()


@patch('refdoc.logic.generate_pkg_docs', Mock())
@patch('refdoc.logic.generate_root_index_rst')
@patch('refdoc.logic.Package.create', Mock(return_value={}))
def test_generates_index_when_gen_index_is_True(p_generate_root_index_rst):
    """
    :param Mock p_generate_root_index_rst:
    """

    with patch('refdoc.logic.open', mock_open()) as p_open:
        logic.generate_docs('fake_pkgs', 'fake_out', gen_index=True)

        p_open.assert_called_once()

    p_generate_root_index_rst.assert_called_once()


@patch('refdoc.logic.generate_pkg_docs', Mock())
@patch('refdoc.logic.generate_root_index_rst', Mock())
@patch('refdoc.logic.Package.create', Mock(return_value={}))
@patch('refdoc.util.set_verbosity_level')
def test_does_not_globally_set_verbosity_when_not_given(p_set_verbosity_level):
    """
    :param Mock p_set_verbosity_level:
    """

    logic.generate_docs('fake_pkgs', 'fake_out')
    p_set_verbosity_level.assert_not_called()


@patch('refdoc.logic.generate_pkg_docs', Mock())
@patch('refdoc.logic.generate_root_index_rst', Mock())
@patch('refdoc.logic.Package.create', Mock(return_value={}))
@patch('refdoc.util.set_verbosity_level')
def test_globally_sets_verbosity_when_given(p_set_verbosity_level):
    """
    :param Mock p_set_verbosity_level:
    """
    logic.generate_docs('fake_pkgs', 'fake_out', verbose=3)
    p_set_verbosity_level.assert_called_once_with(3)
