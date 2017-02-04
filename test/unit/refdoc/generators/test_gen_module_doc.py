# -*- coding: utf-8 -*-
from __future__ import absolute_import
from refdoc.toctree import Toctree
from refdoc.generators import gen_module_doc
from refdoc import rst


def test_output_contains_the_module_name_as_title():
    assert rst.title('``fake.module``') in gen_module_doc('fake.module')


def test_there_is_no_modules_section_if_toctree_is_not_given():
    assert rst.section('Modules') not in gen_module_doc('fake.module')


def test_modules_section_exists_if_toctree_is_given():
    toctree = Toctree()
    toctree.add('item1.rst')
    toctree.add('item2.rst')

    doc_src = gen_module_doc('fake.module', toctree)
    assert rst.section('Modules') in doc_src
    assert str(toctree) in doc_src


def test_automodule_directive_is_present_and_correct():
    assert rst.automodule('fake.module') in gen_module_doc('fake.module')
