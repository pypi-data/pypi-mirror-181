# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sift']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.8',
 'matplotlib>=3.3',
 'numpy>=1.15',
 'pandas>=1.3',
 'pykeops>=2.0',
 'rich>=10',
 'scanpy>=1.7',
 'scipy>=1.5.0',
 'seaborn>=0.10']

extras_require = \
{'dev': ['pre-commit>=2.10'],
 'docs': ['sphinx>=4',
          'furo>=2022.04.07',
          'nbsphinx>=0.8',
          'sphinx-autodoc-typehints>=1.12'],
 'gpu': ['torch>=1.8.0'],
 'test': ['pytest>=7']}

setup_kwargs = {
    'name': 'sift-sc',
    'version': '0.1.0',
    'description': 'Biological signal filtering in single-cell data.',
    'long_description': 'SiFT - Biological signal filtering in single-cell data\n======================================================\n\n.. image:: https://raw.githubusercontent.com/nitzanlab/sift-sc/main/docs/_static/img/sift_gc.png\n    :width: 200px\n    :align: center\n    :alt: SiFT logo\n\nSignal FilTering is a tool for uncovering hidden biological processes in single-cell data.\nIt can be applied to a wide range of tasks, from the removal of unwanted variation as a pre-processing step,\nthrough revealing hidden biological structure by utilizing prior knowledge with respect to existing signal,\nto uncovering trajectories of interest using reference data to remove unwanted variation.\n\n.. image:: https://raw.githubusercontent.com/nitzanlab/sift-sc/main/docs/_static/img/sift_abs.png\n    :width: 600px\n    :align: center\n    :alt: SiFT pipeline\n\nVisit our `documentation`_ for installation, tutorials, examples and more.\n\nManuscript\n----------\nPlease see our manuscript `Zoe Piran and Mor Nitzan (2022)`_.\n\nInstallation\n------------\nInstall SiFT via PyPI by running::\n\n    pip install sift-sc\n\n.. _documentation: https://sift-sc.readthedocs.io/\n.. _Zoe Piran and Mor Nitzan (2022): https://github.com/nitzanlab/sift-sc\n',
    'author': 'Zoe Piran',
    'author_email': 'zoe.piran@mail.huji.ac.il',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nitzanlab/sift-sc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
