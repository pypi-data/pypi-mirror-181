# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syncopy',
 'syncopy.datatype',
 'syncopy.datatype.methods',
 'syncopy.io',
 'syncopy.nwanalysis',
 'syncopy.plotting',
 'syncopy.preproc',
 'syncopy.shared',
 'syncopy.specest',
 'syncopy.specest.wavelets',
 'syncopy.statistics',
 'syncopy.tests',
 'syncopy.tests.backend']

package_data = \
{'': ['*']}

install_requires = \
['dask-jobqueue>=0.8',
 'dask[distributed]>=2022.6',
 'fooof>=1.0',
 'h5py>=2.9',
 'ipdb>=0.13.9,<0.14.0',
 'matplotlib>=3.5',
 'memory-profiler>=0.60.0,<0.61.0',
 'natsort>=8.1.0,<9.0.0',
 'numpy>=1.10',
 'numpydoc>=1.4.0,<2.0.0',
 'psutil>=5.9',
 'scipy>=1.5',
 'tqdm>=4.31']

setup_kwargs = {
    'name': 'esi-syncopy',
    'version': '2022.12',
    'description': 'A toolkit for user-friendly large-scale electrophysiology data analysis. Syncopy is compatible with the Matlab toolbox FieldTrip.',
    'long_description': '.. image:: https://raw.githubusercontent.com/esi-neuroscience/syncopy/master/doc/source/_static/syncopy_logo_small.png\n\t   :alt: Syncopy-Logo\n\nSystems Neuroscience Computing in Python\n========================================\n\n\n|Conda Version| |PyPi Version| |License|\n\n.. |Conda Version| image:: https://img.shields.io/conda/vn/conda-forge/esi-syncopy.svg\n   :target: https://anaconda.org/conda-forge/esi-syncopy\n.. |PyPI version| image:: https://badge.fury.io/py/esi-syncopy.svg\n   :target: https://badge.fury.io/py/esi-syncopy\n.. |License| image:: https://img.shields.io/github/license/esi-neuroscience/syncopy\n\n|Master Tests| |Master Coverage|\n\n.. |Master Tests| image:: https://github.com/esi-neuroscience/syncopy/actions/workflows/cov_test_workflow.yml/badge.svg?branch=master\n   :target: https://github.com/esi-neuroscience/syncopy/actions/workflows/cov_test_workflow.yml\n.. |Master Coverage| image:: https://codecov.io/gh/esi-neuroscience/syncopy/branch/master/graph/badge.svg?token=JEI3QQGNBQ\n   :target: https://codecov.io/gh/esi-neuroscience/syncopy\n\nSyncopy aims to be a user-friendly toolkit for *large-scale*\nelectrophysiology data-analysis in Python. We strive to achieve the following goals:\n\n1. Syncopy is a *fully open source Python* environment for electrophysiology\n   data analysis.\n2. Syncopy is *scalable* and built for *very large datasets*. It automatically\n   makes use of available computing resources and is developed with built-in\n   parallelism in mind.\n3. Syncopy is *compatible with FieldTrip*. Data and results can be loaded into\n   MATLAB and Python, parameter names and function call syntax are as similar as possible\n\nSyncopy is developed at the\n`Ernst Strüngmann Institute (ESI) gGmbH for Neuroscience in Cooperation with Max Planck Society <https://www.esi-frankfurt.de/>`_\nand released free of charge under the\n`BSD 3-Clause "New" or "Revised" License <https://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_(%22BSD_License_2.0%22,_%22Revised_BSD_License%22,_%22New_BSD_License%22,_or_%22Modified_BSD_License%22)>`_.\n\nContact\n-------\nTo report bugs or ask questions please use our `GitHub issue tracker <https://github.com/esi-neuroscience/syncopy/issues>`_.\nFor general inquiries please contact syncopy (at) esi-frankfurt.de.\n\nInstallation\n============\n\nWe recommend to install SynCoPy into a new conda environment:\n\n#. Install the `Anaconda Distribution for your Operating System <https://www.anaconda.com/products/distribution>`_ if you do not yet have it.\n#. Start a new terminal.\n\n   * You can do this by starting ```Anaconda navigator```, selecting ```Environments``` in the left tab, selecting the ```base (root)``` environment, and clicking the green play button and then ```Open Terminal```.\n   * Alternatively, under Linux, you can just type ```bash``` in your active terminal to start a new session.\n\nYou should see a terminal with a command prompt that starts with ```(base)```, indicating that you are\nin the conda ```base``` environment.\n\nNow we create a new environment named ```syncopy``` and install syncopy into this environment:\n\n.. code-block:: bash\n\n   conda create -y --name syncopy\n   conda activate syncopy\n   conda install -y -c conda-forge esi-syncopy\n\nGetting Started\n===============\nPlease visit our `online documentation <http://syncopy.org>`_.\n\nDeveloper Installation\n-----------------------\n\nTo get the latest development version, please clone our GitHub repository:\n\n.. code-block:: bash\n\n   git clone https://github.com/esi-neuroscience/syncopy.git\n   cd syncopy/\n   pip install -e .\n',
    'author': 'Stefan Fürtinger',
    'author_email': 'sfuerti@esi-frankfurt.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://syncopy.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
