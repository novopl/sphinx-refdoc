# -*- coding: utf-8 -*-
"""
Helper commands for releasing to pypi.
"""
from __future__ import absolute_import, unicode_literals
from fabric.api import local

from .common import _bump_version_file, _inside_repo, _repo_path, _sysmsg


def release(component='patch', target='local'):
    """ Release a new version of the project.

    This will bump the version number (patch component by default) + add and tag
    a commit with that change. Finally it will upload the package to pypi.
    """
    with _inside_repo(quiet=True):
        git_status = local('git status --porcelain', capture=True).strip()
        has_changes = len(git_status) > 0

    if has_changes:
        _sysmsg("Cannot release: there are uncommitted changes")
        exit(1)

    _sysmsg("Bumping package version")
    old_ver, new_ver = _bump_version_file(_repo_path('VERSION'), component)

    _sysmsg("  old version: ^35{}".format(old_ver))
    _sysmsg("  new version: ^35{}".format(new_ver))

    _sysmsg("Creating commit that marks the release")
    with _inside_repo(quiet=True):
        local('git add VERSION && git commit -m "Release: v{}"'.format(new_ver))
        local('git tag -a "{ver}" -m "Mark {ver} release"'.format(ver=new_ver))

    _sysmsg("Uploading to pypi server ^33{}".format(target))
    with _inside_repo(quiet=True):
        local('python setup.py sdist register -r "{}"'.format(target))
        local('python setup.py sdist upload -r "{}"'.format(target))


def upload(target='local'):
    """ Release to a given pypi server ('local' by default). """
    _sysmsg("Uploading to pypi server ^33{}".format(target))
    with _inside_repo(quiet=True):
        local('python setup.py sdist register -r "{}"'.format(target))
        local('python setup.py sdist upload -r "{}"'.format(target))
