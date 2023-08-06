# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djangokit',
 'djangokit.cli',
 'djangokit.cli.scaffolding',
 'djangokit.cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['org-djangokit-core', 'typer[all]>=0.7.0', 'watchdog>=2.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1']}

entry_points = \
{'console_scripts': ['djangokit = djangokit.cli.__main__:app',
                     'dk = djangokit.cli.__main__:app']}

setup_kwargs = {
    'name': 'org-djangokit-cli',
    'version': '0.0.1',
    'description': 'DjangoKit command line interface',
    'long_description': "# DjangoKit CLI\n\nThis package provides the DjangoKit command line interface. When it's\ninstalled, it will install the `djangokit` console script.\n\nTo see a list of commands, run `djangokit` without any arguments (or use\nthe `dk` alias as shown here):\n\n    dk\n\nTo run a Django management command:\n\n    dk manage <args>\n\n## Configuring the CLI\n\nThe DjangoKit CLI can be configured via global options passed to the\n`djangokit` base command or via environment variables, which can be\nadded to your project's `.env` file(s). Using env vars is useful when\nyou want to change a default permanently.\n\n- `--env` / `ENV`: Specify the environment to run commands in.\n\n- `--dotenv-path` / `DOTENV_PATH`: Path to `.env` file. This will be\n  derived from `ENV` if not specified.\n\n- `--settings-module` / `DJANGO_SETTINGS_MODULE`: Specify the Django\n  settings module.\n\n- `--additional_settings_module` / `DJANGO_ADDITIONAL_SETTINGS_MODULE`:\n  Specify an *additional* Django settings module that will be loaded\n  after (and override) the base settings module.\n\n- `--typescript` / `DJANGOKIT_CLI_USE_TYPESCRIPT`: Since using\n  TypeScript is the default, you can use this to disable TypeScript.\n  This will affect how files are generated, for example (e.g. when using\n  `dk add-page`).\n\n- `--quiet` / `DJANGOKIT_CLI_QUIET`: Squelch stdout.\n",
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
