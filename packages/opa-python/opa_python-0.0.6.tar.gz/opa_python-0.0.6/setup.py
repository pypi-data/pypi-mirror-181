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
    'version': '0.0.6',
    'description': 'A Python OPA client library',
    'long_description': '# OPA Python\n\nPython client library for Open Policy Framework (OPA).\n\n## Installation\n\n    python -m pip install opa-python\n    \n## Compatibility\n\nThe library has been tested with:\n\n- Python 3.10\n- OPA 0.40.0\n    \n## Usage\n\nCreate a client instance:\n\n```python\nfrom opa import OPAClient\nclient = OPAClient(url="http://opa-server/")\n```\n\nVerify that the OPA server is up and ready to accept requests:\n\n```python\nclient.check_health()\n```\n    \nCreate or update a document:\n\n```python\ndata = {\n    "users": [\n        "bilbo",\n        "frodo",\n        "gandalf",\n    ],\n}\nclient.save_document("my.data", data)\n```\n    \nCreate or update a policy:\n\n```python\npolicy = """\npackage my.policy\n\ndefault allow := false\n\nallow {\n    data.my.data.users[_] = input.name\n}\n"""\nclient.save_policy("policy-id", policy)\n```\n    \nRequest decisions by evaluating input against the policy and data:\n\n```python\nclient.check_policy("my.policy.allow", {"name": "bilbo"})\nclient.check_policy("my.policy.allow", {"name": "sauron"})\n```\n\nWe\'re working on the documentation. Please refer to the tests or source code\nin the meantime.\n    \n## Local installation\n\nInstall [Poetry](https://python-poetry.org/), create new environment and\ninstall the dependencies:\n\n    poetry install\n    \n## Running the test suite\n\nNOTE: Each individual test that communicates with OPA creates a fresh Docker\ncontainer. This is pretty neat from a testing perspective, but means that\nrunning the entire suite takes a bit of time.\n\nMake sure you do not have any services listening to `8181` when you start the\ntests! We might add a configuration for setting the port later, or run the\ntests in Docker as well.\n\nRun the tests:\n\n    poetry run pytest\n    \nRun specific test module:\n\n    poetry run pytest tests/test_integration.py\n    \n## Publishing\n\nSet your credentials:\n\n    poetry config pypi-token.pypi <token>\n\nBuild and publish:\n\n    poetry publish --build\n',
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
