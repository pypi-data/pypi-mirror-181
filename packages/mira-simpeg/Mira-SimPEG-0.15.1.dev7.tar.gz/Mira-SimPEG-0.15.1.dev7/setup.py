# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['SimPEG',
 'SimPEG._EM.Static.SP',
 'SimPEG.dask',
 'SimPEG.dask.electromagnetics',
 'SimPEG.dask.electromagnetics.frequency_domain',
 'SimPEG.dask.electromagnetics.static',
 'SimPEG.dask.electromagnetics.static.induced_polarization',
 'SimPEG.dask.electromagnetics.static.resistivity',
 'SimPEG.dask.potential_fields',
 'SimPEG.dask.potential_fields.gravity',
 'SimPEG.dask.potential_fields.magnetics',
 'SimPEG.directives',
 'SimPEG.electromagnetics',
 'SimPEG.electromagnetics.analytics',
 'SimPEG.electromagnetics.frequency_domain',
 'SimPEG.electromagnetics.natural_source',
 'SimPEG.electromagnetics.natural_source.utils',
 'SimPEG.electromagnetics.static',
 'SimPEG.electromagnetics.static.induced_polarization',
 'SimPEG.electromagnetics.static.resistivity',
 'SimPEG.electromagnetics.static.spectral_induced_polarization',
 'SimPEG.electromagnetics.static.utils',
 'SimPEG.electromagnetics.time_domain',
 'SimPEG.electromagnetics.utils',
 'SimPEG.electromagnetics.viscous_remanent_magnetization',
 'SimPEG.flow',
 'SimPEG.flow.richards',
 'SimPEG.potential_fields',
 'SimPEG.potential_fields.gravity',
 'SimPEG.potential_fields.magnetics',
 'SimPEG.regularization',
 'SimPEG.seismic',
 'SimPEG.seismic.straight_ray_tomography',
 'SimPEG.utils',
 'SimPEG.utils.drivers',
 'SimPEG.utils.io_utils']

package_data = \
{'': ['*']}

install_requires = \
['discretize>=0.7.0',
 'empymod',
 'geoh5py',
 'numpy>=1.7',
 'pandas',
 'properties>=0.5.2',
 'pymatsolver>=0.1.1',
 'scikit-learn>=0.22',
 'scipy>=1.0.0',
 'utm',
 'vectormath>=0.2.0']

extras_require = \
{'dask': ['dask', 'fsspec>=0.3.3', 'zarr'], 'regular': ['geoana', 'matplotlib']}

