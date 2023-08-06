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
    'version': '0.1.1',
    'description': "'Sphinx-Graph' is a plain-text, VCS-friendly, requirements management tool.",
    'long_description': "# Sphinx Graph\n\n[![codecov](https://codecov.io/gh/danieleades/sphinx-graph/branch/main/graph/badge.svg?token=WLPNTQXHrK)](https://codecov.io/gh/danieleades/sphinx-graph)\n[![CI](https://github.com/danieleades/sphinx-graph/actions/workflows/ci.yaml/badge.svg)](https://github.com/danieleades/sphinx-graph/actions/workflows/ci.yaml)\n[![sponsor](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/danieleades)\n[![Documentation Status](https://readthedocs.org/projects/sphinx-graph/badge/?version=main)](https://sphinx-graph.readthedocs.io/en/main/?badge=main)\n\n'Sphinx-Graph' is a plain-text, VCS-friendly, requirements management tool.\n\nWith Sphinx-Graph you define relationships between items in a document. These items form a directed acyclic graph (DAG). The extension-\n\n- checks for cyclic references\n- populates items with links to their 'neighbours'\n- (optionally) tracks a hash of each item to trigger reviews when any parents change\n\nSphinx Graph is *heavily* inspired by [Sphinx-Needs](https://github.com/useblocks/sphinx-needs). Sphinx-Graph started life as a proof of concept refactor of Sphinx-Needs using modern python and strict type checking.\n\n- Sphinx-Needs is the full-featured, grand-daddy of Sphinx-Graph\n- By comparison, Sphinx-Graph is streamlined, and focuses on a much smaller feature set\n\n## Vertices\n\nThe core sphinx directive provided by this extension is a 'Vertex'. A Vertex directive can be used to define relationships between text elements.\n\n```rst\n.. vertex:: USR-001\n\n   this is a user requirement.\n\n   This user requirement forms the basis of derived system requirements. When it is rendered in a\n   sphinx document it will be augmented with links to any child vertices.\n\n.. vertex:: SYS-001\n   :parents: USR-001\n\n   this is system requirement of some sort.\n\n   It is derived from a higher-level user requirement (USR-001).\n   When it is rendered in a sphinx document, it will be augmented with links to its parent as well\n   as any 'children'.\n\n.. vertex:: SYS-002\n   :parents: USR-001:iG91\n\n   this is another system requirement. This time the link to USR-001 is tracking the 'fingerprint'\n   of its parent.\n\n   The fingerprint is a 4-character hash. If USR-001 is modified, then SYS-002 will fail the build\n   until the fingerprint is updated (the build error provides the new fingerprint). This means that\n   changing a Vertex will trigger a review of all dependent vertices.\n```\n\ncheck the [example project](https://sphinx-graph.readthedocs.io/en/main/src/example/index.html) in the documentation\n\n---\n\n*Was this useful? [Buy me a coffee](https://github.com/sponsors/danieleades/sponsorships?sponsor=danieleades&preview=true&frequency=recurring&amount=5)*\n",
    'author': 'Daniel Eades',
    'author_email': 'danieleades@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/danieleades/sphinx-graph',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
