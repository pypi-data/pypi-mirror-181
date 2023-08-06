# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datatoolkit']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.4.0,<3.0.0',
 'hyperopt>=0.2.7,<0.3.0',
 'networkx>=2.6.3,<3.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'statsmodels>=0.13.0,<0.14.0',
 'typeguard>=2.12.1,<3.0.0']

setup_kwargs = {
    'name': 'datatoolkit',
    'version': '0.2.5',
    'description': 'A collection of tools for visualization and data processing for exploratory data analysis',
    'long_description': '[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5563180.svg)](https://doi.org/10.5281/zenodo.5563180)\n[![Documentation Status](https://readthedocs.org/projects/datatoolkit/badge/?version=latest)](https://datatoolkit.readthedocs.io/?badge=latest)\n[![Build_and_test_code](https://github.com/hsteinshiromoto/datatoolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/hsteinshiromoto/datatoolkit/actions/workflows/ci.yml)\n![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hsteinshiromoto/datatoolkit?style=flat)\n![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)\n\n# 1. Datatoolkit\n\nA collection of tools for visualization and data processing for exploratory data analysis.\n\n# 2. Table of Contents\n\n- [1. Datatoolkit](#1-datatoolkit)\n- [2. Table of Contents](#2-table-of-contents)\n- [3. Documentation](#3-documentation)\n\n# 3. Documentation\n\nhttps://datatoolkit.readthedocs.io/en/latest/',
    'author': 'Humberto STEIN SHIROMOTO',
    'author_email': 'h.stein.shiromoto@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
