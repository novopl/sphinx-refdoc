# -*- coding: utf-8 -*-
from __future__ import absolute_import
from mock import patch
from click.testing import CliRunner
from refdoc.cli import gendocs


@patch('refdoc.cli.gen_reference_docs')
def test_uses_gen_reference_docs(gen_reference_docs):
    runner = CliRunner()

    result = runner.invoke(gendocs, ['src', 'dst'])

    assert result.exit_code == 0
    gen_reference_docs.assert_called_once_with('src', 'dst')
