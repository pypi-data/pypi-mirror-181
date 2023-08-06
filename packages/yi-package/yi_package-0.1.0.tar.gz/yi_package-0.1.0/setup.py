# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['yi_package']
install_requires = \
['ipykernel>=6.19.2,<7.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'nltk>=3.8,<4.0',
 'pandas>=1.5.2,<2.0.0',
 'praw>=7.6.1,<8.0.0',
 'seaborn>=0.12.1,<0.13.0',
 'spacy>=3.4.4,<4.0.0',
 'wordcloud>=1.8.2.2,<2.0.0.0']

setup_kwargs = {
    'name': 'yi-package',
    'version': '0.1.0',
    'description': 'Option B2 ',
    'long_description': '# yi_package\n\nOption B2 \n\n## Installation\n\n```bash\n$ pip install yi_package\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`yi_package` was created by Paige Yi. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`yi_package` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Paige Yi',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pjyi/yi_pacakge',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
