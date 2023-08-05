# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['df', 'df.scripts']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'deepfilterlib==0.4.0',
 'loguru>=0.5',
 'numpy>=1.22,<2.0',
 'requests>=2.27,<3.0']

extras_require = \
{'dnsmos-local': ['onnxruntime>=1.11,<2.0'],
 'eval': ['pystoi>=0.3,<0.4', 'pesq>=0.0.3,<0.0.4', 'scipy>=1,<2'],
 'soundfile': ['soundfile>=0.10,<0.11'],
 'train': ['deepfilterdataloader==0.4.0', 'icecream>=2,<3']}

entry_points = \
{'console_scripts': ['deep-filter-py = df.enhance:run',
                     'deepFilter = df.enhance:run']}

setup_kwargs = {
    'name': 'deepfilternet',
    'version': '0.4.0',
    'description': 'Noise supression using deep filtering',
    'long_description': 'None',
    'author': 'Hendrik Schröter',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Rikorose/DeepFilterNet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
