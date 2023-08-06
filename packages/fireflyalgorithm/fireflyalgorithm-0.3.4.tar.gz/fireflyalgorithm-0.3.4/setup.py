# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fireflyalgorithm']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.11" and python_version < "4.0"': ['numpy>=1.22.0,<2.0.0'],
 ':python_version >= "3.7" and python_version < "3.11"': ['numpy>=1.21.5,<2.0.0']}

setup_kwargs = {
    'name': 'fireflyalgorithm',
    'version': '0.3.4',
    'description': 'Implementation of Firefly Algorithm in Python',
    'long_description': '<p align="center">\n  <img width="200" src="https://raw.githubusercontent.com/firefly-cpp/FireflyAlgorithm/master/.github/imgs/firefly_logo.png">\n</p>\n\n---\n\n# Firefly Algorithm --- Implementation of Firefly algorithm in Python\n\n---\n\n[![PyPI Version](https://img.shields.io/pypi/v/fireflyalgorithm.svg)](https://pypi.python.org/pypi/fireflyalgorithm)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fireflyalgorithm.svg)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/fireflyalgorithm.svg)\n[![Downloads](https://pepy.tech/badge/fireflyalgorithm)](https://pepy.tech/project/fireflyalgorithm)\n[![GitHub license](https://img.shields.io/github/license/firefly-cpp/FireflyAlgorithm.svg)](https://github.com/firefly-cpp/FireflyAlgorithm/blob/master/LICENSE)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/FireflyAlgorithm.svg)\n[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/firefly-cpp/FireflyAlgorithm.svg)](http://isitmaintained.com/project/firefly-cpp/FireflyAlgorithm "Average time to resolve an issue")\n[![Percentage of issues still open](http://isitmaintained.com/badge/open/firefly-cpp/FireflyAlgorithm.svg)](http://isitmaintained.com/project/firefly-cpp/FireflyAlgorithm "Percentage of issues still open")\n![GitHub contributors](https://img.shields.io/github/contributors/firefly-cpp/FireflyAlgorithm.svg)\n\n## About\n\nThis package implements a nature-inspired algorithm for optimization called Firefly Algorithm (FA) in Python programming language.\n\n## Installation:\n\n```sh\npip install fireflyalgorithm\n```\nTo install FireflyAlgorithm on Fedora, use:\n```sh\ndnf install python-fireflyalgorithm\n```\n\n## Usage:\n\n```python\nimport numpy as np\nfrom fireflyalgorithm import FireflyAlgorithm\n\ndef sphere(x):\n    return np.sum(x ** 2)\n\nFA = FireflyAlgorithm()\nbest = FA.run(function=sphere, dim=10, lb=-5, ub=5, max_evals=10000)\n\nprint(best)\n```\n\n## Reference Papers:\n\nI. Fister Jr.,  X.-S. Yang,  I. Fister, J. Brest. [Memetic firefly algorithm for combinatorial optimization](http://www.iztok-jr-fister.eu/static/publications/44.pdf) in Bioinspired Optimization Methods and their Applications (BIOMA 2012), B. Filipic and J.Silc, Eds.\nJozef Stefan Institute, Ljubljana, Slovenia, 2012\n\nI. Fister, I. Fister Jr.,  X.-S. Yang, J. Brest. [A comprehensive review of firefly algorithms](http://www.iztok-jr-fister.eu/static/publications/23.pdf). Swarm and Evolutionary Computation 13 (2013): 34-46.\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n',
    'author': 'Iztok Fister Jr.',
    'author_email': 'iztok@iztok-jr-fister.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/firefly-cpp/FireflyAlgorithm',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
