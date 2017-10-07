# -*- coding: utf-8 -*-
"""
Code linting commands.
"""
from __future__ import absolute_import, unicode_literals

from six import string_types
from fabric.api import local

from .common import (
    _repo_path,
    _surround_paths_with_quotes,
    _sysmsg,
)


PEP8_CMD = 'pep8 --config {} {{}}'.format(
    _repo_path('ops/tools/pep8.ini')
)
PYLINT_CMD = 'pylint --rcfile {} {{}}'.format(
    _repo_path('ops/tools/pylint.ini')
)


def _lint_files(paths):
    """ Run static analysis on the given files.

    :param paths:   Iterable with each item being path that should be linted..
    """
    if isinstance(paths, string_types):
        raise ValueError("paths must be an array of strings")

    _sysmsg("Linting")
    for path in paths:
        print("--   {}".format(path))

    paths = _surround_paths_with_quotes(paths)

    _sysmsg("Checking PEP8 compatibility")
    pep8_ret = local(PEP8_CMD.format(paths)).return_code

    _sysmsg("Running linter")
    pylint_ret = local(PYLINT_CMD.format(paths)).return_code

    if pep8_ret != 0:
        print("pep8 failed with return code {}".format(pep8_ret))

    if pylint_ret:
        print("pylint failed with return code {}".format(pylint_ret))

    return pep8_ret == pylint_ret == 0


def lint():
    """ Run pep8 and pylint on all project files. """
    paths = [
        _repo_path('src/refdoc'),
        _repo_path('ops/commands'),
        _repo_path('test'),
    ]
    if not _lint_files(paths):
        exit(1)
