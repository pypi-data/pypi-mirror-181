# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imap_pydantic_client',
 'imap_pydantic_client.decoder',
 'imap_pydantic_client.factorys',
 'imap_pydantic_client.helpers']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=15.3.4,<16.0.0',
 'IMAPClient>=2.3.1,<3.0.0',
 'email-validator>=1.3.0,<2.0.0',
 'faker-web>=0.3.1,<0.4.0',
 'mdgen>=0.1.10,<0.2.0',
 'pydantic>=1.10.2,<2.0.0']

entry_points = \
{'console_scripts': ['cli_command_name = package_name:function']}

setup_kwargs = {
    'name': 'imap-pydantic-client',
    'version': '0.2.0',
    'description': '',
    'long_description': '# IMAP Pydantic Client Library\n## [Changelog](CHANGELOG.md)\n### Библиотека для работы с почтовыми серверами, отдает в ответ Pydantic модели\n',
    'author': 'alexander.mescheryakov',
    'author_email': 'avm@sh-inc.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MattiooFR/package_name',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
