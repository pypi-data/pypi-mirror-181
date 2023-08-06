# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pureml',
 'pureml.cli',
 'pureml.components',
 'pureml.config',
 'pureml.decorators',
 'pureml.packaging',
 'pureml.packaging.model_packaging',
 'pureml.pipeline',
 'pureml.pipeline.data',
 'pureml.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'PyJWT>=2.4.0,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'joblib>=1.2.0,<2.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pyarrow>=8.0.0,<9.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.28.1,<3.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pureml = pureml.cli.main:app']}

setup_kwargs = {
    'name': 'pureml',
    'version': '0.1.2.2',
    'description': '',
    'long_description': "# Pure\n\n\nPureML is the tool that lets you register, version, compare and stage models without the hassle of complex software. The core of PureML is the seamless collaboration across the team. \n\n\n# Documentation\n\nSee [PureML documentation](https://docs.pureml.com)\n\n\n\n# Installation\n\n## Get prerequisites\n* python versions `^3.8.0` are supported\n\n## Install package\n\n```bash\npip install pureml\n```\n\n\n# Getting Help\nIf you get stuck, don't worry we are here to help.\n\n- [PureML App](https://app.pureml.com)\n- [PureML Discord](https://discord.gg/xNUHt9yguJ)\n\n\n\n\n",
    'author': 'vamsidhar muthireddy',
    'author_email': 'vamsi.muthireddy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pureml.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
