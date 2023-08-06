# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_git_version_plugin']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.29,<4.0.0', 'poetry>=1.2.0,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['poetry-git-version-plugin = '
                               'poetry_git_version_plugin.plugins:PoetryGitVersionApplicationPlugin'],
 'poetry.plugin': ['poetry-git-version-plugin = '
                   'poetry_git_version_plugin.plugins:PoetryGitVersionPlugin']}

setup_kwargs = {
    'name': 'poetry-git-version-plugin',
    'version': '0.0.5',
    'description': 'Poetry plugin to get package version from git',
    'long_description': '# Poetry Git Version Plugin\n\nPoetry plugin to get package version from git.\n\n> Descendant of `poetry-version-plugin`, which **does not work** on `poetry 1.2.0`.\n\n## Functionality\n\n- Project tag parsing\n- Substitution of the project tag (if any) in the poetry.version value\n- Maintenance of PEP 440\n- Command to output a new version\n\n## Quick start\n\n```bash\npoetry self add poetry-git-version-plugin\npoetry git-version # Write your git tag\npoetry -v git-version # print process\n```\n\n## Dependencies\n\n```toml\n[tool.poetry.dependencies]\npython = ">=3.10"\npoetry = ">=1.2.0"\n```\n\n## Setup\n\n```toml\n[tool.poetry-git-version-plugin]\n# Ignore "tag missing" errors\nignore_exception = true\n\n# If the tag is missing.\n# Returns a version, computed from the latest version tag.\n# It takes the version tag, increases the version tag by the number of commits since, adds a local label specifying the git commit hash and the dirty status.\n# Example: 1.3.2+5-5babef6\nuse_last_tag = true\n```\n\n## Contribute\n\nIssue Tracker: <https://gitlab.com/rocshers/python/poetry-git-version-plugin/-/issues>  \nSource Code: <https://gitlab.com/rocshers/python/poetry-git-version-plugin>\n',
    'author': 'irocshers',
    'author_email': 'develop.iam@rocshers.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/rocshers/python/poetry-git-version-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
