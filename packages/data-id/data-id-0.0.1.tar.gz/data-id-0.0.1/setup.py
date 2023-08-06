# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_id']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1,<9.0', 'rich', 'runtype>=0.2.6,<0.3.0', 'sqeleton']

entry_points = \
{'console_scripts': ['data-id = data_id.__main__:main']}

setup_kwargs = {
    'name': 'data-id',
    'version': '0.0.1',
    'description': 'Command-line tool and Python library to efficiently identify PII in database tables.',
    'long_description': '# data-pii',
    'author': 'Datafold',
    'author_email': 'data-id@datafold.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/datafold/data-id',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
