# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thlock']

package_data = \
{'': ['*']}

install_requires = \
['aetcd3>=0.1.0a7,<0.2.0']

setup_kwargs = {
    'name': 'thlock',
    'version': '0.9.1',
    'description': 'TangledHub thlock library',
    'long_description': "[![Build][build-image]]()\n[![Status][status-image]][pypi-project-url]\n[![Stable Version][stable-ver-image]][pypi-project-url]\n[![Coverage][coverage-image]]()\n[![Python][python-ver-image]][pypi-project-url]\n[![License][bsd3-image]][bsd3-url]\n\n\n# thlock\n\n## Overview\nTangledHub library for etcd_lock with a focus on asynchronous functions\n\n## Licencing\nthlock is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details\n\n---\n\n## Installation\n```bash\npip install thlock\n```\n\n## Testing\n```bash\ndocker-compose build thlock-test ; docker-compose run --rm thlock-test\n```\n\n## Building\n```bash\ndocker-compose build thlock-build ; docker-compose run --rm thlock-build\n```\n\n## Publish\n```bash\ndocker-compose build thcrypto-lock ; docker-compose run --rm -e PYPI_USERNAME=__token__ -e PYPI_PASSWORD=__SECRET__ thlock-publish\n```\n\n---\n\n## Usage\n\n### setup\n\nCreate instance of EtcdLock\n\n```python\n\nHOST = 'etcd-test'\nPORT = 2379\n\n# create instance of EtcdLock\nlock = EtcdLock(host=HOST, port=PORT, name='lock-0')\n\n```\n\n\n### Acquire lock\n\n```python\n\nHOST = 'etcd-test'\nPORT = 2379\n\n# create instance of EtcdLock\nlock = EtcdLock(host=HOST, port=PORT, name='lock-0')\n\n# acquire lock\nawait lock.acquire()\n\n```\n\n\n<!-- Links -->\n\n<!-- Badges -->\n[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg\n[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause\n[build-image]: https://img.shields.io/badge/build-success-brightgreen\n[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green\n\n[pypi-project-url]: https://pypi.org/project/thlock/\n[stable-ver-image]: https://img.shields.io/pypi/v/thlock?label=stable\n[python-ver-image]: https://img.shields.io/pypi/pyversions/thlock.svg?logo=python&logoColor=FBE072\n[status-image]: https://img.shields.io/pypi/status/thlock.svg\n\n\n",
    'author': 'TangledHub',
    'author_email': 'info@tangledgroup.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/tangledlabs/thlock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
