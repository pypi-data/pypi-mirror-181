# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wrapper']

package_data = \
{'': ['*']}

install_requires = \
['keyring>=23.8.2,<24.0.0',
 'kraken-common>=0.4.0,<0.5.0',
 'pex>=2.1.103,<3.0.0',
 'setuptools>=33.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['krakenw = kraken.wrapper.main:main']}

setup_kwargs = {
    'name': 'kraken-wrapper',
    'version': '0.2.0',
    'description': '',
    'long_description': '# kraken-wrapper\n\nProvides the `krakenw` command which is a wrapper around Kraken build scripts to construct an isolated and\nreproducible build environment as per the dependencies specified in the script.\n\nBuild scripts _must_ invoke the `kraken.common.buildscript` function at the top to be compatible with Kraken\nwrapper.\n\n<table align="center"><tr><th>Python</th><th>BuildDSL</th></tr>\n<tr><td>\n\n```py\nfrom kraken.common import buildscript\n\nbuildscript(\n    requirements=["kraken-std ^0.4.16"],\n)\n```\n\n</td><td>\n\n```py\nbuildscript {\n    requires "kraken-std ^0.4.16"\n}\n\n\n```\n\n</td></tr></table>\n\nFor backwards compatibility, Kraken wrapper currently still supports reading the build script\'s dependencies from\nthe comment block at the top of the file. Build scripts that still use this method will trigger a warning log with\na recommendation of `buildscript()` code to place at the top of the file instead.\n\n## Recommendations\n\n* When using *local requirements*, using the `VENV` type is a lot faster because it can leverage Pip\'s `in-tree-build`\nfeature. Pex [does not currently support in-tree builds](https://github.com/pantsbuild/pex/issues/1357#issuecomment-860133766).\n  * [`kraken-std`][kraken-std] has a local requirement on itself so that it can use itself to build itself 🤯\n\n[kraken-std]: https://github.com/kraken-build/kraken-std\n\n## Credential management\n\n  [keyring]: https://github.com/jaraco/keyring\n\nPip doesn\'t really have a good way to globally configure credentials for Python package indexes when they are not\nconfigured as an alias in `.piprc` aside from `~/.netrc`. Both of these methods have the drawback that the password\nis stored in plain text on disk. Pip does technically support looking up a password from the system keychain using\nthe [`keyring`][keyring] package, but it doesn\'t store the username and so will have to ask for it via stdin.\n\nTo work around this limitation, kraken-wrapper offers the `auth` command which allows you to configure credentials\nwhere the username is stored in `~/.config/krakenw/config.toml` and the password is stored in the system keychain\n(also using the [`keyring`][keyring] package).\n\n    $ krakenw auth example.jfrog.io -u my@email.org \n    Password for my@email.org:\n\n> __Important note__: If no backend for the `keyring` package is available, kraken-wrapper will fall back to writing\n> the password as plain text into the same configuration file. A corresponding warning will be printed.\n\n## Environment variables\n\nThe following environment variables are handled by kraken-wrapper:\n\n| Variable | Description |\n| -------- | ----------- |\n| `KRAKENW_USE` | If set, it will behave as if the `--use` flag was specified (although the `--use` flag if given will still take precedence over the environment variable). Can be used to enforce a certain type of build environment to use. Available values are `PEX_ZIPAPP`, `PEX_PACKED`, `PEX_LOOSE` and `VENV` (default). |\n| `KRAKENW_REINSTALL` | If set to `1`, behaves as if `--reinstall` was specified. |\n| `KRAKENW_INCREMENTAL` |  If set to `1`, virtual environment build environments are "incremental", i.e. they will be reused if they already exist and their installed distributions will be upgraded. |\n',
    'author': 'Unknown',
    'author_email': 'me@unknown.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
