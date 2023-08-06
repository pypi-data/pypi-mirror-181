# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clinlp']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=3.4.4,<4.0.0']

setup_kwargs = {
    'name': 'clinlp',
    'version': '0.0.1',
    'description': '',
    'long_description': '# clinlp\n\n![clinlp](media/clinlp.png)\n\nCreate performant and production-ready NLP pipelines for clinical text written in Dutch using `clinlp`.\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
