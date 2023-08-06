# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fast_json_pointer']

package_data = \
{'': ['*']}

extras_require = \
{'cli': ['typer[all]>=0.7.0,<0.8.0']}

entry_points = \
{'console_scripts': ['fjp = fast_json_pointer.cli:app']}

setup_kwargs = {
    'name': 'fast-json-pointer',
    'version': '0.3.3',
    'description': 'Implements RFC 6901 JSON pointers, and json-schema draft relative pointer resolution.',
    'long_description': 'Fast JSON Pointer\n=================\n\n.. inclusion-marker-do-not-remove\n\n.. _RFC 6901: https://www.rfc-editor.org/rfc/rfc6901\n.. _relative JSON pointer: https://json-schema.org/draft/2020-12/relative-json-pointer\n\nImplements `RFC 6901`_ JSON pointers, and `relative JSON pointer`_ resolution.\n\nThis module is not necissarily fast (yet), but there are enough variations on\n``json-pointer`` in pypi to merit picking some prefix to differentiate, and "fast"\nseemed a relatively short and punchy choice.\n\nIf you need this to *really* be fast, open an issue and let me know. I want to do\na rust extension module at some point. That ought to be fast enough to claim we\'re\nfast.\n\n.. list-table::\n\n   * - Package\n     - |pypi| |license| |py status| |formats| |python| |py impls| |downloads|\n   * - build\n     - |checks| |rtd build| |coverage|\n   * - Git\n     - |last commit| |commit activity| |commits since| |issues| |prs|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/fast-json-pointer\n   :target: https://pypi.org/project/fast-json-pointer/\n   :alt: PyPI\n   \n.. |downloads| image:: https://img.shields.io/pypi/dm/fast-json-pointer\n   :target: https://pypistats.org/packages/fast-json-pointer\n   :alt: PyPI - Downloads\n\n.. |formats| image:: https://img.shields.io/pypi/format/fast-json-pointer\n   :target: https://pypi.org/project/fast-json-pointer/\n   :alt: PyPI - Format\n\n.. |py status| image:: https://img.shields.io/pypi/status/fast-json-pointer\n   :target: https://pypi.org/project/fast-json-pointer/\n   :alt: PyPI - Status\n\n.. |py impls| image:: https://img.shields.io/pypi/implementation/fast-json-pointer\n   :target: https://pypi.org/project/fast-json-pointer/\n   :alt: PyPI - Implementation\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/fast-json-pointer\n   :target: https://pypi.org/project/fast-json-pointer/\n   :alt: PyPI - Python Version\n\n.. |license| image:: https://img.shields.io/github/license/slowAPI/fast-json-pointer\n   :target: https://github.com/slowAPI/fast-json-pointer\n   :alt: GitHub\n\n.. |checks| image:: https://img.shields.io/github/checks-status/slowAPI/fast-json-pointer/main?logo=github\n   :target: https://github.com/slowAPI/fast-json-pointer\n   :alt: GitHub branch checks state\n\n.. |rtd build| image:: https://img.shields.io/readthedocs/fast-json-pointer\n   :target: https://fast-json-pointer.readthedocs.io/en/latest/?badge=latest\n   :alt: Read the Docs\n\n.. |coverage| image:: https://coveralls.io/repos/github/SlowAPI/fast-json-pointer/badge.svg?branch=main\n   :target: https://coveralls.io/github/SlowAPI/fast-json-pointer?branch=main\n   :alt: Coverage\n\n.. |last commit| image:: https://img.shields.io/github/last-commit/slowAPI/fast-json-pointer\n   :target: https://github.com/slowAPI/fast-json-pointer\n   :alt: GitHub last commit\n\n.. |commit activity| image:: https://img.shields.io/github/commit-activity/m/slowAPI/fast-json-pointer\n   :target: https://github.com/slowAPI/fast-json-pointer\n   :alt: GitHub commit activity\n\n.. |commits since| image:: https://img.shields.io/github/commits-since/slowAPI/fast-json-pointer/latest\n   :target: https://github.com/slowAPI/fast-json-pointer\n   :alt: GitHub commits since latest release (by SemVer)\n\n.. |issues| image:: https://img.shields.io/github/issues/slowAPI/fast-json-pointer\n   :target: https://github.com/SlowAPI/fast-json-pointer/issues\n   :alt: GitHub issues\n\n.. |prs| image:: https://img.shields.io/github/issues-pr/slowAPI/fast-json-pointer\n   :target: https://github.com/SlowAPI/fast-json-pointer/pulls\n   :alt: GitHub pull requests',
    'author': 'Tristan Sweeney',
    'author_email': 'sweeneytri@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SlowAPI/py-json-pointer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