setup_kwargs = {
    'name': 'mira-simpeg',
    'version': '0.15.1.dev7',
    'description': 'Mira Geoscience fork of SimPEG: Simulation and Parameter Estimation in Geophysics',
    'long_description': '.. image:: https://raw.github.com/simpeg/simpeg/main/docs/images/simpeg-logo.png\n    :alt: SimPEG Logo\n\nSimPEG\n******\n\n.. image:: https://img.shields.io/pypi/v/SimPEG.svg\n    :target: https://pypi.python.org/pypi/SimPEG\n    :alt: Latest PyPI version\n\n.. image:: https://img.shields.io/conda/v/conda-forge/SimPEG.svg\n    :target: https://anaconda.org/conda-forge/SimPEG\n    :alt: Latest conda-forge version\n\n.. image:: https://img.shields.io/github/license/simpeg/simpeg.svg\n    :target: https://github.com/simpeg/simpeg/blob/main/LICENSE\n    :alt: MIT license\n\n.. image:: https://dev.azure.com/simpeg/simpeg/_apis/build/status/simpeg.simpeg?branchName=main\n    :target: https://dev.azure.com/simpeg/simpeg/_build/latest?definitionId=2&branchName=main\n    :alt: Azure pipeline\n\n.. image:: https://codecov.io/gh/simpeg/simpeg/branch/main/graph/badge.svg\n    :target: https://codecov.io/gh/simpeg/simpeg\n    :alt: Coverage status\n\n.. image:: https://api.codacy.com/project/badge/Grade/4fc959a5294a418fa21fc7bc3b3aa078\n    :target: https://www.codacy.com/app/lindseyheagy/simpeg?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=simpeg/simpeg&amp;utm_campaign=Badge_Grade\n    :alt: codacy\n\n.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.596373.svg\n   :target: https://doi.org/10.5281/zenodo.596373\n\n.. image:: https://img.shields.io/discourse/users?server=http%3A%2F%2Fsimpeg.discourse.group%2F\n    :target: http://simpeg.discourse.group/\n\n.. image:: https://img.shields.io/badge/Slack-simpeg-4A154B.svg?logo=slack\n    :target: http://slack.simpeg.xyz\n\n.. image:: https://img.shields.io/badge/Youtube%20channel-GeoSci.xyz-FF0000.svg?logo=youtube\n    :target: https://www.youtube.com/channel/UCBrC4M8_S4GXhyHht7FyQqw\n\nSimulation and Parameter Estimation in Geophysics  -  A python package for simulation and gradient based parameter estimation in the context of geophysical applications.\n\nThe vision is to create a package for finite volume simulation with applications to geophysical imaging and subsurface flow. To enable the understanding of the many different components, this package has the following features:\n\n* modular with respect to the spacial discretization, optimization routine, and geophysical problem\n* built with the inverse problem in mind\n* provides a framework for geophysical and hydrogeologic problems\n* supports 1D, 2D and 3D problems\n* designed for large-scale inversions\n\nYou are welcome to join our forum and engage with people who use and develop SimPEG at: http://simpeg.discourse.group/.\n\nWeekly meetings are open to all. They are generally held on Wednesdays at 10:30am PDT. Please see the calendar (`GCAL <https://calendar.google.com/calendar/b/0?cid=ZHVhamYzMWlibThycWdkZXM5NTdoYXV2MnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ>`_, `ICAL <https://calendar.google.com/calendar/ical/duajf31ibm8rqgdes957hauv2s%40group.calendar.google.com/public/basic.ics>`_) for information on the next meeting.\n\nOverview Video\n==============\n\n.. image:: https://img.youtube.com/vi/yUm01YsS9hQ/0.jpg\n    :target: https://www.youtube.com/watch?v=yUm01YsS9hQ\n    :alt: All of the Geophysics But Backwards\n\nWorking towards all the Geophysics, but Backwards - SciPy 2016\n\n\nCiting SimPEG\n=============\n\nThere is a paper about SimPEG!\n\n\n    Cockett, R., Kang, S., Heagy, L. J., Pidlisecky, A., & Oldenburg, D. W. (2015). SimPEG: An open source framework for simulation and gradient based parameter estimation in geophysical applications. Computers & Geosciences.\n\n**BibTex:**\n\n.. code::\n\n    @article{cockett2015simpeg,\n      title={SimPEG: An open source framework for simulation and gradient based parameter estimation in geophysical applications},\n      author={Cockett, Rowan and Kang, Seogi and Heagy, Lindsey J and Pidlisecky, Adam and Oldenburg, Douglas W},\n      journal={Computers \\& Geosciences},\n      year={2015},\n      publisher={Elsevier}\n    }\n\nElectromagnetics\n----------------\n\nIf you are using the electromagnetics module of SimPEG, please cite:\n\n    Lindsey J. Heagy, Rowan Cockett, Seogi Kang, Gudni K. Rosenkjaer, Douglas W. Oldenburg, A framework for simulation and inversion in electromagnetics, Computers & Geosciences, Volume 107, 2017, Pages 1-19, ISSN 0098-3004, http://dx.doi.org/10.1016/j.cageo.2017.06.018.\n\n**BibTex:**\n\n.. code::\n\n    @article{heagy2017,\n        title= "A framework for simulation and inversion in electromagnetics",\n        author= "Lindsey J. Heagy and Rowan Cockett and Seogi Kang and Gudni K. Rosenkjaer and Douglas W. Oldenburg",\n        journal= "Computers & Geosciences",\n        volume = "107",\n        pages = "1 - 19",\n        year = "2017",\n        note = "",\n        issn = "0098-3004",\n        doi = "http://dx.doi.org/10.1016/j.cageo.2017.06.018"\n    }\n\n\nInstalling from the sources\n===========================\n\nThis Python package can be installed with ``pip``.\nThe dependencies are defined in ``pyproject.toml``. It replaces the former ``requirements.txt`` and ``setup.py`` files\n(see `pip documentation`_ to learn more about ``pyproject.toml``).\n\nAs this branch is meant to be used with a geopps environment, some conflicting packages have been moved\nto "extras" and declared optional. To use it outside of ``geoapps``, install it with ``simpeg[regular]``.\nTo benefit from dask, install it with ``simpeg[regular, dask]``.\n\n.. _pip documentation: https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/\n\nInstall from a local clone\n--------------------------\npip install path/to/simpeg[regular,dask]\n\nInstall from a local clone in editable mode\n-------------------------------------------\npip install -e path/to/simpeg[regular,dask]\n\n\nLinks\n=====\n\nWebsite:\nhttp://simpeg.xyz\n\n\nSlack (real time chat):\nhttp://slack.simpeg.xyz\n\n\nDocumentation:\nhttp://docs.simpeg.xyz\n\n\nCode:\nhttps://github.com/simpeg/simpeg\n\n\nTests:\nhttps://travis-ci.org/simpeg/simpeg\n\n\nBugs & Issues:\nhttps://github.com/simpeg/simpeg/issues\n',
    'author': 'Rowan Cockett',
    'author_email': 'rowanc1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://simpeg.xyz/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
}


setup(**setup_kwargs)
