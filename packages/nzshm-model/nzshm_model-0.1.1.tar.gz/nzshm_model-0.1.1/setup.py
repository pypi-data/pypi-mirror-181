# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nzshm_model',
 'nzshm_model.source_logic_tree',
 'scripts',
 'tests',
 'tests.fixtures']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0']

extras_require = \
{'scripts': ['click[scripts]>=8.1.3,<9.0.0'],
 'toshi': ['nshm-toshi-client[toshi]>=1.0.0', 'boto3[toshi]>=1.26.28,<2.0.0']}

entry_points = \
{'console_scripts': ['slt = scripts.slt:slt']}

setup_kwargs = {
    'name': 'nzshm-model',
    'version': '0.1.1',
    'description': 'The logic tree definitions, final configurations, and versioning of the New Zealand | Aotearoa National Seismic Hazard Model',
    'long_description': '# New Zealand | Aotearoa National Seismic Hazard Model\nThe logic tree definitions, final configurations, and versioning of the New Zealand | Aotearoa National Seismic Hazard Model are stored here\n\nFor model data see [nshm.gns.cri.nz](https://nshm.gns.cri.nz)',
    'author': 'Chris DiCaprio',
    'author_email': 'c.dicaprio@gns.cri.nz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
