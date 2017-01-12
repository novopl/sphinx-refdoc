# -*- coding: utf-8 -*-
"""
This is fabrics configuration file.
"""
from __future__ import absolute_import
from os import environ, makedirs
from os.path import exists

from fabric.api import local, quiet
from fabutils.api import (
    bump_version_file,
    infomsg,
    lint_files,
    get_changed_files,
    get_staged_files,
    rm_glob,
    sysmsg,
)

from refdoc import gen_reference_docs


__all__ = [
    'check',
    'clean',
    'devinit',
    'gendocs',
    'lint',
    'lint_changes',
    'lint_commit',
    'release',
    'test',
    'testall',
    'upload',
]


SRC_DIR = environ.get('SRC_DIR', 'src')
DIST_DIR = environ.get('DIST_DIR', 'local/dist')


def check():
    """ Run all the checks on the codebase (linting & tests). """
    lint()
    test()


def clean():
    """ Remove temporary files like python cache, swap files, etc. """
    patterns = [
        '__pycache__',
        '*.py[cod]',
        '.swp',
    ]

    for pattern in patterns:
        rm_glob(pattern)


def devinit():
    """ Initialize development environment.

    This will run in the current virtualenv (or globally if none is active at
    the moment).
    """
    sysmsg("Initializing development environment")

    infomsg("Updating pip and setuptools")
    local('pip install -U pip setuptools')

    infomsg("Installing dependencies")
    local('pip install -r requirements.txt')

    infomsg("Installing development dependencies")
    local('pip install -r devrequirements.txt')

    infomsg("Running setup.py develop")
    local('python setup.py develop')


def gendocs():
    """ Build project documentation. """
    gen_reference_docs(SRC_DIR, dst_dir='docs/ref')

    if not exists('docs/_static'):
        makedirs('docs/_static')

    local('sphinx-build -b html -d local/build/temp . docs/html')
    local('ln -f docs/html/README.html docs/html/index.html')


def lint_changes():
    """ Run pep8 and pylint against files changed since last commit. """
    if not lint_files(p for p in get_changed_files() if exists(p)):
        exit(1)


def lint_commit():
    """ Run pep8 and pylint against files staged for commit. """
    if not lint_files(p for p in get_staged_files() if exists(p)):
        exit(1)


def lint():
    """ Run pep8 and pylint on all project files. """
    if not lint_files(['{}/refdoc'.format(SRC_DIR)]):
        exit(1)


def release(component='patch', target='local'):
    with quiet():
        git_status = local('git status --porcelain', capture=True).strip()
        has_changes = len(git_status) > 0

    if has_changes:
        sysmsg("Cannot release: there are uncommitted changes")
        exit(1)

    infomsg("Bumping package version")

    old_ver, new_ver = bump_version_file('VERSION', component)
    infomsg("  old version: \033[35m{}".format(old_ver))
    infomsg("  new version: \033[35m{}".format(new_ver))

    infomsg("Uploading to pypi server \033[33m{}".format(target))
    with quiet():
        local('python setup.py sdist register -r "{}"'.format(target))
        local('python setup.py sdist upload -r "{}"'.format(target))

    # Commit the bumped version
    with quiet():
        infomsg("Creating commit that marks the release")
        local('git add VERSION && git commit -m "Release: v{}"'.format(new_ver))
        local('git tag -a "{ver}" -m "Mark {ver} release"'.format(ver=new_ver))


def test(quick=False, junit=False):
    """ Run tests against the current python version. """
    sysmsg("Running tests against the current python version")

    args = ['test/unit']

    if not quick:
        args += [
            '--cov',
            '--cov-report=term:skip-covered',
            '--cov-report=html:{}/coverage'.format(DIST_DIR),
        ]

    if junit:
        args += [
            '--junitxml={}/test-results.xml'.format(DIST_DIR),
        ]

    infomsg("Running with:\n{}".format("\n".join(args)))
    local('pytest {}'.format(' '.join(args)))


def testall():
    """ Run tests against all supported python versions. """
    sysmsg("Running tests against all supported python versions")
    local('tox')


def upload(target='local'):
    """ Release to a given pypi server ('local' by default). """
    sysmsg("Uploading to pypi server \033[33m{}".format(target))
    local('python setup.py sdist register -r "{}"'.format(target))
    local('python setup.py sdist upload -r "{}"'.format(target))
