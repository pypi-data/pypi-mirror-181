# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['censusdis']

package_data = \
{'': ['*']}

install_requires = \
['Rtree>=1.0.0,<2.0.0',
 'divintseg>=0.2.0,<0.3.0',
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
    'version': '0.8.2',
    'description': 'US Census utilities for a variety of data loading and mapping purposes.',
    'long_description': '# censusdis\n\n[![Hippocratic License HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl-eco-extr-ffd-law-mil-sv.html)\n\n[![Documentation Status](https://readthedocs.org/projects/censusdis/badge/?version=latest)](https://censusdis.readthedocs.io/en/latest/?badge=latest)\n\n[![lint](https://github.com/vengroff/censusdis/actions/workflows/lint.yml/badge.svg)](https://github.com/vengroff/censusdis/actions/workflows/lint.yml)\n\n![Tests Badge](reports/junit/tests-badge.svg)\n![Coverage Badge](reports/coverage/coverage-badge.svg)\n\n## Introduction \n\n`censusdis` is a package for discovering, loading, analyzing, and computing\ndiversity, integration, and segregation metrics\nto U.S. Census demographic data. It is designed to be intuitive and Pythonic,\nbut give users access to the full collection of data and maps the US Census\npublishes via their APIs. Data and maps are returned in familiar\n[Pandas](https://pandas.pydata.org/)\nand \n[GeoPandas](https://geopandas.org/en/stable/)\nformats for easy integration with a wide variety of other Python data \nanalysis, machine learning, and plotting tools.\n\n### Data Loading\n\nThe `censusdis` data loading capabilities have been tested extensively with data from the \n[American Community Survey (ACS) 5-year data set](https://www.census.gov/data/developers/data-sets/acs-5year.html).\nThey also work well with other data sets available via the US Census API. \n\n### Maps\n\n\'censusdis\' can also be used to load geographic data from the US Census\nfor geospatial calculations. Maps for a variety of geographic features \nas described [here](https://www.census.gov/cgi-bin/geo/shapefiles/index.php)\ncan be downloaded and cached locally via Python APIs instead of by manual\ndownload from the US Census website.\n\nAdditionally, for plotting high quality maps, `censusdis` can download\ncartographic boundary file data. These are available at various resolutions\nand sometimes change from year to year. For example, here is what is\navailable from the US Census for \n[2020](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html).\n\n### Installation and Getting Started\n\n`censusdis` can be installed in any python 3.9+ virtual environment using\n\n```shell\npip install censusdis\n```\n\nFrom there, you can download your first data with something as simple as\n\n```python\nimport censusdis.data as ced\n\ndf_county_names = ced.download_detail(\n    \'acs/acs5\',\n    2020,\n    [\'NAME\'],\n    state="*",\n    county="*"\n)\n```\n\nThis will return a dataframe of containing the names of all 3,221 counties\nin the United States as of 2020.\n\nOf course, there is far more you can do with `censusdis` than this. We encourage\nyou to check out the [sample notebooks](https://github.com/vengroff/censusdis/tree/main/notebooks)\nprovided with the project for more complete examples.\n\n## Modules\n\nThe modules that make up the `censusdis` package are\n\n| Module                | Description                                                                                                   |\n|-----------------------|:--------------------------------------------------------------------------------------------------------------|\n| `censusdis.geography` | Code for managing geography hierarchies in which census data is organized.                                    | \n| `censusdis.data`      | Code for fetching data from the US Census API, including managing datasets, groups, and variable hierarchies. |\n| `censusdis.maps`      | Code for downloading map data from the US, caching it locally, and using it to render maps.                   |\n| `censusdis.states`    | Constants defining the US States. Used by the three other modules.                                            |\n\n## Demonstration Notebooks\n\nThere are several demonstration notebooks available to illustrate how `censusdis` can\nbe used. They are found in the \n[notebook](https://github.com/vengroff/censusdis/tree/main/notebooks) \ndirectory of the source code.\n\nThe notebooks include\n\n| Notebook Name                                                                                                      | Description                                                                                                                                                                          |\n|--------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| [SoMa DIS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/SoMa%20DIS%20Demo.ipynb)           | Load race and ethnicity data for two towns in Essex County, NJ and compute diversity and integration metrics.                                                                        |\n| [ACS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/ACS%20Demo.ipynb)                       | Load American Community Survey (ACS) data for New Jersey and plot diversity statewide at the census block group level.                                                               |\n| [PUMS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/PUMS%20Demo.ipynb)                     | Load Public-Use Microdata Samples (PUMS) data for Massachusetts and plot it.                                                                                                         |\n| [Seeing White.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Seeing%20White.ipynb)               | Load nationwide demographic data at the county level and plot of map of the US showing the percent of the population who identify as white only (no other race) at the county level. | \n| [Map Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Map%20Demo.ipynb)                       | Demonstrate loading at plotting maps of New Jersey at different geographic granularity.                                                                                              |\n| [Exploring Variables.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Exploring%20Variables.ipynb) | Load metatdata on a group of variables, visualize the tree hierarchy of variables in the group, and load data from the leaves of the tree.                                           |\n| [Map Geographies.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Map%20Geographies.ipynb)         | Illustrates a large number of different map geogpraphies and how to load them.                                                                                                       |\n\n## Diversity and Integration Metrics\n\nDiversity and integration metrics from the `divintseg` package are \ndemonstrated in some notebooks.\n\nFor more information on these metrics\nsee the [divintseg](https://github.com/vengroff/divintseg/) \nproject.\n\n',
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
