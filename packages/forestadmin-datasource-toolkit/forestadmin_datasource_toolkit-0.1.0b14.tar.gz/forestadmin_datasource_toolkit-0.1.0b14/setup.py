# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forestadmin',
 'forestadmin.datasource_toolkit',
 'forestadmin.datasource_toolkit.context',
 'forestadmin.datasource_toolkit.context.relaxed_wrappers',
 'forestadmin.datasource_toolkit.decorators',
 'forestadmin.datasource_toolkit.decorators.action',
 'forestadmin.datasource_toolkit.decorators.action.context',
 'forestadmin.datasource_toolkit.decorators.action.types',
 'forestadmin.datasource_toolkit.decorators.computed',
 'forestadmin.datasource_toolkit.decorators.operators_replace',
 'forestadmin.datasource_toolkit.decorators.proxy',
 'forestadmin.datasource_toolkit.decorators.publication',
 'forestadmin.datasource_toolkit.decorators.rename',
 'forestadmin.datasource_toolkit.decorators.search',
 'forestadmin.datasource_toolkit.decorators.segments',
 'forestadmin.datasource_toolkit.interfaces',
 'forestadmin.datasource_toolkit.interfaces.models',
 'forestadmin.datasource_toolkit.interfaces.query',
 'forestadmin.datasource_toolkit.interfaces.query.condition_tree',
 'forestadmin.datasource_toolkit.interfaces.query.condition_tree.nodes',
 'forestadmin.datasource_toolkit.interfaces.query.condition_tree.transforms',
 'forestadmin.datasource_toolkit.interfaces.query.filter',
 'forestadmin.datasource_toolkit.interfaces.query.projections',
 'forestadmin.datasource_toolkit.interfaces.query.sort',
 'forestadmin.datasource_toolkit.utils',
 'forestadmin.datasource_toolkit.validations']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.2,<5.0', 'tzdata>=2022.6,<2023.0']

extras_require = \
{':python_full_version < "3.7.1"': ['pandas==1.1.5'],
 ':python_full_version >= "3.7.1" and python_version < "3.8"': ['pandas==1.3.5'],
 ':python_version < "3.9"': ['backports.zoneinfo[tzdata]>=0.2.1,<0.3.0'],
 ':python_version >= "3.8"': ['pandas>=1.4.2,<1.5.0']}

setup_kwargs = {
    'name': 'forestadmin-datasource-toolkit',
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
