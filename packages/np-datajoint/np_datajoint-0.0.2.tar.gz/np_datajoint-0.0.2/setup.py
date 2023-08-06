# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['np_datajoint', 'np_datajoint.hpc']

package_data = \
{'': ['*']}

install_requires = \
['datajoint>=0.13,<0.14',
 'djsciops>=1,<2',
 'fabric>=2,<3',
 'ipykernel>=6,<7',
 'ipython>=8,<9',
 'ipywidgets>=7,<8',
 'jupyter>=1,<2',
 'np_logging>=0,<1',
 'numpy>=1,<2',
 'pandas>=1.5,<2.0',
 'requests>=2,<3',
 'seaborn>=0,<1']

setup_kwargs = {
    'name': 'np-datajoint',
    'version': '0.0.2',
    'description': 'Tools for spike-sorting Mindscope neuropixels ecephys sessions on DataJoint, retrieving results and comparing with locally-sorted equivalents.',
    'long_description': 'Tools for spike-sorting Mindscope neuropixels ecephys sessions on DataJoint, retrieving results and comparing with locally-sorted equivalents.',
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'Ben Hardcastle',
    'maintainer_email': 'ben.hardcastle@alleninstitute.org',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
