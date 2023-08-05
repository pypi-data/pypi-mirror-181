# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ujsondiff']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis>=6.60.0,<7.0.0']

setup_kwargs = {
    'name': 'ujsondiff',
    'version': '3.0.0',
    'description': 'Diff JSON and JSON-like structures in Python',
    'long_description': '## ujsondiff\n========\n\nDiff JSON and JSON-like structures in Python.\n\n# Installation\n------------\n\n`pip install ujsondiff`\n\n# Quickstart\n----------\n\n```\n>>> import ujsondiff as jd\n>>> from ujsondiff import diff\n\n>>> diff({\'a\': 1, \'b\': 2}, {\'b\': 3, \'c\': 4})\n{\'c\': 4, \'b\': 3, delete: [\'a\']}\n\n>>> diff([\'a\', \'b\', \'c\'], [\'a\', \'b\', \'c\', \'d\'])\n{insert: [(3, \'d\')]}\n\n>>> diff([\'a\', \'b\', \'c\'], [\'a\', \'c\'])\n{delete: [1]}\n\n# Typical diff looks like what you\'d expect...\n>>> diff({\'a\': [0, {\'b\': 4}, 1]}, {\'a\': [0, {\'b\': 5}, 1]})\n{\'a\': {1: {\'b\': 5}}}\n\n# ...but similarity is taken into account\n>>> diff({\'a\': [0, {\'b\': 4}, 1]}, {\'a\': [0, {\'c\': 5}, 1]})\n{\'a\': {insert: [(1, {\'c\': 5})], delete: [1]}}\n\n# Support for various diff syntaxes\n>>> diff({\'a\': 1, \'b\': 2}, {\'b\': 3, \'c\': 4}, syntax=\'explicit\')\n{insert: {\'c\': 4}, update: {\'b\': 3}, delete: [\'a\']}\n\n>>> diff({\'a\': 1, \'b\': 2}, {\'b\': 3, \'c\': 4}, syntax=\'symmetric\')\n{insert: {\'c\': 4}, \'b\': [2, 3], delete: {\'a\': 1}}\n\n# Special handling of sets\n>>> diff({\'a\', \'b\', \'c\'}, {\'a\', \'c\', \'d\'})\n{discard: set([\'b\']), add: set([\'d\'])}\n\n# Load and dump JSON\n>>> print diff(\'["a", "b", "c"]\', \'["a", "c", "d"]\', load=True, dump=True)\n{"$delete": [1], "$insert": [[2, "d"]]}\n\n# NOTE: Default keys in the result are objects, not strings!\n>>> d = diff({\'a\': 1, \'delete\': 2}, {\'b\': 3, \'delete\': 4})\n>>> d\n{\'delete\': 4, \'b\': 3, delete: [\'a\']}\n>>> d[jd.delete]\n[\'a\']\n>>> d[\'delete\']\n4\n# Alternatively, you can use marshal=True to get back strings with a leading $\n>>> diff({\'a\': 1, \'delete\': 2}, {\'b\': 3, \'delete\': 4}, marshal=True)\n{\'delete\': 4, \'b\': 3, \'$delete\': [\'a\']}\n\n```',
    'author': 'BP Greyling',
    'author_email': 'bpgreyling@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CrispyCrafter/ujsondiff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
