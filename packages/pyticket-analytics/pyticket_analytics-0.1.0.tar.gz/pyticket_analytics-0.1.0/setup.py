# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyticket_analytics']

package_data = \
{'': ['*']}

install_requires = \
['dotenv>=0.0.5,<0.0.6',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pyticket-analytics',
    'version': '0.1.0',
    'description': 'A python package to access ticketmaster data using python, and to provide tools for simple data analytics for the accessed data.',
    'long_description': '# pyticket_analytics\n\nA python package to access ticketmaster data using python, and to provide tools for simple data analytics for the accessed data.\n\n## Installation\n\n```bash\n$ pip install pyticket_analytics\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pyticket_analytics` was created by Ega Kurnia Yazid. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pyticket_analytics` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Ega Kurnia Yazid',
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
