# -*- coding: utf-8 -*-
"""
Project related helpers.
"""
from __future__ import absolute_import, unicode_literals

from contextlib import contextmanager

from os.path import dirname, join, normpath
from fabric.api import lcd, local, quiet as fabric_quiet


def _current_branch():
    with fabric_quiet():
        return local('git symbolic-ref --short HEAD', capture=True).stdout


def _repo_path(path):
    """ Return absolute path to the repo dir (root project directory). """
    return normpath(join(dirname(__file__), '../../..', path))


@contextmanager
def _inside_repo(path='.', quiet=False):
    """ Return absolute path to the repo dir (root project directory). """
    with lcd(_repo_path(path)):
        if quiet:
            with fabric_quiet():
                yield
        else:
            yield
