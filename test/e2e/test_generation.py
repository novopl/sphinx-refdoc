# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from os.path import exists, join
from shutil import rmtree
from tempfile import mkdtemp
from refdoc.logic import generate_docs
import pytest


@pytest.fixture()
def tempdir():
    """ Create a temp directory to store the generated files. """
    tempdir = mkdtemp(prefix='sphinx-refdoc-e2e-tests')

    yield tempdir

    rmtree(tempdir)


def test_package_directory_exists(tempdir):
    generate_docs(['src/refdoc'], tempdir)

    pkg_path = join(tempdir, 'refdoc')
    assert exists(pkg_path)


def test_all_refdoc_submodules_exist(tempdir):
    generate_docs(['src/refdoc'], tempdir)

    files = os.listdir(join(tempdir, 'refdoc'))
    results = frozenset([f for f in files if f != 'index.rst'])
    expected = frozenset((
        'cli.rst',
        'generators.rst',
        'logic.rst',
        'models',
        'rst.rst',
        'toctree.rst',
        'util.rst'
    ))

    assert results == expected
