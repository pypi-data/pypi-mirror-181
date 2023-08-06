# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysource_minimize']

package_data = \
{'': ['*']}

install_requires = \
['asttokens>=2.0.8,<3.0.0', 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'pysource-minimize',
    'version': '0.3.0',
    'description': 'find failing section in python source',
    'long_description': '# minimize source code\n\nIf you build a linter, formatter or any other tool which has to analyse python source code you might end up searching bugs in pretty large input files.\n\n\n`pysource_minimize` is able to remove everything from the python source which is not related to the problem.\n\nExample:\n``` pycon\n>>> from pysource_minimize import minimize\n\n>>> source = """\n... def f():\n...     print("bug"+"other string")\n...     return 1+1\n... f()\n... """\n\n>>> print(minimize(source, lambda new_source: "bug" in new_source))\n"""bug"""\n\n\n```\n',
    'author': 'Frank Hoffmann',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
