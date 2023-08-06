# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['e_dnevnik_api']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'e-dnevnik-api',
    'version': '0.1.0',
    'description': 'Unofficial API for e-Dnevnik',
    'long_description': '# e-Dnevnik API\n\ne-Dnevnik API is an unofficial API for [e-Dnevnik](https://ocjene.skole.hr).\n',
    'author': 'Ivan Paljetak',
    'author_email': 'ip@noreply.codeberg.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/ip/e-Dnevnik-API',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
