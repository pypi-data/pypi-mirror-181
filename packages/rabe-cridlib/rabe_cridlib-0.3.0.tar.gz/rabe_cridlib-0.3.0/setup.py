# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cridlib', 'cridlib.strategy']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2022.6', 'requests>=2.28.1,<3.0.0', 'uritools>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'rabe-cridlib',
    'version': '0.3.0',
    'description': 'Generate CRIDs for RaBe',
    'long_description': '# RaBe cridlib for Python\n\nGenerate [RaBe CRIDs](https://github.com/radiorabe/crid-spec) based on several data sources:\n\n* Songticker for current CRID\n* `archiv.rabe.ch` for past CRIDs\n* TBD: LibreTime for future CRIDs\n\n## Installation\n\n```bash\npoetry add rabe-cridlib\n\n# or on old setup style projects\npip -m install rabe-cridlib\n```\n\n## Usage\n\n```python\n>>> import cridlib\n>>>\n>>> # parse an existing crid\n>>> crid = cridlib.parse("crid://rabe.ch/v1/klangbecken#t=clock=19930301T131200.00Z")\n>>> print(f"version: {crid.version}, show: {crid.show}, start: {crid.start}")\nversion: v1, show: klangbecken, start: 1993-03-01 13:12:00\n\n>>> # get crid for current show\n>>> crid = cridlib.get()\n>>> print(f"version: {crid.version}, show: {crid.show}")  # doctest:+ELLIPSIS\nversion: v1, show: ...\n\n```\n\n## Development\n\n```bash\n# setup a dev env\npython -mvenv env\n. env/bin/activate\n\n# install a modern poetry version\npython -mpip install poetry>=1.2.0\n\n# install deps and dev version\npoetry install\n\n# make changes, run tests\npytest\n```\n\n## Release Management\n\nThe CI/CD setup uses semantic commit messages following the [conventional commits standard](https://www.conventionalcommits.org/en/v1.0.0/).\nThere is a GitHub Action in [.github/workflows/semantic-release.yaml](./.github/workflows/semantic-release.yaml)\nthat uses [go-semantic-commit](https://go-semantic-release.xyz/) to create new\nreleases.\n\nThe commit message should be structured as follows:\n\n```\n<type>[optional scope]: <description>\n\n[optional body]\n\n[optional footer(s)]\n```\n\nThe commit contains the following structural elements, to communicate intent to the consumers of your library:\n\n1. **fix:** a commit of the type `fix` patches gets released with a PATCH version bump\n1. **feat:** a commit of the type `feat` gets released as a MINOR version bump\n1. **BREAKING CHANGE:** a commit that has a footer `BREAKING CHANGE:` gets released as a MAJOR version bump\n1. types other than `fix:` and `feat:` are allowed and don\'t trigger a release\n\nIf a commit does not contain a conventional commit style message you can fix\nit during the squash and merge operation on the PR.\n\nOnce a commit has landed on the `main` branch a release will be created and automatically published to [pypi](https://pypi.org/)\nusing the GitHub Action in [.github/workflows/release.yaml](./.github/workflows/release.yaml) which uses [poetry](https://python-poetry.org/)\nto publish the package to pypi.\n\n## License\n\nThis package is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, version 3 of the License.\n\n## Copyright\n\nCopyright (c) 2022 [Radio Bern RaBe](http://www.rabe.ch)\n',
    'author': 'RaBe IT-Reaktion',
    'author_email': 'it@rabe.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/radiorabe/python-rabe-cridlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
