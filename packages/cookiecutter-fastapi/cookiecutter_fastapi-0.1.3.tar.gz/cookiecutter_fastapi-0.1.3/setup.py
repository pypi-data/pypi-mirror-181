# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0',
 'furo>=2022.12.7,<2023.0.0',
 'pytest-cookies>=0.6.1,<0.7.0',
 'pytest>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'cookiecutter-fastapi',
    'version': '0.1.3',
    'description': 'Cookiecutter for fastapi projects',
    'long_description': "# Cookiecutter Fastapi\n\n[![PyPI](https://img.shields.io/pypi/v/cookiecutter-fastapi.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/cookiecutter-fastapi.svg)][status]\n[![Read the documentation at https://cookiecutter-fastapi.readthedocs.io/](https://img.shields.io/readthedocs/cookiecutter-fastapi/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![python](https://img.shields.io/pypi/pyversions/cookiecutter-fastapi)](https://github.com/Tobi-De/cookiecutter-fastapi)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/cookiecutter-fastapi/blob/main/LICENSE)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[read the docs]: https://cookiecutter-fastapi.readthedocs.io/\n[pypi_]: https://pypi.org/project/fastapi-paginator/\n[status]: https://pypi.org/project/fastapi-paginator/\n\nA [Cookiecutter](https://github.com/audreyr/cookiecutter) template for [fastapi](https://fastapi.tiangolo.com) projects, inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).\n\n✨📚✨ [Read the full documentation][read the docs]\n\n## Features\n\n-  [fastapi-users](https://github.com/fastapi-users/fastapi-users) for users authentication and management\n-  [Pydantic](https://pydantic-docs.helpmanual.io/) for settings management\n-  Include a cli tool built with [typer](https://github.com/tiangolo/typer) to simplify project management\n-  [Pre-commit](https://pre-commit.com/) integration included by default\n-  [Tortoise-orm](https://tortoise.github.io/) and [aerich](https://github.com/tortoise/aerich) database setup by default but switchable\n-  Limit-offset pagination helpers included\n-  Sending emails using [aiosmtplib](https://aiosmtplib.readthedocs.io/en/stable/client.html) or [Amazon SES](https://aws.amazon.com/fr/ses/)\n-  Optional integration with [sentry](https://docs.sentry.io/platforms/python/) for error logging\n-  Production [Dockerfile](https://www.docker.com/) included\n-  Integration with [arq](https://github.com/samuelcolvin/arq) for background tasks\n-  Optional setup of HTML templates rendering using [jinja2](https://jinja.palletsprojects.com/en/3.1.x/)\n-  [Procfile](https://devcenter.heroku.com/articles/procfile) for deploying to heroku\n-  Implement the [Health Check API patterns](https://microservices.io/patterns/observability/health-check-api.html) on your fastapi application\n\n### ORM/ODM options\n\n- [Tortoise ORM](https://tortoise.github.io/)\n- [Beanie](https://github.com/roman-right/beanie)\n\n## Usage\n\nInstall the cookiecutter package:\n\n```shell\npip install cookiecutter black isort\n```\n\n**Note**: `Black` and `isort` are used to format your project right after it has been generated.\n\nNow run it against this repo:\n\n```shell\ncookiecutter https://github.com/Tobi-De/cookiecutter-fastapi\n```\n\nYou'll be prompted for some values. Provide them, then a fastapi project will be created for you.\n\n## Contributing\n\nContributions are very welcome. To learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Cookiecutter Fastapi_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n[file an issue]: https://github.com/tobi-de/cookiecutter-fastapi/issues\n\n<!-- github-only -->\n\n[license]: https://github.com/tobi-de/cookiecutter-fastapi/blob/main/LICENSE\n[contributor guide]: https://github.com/tobi-de/cookiecutter-fastapi/blob/main/CONTRIBUTING.md\n",
    'author': 'Tobi-De',
    'author_email': 'tobidegnon@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://cookiecutter-fastapi.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
