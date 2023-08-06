# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starapi', 'starapi.filesystem', 'starapi.filesystem.driver', 'starapi.spec']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'google-cloud-storage>=2.7.0,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'starlette>=0.20.4,<0.21.0']

setup_kwargs = {
    'name': 'starapi',
    'version': '0.3.3',
    'description': 'StarAPI based on starlette and pydantic.',
    'long_description': '# starapi',
    'author': 'jonars',
    'author_email': 'jonarsli13@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JonarsLi/flask-restapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
