Fast JSON Pointer
=================

.. inclusion-marker-do-not-remove

.. _RFC 6901: https://www.rfc-editor.org/rfc/rfc6901
.. _relative JSON pointer: https://json-schema.org/draft/2020-12/relative-json-pointer

Implements `RFC 6901`_ JSON pointers, and `relative JSON pointer`_ resolution.

This module is not necissarily fast (yet), but there are enough variations on
``json-pointer`` in pypi to merit picking some prefix to differentiate, and "fast"
seemed a relatively short and punchy choice.

If you need this to *really* be fast, open an issue and let me know. I want to do
a rust extension module at some point. That ought to be fast enough to claim we're
fast.

.. list-table::

   * - Package
     - |pypi| |license| |py status| |formats| |python| |py impls| |downloads|
   * - build
     - |checks| |rtd build| |coverage|
   * - Git
     - |last commit| |commit activity| |commits since| |issues| |prs|

.. |pypi| image:: https://img.shields.io/pypi/v/fast-json-pointer
   :target: https://pypi.org/project/fast-json-pointer/
   :alt: PyPI
   
.. |downloads| image:: https://img.shields.io/pypi/dm/fast-json-pointer
   :target: https://pypistats.org/packages/fast-json-pointer
   :alt: PyPI - Downloads

.. |formats| image:: https://img.shields.io/pypi/format/fast-json-pointer
   :target: https://pypi.org/project/fast-json-pointer/
   :alt: PyPI - Format

.. |py status| image:: https://img.shields.io/pypi/status/fast-json-pointer
   :target: https://pypi.org/project/fast-json-pointer/
   :alt: PyPI - Status

.. |py impls| image:: https://img.shields.io/pypi/implementation/fast-json-pointer
   :target: https://pypi.org/project/fast-json-pointer/
   :alt: PyPI - Implementation

.. |python| image:: https://img.shields.io/pypi/pyversions/fast-json-pointer
   :target: https://pypi.org/project/fast-json-pointer/
   :alt: PyPI - Python Version

.. |license| image:: https://img.shields.io/github/license/slowAPI/fast-json-pointer
   :target: https://github.com/slowAPI/fast-json-pointer
   :alt: GitHub

.. |checks| image:: https://img.shields.io/github/checks-status/slowAPI/fast-json-pointer/main?logo=github
   :target: https://github.com/slowAPI/fast-json-pointer
   :alt: GitHub branch checks state

.. |rtd build| image:: https://img.shields.io/readthedocs/fast-json-pointer
   :target: https://fast-json-pointer.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs

.. |coverage| image:: https://coveralls.io/repos/github/SlowAPI/fast-json-pointer/badge.svg?branch=main
   :target: https://coveralls.io/github/SlowAPI/fast-json-pointer?branch=main
   :alt: Coverage

.. |last commit| image:: https://img.shields.io/github/last-commit/slowAPI/fast-json-pointer
   :target: https://github.com/slowAPI/fast-json-pointer
   :alt: GitHub last commit

.. |commit activity| image:: https://img.shields.io/github/commit-activity/m/slowAPI/fast-json-pointer
   :target: https://github.com/slowAPI/fast-json-pointer
   :alt: GitHub commit activity

.. |commits since| image:: https://img.shields.io/github/commits-since/slowAPI/fast-json-pointer/latest
   :target: https://github.com/slowAPI/fast-json-pointer
   :alt: GitHub commits since latest release (by SemVer)

.. |issues| image:: https://img.shields.io/github/issues/slowAPI/fast-json-pointer
   :target: https://github.com/SlowAPI/fast-json-pointer/issues
   :alt: GitHub issues

.. |prs| image:: https://img.shields.io/github/issues-pr/slowAPI/fast-json-pointer
   :target: https://github.com/SlowAPI/fast-json-pointer/pulls
   :alt: GitHub pull requests