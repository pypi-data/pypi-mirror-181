# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isegeval', 'isegeval.click']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'scipy>=1.9.3,<2.0.0', 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'isegeval',
    'version': '0.1.0',
    'description': 'A Python Library to Evaluate Interactive Segmentation Models',
    'long_description': '# isegeval\n\nThis is a library to evaluate click-based interactive segmentation models. isegeval could evaluate\nthe number of click (NoC) performance of the given model on the given dataset.\n\n\n## Usage\n\nYou could evaluate your model as follows. See [notebooks](./notebooks) for more detail.\n\n```py\nfrom isegeval import evaluate\nfrom isegeval.core import ModelFactory\n\n\n# Each item is the tuple of an image and its correspoinding ground truth mask.\ndataset: Sequence[tuple[np.ndarray, np.ndarray]] = YourDataset()\n\n# A factory of your model that you want to evaluate. The factory should implement get_model method.\nmodel_factory: ModelFactory = YourModelFactory()\n\nevaluate(dataset, model_factory)\n```\n\n\n## Installation\n\n```bash\npip install isegeval\n```\n',
    'author': 'yasufumi',
    'author_email': 'yasufumi.taniguchi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tech-sketch/isegeval',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
