# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.idb',
 'roc.idb.commands',
 'roc.idb.converters',
 'roc.idb.models',
 'roc.idb.models.music',
 'roc.idb.models.versions',
 'roc.idb.parsers',
 'roc.idb.parsers.mib_parser',
 'roc.idb.parsers.palisade_parser',
 'roc.idb.parsers.srdb_parser',
 'roc.idb.tasks',
 'roc.idb.tests',
 'roc.idb.tools']

package_data = \
{'': ['*']}

install_requires = \
['poppy-core>=0.9.4', 'poppy-pop>=0.7.5', 'sqlalchemy', 'xlwt==1.3.0']

setup_kwargs = {
    'name': 'roc-idb',
    'version': '1.3.0',
    'description': 'Plugin to manage the IDB',
    'long_description': "\nROC IDB\n=======\n\n[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/IDB/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/IDB/pipelines)\n\n\nA plugin to manage different IDB source/version\n\nInstallation\n------------\n\nTo install the roc.idb plugin:\n\n\n#. Install\n   a. with pip: ``pip install .``.\n   b. or with poetry: ``poetry install``.\n#. In ``settings.py``\\ , add ``'roc.idb'`` to ``PLUGINS``.\n#. Run ``manage.py piper descriptor``.\n\nPlugin Maintenance\n------------------\n\nThis plugin use `poetry <https://python-poetry.org/>`_ as primary build system but a standard ``setup.py`` can be generated using `dephell <https://github.com/dephell/dephell>`_\\ :\n\n.. code-block::\n\n   dephell deps convert\n\nVersion bumping can be handled using:\n\n.. code-block::\n\n   poetry version --help\n\nDescriptor bumping can be handled using:\n\n.. code-block::\n\n   poetry run python bump_descriptor.py\n\nEditor config can be created/updated using:\n\n.. code-block::\n\n   dephell generate editorconfig\n\nPre-commit hooks can be applied using\n\n.. code-block::\n\n   poetry run pre-commit run -a\n\nPublish a new tag on Gitlab\n-------------------------------\n\n1. Update the version using ``poetry version <bump_level>`` where <bump_level> can be patch, minor or major\n2. Update the descriptor using ``poetry run python bump_descriptor.py``\n3. Generate the new setup file using ``poetry run dephell deps convert``\n4. Apply code formatters using ``poetry run pre-commit run -a``\n5. Commit and tag\n\n\nAuthors\n-------\n\n\n* Sonny LION sonny.lion@obspm.fr\n\nLicense\n-------\n\nThis project is licensed under no License\n\nAcknowledgments\n---------------\n\n\n* ROC team\n",
    'author': 'Sonny LION',
    'author_email': 'sonny.lion@obspm.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/IDB',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
