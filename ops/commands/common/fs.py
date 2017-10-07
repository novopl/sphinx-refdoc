# -*- coding: utf-8 -*-
"""
File system related helpers.
"""
from __future__ import absolute_import, unicode_literals
from os import remove
from os.path import exists, isdir
from shutil import rmtree

from six import string_types
from fabric.api import local, quiet
from . import log
from .log import _sysmsg


def _surround_paths_with_quotes(paths):
    """ Put quotes around all paths and join them with space in between. """
    if isinstance(paths, string_types):
        raise ValueError(
            "paths cannot be a string. "
            "Use array with one element instead."
        )
    return ' '.join('"' + path + '"' for path in paths)


def _rm_glob(pattern):
    """ Remove all files matching the given glob *pattern*. """
    log._sysmsg("Removing files matching {}", pattern)

    with quiet():
        cmd = ' '.join([
            'find . -name "{}"'.format(pattern),
            "| sed '/^\.\/env/d'",   # Remove entries starting with ./env
            "| sed '/^\.\/\.tox/d'"  # Remove entries starting with ./.tox
        ])
        matches = local(cmd, capture=True)

    for path in matches.splitlines():
        # might be a child of a dir deleted in an earlier iteration
        if not exists(path):
            continue

        if not isdir(path):
            _sysmsg('  ^91[file] ^90{}'.format(path))
            remove(path)
        else:
            _sysmsg('  ^91[dir]  ^90{}'.format(path))
            rmtree(path)
