# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['comic_home_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'comic-home-api',
    'version': '0.1.0',
    'description': 'A comic home api package.',
    'long_description': '# comic_home_api\n\nA comic home api package.\n\n## Installation\n\n```bash\n$ pip install comic_home_api\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`comic_home_api` was created by Hongbo Liu. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`comic_home_api` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Hongbo Liu',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
