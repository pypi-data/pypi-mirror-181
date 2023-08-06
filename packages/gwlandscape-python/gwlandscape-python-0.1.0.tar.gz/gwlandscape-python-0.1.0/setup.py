# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gwlandscape_python',
 'gwlandscape_python.tests',
 'gwlandscape_python.utils',
 'gwlandscape_python.utils.tests']

package_data = \
{'': ['*']}

install_requires = \
['graphene-file-upload>=1.3.0,<2.0.0',
 'gwdc-python>=0.4.0,<0.5.0',
 'importlib-metadata>=4.5.0,<5.0.0',
 'jwt>=1.2.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.61.2,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=4.0.2,<5.0.0', 'sphinx-rtd-theme>=0.5.2,<0.6.0']}

setup_kwargs = {
    'name': 'gwlandscape-python',
    'version': '0.1.0',
    'description': 'Wrapper of GWDC API, used for interacting with the GWLandscape endpoints',
    'long_description': "GWLandscape Python API\n======================\n\n`GWLandscape <https://gwlandscape.org.au/>`_ is a service used to handle both the submission of COMPAS jobs (todo)\n\nCheck out the `documentation <https://gwlandscape-python.readthedocs.io/en/latest/>`_ for more information.\n\nInstallation\n------------\n\nThe gwlandscape-python package can be installed with\n\n::\n\n    pip install gwlandscape-python\n\n\nExample\n-------\n\n::\n\n    >>> from gwlandscape_python import GWLandscape\n    >>> gwc = GWLandscape(token='<user_api_token_here>')\n\n",
    'author': 'Thomas Reichardt',
    'author_email': 'treichardt@swin.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gravitationalwavedc/gwlandscape_python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
