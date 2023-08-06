# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinx_graph']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.8.8,<3.0.0', 'sphinx>=5.3.0,<6.0.0']

setup_kwargs = {
    'name': 'sphinx-graph',
    'version': '0.1.0',
    'description': "'Sphinx-Graph' is a plain-text, VCS-friendly, requirements management tool.",
    'long_description': 'None',
    'author': 'Daniel Eades',
    'author_email': 'danieleades@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
