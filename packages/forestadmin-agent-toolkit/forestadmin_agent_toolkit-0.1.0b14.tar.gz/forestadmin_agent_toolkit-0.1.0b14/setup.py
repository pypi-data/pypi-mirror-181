# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forestadmin',
 'forestadmin.agent_toolkit',
 'forestadmin.agent_toolkit.resources',
 'forestadmin.agent_toolkit.resources.actions',
 'forestadmin.agent_toolkit.resources.collections',
 'forestadmin.agent_toolkit.resources.security',
 'forestadmin.agent_toolkit.services',
 'forestadmin.agent_toolkit.services.permissions',
 'forestadmin.agent_toolkit.services.serializers',
 'forestadmin.agent_toolkit.utils',
 'forestadmin.agent_toolkit.utils.forest_schema']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8,<4.0',
 'cachetools>=5.2,<6.0',
 'forestadmin-datasource-toolkit>=0.1.0-beta.14,<0.2.0',
 'marshmallow-jsonapi>=0.24.0,<1.0',
 'oic>=1.4,<2.0',
 'python-jose>=3.3,<4.0',
 'typing-extensions>=4.2.0,<5.0',
 'tzdata>=2022.6,<2022.7']

extras_require = \
{':python_full_version < "3.7.1"': ['pandas==1.1.5'],
 ':python_full_version >= "3.7.1" and python_version < "3.8"': ['pandas==1.3.5'],
 ':python_version < "3.9"': ['backports.zoneinfo[tzdata]>=0.2.1,<0.3.0'],
 ':python_version >= "3.8"': ['pandas>=1.4.2,<1.5.0']}

setup_kwargs = {
    'name': 'forestadmin-agent-toolkit',
    'version': '0.1.0b14',
    'description': '',
    'long_description': '',
    'author': 'Valentin Monté',
    'author_email': 'valentinm@forestadmin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
