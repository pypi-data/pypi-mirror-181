# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lapidary',
 'lapidary.runtime',
 'lapidary.runtime.auth',
 'lapidary.runtime.model',
 'lapidary.runtime.openapi']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.23.0,<0.24.0',
 'inflection>=0.5.1,<0.6.0',
 'platformdirs>=2.6.0,<3.0.0',
 'pydantic[email]>=1.10.2,<2.0.0',
 'python-mimeparse>=1.6.0,<2.0.0',
 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'lapidary',
    'version': '0.7.3',
    'description': 'Python async OpenAPI client library',
    'long_description': 'Base classes for [Lapidary](https://github.com/pytohon-lapidary/lapidary) async OpenAPI client generator.\n',
    'author': 'Raphael Krupinski',
    'author_email': 'rafalkrupinski@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/python-lapidary/lapidary',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
