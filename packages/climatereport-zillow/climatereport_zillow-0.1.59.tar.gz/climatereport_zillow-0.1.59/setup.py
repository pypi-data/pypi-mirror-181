# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['climatereport_zillow']

package_data = \
{'': ['*'],
 'climatereport_zillow': ['data/fsf_fire_state_summary.csv',
                          'data/fsf_fire_state_summary.csv',
                          'data/fsf_fire_state_summary.csv',
                          'data/fsf_fire_state_summary.csv',
                          'data/fsf_fire_state_summary.csv',
                          'data/fsf_fire_state_summary.csv',
                          'data/fsf_fire_zcta_summary.csv',
                          'data/fsf_fire_zcta_summary.csv',
                          'data/fsf_fire_zcta_summary.csv',
                          'data/fsf_fire_zcta_summary.csv',
                          'data/fsf_fire_zcta_summary.csv',
                          'data/fsf_fire_zcta_summary.csv',
                          'data/fsf_flood_state_summary.csv',
                          'data/fsf_flood_state_summary.csv',
                          'data/fsf_flood_state_summary.csv',
                          'data/fsf_flood_state_summary.csv',
                          'data/fsf_flood_state_summary.csv',
                          'data/fsf_flood_state_summary.csv',
                          'data/fsf_flood_zcta_summary.csv',
                          'data/fsf_flood_zcta_summary.csv',
                          'data/fsf_flood_zcta_summary.csv',
                          'data/fsf_flood_zcta_summary.csv',
                          'data/fsf_flood_zcta_summary.csv',
                          'data/fsf_flood_zcta_summary.csv',
                          'data/fsf_heat_state_summary.csv',
                          'data/fsf_heat_state_summary.csv',
                          'data/fsf_heat_state_summary.csv',
                          'data/fsf_heat_state_summary.csv',
                          'data/fsf_heat_state_summary.csv',
                          'data/fsf_heat_state_summary.csv',
                          'data/fsf_heat_zcta_summary.csv',
                          'data/fsf_heat_zcta_summary.csv',
                          'data/fsf_heat_zcta_summary.csv',
                          'data/fsf_heat_zcta_summary.csv',
                          'data/fsf_heat_zcta_summary.csv',
                          'data/fsf_heat_zcta_summary.csv']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'climatereport-zillow',
    'version': '0.1.59',
    'description': 'Zillow listings do not contain a section on the environmental risk of the property. This package compiles a report on the climate risks of the property in the zillow listing.',
    'long_description': '# climatereport_zillow\n\nUnlike other real estate sites, Zillow listings do not contain a section on the environmental risk of the property in the listing. This package takes a Zillow url as input and uses it to compile an HTML report on the climate risks of the property in the zillow listing. This report will automatically open after running the function. The report includes data provided by the First Street Foundation, under the the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License. \n\n## Installation\n\n```bash\n$ pip install climatereport_zillow\n\n```\n\n## How to Use\n\n$ from climatereport_zillow import climatereport_zillow\n$ climatereport_zillow("https://www.zillow.com/homedetails/13353-Cavandish-Ln-Moreno-Valley-CA-92553/18008847_zpid/")\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`climatereport_zillow` was created by Darci Kovacs. It is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License\n license. \n\n## Credits\n\n`climatereport_zillow` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Darci Kovacs',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DarciKovacs/climatereport_zillow',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
