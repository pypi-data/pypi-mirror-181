# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['censusdis']

package_data = \
{'': ['*']}

install_requires = \
['Rtree>=1.0.0,<2.0.0',
 'divintseg>=0.2.4,<0.3.0',
 'geopandas>=0.11.1,<0.12.0',
 'geopy>=2.2.0,<3.0.0',
 'matplotlib>=3.5.3,<4.0.0',
 'requests>=2.28.1,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=5.1.1,<6.0.0',
          'sphinx-rtd-theme==1.0.0',
          'sphinx-copybutton>=0.5.1,<0.6.0',
          'sphinxcontrib-napoleon==0.7',
          'toml>=0.10.0,<0.11.0']}

setup_kwargs = {
    'name': 'censusdis',
    'version': '0.8.6',
    'description': 'US Census utilities for a variety of data loading and mapping purposes.',
    'long_description': '# censusdis\n\n[![Hippocratic License HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl-eco-extr-ffd-law-mil-sv.html)\n\n[![Documentation Status](https://readthedocs.org/projects/censusdis/badge/?version=latest)](https://censusdis.readthedocs.io/en/latest/?badge=latest)\n\n![Tests Badge](reports/junit/tests-badge.svg)\n![Coverage Badge](reports/coverage/coverage-badge.svg)\n![Notebook Tests Badge](reports/nbmake/nbmake-badge.svg)\n\n![PyPI - Downloads](https://img.shields.io/pypi/dm/censusdis)\n\n[<img src="docs/_static/images/sample00.png" alt="Integration in SoMa Tracts" height=160>](notebooks/SoMa%20DIS%20Demo.ipynb)\n[<img src="docs/_static/images/sample01.png" alt="Diversity in New Jersey" height=160>](notebooks/Data%20With%20Geometry.ipynb)\n[<img src="docs/_static/images/sample02.png" alt="2020 Median Income by County in Georgia" height=160>](notebooks/Data%20With%20Geometry.ipynb)\n[<img src="docs/_static/images/sample03.png" alt="White Alone Population as a Percent of County Population" height=160>](notebooks/Seeing%20White.ipynb)\n[<img src="docs/_static/images/sample04.png" alt="Average Age by Public Use Microdata Area in Massachusetts" height=160>](notebooks/PUMS%20Demo.ipynb)\n\n## Introduction \n\n`censusdis` is a package for discovering, loading, analyzing, and computing\ndiversity, integration, and segregation metrics\nto U.S. Census demographic data. It is designed to be intuitive and Pythonic,\nbut give users access to the full collection of data and maps the US Census\npublishes via their APIs. \n\n> ### I\'m sold! I want to dive right in!\n> \n> To get straight to installing and trying out\n> code hop over to our \n> [Getting Started](https://censusdis.readthedocs.io/en/latest/intro.html)\n> guide.\n\n`censusdis` lets you quickly and easily load US Census data and make plots like \nthis one:\n\n![Median income by block group in GA](docs/_static/images/sample02.png)\n\nWe downloaded the data behind this plot, including\nthe geometry of all the block groups, with a\nsingle call:\n\n```python\nimport censusdis.data as ced\nfrom censusdis.states import STATE_GA\n\n# This is a census variable for median household income.\n# See https://api.census.gov/data/2020/acs/acs5/variables/B19013_001E.html\nMEDIAN_HOUSEHOLD_INCOME_VARIABLE = "B19013_001E"\n\ngdf_bg = ced.download_detail(\n    "acs/acs5",  # The American Community Survey 5-Year Data\n    2020, \n    ["NAME", MEDIAN_HOUSEHOLD_INCOME_VARIABLE], \n    state=STATE_GA, \n    block_group="*", \n    with_geometry=True\n)\n```\n\nSimilarly, we can download data and geographies, do a little\nanalysis on our own using familiar [Pandas](https://pandas.pydata.org/)\ndata frame operations, and plot graphs like these\n\n![Percent of population identifying as white by county](docs/_static/images/sample03.png)\n![Integration is SoMa](docs/_static/images/sample00.png)\n\n## Modules\n\nThe modules that make up the `censusdis` package are\n\n| Module                | Description                                                                                                   |\n|-----------------------|:--------------------------------------------------------------------------------------------------------------|\n| `censusdis.geography` | Code for managing geography hierarchies in which census data is organized.                                    | \n| `censusdis.data`      | Code for fetching data from the US Census API, including managing datasets, groups, and variable hierarchies. |\n| `censusdis.maps`      | Code for downloading map data from the US, caching it locally, and using it to render maps.                   |\n| `censusdis.states`    | Constants defining the US States. Used by the three other modules.                                            |\n\n## Demonstration Notebooks\n\nThere are several demonstration notebooks available to illustrate how `censusdis` can\nbe used. They are found in the \n[notebook](https://github.com/vengroff/censusdis/tree/main/notebooks) \ndirectory of the source code.\n\nThe demo notebooks include\n\n| Notebook Name                                                                    | Description                                                                                                                                                                          |\n|----------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| [ACS Demo.ipynb](./notebooks/ACS%20Demo.ipynb)                                   | Load American Community Survey (ACS) data for New Jersey and plot diversity statewide at the census block group level.                                                               |\n| [Data With Geometry.ipynb](./notebooks/Data%20With%Geometry.ipynb)               | Load American Community Survey (ACS) data for New Jersey and plot diversity statewide at the census block group level.                                                               |\n| [Exploring Variables.ipynb](./notebooks/Exploring%20Variables.ipynb)             | Load metatdata on a group of variables, visualize the tree hierarchy of variables in the group, and load data from the leaves of the tree.                                           |\n| [Getting Started Examples.ipynb](./notebooks/Getting%20Started%20Examples.ipynb) | Sample code from the [Getting Started](https://censusdis.readthedocs.io/en/latest/intro.html) guide.                                                                                 |                                                         |\n| [Map Demo.ipynb](./notebooks/Map%20Demo.ipynb)                                   | Demonstrate loading at plotting maps of New Jersey at different geographic granularity.                                                                                              |\n| [Map Geographies.ipynb](./notebooks/Map%20Geographies.ipynb)                     | Illustrates a large number of different map geogpraphies and how to load them.                                                                                                       |\n| [PUMS Demo.ipynb](./notebooks/PUMS%20Demo.ipynb)                                 | Load Public-Use Microdata Samples (PUMS) data for Massachusetts and plot it.                                                                                                         |\n| [Seeing White.ipynb](./notebooks/Seeing%20White.ipynb)                           | Load nationwide demographic data at the county level and plot of map of the US showing the percent of the population who identify as white only (no other race) at the county level. | \n| [SoMa DIS Demo.ipynb](./notebooks/SoMa%20DIS%20Demo.ipynb)                       | Load race and ethnicity data for two towns in Essex County, NJ and compute diversity and integration metrics.                                                                        |\n\n## Diversity and Integration Metrics\n\nDiversity and integration metrics from the `divintseg` package are \ndemonstrated in some notebooks.\n\nFor more information on these metrics\nsee the [divintseg](https://github.com/vengroff/divintseg/) \nproject.\n\n',
    'author': 'Darren Vengroff',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vengroff/censusdis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
