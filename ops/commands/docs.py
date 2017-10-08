# -*- coding: utf-8 -*-
"""
Various commands that do not fit another category but there's not enough of them
to justify a separate module.
"""
from __future__ import absolute_import, unicode_literals
import os
from os.path import exists
from shutil import rmtree

from fabric.api import local, lcd, shell_env
from refdoc import generate_docs

from .common import _repo_path, _sysmsg, _is_true


ASSETS_PATH = _repo_path('docs/assets')
SRC_PATH = _repo_path('src')
DOCS_PATH = _repo_path('docs')
BUILD_PATH = _repo_path('.build/docs')
OUT_PATH = _repo_path('docs/html')
REF_DOCS_PATH = _repo_path('docs/ref')
PKG_PATHS = [
    _repo_path('src/refdoc'),
    _repo_path('ops/commands'),
]


def docs(recreate='no'):
    """ Build project documentation. """
    _sysmsg('Ensuring assets directory ^94{}^32 exists', ASSETS_PATH)
    if not exists(ASSETS_PATH):
        os.makedirs(ASSETS_PATH)

    if _is_true(recreate) and exists(OUT_PATH):
        _sysmsg("^91Deleting ^94{}".format(OUT_PATH))
        rmtree(OUT_PATH)

    _sysmsg('Removing previously generated reference documentation')
    if exists(REF_DOCS_PATH):
        rmtree(REF_DOCS_PATH)

    os.makedirs(REF_DOCS_PATH)

    _sysmsg('Generating reference documentation')
    generate_docs(PKG_PATHS, out_dir=REF_DOCS_PATH)

    with shell_env(PYTHONPATH='.:{}'.format(SRC_PATH)):
        with lcd(DOCS_PATH):
            _sysmsg('Building docs with ^35sphinx')
            _sysmsg('   build dir:  ^33'.format(BUILD_PATH))
            _sysmsg('   docs src:   ^33'.format(DOCS_PATH))
            _sysmsg('   out:        ^33'.format(OUT_PATH))

            local('sphinx-build -b html -d {build} {docs} {out}'.format(
                build=BUILD_PATH,
                docs=DOCS_PATH,
                out=OUT_PATH,
            ))