# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panoptisch']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0']

entry_points = \
{'console_scripts': ['panoptisch = panoptisch:main']}

setup_kwargs = {
    'name': 'panoptisch',
    'version': '0.1.6',
    'description': 'A recursive Python dependency scanner.',
    'long_description': " ## Panoptisch: A recursive dependency scanner for Python projects\n![](https://img.shields.io/github/commit-activity/w/R9295/panoptisch?style=flat-square)\n![](https://img.shields.io/github/issues/R9295/panoptisch?style=flat-square)\n![](https://img.shields.io/pypi/v/panoptisch?style=flat-square)\n[![Downloads](https://pepy.tech/badge/panoptisch/week)](https://pepy.tech/project/panoptisch)\n![](https://img.shields.io/pypi/format/panoptisch?style=flat-square)\n![](https://img.shields.io/badge/code%20style-black-000000.svg)\n####  ⚠️🚨 Early stage! May not work as expected! Feedback welcome! 🚨⚠️\n#### See: [Introduction Video](https://youtu.be/bDJWl_odXx0)\n#### What?\nPanoptisch scans your Python file or module to find it's imports (aka dependencies) and recursively does so for all dependencies and sub-dependencies.\nIt then generates a dependency tree in JSON for you to parse and enforce import policies.\nImports are resolved by mimicing Python's import system. It's completely static besides the importing of modules to find the location of its source file(s). Panoptisch also features a minimal sandbox to prevent side-effects when importing dependencies. Note that the sandbox is not foolproof!\n\n##### Please NOTE:\nThere are known **limitations and issues** at this stage. Please read this before using Panoptisch.  \nSee: ``LIMITATIONS.md`` [LINK](LIMITATIONS.md).\n\n\n#### Motivation\nI was not able to find a proper dependency scanner for Python. Panoptisch was born out of the need to accurately verify dependency usage accross an entire project.  \nIt's aim is to generate a JSON report that can be parsed and evaluated to **assert import policies**.  \nFor example, you may want to restrict ``os``, ``socket``, ``sys`` and ``importlib`` imports to selected packages.\n\n\n#### Usage\n\n1. Install ``Panoptisch`` in the same virtual environment as your project, this is important!  \n```\npip install panoptisch\n```\n\n2. Use\n```\nusage: panoptisch <module>\n\npositional arguments:\n  module                Name of module or file you wish to scan.\n\noptions:\n  -h, --help            show this help message and exit.\n  --show-stdlib-dir     Prints the automatically resolved stdlib directory.\n  --max-depth MAX_DEPTH\n                        Maximum dependency depth.\n  --out OUT             File to output report.\n  --auto-stdlib-dir     Ignore stdlib modules by automatically resolving their path. MAY BE BUGGY. Try running panoptisch <module_name> --show-stdlib-dir to see the directory before using this.\n  --stdlib-dir STDLIB_DIR Ignore stdlib modules by providing their path.\n  --omit-not-found      Do not include modules that could not be resolved in report.\n  --no-sandbox          Ignore the minimal sandbox implementation.\n```\nA typical run may be\n```\n$ panoptisch <module or file> --max-depth 5 --omit-not-found\n```\n3. See report\n```\n$ more out.json\n```\n4. We might not be interested in the dependencies of standard library modules as we place an implicit trust in them.  \nTo filter them out, use the ``--show-stdlib-dir`` arguement to see if Panoptisch can automatically resolve your standard library directory, typically ``/usr/local/lib/python3.x`` on linux installations. Then you can exclude it using \n```\n$ panoptisch <module or file> --auto-stdlib-dir\n```\nIf Panoptisch cannot automatically resolve your standard library directory, you can find it yourself and provide it as an argument to ``stdlib-dir``\n```\n$ panoptisch <module or file> --stdlib-dir /the/path/to/your/standardlibrary/\n```\n#### LICENSE\nAll work is licensed under the [GNU General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.en.html).\n\n#### Contributing\nFeedback, contributions and issues welcome. \n\n",
    'author': 'aarnav',
    'author_email': 'aarnavbos@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/R9295/panoptisch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
