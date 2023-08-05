# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['delfino_core', 'delfino_core.commands']

package_data = \
{'': ['*']}

install_requires = \
['delfino>=0.24.0']

extras_require = \
{'all': ['black',
         'isort',
         'pre-commit',
         'pytest',
         'coverage',
         'pytest-cov',
         'mypy',
         'pylint',
         'pycodestyle',
         'pydocstyle',
         'twine',
         'gitpython',
         'packaging',
         'psutil'],
 'build-docker': ['packaging'],
 'dependencies-update': ['gitpython'],
 'format': ['black', 'isort', 'pre-commit'],
 'lint': ['pylint', 'pycodestyle', 'pydocstyle', 'psutil'],
 'test': ['pytest', 'coverage', 'pytest-cov'],
 'typecheck': ['mypy'],
 'upload-to-pypi': ['twine'],
 'verify-all': ['black',
                'isort',
                'pre-commit',
                'pytest',
                'coverage',
                'pytest-cov',
                'mypy',
                'pylint',
                'pycodestyle',
                'pydocstyle',
                'psutil']}

entry_points = \
{'delfino.plugin': ['delfino-core = delfino_core.commands']}

setup_kwargs = {
    'name': 'delfino-core',
    'version': '3.3.0',
    'description': 'Delfino core plugin',
    'long_description': '<h1 align="center" style="border-bottom: none;"> 🔌&nbsp;&nbsp;Delfino Core&nbsp;&nbsp; 🔌</h1>\n<h3 align="center">A <a href="https://github.com/radeklat/delfino">Delfino</a> plugin with core functionality.</h3>\n\n<p align="center">\n    <a href="https://app.circleci.com/pipelines/github/radeklat/delfino-core?branch=main">\n        <img alt="CircleCI" src="https://img.shields.io/circleci/build/github/radeklat/delfino-core">\n    </a>\n    <a href="https://app.codecov.io/gh/radeklat/delfino-core/">\n        <img alt="Codecov" src="https://img.shields.io/codecov/c/github/radeklat/delfino-core">\n    </a>\n    <a href="https://github.com/radeklat/delfino-core/tags">\n        <img alt="GitHub tag (latest SemVer)" src="https://img.shields.io/github/tag/radeklat/delfino-core">\n    </a>\n    <img alt="Maintenance" src="https://img.shields.io/maintenance/yes/2022">\n    <a href="https://github.com/radeklat/delfino-core/commits/main">\n        <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/radeklat/delfino-core">\n    </a>\n    <a href="https://www.python.org/doc/versions/">\n        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/delfino-core">\n    </a>\n    <a href="https://pypistats.org/packages/delfino-core">\n        <img alt="Downloads" src="https://img.shields.io/pypi/dm/delfino-core">\n    </a>\n</p>\n\n# Commands\n  \n| Command               | Description                                         |\n|-----------------------|-----------------------------------------------------|\n| build-docker          | Build and push a docker image.                      |\n| coverage-open         | Open coverage results in default browser.           |\n| coverage-report       | Analyse coverage and generate a term/HTML report.   |\n| dependencies-update   | Manages the process of updating dependencies.       |\n| format                | Runs black code formatter and isort on source code. |\n| lint                  | Run linting on the entire code base.                |\n| lint-pycodestyle      | Run PEP8 checking on code.                          |\n| lint-pydocstyle       | Run docstring linting on source code.               |\n| lint-pylint           | Run pylint on code.                                 |\n| switch-python-version | Switches Python venv to a different Python version. |\n| test-all              | Run all tests, and generate coverage report.        |\n| test-integration      | Run integration tests.                              |\n| test-unit             | Run unit tests.                                     |\n| typecheck             | Run type checking on source code.                   |\n| upload-to-pypi        | Upload package to a public Pypi repository.         |\n| verify-all            | Runs all verification commands.                     |\n\n# Installation\n\n- pip: `pip install delfino-core`\n- Poetry: `poetry add -D delfino-core`\n- Pipenv: `pipenv install -d delfino-core`\n\n## Optional dependencies\n\nEach project may use different sub-set of [commands](#commands). Therefore, dependencies of all commands are optional and checked only when the command is executed.\n\nUsing `[all]` installs all the [optional dependencies](https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#optional-dependencies) used by all the commands. If you want only a sub-set of those dependencies, there are finer-grained groups available:\n\n- For individual commands (matches the command names):\n  - `upload-to-pypi`\n  - `build-docker`\n  - `typecheck`\n  - `format`\n  - `dependencies-update`\n- For groups of commands:\n  - `test` - for testing and coverage commands\n  - `lint` - for all the linting commands\n- For groups of groups:\n  - `verify-all` - same as `[typecheck,format,test,lint]`\n  - `all` - all optional packages\n\n# Configuration\n\nDelfino doesn\'t load any plugins by default. To enable this plugin, add the following config into `pyproject.toml`:\n\n```toml\n[tool.delfino.plugins.delfino-core]\n\n```\n\n## Plugin configuration\n\nThis plugin has several options. All the values are optional and defaults are shown below: \n\n```toml\n[tool.delfino.plugins.delfino-core]\n# Source files - may have different rules than tests (usually stricter)\nsources_directory = "src"\n\n# Test files\ntests_directory = "tests"\n\n# Where to store reports generated by various tools\nreports_directory = "reports"\n\n# Types of tests you have nested under the `tests_directory`. Will be executed in given order.\ntest_types = ["unit", "integration"]\n\n# Commands to run as a quality gate in given order.\nverify_commands = ["format", "lint", "typecheck", "test-all"]\n\n# Do not install pre-commit if this is set to true.\ndisable_pre_commit = false\n```\n\n## Commands configuration\n\nSeveral commands have their own configuration as well:\n\n```toml\n[tool.delfino.plugins.delfino-core.dockerhub]\n# User name for logging in into dockerhub\nusername = ""\n\n# Platforms to build with dockerx\nbuild_for_platforms = [\n    "linux/arm/v7",\n    "linux/arm64",\n    "linux/amd64",\n]\n\n[tool.delfino.plugins.delfino-core.typecheck]\n# One or more directories where type hint will be required. By default they are optional.\nstrict_directories = []  \n```\n\n# Usage\n\nRun `delfino --help`.\n\n# Development\n\nTo develop against editable `delfino` sources:\n\n1. Make sure `delfino` sources are next to this plugin:\n    ```shell\n    cd ..\n    git clone https://github.com/radeklat/delfino.git\n    ```\n2. Install `delfino` as editable package:\n    ```shell\n    pip install -e ../delfino\n    ```\n   Note that poetry will reset this to the released package when you install/update anything.\n',
    'author': 'Radek Lát',
    'author_email': 'radek.lat@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/radeklat/delfino-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
