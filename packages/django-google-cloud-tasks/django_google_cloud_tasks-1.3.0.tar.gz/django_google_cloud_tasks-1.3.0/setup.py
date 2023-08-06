# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_cloud_tasks',
 'django_cloud_tasks.management',
 'django_cloud_tasks.management.commands',
 'django_cloud_tasks.migrations',
 'django_cloud_tasks.tasks',
 'django_cloud_tasks.tests']

package_data = \
{'': ['*']}

install_requires = \
['django>=4,<5', 'gcp-pilot[pubsub,tasks]']

setup_kwargs = {
    'name': 'django-google-cloud-tasks',
    'version': '1.3.0',
    'description': 'Async Tasks with HTTP endpoints',
    'long_description': 'None',
    'author': 'Joao Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
