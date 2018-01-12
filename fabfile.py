# -*- coding: utf-8 -*-
"""
This is fabrics configuration file.
"""
from __future__ import absolute_import


# Configure the build
from ops.commands.common import conf
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
        'env/lib/python3.6/site-packages/fabops/commands'
    ],
    'TEST_TYPES': {
        'default': {'paths': ['test']}
    }
})


# Import all commands
from ops.commands.clean import *
from ops.commands.docs import *
from ops.commands.release import *
from ops.commands.frontend import *
from ops.commands.git import *
from ops.commands.lint import *
from ops.commands.ops import *
from ops.commands.test import *
