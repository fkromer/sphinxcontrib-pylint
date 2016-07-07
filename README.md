# sphinxcontrib-pylint
Sphinx-doc extension for pylint integration.

Developed and tested with pylint 1.5.5, astroid 1.4.5 and Python 3.4.3.

## Usage
- In *conf.py* e.g. *./tests/docs/conf.py* (sphinx-doc configuration file) insert
  the pylint extension options `pylint_<option> = <option value>`.
  `pylint_package_dir` needs to be set relative to the sphinx-doc srcdir
  (usually <project>/docs/ where conf.py is located in).
- In the sphinx-doc input text file e.g. *./tests/docs/index.rst* insert
  `.. message-list::` at the location where the pylint messages shall be inserted
  as listing (actualy a table).
- In the sphinx-doc input text file e.g. *./tests/docs/index.rst* insert
  `.. package-diagram::` at the location where the pyreverse diagram shall be
  inserted (inlining of pyreverse *.dot output into graphviz directive)
- In the sphinx-doc input text file e.g. *./tests/docs/index.rst* insert
  `.. class-diagram::` at the location where the pyreverse class diagram shall be
  inserted for the class of interest (inlining of pyreverse *.dot output into graphviz directive).

- The pylint messages are generated for *./tests/package/test.py* (on a file-by-file basis right now).

## Manual acceptance test execution
- In *./tests/docs/conf.py* (sphinx-doc configuration file) let the system know
  about the extension using `sys.path.insert(0, os.path.abspath('../../sphinxcontrib'))`
  (not required when the package will be installed using setup.py) with the option
  `pylint_debug=True` for debug output. 
- In *./tests/docs/conf.py* (sphinx-doc configuration file) let sphinx-doc know
  about the extension `extensions = ['pylint']` (instead of `extensions = [sphinxcontrib.pylint]`
  ~ when the package will be installed using setup.py).
- In *./tests/docs/* run `sphinx-build -b html . _build`.
- Open *./tests/docs/_build/index.html* and check the listing of the pylint messages
  (right now fake messages are used).
