# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postfixcalc']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.12.0,<23.0.0']

setup_kwargs = {
    'name': 'postfixcalc',
    'version': '0.4.0',
    'description': 'the stupid postfix evaluator',
    'long_description': '# postfixcalc\n\nSimple and stupid infix to postfix converter and evaluator.\n',
    'author': 'Mahdi Haghverdi',
    'author_email': 'mahdihaghverdiliewpl@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
