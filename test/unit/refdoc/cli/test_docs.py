# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import
from mock import patch
from click.testing import CliRunner
from refdoc.cli import docs


@patch('refdoc.logic.generate_docs')
def test_uses_gen_reference_docs(generate_docs):
    runner = CliRunner()

    result = runner.invoke(docs, ['-i', 'src', '-o', 'dst'])

    assert result.exit_code == 0
    generate_docs.assert_called_once_with(('src',), 'dst', False, 0)
