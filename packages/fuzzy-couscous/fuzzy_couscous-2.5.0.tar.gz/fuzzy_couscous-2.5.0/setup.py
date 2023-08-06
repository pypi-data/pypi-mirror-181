# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuzzy_couscous',
 'fuzzy_couscous.commands',
 'fuzzy_couscous.commands.remove_poetry']

package_data = \
{'': ['*']}

install_requires = \
['dict-deep>=4.1.2,<5.0.0',
 'httpx>=0.23.1,<0.24.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'rich>=12.6.0,<13.0.0',
 'tomli-w>=1.0.0,<2.0.0',
 'typer>=0.7.0,<0.8.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['cuzzy = fuzzy_couscous.main:cli',
                     'fuzzy-couscous = fuzzy_couscous.main:cli']}

setup_kwargs = {
    'name': 'fuzzy-couscous',
    'version': '2.5.0',
    'description': 'A cli tool to bootstrap your django projects and enhance your development experience.',
    'long_description': "# fuzzy-couscous\n\n[![pypi](https://badge.fury.io/py/fuzzy-couscous.svg)](https://pypi.org/project/fuzzy-couscous/)\n[![Docs: Mkdocs](https://img.shields.io/badge/mkdocs-docs-blue.svg)](https://tobi-de.github.io/fuzzy-couscous)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/fuzzy-couscous/blob/master/LICENSE)\n[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://www.djlint.com)\n[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)\n\n✨📚✨ [Read the full documentation](https://tobi-de.github.io/fuzzy-couscous)\n\nMy highly opinionated django project template based on [django's startproject --template](https://docs.djangoproject.com/en/stable/ref/django-admin/#startproject).\nThis project is heavily inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) but is meant to be a lighter version.\nThis template also comes with a cli tool with [additional commands](https://tobi-de.github.io/fuzzy-couscous/usage/#cuzzy) to hopefully improve your django development experience.\n\n![showcase gif](https://raw.githubusercontent.com/Tobi-De/fuzzy-couscous/main/docs/assets/cuzzy_demo.gif)\n\n## Features\n\n- Django 4+\n- Python 3.10+\n- Frontend: [htmx](https://htmx.org/) with [editor support](https://oluwatobi.dev/blog/posts/htmx-support-in-pycharm/) using [web-types](https://github.com/JetBrains/web-types#web-types)\n- Template fragment with [django-render-block](https://github.com/clokep/django-render-block)\n- Secure production settings, https only.\n- Settings using [django-environ](https://github.com/joke2k/django-environ)\n- Login / signup via [django-allauth](https://github.com/pennersr/django-allauth)\n- Custom user model based on [django-improved-user](https://github.com/jambonsw/django-improved-user)\n- Login using email instead of username\n- Automatically reload your browser in development via [django-browser-reload](https://github.com/adamchainz/django-browser-reload)\n- Better development experience with [django-fastdev](https://github.com/boxed/django-fastdev)\n- [Amazon SES](https://aws.amazon.com/ses/?nc1=h_ls) for production email via [Anymail](https://github.com/anymail/django-anymail)\n- [Docker](https://www.docker.com/) ready for production\n- Optional production cache settings using the `CACHE_URL` or `REDIS_URL` environment variables.\n- `captain-definition` for deploying to [caprover](https://caprover.com/)\n- [Sentry](https://sentry.io/welcome/) for performance/error monitoring\n- Serve static files with [Whitenoise](https://whitenoise.evans.io/en/latest/)\n- Default integration with [pre-commit](https://github.com/pre-commit/pre-commit) for identifying simple issues before submission to code review\n- Integrated task runner with [poethepoet](https://github.com/nat-n/poethepoet)\n- Dependency management using [poetry](https://github.com/python-poetry/poetry) (can be replaced by [virtualenv](https://github.com/pypa/virtualenv) using the [`remove-poetry` command](https://tobi-de.github.io/fuzzy-couscous/usage/#cuzzy-remove-poetry))\n\n## Templates\n\nI use github branches to create variations of the base template.\n\n- [main](https://github.com/Tobi-De/fuzzy-couscous): The base template\n- [tailwind](https://github.com/Tobi-De/fuzzy-couscous/tree/tailwind): The base template + [tailwindcss](https://github.com/timonweb/pytailwindcss)  via [pytailwindcss](https://github.com/timonweb/pytailwindcss)\n- [bootstrap](https://github.com/Tobi-De/fuzzy-couscous/tree/bootstrap): The base template + [bootstrap5](https://getbootstrap.com/) via [django-bootstrap5](https://github.com/zostera/django-bootstrap5)\n\n## Quickstart\n\nInstall the latest version of the package\n\n```shell\npip install fuzzy-couscous --upgrade\n```\n\nInitialize a new project\n\n```shell\ncuzzy make project_name\n```\n\n> **Note**: You must have django installed in your global python interpreter for this command to work. If you try to\n> run this command on a version of django lower than **4**, it will fail with a nasty error.\n\n## Development\n\nPoetry is required (not really, you can set up the environment however you want and install the requirements\nmanually) to set up a virtualenv, install it then run the following:\n\n```sh\npoetry install\npre-commit install --install-hooks\n```\n\nTests can then be run quickly in that environment:\n\n```sh\npytest\n```\n\n## Feedback\n\nIf you have any feedback, please reach out to me at tobidegnon@proton.me or [open a discussion](https://github.com/Tobi-De/fuzzy-couscous/discussions/new).\n\n## Contributors\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n",
    'author': 'Tobi-De',
    'author_email': 'tobidegnon@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://tobi-de.github.io/fuzzy-couscous/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
