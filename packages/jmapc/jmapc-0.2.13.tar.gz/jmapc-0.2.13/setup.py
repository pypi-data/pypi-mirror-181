# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jmapc', 'jmapc.fastmail', 'jmapc.methods', 'jmapc.models']

package_data = \
{'': ['*']}

install_requires = \
['brotli>=1.0.9',
 'dataclasses-json',
 'python-dateutil',
 'requests',
 'sseclient']

setup_kwargs = {
    'name': 'jmapc',
    'version': '0.2.13',
    'description': 'JMAP client library for Python',
    'long_description': '# jmapc: A [JMAP][jmapio] client library for Python\n\n[![PyPI](https://img.shields.io/pypi/v/jmapc)][pypi]\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jmapc)][pypi]\n[![Build](https://img.shields.io/github/checks-status/smkent/jmapc/main?label=build)][gh-actions]\n[![codecov](https://codecov.io/gh/smkent/jmapc/branch/main/graph/badge.svg)][codecov]\n[![GitHub stars](https://img.shields.io/github/stars/smkent/jmapc?style=social)][repo]\n\n[![jmapc][logo]](#)\n\nCurrently implemented:\n\n* Basic models\n* Request methods:\n  * `Core/echo`\n  * `Email/changes`\n  * `Email/copy`\n  * `Email/get`\n  * `Email/query`\n  * `Email/queryChanges`\n  * `Email/set`\n  * `EmailSubmission/*` (`get`, `changes`, `query`, `queryChanges`, `set`)\n  * `Identity/*` (`get`, `changes`, `set`)\n  * `Mailbox/*` (`get`, `changes`, `query`, `queryChanges`, `set`)\n  * `SearchSnippet/*` (`get`)\n  * `Thread/*` (`get`, `changes`)\n  * Arbitrary methods via the `CustomMethod` class\n* Fastmail-specific methods:\n  * [`MaskedEmail/*` (`get`, `set`)][fastmail-maskedemail]\n* Combined requests with support for result references\n* Basic JMAP method response error handling\n* EventSource event handling\n* Unit tests for basic functionality and methods\n\n## Installation\n\n[jmapc is available on PyPI][pypi]:\n\n```console\npip install jmapc\n```\n\n## Examples\n\nAny of the included examples can be invoked with `poetry run`:\n\n```console\nJMAP_HOST=jmap.example.com \\\nJMAP_API_TOKEN=ness__pk_fire \\\npoetry run examples/identity_get.py\n```\n\nIf successful, `examples/identity_get.py` should output something like:\n\n```\nIdentity 12345 is for Ness at ness@onett.example.com\nIdentity 67890 is for Ness at ness-alternate@onett.example.com\n```\n\n## Development\n\n### [Poetry][poetry] installation\n\nVia [`pipx`][pipx]:\n\n```console\npip install pipx\npipx install poetry\npipx inject poetry poetry-dynamic-versioning poetry-pre-commit-plugin\n```\n\nVia `pip`:\n\n```console\npip install poetry\npoetry self add poetry-dynamic-versioning poetry-pre-commit-plugin\n```\n\n### Development tasks\n\n* Setup: `poetry install`\n* Run static checks: `poetry run poe lint` or\n  `poetry run pre-commit run --all-files`\n* Run static checks and tests: `poetry run poe test`\n\n---\n\nCreated from [smkent/cookie-python][cookie-python] using\n[cookiecutter][cookiecutter]\n\n[codecov]: https://codecov.io/gh/smkent/jmapc\n[cookie-python]: https://github.com/smkent/cookie-python\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[fastmail-maskedemail]: https://www.fastmail.com/developer/maskedemail/\n[gh-actions]: https://github.com/smkent/jmapc/actions?query=branch%3Amain\n[logo]: https://raw.github.com/smkent/jmapc/main/img/jmapc.png\n[jmapio]: https://jmap.io\n[pipx]: https://pypa.github.io/pipx/\n[poetry]: https://python-poetry.org/docs/#installation\n[pypi]: https://pypi.org/project/jmapc/\n[repo]: https://github.com/smkent/jmapc\n',
    'author': 'Stephen Kent',
    'author_email': 'smkent@smkent.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/smkent/jmapc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
