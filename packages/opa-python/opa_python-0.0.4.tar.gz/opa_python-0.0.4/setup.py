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
    'version': '0.0.4',
    'description': 'A Python OPA client library',
    'long_description': '# OPA Python\n\nPythong client library for Open Policy Framework (OPA).\n\n## Installation\n\nopa-python is available on PyPi and can be installed with pip:\n\n    pip install opa-python\n    \nOr Poetry if you prefer that:\n\n    poetry add opa-python\n    \n## Compatibility\n\nThe library has been tested with:\n\n- Python 3.10\n- OPA 0.40.0\n    \n## Usage\n\nCreate a client instance:\n\n    from opa import OPAClient\n    client = OPAClient(url="http://opa-server/")\n    \nCreate or update a document:\n\n    data = {\n        "users": [\n            "bilbo",\n            "frodo",\n            "gandalf",\n        ],\n    }\n    client.save_document("my.data", data)\n    \nCreate or update a policy:\n\n    policy = """\n    package my.policy\n\n    default allow := false\n\n    allow {\n        data.my.data.users[_] = input.name\n    }\n    """\n    client.save_policy("policy-id", policy)\n    \nCheck the policy:\n\n    client.check_policy({"name": "bilbo"}, "my.policy.allow")\n\nOr with another input value:\n\n    client.check_policy({"name": "sauron"}, "my.policy.allow")\n\nWe\'re working on the documentation. Please refer to the tests or source code\nin the meantime.\n    \n## Local installation\n\nInstall [Poetry](https://python-poetry.org/), create new environment and\ninstall the dependencies:\n\n    poetry install\n    \n## Running the test suite\n\nNOTE: Each individual test that communicates with OPA creates a fresh Docker\ncontainer. This is pretty neat from a testing perspective, but means that\nrunning the entire suite takes a bit of time.\n\nMake sure you do not have any services listening to `8181` when you start the\ntests! We might add a configuration for setting the port later, or run the\ntests in Docker as well.\n\nRun the tests:\n\n    poetry run pytest\n    \nRun specific test module:\n\n    poetry run pytest tests/test_integration.py\n    \n## Publishing\n\nSet your credentials:\n\n    poetry config pypi-token.pypi <token>\n\nBuild and publish:\n\n    poetry publish --build\n',
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
