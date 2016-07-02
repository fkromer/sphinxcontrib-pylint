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
copyright = u'2016, thinwybk'
version = '0.1'
release = '0.1'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']

# Options for pylint
pylint_package_dir = '../package'
pylint_debug = True
pylint_ignore = ''
pylint_jobs = '2'
pylint_confidence = 'UNDEFINED'
pylint_enable = 'classes'
pylint_disable = 'similarities'
