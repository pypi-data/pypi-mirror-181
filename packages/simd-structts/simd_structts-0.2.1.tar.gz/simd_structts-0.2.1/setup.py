# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['simd_structts',
 'simd_structts.backends',
 'simd_structts.backends.py_ssm',
 'simd_structts.backends.simd',
 'simd_structts.backends.statsmodels',
 'simd_structts.base']

package_data = \
{'': ['*']}

install_requires = \
['simdkalman>=1.0.1,<2.0.0', 'statsmodels>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'simd-structts',
    'version': '0.2.1',
    'description': 'SIMD StuctTS Model with various backends',
    'long_description': '# simd-structts\n[![pypi](https://img.shields.io/pypi/v/simd-structts)](https://pypi.org/project/simd-structts/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simd-structts)\n[![Build Status](https://travis-ci.org/vshulyak/simd-structts.svg?branch=master)](https://travis-ci.org/vshulyak/simd-structts)\n[![codecov](https://codecov.io/github/vshulyak/simd-structts/branch/master/graph/badge.svg)](https://codecov.io/github/vshulyak/simd-structts)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/github/license/vshulyak/simd_structts)](https://github.com/vshulyak/simd-structts/blob/master/LICENSE)\n[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/vshulyak/simd-structts/issues)\nMultivariate forecasting using StructTS/Unobserved Components model without MLE param estimation.\n\n## 🤦🏾\u200d Motivation\n\nI love structts model and Kalman filters for forecasting. Sometimes you just want a model that works out of the box\nwithout *designing* a model with a Kalman filter, especially if you need to use long seasonalites and exog variables.\nDefining all these state space matrices gets tedious pretty quickly...\n\nThe code in this repo is an attempt to bring a familiar API to multivariate StructTS model, currently with the simdkalman library as a backend.\n\n## 👩🏾\u200d🚀 Installation\n\n      pip install simd-structts\n\n\n## 📋 WIP:\n- [x] Statsmodels and simdkalman backend implementation.\n- [x] Equal filtered/smoothed/predicted states for level/trend models.\n- [x] Proper testing for multiple python versions.\n- [x] Equal filtered/smoothed/predicted states for exog components.\n- [x] Equal filtered/smoothed/predicted states for long seasonal fourier components.\n- [x] Passing tests for statsmodels-like initialization of model.\n- [ ] Pretty API with ABC and stuff.\n- [ ] Example notebook\n- [ ] Gradient methods for finding optimal params\n',
    'author': 'Vladimir Shulyak',
    'author_email': 'vladimir@shulyak.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vshulyak/simd-structts',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
