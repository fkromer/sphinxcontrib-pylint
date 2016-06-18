# -*- coding: utf-8 -*-

import sys
import os

# manual build: sphinx-build -b html . _build

sys.path.insert(0, os.path.abspath('../../sphinxcontrib')) # manual build: use this statement

extensions = ['pylint'] # manual build: pylint instead of sphinxcontrib.pylint
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'test'
copyright = u'2013, thinwybk'
version = '1.0'
release = '1.0'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']

# Options for pylint
pylint_debug = True
pylint_ignore = ''
pylint_jobs = '2'
pylint_confidence = 'UNDEFINED'
pylint_enable = 'classes'
pylint_disable = 'similarities'
