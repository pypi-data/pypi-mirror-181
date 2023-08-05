# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['atap_widgets']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.0,<3.0',
 'dask[dataframe]>=2022.9.2,<2023.0.0',
 'ipywidgets>=8.0,<9.0',
 'openpyxl',
 'pandas>=1.3,<2.0',
 'spacy>=3.0,<4.0',
 'textacy',
 'xlsxwriter>=3,<4']

setup_kwargs = {
    'name': 'atap-widgets',
    'version': '0.5.0',
    'description': 'Interactive widgets used by the Australian Text Analytics Platform',
    'long_description': "atap_widgets\n==============\n\n|PyPI| |Status| |Python Version|\n\n|Read the Docs| |Tests| |License|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/atap_widgets.svg\n   :target: https://pypi.org/project/atap_widgets/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/atap_widgets.svg\n   :target: https://pypi.org/project/atap_widgets/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/atap_widgets\n   :target: https://pypi.org/project/atap_widgets\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/atap_widgets\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/atap_widgets/latest.svg?label=Read%20the%20Docs\n   :target: https://atap_widgets.readthedocs.io/\n   :alt: Read the documentation at https://atap_widgets.readthedocs.io/\n.. |Tests| image:: https://github.com/Australian-Text-Analytics-Platform/atap_widgets/actions/workflows/tests.yml/badge.svg\n   :target: https://github.com/Australian-Text-Analytics-Platform/atap_widgets/actions?workflow=Tests\n   :alt: Tests\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nThis package is part of the atap_ project.\n\nFeatures\n--------\n\n* Conversation recurrence plotting\n* Concordance search and export\n\n\nRequirements\n------------\n\n* Python 3.8+\n* spacy\n* pandas\n* Interactive widgets are designed for use in Jupyter Lab (3+)\n\n\nInstallation\n------------\n\nYou can install *atap_widgets* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install atap_widgets\n\n**NOTE**: on M1 Macs with the new Apple Silicon chip, you may need a Rust compiler installed. Rust can be installed with a single command via https://rustup.rs/ . You may also need `cmake`: install via Homebrew with `brew install cmake`.\n\nDevelopment\n------------\n\nThis project uses poetry_ for dependency management and\npackaging. Please see the poetry_ docs for details.\nDependencies are specified in ``pyproject.toml``.\n\nThis repository is configured to automatically publish\nnew releases to PyPI if you merge a pull request with\nan updated version number. That means to release\na new version with new features/fixes, you should:\n\n* Create a branch\n* Perform your work on that branch\n* Update the package version, e.g. with ``poetry version patch`` or ``poetry version minor``\n* Commit the changes to ``pyproject.toml``\n* Create a pull request for the branch on GitHub\n* Merge the branch into ``main`` when you're ready to release\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*atap_widgets* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/Australian-Text-Analytics-Platform/atap_widgets/issues\n.. _pip: https://pip.pypa.io/\n.. _poetry: https://python-poetry.org/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://atap_widgets.readthedocs.io/en/latest/usage.html\n.. _atap: https://www.atap.edu.au/\n",
    'author': 'Marius Mather',
    'author_email': 'marius.mather@sydney.edu.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Australian-Text-Analytics-Platform/atap_widgets',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
