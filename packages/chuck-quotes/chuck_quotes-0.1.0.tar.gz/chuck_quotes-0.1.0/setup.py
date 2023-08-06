# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chuckquotes']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'chuck-quotes',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Chuck Quotes\n\nDemo package to retrieve Chuck Norris quotes from webservice.',
    'author': 'Juanjo Salvador',
    'author_email': 'juanjosalvador@netc.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
