# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cmudict']

package_data = \
{'': ['*'],
 'cmudict': ['data/LICENSE',
             'data/LICENSE',
             'data/LICENSE',
             'data/LICENSE',
             'data/LICENSE',
             'data/LICENSE',
             'data/LICENSE',
             'data/README',
             'data/README',
             'data/README',
             'data/README',
             'data/README',
             'data/README',
             'data/README',
             'data/README.developer',
             'data/README.developer',
             'data/README.developer',
             'data/README.developer',
             'data/README.developer',
             'data/README.developer',
             'data/README.developer',
             'data/cmudict.dict',
             'data/cmudict.dict',
             'data/cmudict.dict',
             'data/cmudict.dict',
             'data/cmudict.dict',
             'data/cmudict.dict',
             'data/cmudict.dict',
             'data/cmudict.phones',
             'data/cmudict.phones',
             'data/cmudict.phones',
             'data/cmudict.phones',
             'data/cmudict.phones',
             'data/cmudict.phones',
             'data/cmudict.phones',
             'data/cmudict.symbols',
             'data/cmudict.symbols',
             'data/cmudict.symbols',
             'data/cmudict.symbols',
             'data/cmudict.symbols',
             'data/cmudict.symbols',
             'data/cmudict.symbols',
             'data/cmudict.vp',
             'data/cmudict.vp',
             'data/cmudict.vp',
             'data/cmudict.vp',
             'data/cmudict.vp',
             'data/cmudict.vp',
             'data/cmudict.vp']}

install_requires = \
['importlib-metadata>=5.1.0,<6.0.0', 'importlib-resources>=5.10.1,<6.0.0']

setup_kwargs = {
    'name': 'cmudict',
    'version': '1.0.12',
    'description': 'A versioned python wrapper package for The CMU Pronouncing Dictionary data files.',
    'long_description': "# CMUdict: Python wrapper for cmudict\n\n[![Latest PyPI version](https://img.shields.io/pypi/v/cmudict.svg)](https://pypi.python.org/pypi/cmudict)\n[![GitHub Workflow Status](https://github.com/prosegrinder/python-cmudict/workflows/Python%20CI/badge.svg?branch=main)](https://github.com/prosegrinder/python-cmudict/actions?query=workflow%3A%22Python+CI%22+branch%3Amain)\n\nCMUdict is a versioned python wrapper package for\n[The CMU Pronouncing Dictionary](https://github.com/cmusphinx/cmudict) data\nfiles. The main purpose is to expose the data with little or no assumption on\nhow it is to be used.\n\n## Installation\n\n`cmudict` is available on PyPI. Simply install it with `pip`:\n\n```bash\npip install cmudict\n```\n\n## Usage\n\nThe cmudict data set includes 4 data files: cmudict.dict, cmudict.phones,\ncmudict.symbols, and cmudict.vp. See\n[The CMU Pronouncing Dictionary](https://github.com/cmusphinx/cmudict) for\ndetails on the data. Chances are, if you're here, you already know what's in the\nfiles.\n\nEach file can be accessed through three functions, one which returns the raw\n(string) contents, one which returns a binary stream of the file, and one which\ndoes minimal processing of the file into an appropriate structure:\n\n```python\n>>> import cmudict\n\n>>> cmudict.dict() # Compatible with NLTK\n>>> cmudict.dict_string()\n>>> cmudict.dict_stream()\n\n>>> cmudict.phones()\n>>> cmudict.phones_string()\n>>> cmudict.phones_stream()\n\n>>> cmudict.symbols()\n>>> cmudict.symbols_string()\n>>> cmudict.symbols_stream()\n\n>>> cmudict.vp()\n>>> cmudict.vp_string()\n>>> cmudict.vp_stream()\n```\n\nThree additional functions are included to maintain compatibility with NLTK:\ncmudict.entries(), cmudict.raw(), and cmudict.words(). See the\n[nltk.corpus.reader.cmudict](http://www.nltk.org/_modules/nltk/corpus/reader/cmudict.html)\ndocumentation for details:\n\n```python\n>>> cmudict.entries() # Compatible with NLTK\n>>> cmudict.raw() # Compatible with NLTK\n>>> cmudict.words() # Compatible with NTLK\n```\n\nAnd finally, the license for the cmudict data set is available as well:\n\n```python\n>>> cmudict.license_string() # Returns the cmudict license as a string\n```\n\n## Credits\n\nBuilt on or modeled after the following open source projects:\n\n- [The CMU Pronouncing Dictionary](https://github.com/cmusphinx/cmudict)\n- [NLTK](https://github.com/nltk/nltk)\n",
    'author': 'David L. Day',
    'author_email': 'david@davidlday.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/prosegrinder/python-cmudict',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
