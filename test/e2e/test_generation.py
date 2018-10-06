# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# stdlib imports
import os
import os.path
import shutil
import tempfile

# 3rd party imports
import pytest

# local imports
from refdoc import generate_docs


@pytest.fixture()
def tempdir():
    """ Create a temp directory to store the generated files. """
    tempdir = tempfile.mkdtemp(prefix='sphinx-refdoc-e2e-tests')

    yield tempdir

    shutil.rmtree(tempdir)


def test_package_directory_exists(tempdir):
    generate_docs(['src/refdoc'], tempdir)

    pkg_path = os.path.join(tempdir, 'refdoc')
    assert os.path.exists(pkg_path)


def test_all_refdoc_submodules_exist(tempdir):
    generate_docs(['src/refdoc'], tempdir)

    files = os.listdir(os.path.join(tempdir, 'refdoc'))
    results = frozenset([f for f in files if f != 'index.rst'])
    expected = frozenset((
        'cli.rst',
        'logic.rst',
        'objects',
        'rst.rst',
        'toctree.rst',
        'util.rst'
    ))

    assert results == expected
