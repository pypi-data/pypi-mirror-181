# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_rr_verify']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypi-rr-verify',
    'version': '0.2.0',
    'description': 'Version tracking of published package.',
    'long_description': '# pypi-rr-verify\n\nList of versions:\n- 0.1.0\n- 0.2.0',
    'author': 'rroko',
    'author_email': 'roko.mislov@reversinglabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
