# -*- coding: utf-8 -*-
"""
Testing commands
"""
from __future__ import absolute_import, unicode_literals
from fabric.api import lcd, local, shell_env

from .common import _is_true, _repo_path, _sysmsg, _surround_paths_with_quotes


def _run_tests(paths, **opts):
    args = []
    sugar = _is_true(opts.get(b'sugar', 'on'))
    junit = _is_true(opts.get(b'junit', 'off'))
    verbose = _is_true(opts.get(b'verbose', 'off'))
    coverage = _is_true(opts.get(b'coverage', 'on'))

    if coverage:
        args += [
            '--cov-config={}'.format(_repo_path('ops/tools/coverage.ini')),
            '--cov={}'.format(_repo_path('src/refdoc')),
            '--cov-report=term:skip-covered',
            '--cov-report=html:{}'.format(_repo_path('.build/coverage')),
        ]

    if junit:
        args += ['--junitxml={}/test-results.xml'.format('.build')]

    if not sugar:
        args += ['-p no:sugar']

    if verbose:
        args += ['-v', '-l', '--full-trace']

    with shell_env(PYTHONPATH=_repo_path('src')):
        local('pytest -c {conf} {args} {paths}'.format(
            conf=_repo_path('ops/tools/pytest.ini'),
            args=' '.join(args),
            paths=_surround_paths_with_quotes(_repo_path(p) for p in paths)
        ))


def testall():
    """ Run tests against all supported python versions using tox. """
    _sysmsg("Running tests against all supported python versions using ^35tox")
    with lcd(_repo_path('.')):
        local('tox')


def test(**opts):
    """ Run all tests against the current python version. """
    _sysmsg("Running all tests")
    with lcd(_repo_path('.')):
        _run_tests(['test'], **opts)


def unittest(**opts):
    """ Run unit tests against the current python version. """
    _sysmsg("Running unit tests")
    with lcd(_repo_path('.')):
        _run_tests(['test/unit'], **opts)


def apitest(**opts):
    """ Run API tests against the current python version. """
    _sysmsg("Running api tests")
    with lcd(_repo_path('.')):
        _run_tests(['test/api'], **opts)
