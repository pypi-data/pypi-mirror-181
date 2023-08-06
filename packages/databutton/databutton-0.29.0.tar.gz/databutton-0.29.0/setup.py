# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databutton',
 'databutton.internal',
 'databutton.jobs',
 'databutton.notify',
 'databutton.secrets',
 'databutton.storage']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.6.0,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'httpx>=0.23.0,<0.24.0',
 'pandas>=0.21.0',
 'pydantic>=1.10.2,<2.0.0',
 'tenacity>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'databutton',
    'version': '0.29.0',
    'description': 'The CLI for databutton.com',
    'long_description': "# databutton-cli\n[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)\n[![PyPI version fury.io](https://badge.fury.io/py/databutton.svg)](https://pypi.python.org/pypi/databutton/)\n[![PyPI download week](https://img.shields.io/pypi/dw/databutton.svg)](https://pypi.python.org/pypi/databutton/)\n![release](https://github.com/databutton/databutton-cli/actions/workflows/release.yaml/badge.svg)\n\n\n\nThe CLI for building and deploying databutton projects\n\n## Getting Started\n\n```bash\nUsage: databutton [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -v, --verbose  Enable verbose logging\n  --help         Show this message and exit.\n\nCommands:\n  build    Build the project, built components will be found in .databutton\n  create   Create a Databutton project in the provided project-directory\n  deploy   Deploy your project to Databutton\n  docs     Launches https://docs.databutton.com\n  init     Creates a new project in Databutton and writes to databutton.json\n  login    Login to Databutton\n  logout   Removes all Databutton login info\n  serve    Starts a web server for production.\n  start    Run the Databutton development server\n  version  Get the library version.\n  whoami   Shows the logged in user\n```\n\n## Developing\n\n### Prerequisites\nThis project uses poetry, so if you haven't already;\n\n`pip install poetry`\n\n### Install dependencies\n\n`poetry install`\n\n### Test\n\n`poetry run pytest -s`\n\n### Lint\n`poetry run flake8 .`\n`poetry run black .`\n`poetry run isort .`\n\nAll these are being run in a github action on pull requests and the main branch.\n\n### Test locally in another package\n\nTo test in another package, you can simply\n\n`pip install -e .` assuming you're in this folder. If not, replace the `.` with the path to the `databutton-cli` folder.\n\n## Authors\n\n* **Databutton** - *Initial work* - [github](https://github.com/databutton)\n\n## License: Copyright (c) Databutton\n\nAll rights reserved.\n\n\n",
    'author': 'Databutton',
    'author_email': 'hi@databutton.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
