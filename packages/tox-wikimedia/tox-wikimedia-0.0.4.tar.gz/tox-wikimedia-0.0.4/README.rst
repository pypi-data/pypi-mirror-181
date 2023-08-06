tox-wikimedia
=============

Automatically configure tox environments to use standard tools in a
hopefully unobtrusive way.

For example::

    [tox]
    envlist=py{34,35,36,37}-{flake8,pytest},py37-{mypy}
    skip_missing_interpreters = True
    requires = tox-wikimedia

    [wikimedia]
    mypy_package = mypackage

The following tools are supported for now:

flake8
------
flake8_: "the modular source code checker: pep8, pyflakes and co"

Command executed: ``flake8``

Dependencies installed: ``flake8``

mypy
----
mypy_: "Optional static typing for Python"

Command executed: ``mypy {mypy_package}``

Dependencies installed: ``mypy``, ``requirements.txt`` (if exists),
``test-requirements.txt`` (if exists)

pytest
------
pytest_: "pytest: simple powerful testing with Python"

Command executed: ``pytest``

Dependencies installed: ``pytest``, ``requirements.txt`` (if exists),
``test-requirements.txt`` (if exists)

.. _flake8: https://pypi.org/project/flake8/
.. _mypy: http://www.mypy-lang.org/
.. _pytest: https://pytest.org/en/latest/
