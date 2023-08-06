# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_first_projecr_demo_1']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow>=2.5.0,<3.0.0',
 'appengine-python-standard>=1.0.0,<2.0.0',
 'google-cloud-datastore>=2.11.0,<3.0.0',
 'google-cloud-storage>=2.7.0,<3.0.0',
 'pytest>=7.2.0,<8.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'my-first-projecr-demo-1',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
