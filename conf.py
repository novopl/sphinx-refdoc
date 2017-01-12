# -*- coding: utf-8 -*-
import os
project = u"sphinx-refdoc"
copyright = u"2016, Mateusz 'novo' Klos"
author = u"Mateusz 'novo' Klos"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
]

version = read('VERSION').strip()
release = read('VERSION').strip()
doctest_test_doctest_blocks='default'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'README'
language = None
exclude_patterns = [
    '_build',
    'env',
    'tmp',
    '.tox',
    'Thumbs.db',
    '.DS_Store'
]
todo_include_todos = False
intersphinx_mapping = {'https://docs.python.org/': None}

pygments_style = 'monokai'
html_theme = 'bizstyle'
html_static_path = ['docs/_static']
htmlhelp_basename = 'sphinxrefdoc'

latex_elements = {}
latex_documents = [
    (master_doc, 'sphinx-refdoc.tex', 'sphinx-refdoc Documentation',
     'Mateusz \'novo\' Klos', 'manual'),
]
man_pages = [
    (master_doc, 'sphinx-refdoc', 'sphinx-refdoc Documentation', [author], 1)
]
texinfo_documents = [
    (master_doc, 'sphinx-refdoc', 'sphinx-refdoc Documentation',
     author, 'sphinx-refdoc', 'One line description of project.',
     'Miscellaneous'),
]
