# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mds_jl6276_finalproject']

package_data = \
{'': ['*']}

install_requires = \
['folium>=0.14.0,<0.15.0', 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'mds-jl6276-finalproject',
    'version': '0.1.0',
    'description': "A final project for MDS 2022 Fall. It includes a function that relies on Yelp api, and the funtion takes in a catagory in terms like 'bars', 'restaurant', etc... and return the location of resaurant in New York On map.",
    'long_description': "# mds_jl6276_finalproject\n\nA final project for MDS 2022 Fall. It includes a function that relies on Yelp api, and the funtion takes in a catagory in terms like 'bars', 'restaurant', etc... and return the location of resaurant in New York On map.\n\n## Installation\n\n```bash\n$ pip install mds_jl6276_finalproject\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`mds_jl6276_finalproject` was created by Jin Liu. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`mds_jl6276_finalproject` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Jin Liu',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
