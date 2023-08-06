# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['air_pollution_check']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'air-pollution-check',
    'version': '0.1.0',
    'description': 'A package for looking into the air pollution data, which can transfer the data into dataframe, add in the overall air pollution to the dataframe, visualize the air pollution data, and output the pollution level comparison from the past to the future for a specific location.',
    'long_description': '# air_pollution_check\n\nA package for looking into the air pollution data, which can transfer the data into dataframe, add in the overall air pollution to the dataframe, visualize the air pollution data, and output the pollution level comparison from the past to the future for a specific location.\n\n## Installation\n\n```bash\n$ pip install air_pollution_check\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`air_pollution_check` was created by Yazhao Huang. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`air_pollution_check` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Yazhao Huang',
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
