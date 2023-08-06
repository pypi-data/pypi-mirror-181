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
    'version': '0.5.0',
    'description': 'the stupid postfix evaluator',
    'long_description': '# postfixcalc\n\nSimple and stupid infix to postfix converter and evaluator.\n\n# How does it work\nThe algorithm is very simple and straightforward\n```python\nfrom postfixcalc.pyeval import evaluate\nfrom postfixcalc.ast_parser import (\n    extract_nums_and_ops,\n    flatten_nodes,\n    infix_to_postfix,\n    make_num,\n    parse,\n    relistexpression,\n)\n\n\nevaluate(\n    infix_to_postfix(\n        make_num(\n            relistexpression(\n                flatten_nodes(\n                    extract_nums_and_ops(\n                        parse(\'(-1) ^ 2\')\n                    ),\n                ),\n            ),\n        ),\n    ),\n)\n```\n## We should trace from bottom to top:\n   1. parse the expression using `ast.parse` function. This function will parse the expression based on Python grammar and math op precedence.\n   2. extract numbers, and operators outta parsed expression\n   3. the extracted list contains many nested lists and tuples, so we flatten most of them\n   4. we generate a better demonstration outta the flattened list\n   5. we make possible strings to numbers, \'-1\' will be -1 and ...\n   6. we generate the postfix notation outta the numbers and operators\n   7. evaluate the result\n\nBut all this pain is done easily thorough `Calc` type in the library\n```python\nfrom postfixcalc import Calc\n\ncalc = Calc(\'(-1) ^ 2\')\nprint(calc.answer)\n```\n\nThis is easy but `Calc` type provide other _cached_propertied_ which are just the results of the upper functions\n```python\nfrom postfixcalc import Calc\n\nc = Calc("2 * -1")\nprint(c.parsed)\nprint(c.extracted)\nprint(c.flattened)\nprint(c.strparenthesized)\nprint(c.listparenthesized)\nprint(c.numerized)\nprint(c.postfix)\nprint(c.answer)\n\n# <ast.BinOp object at 0x7fcd313ecbe0>\n# [([2], <ast.Mult object at 0x7fcd32002a70>, [(<ast.USub object at 0x7fcd32003010>, [1])])]\n# ([2], <ast.Mult object at 0x7fcd32002a70>, (<ast.USub object at 0x7fcd32003010>, [1]))\n# 2 * (-1)\n# [2, \'*\', \'(\', \'-1\', \')\']\n# [2, \'*\', \'(\', -1, \')\']\n# [2, -1, \'*\']\n# -2\n```\n',
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
