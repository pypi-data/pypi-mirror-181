# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycconverter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycconverter',
    'version': '0.0.6',
    'description': 'convert all python script to pyc file in given directory',
    'long_description': '\n## can be imported by\n\nfrom pycconverter import PycConverter\n\n### or\n\nimport pycconverter\n\n## Convert all .py files to .pyc files\n\n#### param Source_path: Path to the source directory\n#### param Destination_path: Path to the destination directory where the .pyc files will be stored\n#### param DirectoryNamePyc: Name of the directory where the .pyc files will be stored\n:return: None\n\n:Example:\n\n```\n>>> from pycconverter import PycConverter\n\n>>> PycConverter(Source_path="/home/user/ProjectsDirectory", Destination_path="/home/user/Projects/PycC", DirectoryNamePyc="BUILD").convert_to_pyc()\n\n```\n',
    'author': 'MonadWizard',
    'author_email': 'monad.wizard.r@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MonadWizard/pycconverter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
