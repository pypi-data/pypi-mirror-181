# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['syllables']

package_data = \
{'': ['*']}

install_requires = \
['cmudict>=1.0.11,<2.0.0', 'importlib-metadata>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'syllables',
    'version': '1.0.6',
    'description': 'A Python package for estimating the number of syllables in a word.',
    'long_description': "# Syllables: A fast syllable estimator for Python\n\n[![Latest PyPI version](https://img.shields.io/pypi/v/syllables.svg)](https://pypi.python.org/pypi/syllables)\n[![Python CI](https://github.com/prosegrinder/python-syllables/workflows/Python%20CI/badge.svg?branch=main)](https://github.com/prosegrinder/python-syllables/actions?query=workflow%3A%22Python+CI%22)\n\nSyllables is a fast, simple syllable estimator for Python. It's intended for use\nin places where speed matters. For situations where accuracy matters, please\nconsider the [cmudict](https://github.com/prosegrinder/python-cmudict) Python\nlibrary instead.\n\n## Installation\n\n`syllables` is available on PyPI. Simply install it with `pip`:\n\n```bash\npip install syllables\n```\n\n## Usage\n\nSyllables provides a single function, estimate, which estimates the number of\nsyllables in a single word.\n\n```python\n>>> import syllables\n>>> syllables.estimate('estimate')\n4\n>>> syllables.estimate('syllables')\n3\n```\n\n## Credits\n\nBuilt on or modeled after the following open source projects:\n\n- [One Bloke: Counting Syllables Accurately in Python on Google App Engine](http://www.onebloke.com/2011/06/counting-syllables-accurately-in-python-on-google-app-engine/)\n",
    'author': 'David L. Day',
    'author_email': 'david@davidlday.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/prosegrinder/python-syllables',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
