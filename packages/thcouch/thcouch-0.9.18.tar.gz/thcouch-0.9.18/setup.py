# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thcouch',
 'thcouch.core',
 'thcouch.core.attachment',
 'thcouch.core.db',
 'thcouch.core.db.design_docs',
 'thcouch.core.doc',
 'thcouch.core.index',
 'thcouch.core.server',
 'thcouch.orm',
 'thcouch.orm.decl']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'json5>=0.9.10,<0.10.0',
 'pyyaml-include>=1.3,<2.0',
 'pyyaml>=6.0,<7.0',
 'thresult>=0.9.14,<0.10.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'thcouch',
    'version': '0.9.18',
    'description': 'Tangled thcouch library',
    'long_description': '[![Build][build-image]]()\n[![Status][status-image]][pypi-project-url]\n[![Stable Version][stable-ver-image]][pypi-project-url]\n[![Coverage][coverage-image]]()\n[![Python][python-ver-image]][pypi-project-url]\n[![License][bsd3-image]][bsd3-url]\n\n\n# thcouch\n\n## Overview\nTangledHub library for couchdb with a focus on asynchronous functions\n\n\n## Licensing\nthcouch is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details\n\n\n## Installation\n```bash\npip instal thcouch\n```\n\n\n## Testing\n```bash\ndocker-compose build --no-cache thcouch-test ; docker-compose run --rm thcouch-test\n```\n\n\n## Building\n```bash\ndocker-compose build thcouch-build ; docker-compose run --rm thcouch-build\n```\n\n\n## Publish\n```bash\ndocker-compose build thcouch-publish ; docker-compose run --rm -e PYPI_USERNAME=__token__ -e PYPI_PASSWORD=__SECRET__ thcouch-publish\n```\n\n\n<!-- Links -->\n\n<!-- Badges -->\n[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg\n[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause\n[build-image]: https://img.shields.io/badge/build-success-brightgreen\n[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green\n\n[pypi-project-url]: https://pypi.org/project/thcouch/\n[stable-ver-image]: https://img.shields.io/pypi/v/thcouch?label=stable\n[python-ver-image]: https://img.shields.io/pypi/pyversions/thcouch.svg?logo=python&logoColor=FBE072\n[status-image]: https://img.shields.io/pypi/status/thcouch.svg\n\n\n\n',
    'author': 'Tangled',
    'author_email': 'info@tangledgroup.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/tangledlabs/thcouch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
