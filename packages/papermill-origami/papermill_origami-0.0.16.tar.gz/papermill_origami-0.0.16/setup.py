# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['papermill_origami',
 'papermill_origami.noteable_airflow',
 'papermill_origami.noteable_dagstermill',
 'papermill_origami.noteable_flytekit',
 'papermill_origami.tests',
 'papermill_origami.tests.noteable_dagstermill']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.2.0,<3.0.0',
 'noteable-origami>=0.0.16,<0.0.17',
 'papermill>=2.4.0,<3.0.0']

extras_require = \
{'airflow': ['apache-airflow>=2.4.2,<3.0.0'],
 'dagster': ['dagstermill>=0.17.6,<0.18.0'],
 'flyte': ['flytekit>=1.2.1,<2.0.0', 'flytekitplugins-papermill>=1.2.1,<2.0.0'],
 'prefect': ['prefect-jupyter>=0.2.0,<0.3.0']}

entry_points = \
{'papermill.engine': ['noteable = papermill_origami.engine:NoteableEngine'],
 'papermill.io': ['https:// = papermill_origami.iorw:NoteableHandler',
                  'noteable:// = papermill_origami.iorw:NoteableHandler']}

setup_kwargs = {
    'name': 'papermill-origami',
    'version': '0.0.16',
    'description': 'The noteable API interface',
    'long_description': '# papermill-origami\n    A papermill engine for running Noteable notebooks\n\n<p align="center">\n<a href="https://github.com/noteable-io/papermill-origami/actions/workflows/ci.yaml">\n    <img src="https://github.com/noteable-io/papermill-origami/actions/workflows/ci.yaml/badge.svg" alt="CI" />\n</a>\n<img alt="PyPI - License" src="https://img.shields.io/pypi/l/papermill-origami" />\n<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/papermill-origami" />\n<img alt="PyPI" src="https://img.shields.io/pypi/v/papermill-origami">\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n---------\n\n[Install](#installation) | [Getting Started](#getting-started) | [License](./LICENSE) | [Code of Conduct](./CODE_OF_CONDUCT.md) | [Contributing](./CONTRIBUTING.md)\n\n<!-- --8<-- [start:intro] -->\n## Intro to Papermill-Origami\n\nPapermill-Origami is the bridge library between the [Origami Noteable SDK](https://noteable-origami.readthedocs.io/en/latest/) and [Papermill](https://papermill.readthedocs.io/en/latest/). It build a papermill engine that can talk to Noteable APIs to run Notebooks. \n<!-- --8<-- [end:intro] -->\n\n<!-- --8<-- [start:requirements] -->\n## Requirements\n\nPython 3.8+\n<!-- --8<-- [end:requirements] -->\n\n<!-- --8<-- [start:install] -->\n## Installation\n\n### Poetry\n\n```shell\npoetry add papermill-origami\n```\n\n### Pip\n```shell\npip install papermill-origami\n```\n<!-- --8<-- [end:install] -->\n\n<!-- --8<-- [start:start] -->\n## Getting Started\n\n### API Token\n\nGet your access token from your User Settings -> API Tokens\n\nor alternatively you can generate a post request to generate a new token\n\n```\ncurl -X \'POST\' \\\n  \'https://app.noteable.io/gate/api/v1/tokens\' \\\n  -H \'accept: application/json\' \\\n  -H \'Content-Type: application/json\' \\\n  -d \'{\n  "ttl": 31536000,\n  "name": "my_token"\n}\'\n```\n\n### Engine Registration\n\nThe `noteable` engine keyword will use the following environment variables by default:\n\n```bash\nNOTEABLE_DOMAIN = app.noteable.io\nNOTEABLE_TOKEN = MY_TOKEN_VALUE_HERE\n```\n\nThen the engine is enabled by running papermill as normal. But now you have access to\nthe `noteable://` scheme as well as the ability to tell papermill to use Noteable as\nthe execution location for your notebook.\n\n```python\nimport papermill as pm\n\nfile_id = \'...\'\n\npm.execute_notebook(\n    f\'noteable://{file_id}\',\n    None, # Set no particular output notebook, but a log of the resulting exeuction link still prints\n    # This turns on the Noteable API interface\n    engine_name=\'noteable\', # exclude this kwarg to run the Notebook locally\n)\n```\n\n#### Advanced Setup\n\nFor more advanced control or reuse of a NoteableClient SDK object you can use\nthe async await pattern around a client constructor. This reuses the connection\nthroughout the life cycle of the context block.\n\n```python\nimport papermill as pm\nfrom papermill.iorw import papermill_io\nfrom papermill_origami import ClientConfig, NoteableClient, NoteableHandler \n\n\ndomain = \'app.noteable.io\'\ntoken = MY_TOKEN_VALUE_HERE\nfile_id = \'...\'\n\nasync with NoteableClient(token, config=ClientConfig(domain=domain)) as client:\n    file = await client.get_notebook(file_id)\n    papermill_io.register("noteable://", NoteableHandler(client))\n    pm.execute_notebook(\n        f\'noteable://{file_id}\',\n        None,\n        engine_name=\'noteable\',\n        # Noteable-specific kwargs\n        file=file,\n        client=client,\n    )\n```\n<!-- --8<-- [end:start] -->\n\n## Contributing\n\nSee [CONTRIBUTING.md](./CONTRIBUTING.md).\n\n-------\n\n<p align="center">Open sourced with ❤️ by <a href="https://noteable.io">Noteable</a> for the community.</p>\n\n<img href="https://pages.noteable.io/private-beta-access" src="https://assets.noteable.io/github/2022-07-29/noteable.png" alt="Boost Data Collaboration with Notebooks">\n',
    'author': 'Matt Seal',
    'author_email': 'matt@noteable.io',
    'maintainer': 'Matt Seal',
    'maintainer_email': 'matt@noteable.io',
    'url': 'https://github.com/noteable-io/papermill-origami',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
