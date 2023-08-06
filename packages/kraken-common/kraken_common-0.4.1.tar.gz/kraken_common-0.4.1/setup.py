# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['common', 'common.pyenv']

package_data = \
{'': ['*']}

install_requires = \
['builddsl>=1.0.0,<2.0.0',
 'setuptools',
 'tomli>=1.0.0,<3.0.0',
 'tomli_w>=0.4.0,<2.0.0',
 'typing-extensions>=3.0.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6,<0.7']}

setup_kwargs = {
    'name': 'kraken-common',
    'version': '0.4.1',
    'description': '',
    'long_description': '# kraken-common\n\nThe <u>`kraken-common`</u> package is the shared utility namespace for the Kraken build system and\nthe Kraken wrapper CLI. It contains various generic utilities, as well as the tools for loading\nthe metadata of a Kraken project.\n\nAside from general utilities that are used by one, the other or both, this package also implements the\nshared logic for executing Kraken Python and BuildDSL build scripts and retrieving its metadata.\n\n### Script runners\n\nThe following types of Kraken script runners are currently available via the `kraken.common` package:\n\n* `PythonScriptRunner`: Matches a `kraken.py` or `.kraken.py` file and runs it as a pure Python script.\n* `BuildDslScriptRunner`: Matches a `kraken.build` or `.kraken.build` file and runs it as a [`builddsl`][0]\n    script, with the `buildscript()` function being available by default.\n\n[0]: https://niklasrosenstein.github.io/python-builddsl/\n\n### Buildscript metadata\n\nA Kraken project contains at least one `.kraken.py` file (build script) and maybe a `.kraken.lock`\nfile (lock file). The build script at the root of a project may contain hints for the Kraken wrapper\nCLI to be able to correctly bootstrap an environment that contains the Kraken build system.\n\n<table align="center"><tr><th>Python</th><th>BuildDSL</th></tr>\n<tr><td>\n\n```py\nfrom kraken.common import buildscript\n\nbuildscript(\n    requirements=["kraken-std ^0.4.16"],\n)\n```\n\n</td><td>\n\n```py\nbuildscript {\n    requires "kraken-std ^0.4.16"\n}\n\n\n```\n\n</td></tr></table>\n\nThe way that this works is that the `buildscript()` function raises an exception that aborts the execution\nof the build script before the rest of the script is executed, and the exception contains the metadata.\nWhen the build script is executed by the Kraken build system instead, the function does nothing.\n\nThe API to capture the data passed to a call to the `buildscript()` function is as follows:\n\n```py\nfrom kraken.common import BuildscriptMetadata\n\nwith BuildscriptMetadata.capture() as metadata_future:\n    ...\n\nmetadata = metadata_future.result()\n```\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
