.. badges


.. package version
.. image:: https://img.shields.io/pypi/v/pyalmostnothing.svg
    :target: https://pypi.org/project/pytest/

.. python versions
.. image:: https://img.shields.io/pypi/pyversions/pyalmostnothing.svg
    :target: https://pypi.org/project/pytest/

.. black
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. codecov
.. image:: https://codecov.io/gh/nazime/pyalmostnothing/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/nazime/pyalmostnothing

.. travis
.. image:: https://travis-ci.com/Nazime/pyalmostnothing.svg?branch=master
  :target: https://travis-ci.com/Nazime/pyalmostnothing

-------------------

pyalmostnothing
===============

pyalmostnothing is python project that does (almost) nothing,
it only show how to structure python projects, test project,
document project, workflow of project, plugin system for a project, ...


features
--------

- public repository
- github
- pytest for unit testing
- tox for ...
- installable with setup.py
- documentation with sphinx
- readthedocs
- coverage (codecov)
- code quality
- how to test coverage?
- CI with travis

    - testing with tox
    - deploy to Pypi


TODO
----

List of TODO to configure project


- Application or Library?
- Public or Private repository?
- Supported environments (py27, py35, py36, pypy, conda, ...)
- Supported OS? (linux, mac, windows)
- CI travis, appveyor, azure piplines?





Features
========

install
-------

.. code:: bash

    pip install <project_name>




Package
-------

The following code work

.. code:: python

    import pyalmostnothing

    print(pyalmostnothing.inc(5))
    # 6
    print(pyalmostnothing.add(3, 6))
    # 9


CLI
---

Can use it in the console

.. code:: bash

    pycalculate inc 5
    # 6
    pycalculate add 5 5
    # 10


Logs
----

Each operation is logged

.. code:: bash


    cat ~/.pycalculate/logs.txt
    inc 5
    add 5 5







Workflow
========

create similar project
----------------------
Cookie cutter

Test the project
----------------

tox --showconfig
tox -vvvvvv  # 3 tox 3 pytest
tox -r  # recreate

.. code:: bash

    git clone <project url>
    pip install tox
    tox

Retest the project

.. code:: bash

    tox

If it doesnt work

.. code:: bash

    # -r recreate
    tox -r

Test only one env

.. code:: bash

    tox -l  # list all envs
    tox -e <env>  # Ex: tox -e py37 for python3.7

Interact with the project
-------------------------
First must run ``tox`` and then chose un environment

.. code:: bash

    tox -l  # list aff environments
    source .tox/<env>/bin/activate  # Ex: source .tox/py37/bin/activate
    deactivate  # to Exit env

Integration with pycharm
------------------------
First run ``tox`` to have the environment, install the plugin
``PyVenv Manage`` and select an environment.

must install pygments in the current environments so that pycharm
can render the ``code`` blocks.

- create venv
- map key (list des racourcies
- run tests
- Editor -> inspections?
- src mark directory as src
- change testrunner to pytest


HTML coverage manually
----------------------


Automatic deploy yo pypi
------------------------
First deploy it manually (to create a scope in Pypi for security reason)

.. code:: bash

    rm -rf dist  # remove folder if exist
    python setup.py sdist bdist_wheel
    # Check if you can upload the package
    twine check dist/*
    twine upload dist/*


Make sure you have ruby install to get travis

.. code:: bash

    sudo apt-get install ruby-dev
    sudo gem install travis


How it work?
============

coverage local
--------------
use the ``parallel`` mode to create separate files and then use ``combine``
to merge them. Use ``branch`` to cover conditions statements.


coverage with codecov
---------------------

- automatically merge coverages from different builds
- need an uploader ``pip install codecov`` and call ``codecov`` after CI builds
- we don't need codecov in tox we only need it in travis
