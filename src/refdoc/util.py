# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import namedtuple
from os import walk, sep
from os.path import relpath


Package = namedtuple('Package', 'fullname path relpath modules')
"""
Represents a python package. This is all the information needed to generate
the documentation for the given package.

:var fullname:  Package fully qualified name.
:var path:      Path to the package.
:var relpath:   Package path relative to the source directory.
:var modules:   A list of python modules within the package.
"""


def gen_ref_file_tree(pkgs):
    """ Generate a nice tree for the reference documentation files.

    :param list<Package> pkgs:
        List of documented packages.
    :return str:
        A tree ready to be printed with fixed-width font.
    """
    lines = []
    pkg_count = len(pkgs)

    for i, pkg in enumerate(pkgs):
        if i < pkg_count - 1:
            prefix = '|   '
            lines.append("├── {}".format(pkg.fullname))
        else:
            prefix = '    '
            lines.append("└── {}".format(pkg.fullname))

        mod_count = len(pkg.modules)
        for j, module in enumerate(pkg.modules):
            if j < mod_count - 1:
                lines.append(prefix + "├── {}".format(module))
            else:
                lines.append(prefix + "└── {}".format(module))

    return '\n'.join(lines)


def get_packages(rootdir):
    """ Find all packages in the given root directory

    :param rootdir:
    :return:
    """
    pkgs = []

    for path, _, files in walk(rootdir):
        if '__init__.py' not in files:
            continue

        rel_path = relpath(path, rootdir)

        pkgs.append(Package(
            fullname=rel_path.replace(sep, '.'),
            path=path,
            relpath=rel_path,
            modules=[
                f[:-3] for f in files
                if f.endswith('.py') and f != '__init__.py'
            ]
        ))

    return pkgs
