# sphinxcontrib-pylint
Sphinx-doc extension for pylint integration.

## Usage
- In *conf.py* e.g. *./tests/docs/conf.py* (sphinx-doc configuration file) insert the pylint extension options `pylint_<option> = <option value>`
- In the sphinx-doc input text file e.g. *./tests/docs/index.rst* insert `.. message-list::` at the location where the pylint messages shall be inserted as listing (actualy a table)
- The pylint messages are generated for *./tests/bzr.py* right now (usually the root directory of the source files).

## Manual acceptance test execution
- In *./tests/docs/conf.py* (sphinx-doc configuration file) let the system know about the extension using `sys.path.insert(0, os.path.abspath('../../sphinxcontrib'))` (not required when the package will be installed using setup.py)
- In *./tests/docs/conf.py* (sphinx-doc configuration file) let sphinx-doc know about the extension `extensions = ['pylint']` (instead of `extensions = [sphinxcontrib.pylint]` ~ when the package will be installed using setup.py)
- In *./tests/docs/* run `sphinx-build -b html . _build`
- Open *./tests/docs/_build/index.html* and check the listing of the pylint messages (right now fake messages are used)
