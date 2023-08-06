# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xpypact', 'xpypact.utils']

package_data = \
{'': ['*']}

install_requires = \
['h5netcdf>=0.13.1',
 'mckit-nuclides>=0.1.1',
 'multipledispatch>=0.6.0',
 'numpy>=1.23.2',
 'openpyxl>=3.0.9',
 'orjson>=3.6.7',
 'pandas>=1.3.4',
 'xarray>=2022.3.0']

setup_kwargs = {
    'name': 'xpypact',
    'version': '0.1.9',
    'description': '"Python tools to work with elements and isotopes"',
    'long_description': "==============================================================================\n*xpypact*: FISPACT output to datasets converter\n==============================================================================\n\n\n\n|Maintained| |License| |Versions| |PyPI| |Docs|\n\n.. contents::\n\n\nNote:\n    This document is in progress.\n\nDescription\n-----------\n\nThe module loads FISPACT JSON output as xarray dataset.\nThis allows efficient data extraction and aggregation.\n\n.. configures and runs FISPACT, converts FISPACT output to xarray datasets.\n\n.. TODO dvp: apply FISPACT v.5 API and describe here.\n\n\nInstallation\n------------\n\n::\n\n    pip install xpypact\n\n.. warning:: Install the hdf5 before installing xpypact for Python3.11.\n\n    Reason:\n\n    We depend on h5py through h5netcdf.\n    The h5py package as for recent version 3.7.0 doesn't provide wheels for Python3.11.\n    So, for python 3.11 pip tries to build the h5py package from sources. This fails, if hdf5 library is not preinstalled.\n\n\n\n.. TODO dvp: check and report all possible ways to install (pip, poetry)\n\n\nExamples\n--------\n\n.. TODO\n\nContributing\n------------\n\n.. image:: https://github.com/MC-kit/xpypact/workflows/Tests/badge.svg\n   :target: https://github.com/MC-kit/xpypact/actions?query=workflow%3ATests\n   :alt: Tests\n.. image:: https://codecov.io/gh/MC-kit/xpypact/branch/master/graph/badge.svg?token=P6DPGSWM94\n   :target: https://codecov.io/gh/MC-kit/xpypact\n   :alt: Coverage\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n   :target: https://pycqa.github.io/isort/\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. image:: https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black\n   :target: https://github.com/guilatrova/tryceratops\n   :alt: try/except style: tryceratops\n\nhttps://www.conventionalcommits.org/en/v1.0.0/#summary\nhttps://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelinesi\n\n\nReferences\n----------\n\n.. TODO dvp: add references to FISPACT, pypact and used libraries:  poetry, xarray etc\n\n\n.. Substitutions\n\n.. |Maintained| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg\n   :target: https://github.com/MC-kit/xpypact/graphs/commit-activity\n.. |Tests| image:: https://github.com/MC-kit/xpypact/workflows/Tests/badge.svg\n   :target: https://github.com/MC-kit/xpypact/actions?workflow=Tests\n   :alt: Tests\n.. |License| image:: https://img.shields.io/github/license/MC-kit/xpypact\n   :target: https://github.com/MC-kit/xpypact\n.. |Versions| image:: https://img.shields.io/pypi/pyversions/xpypact\n   :alt: PyPI - Python Version\n.. |PyPI| image:: https://img.shields.io/pypi/v/xpypact\n   :target: https://pypi.org/project/xpypact/\n   :alt: PyPI\n.. |Docs| image:: https://readthedocs.org/projects/xpypact/badge/?version=latest\n   :target: https://xpypact.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n",
    'author': 'dvp',
    'author_email': 'dmitri_portnov@yahoo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MC-kit/xpypact',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
