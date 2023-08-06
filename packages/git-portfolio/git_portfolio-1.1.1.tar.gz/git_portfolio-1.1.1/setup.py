# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['git_portfolio',
 'git_portfolio.domain',
 'git_portfolio.request_objects',
 'git_portfolio.use_cases']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0,<9', 'github3.py>=3.2.0', 'inquirer>=2.10.1', 'pyyaml>=5.3.1']

entry_points = \
{'console_scripts': ['gitp = git_portfolio.__main__:main']}

setup_kwargs = {
    'name': 'git-portfolio',
    'version': '1.1.1',
    'description': 'Git Portfolio',
    'long_description': "Git Portfolio\n=============\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/git-portfolio.svg\n   :target: https://pypi.org/project/git-portfolio/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/git-portfolio\n   :target: https://pypi.org/project/git-portfolio\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/git-portfolio\n   :target: https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/git-portfolio/latest.svg?label=Read%20the%20Docs\n   :target: https://git-portfolio.readthedocs.io/\n   :alt: Read the documentation at https://git-portfolio.readthedocs.io/\n.. |Tests| image:: https://github.com/staticdev/git-portfolio/workflows/Tests/badge.svg\n   :target: https://github.com/staticdev/git-portfolio/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/staticdev/git-portfolio/branch/main/graph/badge.svg\n   :target: https://app.codecov.io/gh/staticdev/git-portfolio\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* Configure multiple working repositories.\n* Batch git_ commands with subcommands: ``add``, ``branch``, ``checkout``, ``commit``, ``diff``, ``fetch``, ``init``, ``merge``, ``mv``, ``pull``, ``push``, ``rebase``, ``reset``, ``rm``, ``show``, ``switch``, ``status`` and ``tag``.\n* Batch API calls on GitHub_: create/close/reopen ``issues``, create/close/reopen/merge ``pull requests`` and delete ``branches`` by name.\n* Batch Poetry_ commands such as: ``add``, ``version patch``, ``install`` or ``update``.\n\n\nRequirements\n------------\n\n* `Create an auth token for GitHub`_, with the ``repo`` privileges enabled by clicking on Generate new token. You will be asked to select scopes for the token. Which scopes you choose will determine what information and actions you will be able to perform against the API. You should be careful with the ones prefixed with write:, delete: and admin: as these might be quite destructive. You can find description of each scope in docs here.\n\nImportant: safeguard your token (once created you won't be able to see it again).\n\n* Install git_ (optional) -  this is needed for all git_ commands. For colored outputs please use the configuration:\n\n.. code:: console\n\n   $ git config --global color.ui always\n\n\nInstallation\n------------\n\nYou can install *Git Portfolio* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install git-portfolio\n\n\n.. basic-usage\n\nBasic usage\n-----------\n\n1. Create initial configuration with:\n\n.. code:: console\n\n   $ gitp config init\n\n\n2. Execute all the commands you want. Eg.:\n\n.. code:: console\n\n   $ gitp issues create  # create same issue for all projects\n   $ gitp checkout -b new-branch  # checks out new branch new-branch in all projects\n   $ gitp poetry version minor  # bumps minor version of all projects that have pyproject.toml version\n\nNote: by convention GitHub commands are always the resource name and action: eg. ``branches delete``, ``issues create`` and ``prs merge`` (for pull requests).\nThis avoid conflicts with batch git commands, as in ``gitp branch`` (executes git command) and ``gitp branches delete`` (execute operations using GitHub API).\n\n\n.. end-basic-usage\n\nComplete instructions can be found at `git-portfolio.readthedocs.io`_.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Git Portfolio* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _Create an auth token for GitHub: https://github.com/settings/tokens\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _git: https://git-scm.com\n.. _GitHub: https://github.com\n.. _MIT: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/staticdev/git-portfolio/issues\n.. _pip: https://pip.pypa.io/\n.. _Poetry: https://python-poetry.org/\n.. _git-portfolio.readthedocs.io: https://git-portfolio.readthedocs.io\n.. github-only\n.. _Contributor Guide: https://git-portfolio.readthedocs.io/en/latest/contributing.html\n",
    'author': 'staticdev',
    'author_email': 'staticdev-support@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/staticdev/git-portfolio',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0',
}


setup(**setup_kwargs)
