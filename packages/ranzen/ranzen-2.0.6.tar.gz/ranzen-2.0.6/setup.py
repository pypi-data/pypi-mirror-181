# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ranzen',
 'ranzen.hydra',
 'ranzen.torch',
 'ranzen.torch.optimizers',
 'ranzen.torch.transforms']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ranzen',
    'version': '2.0.6',
    'description': 'A toolkit facilitating machine-learning experimentation.',
    'long_description': '# ranzen 🎒\n\nA python toolkit facilitating machine-learning experimentation.\n\n[Documentation](https://wearepal.github.io/ranzen/)\n\n## Install\n\nRun\n```\npip install ranzen\n```\n\nor install directly from GitHub:\n```\npip install git+https://github.com/predictive-analytics-lab/ranzen.git@main\n```\n',
    'author': 'PAL',
    'author_email': 'info@predictive-analytics-lab.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/predictive-analytics-lab/ranzen',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
