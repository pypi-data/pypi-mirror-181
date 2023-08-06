# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['isaura',
 'isaura.blocs',
 'isaura.core',
 'isaura.dtypes',
 'isaura.handle',
 'isaura.iac',
 'isaura.local',
 'isaura.routes',
 'isaura.routes.precalc',
 'isaura.routes.precalc.get',
 'isaura.routes.precalc.get.app',
 'isaura.routes.schemas',
 'isaura.routes.status',
 'isaura.routes.status.get',
 'isaura.routes.status.get.app',
 'isaura.service',
 'isaura.utils']

package_data = \
{'': ['*']}

install_requires = \
['aws-lambda-powertools[pydantic]>=2.2.0,<3.0.0',
 'boto3>=1.26.8,<2.0.0',
 'h5py>=3.7.0,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pydantic[dotenv]>=1.10.2,<2.0.0',
 'sqlalchemy>=1.3.0,<1.4.0',
 'xdg>=5.1.1,<6.0.0']

setup_kwargs = {
    'name': 'isaura',
    'version': '0.18.0',
    'description': 'Isaura data lake for pre-computed Ersilia properties',
    'long_description': 'None',
    'author': 'Ersilia Open Source Initiative',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
