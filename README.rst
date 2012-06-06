Setuptools flakes command
=========================

This package expose `pyflakes`_ as flakes command to setup.py.
It is a fork of `Zooko O'Whielacronx`_ code.

.. _`Zooko O'Whielacronx`: http://pypi.python.org/pypi/setuptools_pyflakes/1.0.5
.. _`pyflakes`: http://pypi.python.org/pypi/pyflakes

Usage
-----

::

  python setup.py flakes
  python setup.py flakes --exclude-packages=foo.bar,baz.qux
  python setup.py flakes --file=./results.log
