# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conduit',
 'conduit.data',
 'conduit.data.datamodules',
 'conduit.data.datamodules.audio',
 'conduit.data.datamodules.tabular',
 'conduit.data.datamodules.vision',
 'conduit.data.datasets',
 'conduit.data.datasets.audio',
 'conduit.data.datasets.tabular',
 'conduit.data.datasets.vision',
 'conduit.fair',
 'conduit.fair.data',
 'conduit.fair.data.datamodules',
 'conduit.fair.data.datamodules.tabular',
 'conduit.fair.data.datamodules.vision',
 'conduit.fair.data.datasets',
 'conduit.fair.data.datasets.vision',
 'conduit.fair.losses',
 'conduit.hydra.conduit.data.datamodules',
 'conduit.hydra.conduit.data.datasets',
 'conduit.hydra.conduit.fair.data.datamodules',
 'conduit.hydra.conduit.fair.models',
 'conduit.hydra.conduit.models',
 'conduit.hydra.conduit.models.self_supervised',
 'conduit.models',
 'conduit.models.self_supervised',
 'conduit.transforms']

package_data = \
{'': ['*'], 'conduit': ['conf/*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'ranzen[hydra]>=2.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'typing-extensions>=4.0.0']

setup_kwargs = {
    'name': 'torch-conduit',
    'version': '0.1.7',
    'description': 'Lightweight framework for dataloading with PyTorch and channeling the power of PyTorch Lightning',
    'long_description': '# conduit :electron:\n\nLightweight framework for channeling the power of PyTorch Lightning.\n',
    'author': 'PAL',
    'author_email': 'info@predictive-analytics-lab.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wearepal/conduit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
