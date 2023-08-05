# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['facrud_router']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.88.0,<0.89.0',
 'pydantic>=1.10.2,<2.0.0',
 'sqlalchemy>=1.4.45,<2.0.0']

setup_kwargs = {
    'name': 'facrud-router',
    'version': '0.1.0',
    'description': 'FastApi CRUD router for SQLAlchemy',
    'long_description': '# facrud-router',
    'author': 'arutyunyan',
    'author_email': '8david@inbox.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
