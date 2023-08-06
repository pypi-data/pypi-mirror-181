# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['node_edge']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'node-edge',
    'version': '0.1.0b5',
    'description': 'A tool to run Node code from Python',
    'long_description': '# node-edge\n\n![Unit Tests](https://github.com/ModelW/py-node-edge/actions/workflows/tests.yml/badge.svg)\n![Documentation](https://readthedocs.org/projects/node-edge/badge/?version=latest)\n\nThis tool allows you to run Node code from Python, including dependency\nmanagement:\n\n```python\nfrom node_edge import NodeEngine\n\npackage = {\n    "dependencies": {\n        "axios": "^1.2.0",\n    },\n}\n\n\nwith NodeEngine(package) as ne:\n    axios = ne.import_from("axios")\n    print(axios.get("https://httpbin.org/robots.txt").data)\n```\n\n## Documentation\n\n[✨ **Documentation is there** ✨](https://node-edge.rtfd.io)\n',
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ModelW/py-node-edge',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
