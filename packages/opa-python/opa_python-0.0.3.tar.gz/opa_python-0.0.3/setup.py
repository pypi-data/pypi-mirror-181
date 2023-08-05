# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opa']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'opa-python',
    'version': '0.0.3',
    'description': 'A Python OPA client library',
    'long_description': '# OPA Python\n\nSimple client for Open Policy Framework (OPA).\n\nUnder construction :)\n\n## Installation\n\nUsing pip:\n\n    pip install opa-python\n    \nUsing Poetry:\n\n    poetry add opa-python\n\n## Usage\n\nSee `./tests` for now :)\n\n## Running the test suite\n\nNOTE: Each individual test that communicates with OPA creates a fresh Docker\ncontainer. This is pretty neat from a testing perspective, but means that\nrunning the entire suite takes a bit of time.\n\nMake sure you do not have any services listening to `8181` when you start the\ntests! We might add a configuration for setting the port later, or run the\ntests in Docker as well.\n\nFirst make sure you have [Poetry](https://python-poetry.org/) installed.\n\nCreate new environment and install the dependencies:\n\n    poetry install\n    \nRun the tests:\n\n    poetry run pytest\n    \nRun specific test module:\n\n    poetry run pytest tests/test_integration.py\n',
    'author': 'Gustaf Sjoberg',
    'author_email': 'gs@helicon.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/heliconhq/opa-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
