# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssdb', 'ssdb.asyncio', 'ssdb.core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-ssdb',
    'version': '1.0.1',
    'description': 'Python implementation of SSDB client',
    'long_description': '# python-ssdb\nPython implementation of SSDB Client\n\n## Features\n- Use connection pool\n- Support both sync & async clients\n    - Sync: `ssdb.SSDB`\n    - Async: `ssdb.asyncio.SSDB`\n',
    'author': 'lsh918',
    'author_email': 'vx0918@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lsh918/python-ssdb',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}
from build_extension import *
build(setup_kwargs)

setup(**setup_kwargs)
