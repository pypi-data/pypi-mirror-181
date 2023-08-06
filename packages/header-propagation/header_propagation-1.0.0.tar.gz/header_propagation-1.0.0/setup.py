# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['header_propagation']

package_data = \
{'': ['*']}

install_requires = \
['starlette>=0.18']

setup_kwargs = {
    'name': 'header-propagation',
    'version': '1.0.0',
    'description': 'Middleware propagating headers from incoming requests to outgoing requests in fastapi',
    'long_description': '# Header Propagation Middleware\n\nMiddleware for propagating headers from incoming requests to outgoing requests for FastAPI.\n\n## Installation\n\n```bash\npip install header-propagation-middleware\n```\n\n## Setup\n\nTo setup the middleware, you need to add it to your FastAPI app.\n\n### Adding Middleware\n\n```python\nfrom header_propagation_middleware import HeaderPropagationMiddleware\n\napp = FastAPI()\napp.add_middleware(HeaderPropagationMiddleware,header_names=["header1","header2"])\n```\n\n#### Configurable middleware argument\n\n**header_names**\n\n-   Type: `List[str]`\n-   Default: `[]`\n-   Description: The list of headers to propagate.\n\n### Accessing propagated headers\n\nYou can access the propagated headers using the `propagated_headers` object.\n\n```python\nfrom header_propagation_middleware import propagated_headers\n\npropagated_headers.get()\n```\n\n**propagated_headers**\n\n-   Type: `dict`\n-   Default: `{}`\n-   Description: The dictionary of propagated headers.\n\n## Tests\n\nRunning test\n\n```bash\npython -m pytest\n```\n\nRunning test with coverage report\n\n```bash\npython -m pytest --cov --cov-report=html:reports/html_dir\n```\n',
    'author': 'Joe Raad',
    'author_email': 'joeraad12@gmail.com',
    'maintainer': 'Joe Raad',
    'maintainer_email': 'joeraad12@gmail.com',
    'url': 'https://github.com/joeraad/header-propagation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
