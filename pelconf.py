# -*- coding: utf-8 -*-
"""
This is fabrics configuration file.
"""
from __future__ import absolute_import

# Configure the build
from peltak.core import conf

conf.init({
    'SRC_DIR': 'src',
    'SRC_PATH': 'src/refdoc',
    'BUILD_DIR': '.build',
    'DOC_SRC_PATHS': 'docs',
    'LINT_PATHS': [
        'src/refdoc',
    ],
    'REFDOC_PATHS': [
        'src/refdoc',
    ],
    'TEST_TYPES': {
        'default': {'paths': ['test']}
    }
})

# Import all commands
from peltak.commands import docs
from peltak.commands import git
from peltak.commands import lint
from peltak.commands import release
from peltak.commands import test
from peltak.commands import version
