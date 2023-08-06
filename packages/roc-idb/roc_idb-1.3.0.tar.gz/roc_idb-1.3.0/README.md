
ROC IDB
=======

[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/IDB/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/IDB/pipelines)


A plugin to manage different IDB source/version

Installation
------------

To install the roc.idb plugin:


#. Install
   a. with pip: ``pip install .``.
   b. or with poetry: ``poetry install``.
#. In ``settings.py``\ , add ``'roc.idb'`` to ``PLUGINS``.
#. Run ``manage.py piper descriptor``.

Plugin Maintenance
------------------

This plugin use `poetry <https://python-poetry.org/>`_ as primary build system but a standard ``setup.py`` can be generated using `dephell <https://github.com/dephell/dephell>`_\ :

.. code-block::

   dephell deps convert

Version bumping can be handled using:

.. code-block::

   poetry version --help

Descriptor bumping can be handled using:

.. code-block::

   poetry run python bump_descriptor.py

Editor config can be created/updated using:

.. code-block::

   dephell generate editorconfig

Pre-commit hooks can be applied using

.. code-block::

   poetry run pre-commit run -a

Publish a new tag on Gitlab
-------------------------------

1. Update the version using ``poetry version <bump_level>`` where <bump_level> can be patch, minor or major
2. Update the descriptor using ``poetry run python bump_descriptor.py``
3. Generate the new setup file using ``poetry run dephell deps convert``
4. Apply code formatters using ``poetry run pre-commit run -a``
5. Commit and tag


Authors
-------


* Sonny LION sonny.lion@obspm.fr

License
-------

This project is licensed under no License

Acknowledgments
---------------


* ROC team
