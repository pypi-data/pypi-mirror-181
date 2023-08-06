# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zouhar_contact']

package_data = \
{'': ['*']}

install_requires = \
['pyroll>=1.0.5.post1,<2.0.0']

setup_kwargs = {
    'name': 'pyroll-zouhar-contact',
    'version': '1.0.1',
    'description': 'Plugin for PyRoll providing the contact area estimation by Zouhar',
    'long_description': '# PyRoll Zouhar Contact Model\n\nPlugin for PyRoll providing the contact area estimation by Zouhar.\n\nTo read about the model approach, see [here](docs/model.md).\n\nTo read about the usage of the plugin, see [here](docs/usage.md).\n',
    'author': 'Max Weiner',
    'author_email': 'max.weiner@imf.tu-freiberg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyroll-project.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
