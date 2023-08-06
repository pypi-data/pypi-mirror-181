# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_plugin']

package_data = \
{'': ['*']}

install_requires = \
['polywrap_core==0.1.0a1',
 'polywrap_manifest==0.1.0a1',
 'polywrap_msgpack==0.1.0a1',
 'polywrap_result==0.1.0a1']

setup_kwargs = {
    'name': 'polywrap-plugin',
    'version': '0.1.0a1',
    'description': 'Plugin package',
    'long_description': '',
    'author': 'Cesar',
    'author_email': 'cesar@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
