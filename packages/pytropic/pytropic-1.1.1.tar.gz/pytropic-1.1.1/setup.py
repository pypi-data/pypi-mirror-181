# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytropic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytropic',
    'version': '1.1.1',
    'description': 'Train and predict string entropy based on character n-grams',
    'long_description': '# Pytropic\n\n[![PyPI version](https://badge.fury.io/py/pytropic.svg)](https://badge.fury.io/py/pytropic) [![Python package](https://github.com/willf/pytropic/actions/workflows/test.yml/badge.svg)](https://github.com/willf/pytropic/actions/workflows/test.yml)\n\n<img alt="An python with a lot of entropy" src="https://user-images.githubusercontent.com/37049/192400489-7a2fdc49-b29a-4299-a1c6-97c8b97b2eaf.png" width=150>\n\nTrain and predict string entropy based on character n-grams\n\n## Features\n\n- Train a model on a corpus of text\n- multiple n-gram sizes\n- Can name models\n\n## Example\n\n```python\n>>> from pytropic import pytropic\n\n>>> en = pytropic.Model(name=\'English 3-gram\', size=3)\n>>> fr = pytropic.Model(name=\'French 3-gram\', size=3)\n\n>>> with open(\'./corpora/bible-english.txt\') as f:\n        en.train(f)\n>>> with open(\'./corpora/bible-french.txt\') as f:\n        fr.train(f)\n\n>>> t = {\'en\': en, \'fr\': fr}\n\n>>> min(t, key=lambda x: t[x].entropy("this is a test"))\nOut: \'en\'\n\n>>> min(t, key=lambda x: t[x].entropy("c\'est un test"))\nOut: \'fr\'\n```\n',
    'author': 'Will Fitzgerald',
    'author_email': '37049+willf@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
