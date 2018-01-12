# -*- coding: utf-8 -*-
"""
This is fabrics configuration file.
"""
from __future__ import absolute_import


# Configure the build
from fabops.commands.common import conf
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
from fabops.commands.clean import *
from fabops.commands.docs import *
from fabops.commands.release import *
from fabops.commands.frontend import *
from fabops.commands.git import *
from fabops.commands.lint import *
from fabops.commands.ops import *
from fabops.commands.test import *
