# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serpentarium']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'serpentarium',
    'version': '0.3.0',
    'description': 'A Python framework for running plugins with conflicting dependencies',
    'long_description': '# serpentarium\nA Python framework for running plugins with conflicting dependencies\n\n## Description\n\nComing soon!\n\n## Installation\n\n`pip install serpentarium`\n\n## Caveats\n\n- This package is highly experimental\n- `import serpentarium` must be the first thing that your code imports so that\n  it can save the state of the interpreter\'s import system before any other\n  imports modify it.\n- MultiprocessingPlugin only works with the "spawn" method (for now). On Linux,\n  you\'ll need to use a multiprocessing Context object with the "spawn" method\n  to generate any Locks, Events, or other synchronization primitives that will\n  be passed to a plugin.\n- SECURITY: This project loads and executes code from files. Do not load or run\n  plugins from untrusted sources.\n\n## Development\n### Pre-commit hooks\n`pre-commit install`\n',
    'author': 'Mike Salvatore',
    'author_email': 'mike.s.salvatore@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guardicode/serpentarium',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
