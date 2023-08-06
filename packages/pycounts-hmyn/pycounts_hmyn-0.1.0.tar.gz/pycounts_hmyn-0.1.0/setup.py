# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycounts_hmyn']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2']

setup_kwargs = {
    'name': 'pycounts-hmyn',
    'version': '0.1.0',
    'description': 'Calculate word counts in a text file!',
    'long_description': '# pycounts_hmyn\n\nCalculate word counts in a text file!\n\n## Installation\n\n```bash\n$ pip install pycounts_hmyn\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pycounts_hmyn` was created by hmyn. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pycounts_hmyn` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'hmyn',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
